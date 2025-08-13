"""API routes for chat functionality with streaming support."""
import uuid
from typing import Any, List, Optional
import json
import asyncio

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.api.deps import CurrentUser, SessionDep
from app.crud_ops.conversation import get_conversation, update_conversation
from app.crud_ops.message import create_message, get_messages_by_conversation
from app.crud_ops.code_block import create_code_block
from app.models.message import MessageCreate, MessageRole
from app.models.code_block import CodeBlockCreate
from app.models.conversation import ConversationUpdate
from app.services.llm_service import (
    llm_service,
    LLMProvider,
    LLMConfig,
    ChatMessage as LLMChatMessage,
)
from app.services.code_parser import code_parser

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    """Request model for chat completion."""
    conversation_id: uuid.UUID
    message: str
    provider: LLMProvider = LLMProvider.OPENAI
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = True


class ChatResponse(BaseModel):
    """Response model for non-streaming chat."""
    message_id: uuid.UUID
    content: str
    code_blocks: List[dict] = []


async def process_and_save_response(
    session: SessionDep,
    user_id: uuid.UUID,
    conversation_id: uuid.UUID,
    content: str,
) -> tuple[uuid.UUID, List[dict]]:
    """Process the LLM response, extract code blocks, and save everything."""
    # Create assistant message
    assistant_message = create_message(
        session=session,
        message_in=MessageCreate(
            role=MessageRole.ASSISTANT.value,
            content=content,
        ),
        conversation_id=conversation_id,
    )
    
    # Extract and save code blocks
    code_blocks_data = code_parser.extract_code_blocks(content)
    saved_code_blocks = []
    
    for block_data in code_blocks_data:
        # Extract tags from the conversation context
        tags = code_parser.extract_tags_from_text(content)
        
        code_block_in = CodeBlockCreate(
            conversation_id=conversation_id,
            code=block_data["code"],
            language=block_data["language"],
            description=block_data.get("description"),
            tags=tags,
            imports=block_data.get("metadata", {}).get("imports", []),
            functions_defined=block_data.get("metadata", {}).get("functions", []),
            variables_created=block_data.get("metadata", {}).get("variables", []),
        )
        
        code_block = create_code_block(
            session=session,
            code_block_in=code_block_in,
            user_id=user_id,
        )
        
        saved_code_blocks.append({
            "id": str(code_block.id),
            "language": code_block.language,
            "description": code_block.description,
        })
        
        # Add code block reference to message
        assistant_message.code_block_ids.append(code_block.id)
    
    # Update message with code block references
    if saved_code_blocks:
        session.add(assistant_message)
        session.commit()
    
    # Update conversation's last message preview
    update_conversation(
        session=session,
        db_conversation=session.get(ConversationUpdate, conversation_id),
        conversation_in=ConversationUpdate(
            last_message_preview=content[:500],
        ),
    )
    
    return assistant_message.id, saved_code_blocks


@router.post("/complete", response_model=ChatResponse)
async def chat_completion(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    request: ChatRequest,
) -> Any:
    """Create a chat completion (non-streaming)."""
    # Verify conversation belongs to user
    conversation = get_conversation(
        session=session,
        conversation_id=request.conversation_id,
        user_id=current_user.id,
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    
    # Save user message
    user_message = create_message(
        session=session,
        message_in=MessageCreate(
            role=MessageRole.USER.value,
            content=request.message,
        ),
        conversation_id=request.conversation_id,
    )
    
    # Get conversation history
    messages = get_messages_by_conversation(
        session=session,
        conversation_id=request.conversation_id,
        limit=50,  # Last 50 messages for context
    )
    
    # Convert to LLM format
    llm_messages = [
        LLMChatMessage(role=msg.role, content=msg.content)
        for msg in messages
    ]
    
    # Create LLM config
    config = LLMConfig(
        provider=request.provider,
        model=request.model or ("gpt-4-turbo-preview" if request.provider == LLMProvider.OPENAI else "claude-3-opus-20240229"),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=False,
    )
    
    # Get completion from LLM
    try:
        response_content = await llm_service.create_chat_completion(
            user=current_user,
            messages=llm_messages,
            config=config,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    
    # Process and save response
    message_id, code_blocks = await process_and_save_response(
        session=session,
        user_id=current_user.id,
        conversation_id=request.conversation_id,
        content=response_content,
    )
    
    return ChatResponse(
        message_id=message_id,
        content=response_content,
        code_blocks=code_blocks,
    )


@router.post("/stream")
async def chat_stream(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    request: ChatRequest,
) -> StreamingResponse:
    """Create a streaming chat completion using Server-Sent Events."""
    # Verify conversation belongs to user
    conversation = get_conversation(
        session=session,
        conversation_id=request.conversation_id,
        user_id=current_user.id,
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    
    # Save user message
    user_message = create_message(
        session=session,
        message_in=MessageCreate(
            role=MessageRole.USER.value,
            content=request.message,
        ),
        conversation_id=request.conversation_id,
    )
    
    # Get conversation history
    messages = get_messages_by_conversation(
        session=session,
        conversation_id=request.conversation_id,
        limit=50,
    )
    
    # Convert to LLM format
    llm_messages = [
        LLMChatMessage(role=msg.role, content=msg.content)
        for msg in messages
    ]
    
    # Create LLM config
    config = LLMConfig(
        provider=request.provider,
        model=request.model or ("gpt-4-turbo-preview" if request.provider == LLMProvider.OPENAI else "claude-3-opus-20240229"),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )
    
    async def generate_events():
        """Generate Server-Sent Events for streaming response."""
        full_response = ""
        
        try:
            # Stream the response
            async for chunk in llm_service.create_chat_stream(
                user=current_user,
                messages=llm_messages,
                config=config,
            ):
                full_response += chunk
                # Send chunk as SSE
                yield f"data: {json.dumps({'type': 'content', 'content': chunk})}\n\n"
            
            # Process and save the complete response
            message_id, code_blocks = await process_and_save_response(
                session=session,
                user_id=current_user.id,
                conversation_id=request.conversation_id,
                content=full_response,
            )
            
            # Send code blocks info
            if code_blocks:
                yield f"data: {json.dumps({'type': 'code_blocks', 'blocks': code_blocks})}\n\n"
            
            # Send completion event
            yield f"data: {json.dumps({'type': 'done', 'message_id': str(message_id)})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate_events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable Nginx buffering
        },
    )