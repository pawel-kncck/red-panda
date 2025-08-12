"""Red Panda models package."""
from sqlmodel import SQLModel

from app.models.user import (
    User,
    UserBase,
    UserCreate,
    UserPublic,
    UsersPublic,
    UserRegister,
    UserUpdate,
    UserUpdateMe,
    UpdatePassword,
    Token,
    TokenPayload,
    NewPassword,
    AuthMessage,
)
from app.models.code_block import (
    CodeBlock,
    CodeBlockCreate,
    CodeBlockPublic,
    CodeBlockSearch,
    CodeBlocksPublic,
    CodeBlockUpdate,
)
from app.models.conversation import (
    Conversation,
    ConversationCreate,
    ConversationPublic,
    ConversationsPublic,
    ConversationUpdate,
)
from app.models.file import (
    File,
    FileCreate,
    FileMetadata,
    FilePublic,
    FilesPublic,
    FileUpdate,
)
from app.models.message import (
    Message,
    MessageCreate,
    MessagePublic,
    MessageRole,
    MessagesPublic,
    MessageUpdate,
)

__all__ = [
    "SQLModel",
    # User
    "User",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserUpdateMe",
    "UserPublic",
    "UsersPublic",
    "UserRegister",
    "UpdatePassword",
    "Token",
    "TokenPayload",
    "NewPassword",
    "AuthMessage",
    # Conversation
    "Conversation",
    "ConversationCreate",
    "ConversationUpdate",
    "ConversationPublic",
    "ConversationsPublic",
    # CodeBlock
    "CodeBlock",
    "CodeBlockCreate",
    "CodeBlockUpdate",
    "CodeBlockPublic",
    "CodeBlocksPublic",
    "CodeBlockSearch",
    # Message
    "Message",
    "MessageCreate",
    "MessageUpdate",
    "MessagePublic",
    "MessagesPublic",
    "MessageRole",
    # File
    "File",
    "FileCreate",
    "FileUpdate",
    "FilePublic",
    "FilesPublic",
    "FileMetadata",
]