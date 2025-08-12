"""Message model for Red Panda chat conversations."""
import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.models.conversation import Conversation


class MessageRole(str, Enum):
    """Role of the message sender."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageBase(SQLModel):
    """Base message model with shared properties."""
    role: MessageRole = Field(description="Role of the message sender")
    content: str = Field(description="Message content")


class MessageCreate(MessageBase):
    """Properties to receive on message creation."""
    conversation_id: uuid.UUID
    code_block_ids: list[uuid.UUID] = Field(default=[], sa_column=Column(JSON))


class MessageUpdate(SQLModel):
    """Properties to receive on message update."""
    content: str | None = None
    code_block_ids: list[uuid.UUID] | None = None


class Message(MessageBase, table=True):
    """Database model for chat messages."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(
        foreign_key="conversation.id", 
        nullable=False,
        ondelete="CASCADE"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # References to code blocks extracted from this message
    code_block_ids: list[uuid.UUID] = Field(
        default=[], 
        sa_column=Column(JSON),
        description="IDs of code blocks extracted from this message"
    )
    
    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")


class MessagePublic(MessageBase):
    """Properties to return via API."""
    id: uuid.UUID
    conversation_id: uuid.UUID
    created_at: datetime
    code_block_ids: list[uuid.UUID]


class MessagesPublic(SQLModel):
    """List of messages to return via API."""
    data: list[MessagePublic]
    count: int