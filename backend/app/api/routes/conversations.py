"""API routes for conversation management."""
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.crud.conversation import (
    create_conversation,
    get_conversation,
    get_conversations,
    count_conversations,
    update_conversation,
    delete_conversation,
)
from app.models.conversation import (
    ConversationCreate,
    ConversationPublic,
    ConversationsPublic,
    ConversationUpdate,
)

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("/", response_model=ConversationPublic, status_code=status.HTTP_201_CREATED)
def create_new_conversation(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    conversation_in: ConversationCreate,
) -> Any:
    """Create new conversation for the current user."""
    conversation = create_conversation(
        session=session,
        conversation_in=conversation_in,
        user_id=current_user.id,
    )
    return conversation


@router.get("/", response_model=ConversationsPublic)
def read_conversations(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Retrieve conversations for the current user."""
    conversations = get_conversations(
        session=session,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )
    count = count_conversations(session=session, user_id=current_user.id)
    
    return ConversationsPublic(data=conversations, count=count)


@router.get("/{conversation_id}", response_model=ConversationPublic)
def read_conversation(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    conversation_id: uuid.UUID,
) -> Any:
    """Get specific conversation by ID."""
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
    return conversation


@router.patch("/{conversation_id}", response_model=ConversationPublic)
def update_existing_conversation(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    conversation_id: uuid.UUID,
    conversation_in: ConversationUpdate,
) -> Any:
    """Update a conversation."""
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
    
    conversation = update_conversation(
        session=session,
        db_conversation=conversation,
        conversation_in=conversation_in,
    )
    return conversation


@router.delete("/{conversation_id}")
def delete_existing_conversation(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    conversation_id: uuid.UUID,
) -> Any:
    """Delete a conversation and all related data."""
    success = delete_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    return {"message": "Conversation deleted successfully"}