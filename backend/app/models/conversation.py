"""Conversation model for Red Panda."""
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.message import Message
    from app.models.code_block import CodeBlock


class ConversationBase(SQLModel):
    """Base conversation model with shared properties."""
    title: str = Field(max_length=255)
    last_message_preview: str | None = Field(default=None, max_length=500)


class ConversationCreate(ConversationBase):
    """Properties to receive on conversation creation."""
    pass


class ConversationUpdate(ConversationBase):
    """Properties to receive on conversation update."""
    title: str | None = Field(default=None, max_length=255)  # type: ignore
    last_message_preview: str | None = Field(default=None, max_length=500)


class Conversation(ConversationBase, table=True):
    """Database model for conversations."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    message_count: int = Field(default=0)
    
    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: list["Message"] = Relationship(back_populates="conversation")
    code_blocks: list["CodeBlock"] = Relationship(back_populates="conversation")


class ConversationPublic(ConversationBase):
    """Properties to return via API."""
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    message_count: int


class ConversationsPublic(SQLModel):
    """List of conversations to return via API."""
    data: list[ConversationPublic]
    count: int