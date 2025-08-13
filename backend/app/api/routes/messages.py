"""API routes for message management within conversations."""
import uuid
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, SessionDep
from app.crud_ops.message import (
    create_message,
    get_messages_by_conversation,
    delete_message,
)
from app.crud_ops.conversation import get_conversation
from app.models.message import (
    MessageCreate,
    MessagePublic,
    MessagesPublic,
)

router = APIRouter(prefix="/conversations/{conversation_id}/messages", tags=["messages"])


@router.post("/", response_model=MessagePublic, status_code=status.HTTP_201_CREATED)
def create_new_message(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    conversation_id: uuid.UUID,
    message_in: MessageCreate,
) -> Any:
    """Create new message in a conversation."""
    # Verify conversation belongs to user
    conversation = get_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    
    message = create_message(
        session=session,
        message_in=message_in,
        conversation_id=conversation_id,
    )
    return message


@router.get("/", response_model=MessagesPublic)
def read_messages(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    conversation_id: uuid.UUID,
    skip: int = 0,
    limit: Optional[int] = None,
) -> Any:
    """Retrieve all messages for a conversation."""
    # Verify conversation belongs to user
    conversation = get_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    
    messages = get_messages_by_conversation(
        session=session,
        conversation_id=conversation_id,
        skip=skip,
        limit=limit,
    )
    
    return MessagesPublic(data=messages, count=len(messages))


@router.delete("/{message_id}")
def delete_existing_message(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    conversation_id: uuid.UUID,
    message_id: uuid.UUID,
) -> Any:
    """Delete a message from a conversation."""
    # Verify conversation belongs to user
    conversation = get_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    
    success = delete_message(session=session, message_id=message_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )
    
    return {"message": "Message deleted successfully"}