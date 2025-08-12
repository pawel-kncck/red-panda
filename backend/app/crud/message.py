"""CRUD operations for Message model."""
import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Session, select
from sqlalchemy import asc

from app.models.message import (
    Message,
    MessageCreate,
)
from app.crud.conversation import update_message_count


def create_message(
    *,
    session: Session,
    message_in: MessageCreate,
    conversation_id: uuid.UUID,
) -> Message:
    """Create a new message in a conversation."""
    db_message = Message(
        **message_in.model_dump(),
        conversation_id=conversation_id,
        created_at=datetime.utcnow(),
    )
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    
    # Update conversation message count
    update_message_count(session=session, conversation_id=conversation_id)
    
    return db_message


def get_message(
    *, session: Session, message_id: uuid.UUID
) -> Optional[Message]:
    """Get a message by ID."""
    return session.get(Message, message_id)


def get_messages_by_conversation(
    *,
    session: Session,
    conversation_id: uuid.UUID,
    skip: int = 0,
    limit: Optional[int] = None,
) -> list[Message]:
    """Get all messages for a conversation, ordered by creation time."""
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(asc(Message.created_at))
        .offset(skip)
    )
    
    if limit:
        statement = statement.limit(limit)
    
    return list(session.exec(statement).all())


def delete_message(
    *, session: Session, message_id: uuid.UUID
) -> bool:
    """Delete a message."""
    message = session.get(Message, message_id)
    if not message:
        return False
    
    session.delete(message)
    session.commit()
    return True


def add_code_block_to_message(
    *,
    session: Session,
    message_id: uuid.UUID,
    code_block_id: uuid.UUID,
) -> Optional[Message]:
    """Add a code block reference to a message."""
    message = session.get(Message, message_id)
    if not message:
        return None
    
    if code_block_id not in message.code_block_ids:
        message.code_block_ids = message.code_block_ids + [code_block_id]
        session.add(message)
        session.commit()
        session.refresh(message)
    
    return message