"""CRUD operations for Conversation model."""
import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Session, select, func
from sqlalchemy import desc

from app.models.conversation import (
    Conversation,
    ConversationCreate,
    ConversationUpdate,
)


def create_conversation(
    *, session: Session, conversation_in: ConversationCreate, user_id: uuid.UUID
) -> Conversation:
    """Create a new conversation for a user."""
    db_conversation = Conversation(
        **conversation_in.model_dump(),
        user_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(db_conversation)
    session.commit()
    session.refresh(db_conversation)
    return db_conversation


def get_conversation(
    *, session: Session, conversation_id: uuid.UUID, user_id: uuid.UUID
) -> Optional[Conversation]:
    """Get a conversation by ID for a specific user."""
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id,
    )
    return session.exec(statement).first()


def get_conversations(
    *,
    session: Session,
    user_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Conversation]:
    """Get all conversations for a user, ordered by most recent."""
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(desc(Conversation.updated_at))
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def count_conversations(*, session: Session, user_id: uuid.UUID) -> int:
    """Count total conversations for a user."""
    statement = select(func.count(Conversation.id)).where(
        Conversation.user_id == user_id
    )
    return session.exec(statement).one()


def update_conversation(
    *,
    session: Session,
    db_conversation: Conversation,
    conversation_in: ConversationUpdate,
) -> Conversation:
    """Update a conversation."""
    conversation_data = conversation_in.model_dump(exclude_unset=True)
    conversation_data["updated_at"] = datetime.utcnow()
    
    for key, value in conversation_data.items():
        setattr(db_conversation, key, value)
    
    session.add(db_conversation)
    session.commit()
    session.refresh(db_conversation)
    return db_conversation


def delete_conversation(
    *, session: Session, conversation_id: uuid.UUID, user_id: uuid.UUID
) -> bool:
    """Delete a conversation and all related messages and code blocks."""
    conversation = get_conversation(
        session=session, conversation_id=conversation_id, user_id=user_id
    )
    if not conversation:
        return False
    
    session.delete(conversation)
    session.commit()
    return True


def update_message_count(
    *, session: Session, conversation_id: uuid.UUID
) -> None:
    """Update the message count for a conversation."""
    conversation = session.get(Conversation, conversation_id)
    if conversation:
        conversation.message_count += 1
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()