import uuid
from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import Column, JSON, Text
from sqlmodel import Field, SQLModel, Relationship


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    
    # BYOK (Bring Your Own Key) fields for LLM API access
    api_keys: dict = Field(
        default={}, 
        sa_column=Column(JSON),
        description="Encrypted API keys for LLM providers"
    )
    api_usage: dict = Field(
        default={}, 
        sa_column=Column(JSON),
        description="Usage tracking for API calls"
    )
    
    # Relationships
    conversations: list["Conversation"] = Relationship(back_populates="user")
    code_blocks: list["CodeBlock"] = Relationship(back_populates="user")
    files: list["File"] = Relationship(back_populates="user")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# ============== Red Panda Core Models ==============

# Conversation Model
class ConversationBase(SQLModel):
    title: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Conversation(ConversationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    
    # Relationships
    user: User = Relationship(back_populates="conversations")
    messages: list["ChatMessage"] = Relationship(back_populates="conversation")
    code_blocks: list["CodeBlock"] = Relationship(back_populates="conversation")


class ConversationCreate(SQLModel):
    title: str = Field(max_length=255)


class ConversationUpdate(SQLModel):
    title: Optional[str] = Field(default=None, max_length=255)


class ConversationPublic(ConversationBase):
    id: uuid.UUID
    user_id: uuid.UUID
    message_count: int = 0
    code_block_count: int = 0


# Message Model for chat conversations
class ChatMessageBase(SQLModel):
    role: str = Field(max_length=50)  # 'user', 'assistant', 'system'
    content: str = Field(sa_column=Column(Text))
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ChatMessage(ChatMessageBase, table=True):
    __tablename__ = "chat_messages"  # Avoid conflict with existing Message class
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", index=True)
    
    # Store code block references
    code_block_ids: list[str] = Field(default=[], sa_column=Column(JSON))
    
    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")


class ChatMessageCreate(SQLModel):
    role: str = Field(max_length=50)
    content: str


class ChatMessagePublic(ChatMessageBase):
    id: uuid.UUID
    conversation_id: uuid.UUID
    code_block_ids: list[str] = []


# CodeBlock Model (CORE FEATURE)
class CodeBlockBase(SQLModel):
    language: str = Field(max_length=50)
    code: str = Field(sa_column=Column(Text))
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Metadata for searchability
    imports: list[str] = Field(default=[], sa_column=Column(JSON))
    functions: list[str] = Field(default=[], sa_column=Column(JSON))
    classes: list[str] = Field(default=[], sa_column=Column(JSON))
    variables: list[str] = Field(default=[], sa_column=Column(JSON))
    
    # Usage tracking
    tags: list[str] = Field(default=[], sa_column=Column(JSON))
    execution_count: int = Field(default=0)
    last_executed: Optional[datetime] = Field(default=None)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CodeBlock(CodeBlockBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", index=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    message_id: Optional[uuid.UUID] = Field(default=None, index=True)
    
    # Relationships
    conversation: Conversation = Relationship(back_populates="code_blocks")
    user: User = Relationship(back_populates="code_blocks")


class CodeBlockCreate(SQLModel):
    language: str = Field(max_length=50)
    code: str
    description: Optional[str] = None
    tags: list[str] = []


class CodeBlockUpdate(SQLModel):
    description: Optional[str] = None
    tags: Optional[list[str]] = None


class CodeBlockPublic(CodeBlockBase):
    id: uuid.UUID
    conversation_id: uuid.UUID
    user_id: uuid.UUID
    message_id: Optional[uuid.UUID] = None


# File Model for CSV uploads
class FileBase(SQLModel):
    filename: str = Field(max_length=255)
    content_type: str = Field(max_length=100)
    file_size: int
    file_path: str = Field(max_length=500)
    
    # CSV metadata
    columns: list[str] = Field(default=[], sa_column=Column(JSON))
    row_count: Optional[int] = Field(default=None)
    column_types: dict = Field(default={}, sa_column=Column(JSON))
    
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


class File(FileBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    conversation_id: Optional[uuid.UUID] = Field(default=None, foreign_key="conversation.id", index=True)
    
    # Relationships
    user: User = Relationship(back_populates="files")


class FileCreate(SQLModel):
    filename: str = Field(max_length=255)
    content_type: str = Field(max_length=100)
    file_size: int


class FilePublic(FileBase):
    id: uuid.UUID
    user_id: uuid.UUID
    conversation_id: Optional[uuid.UUID] = None


