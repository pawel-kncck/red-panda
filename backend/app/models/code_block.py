"""CodeBlock model for Red Panda - Core feature for code storage and reusability."""
import uuid
from datetime import datetime

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class CodeBlockBase(SQLModel):
    """Base code block model with shared properties."""
    code: str = Field(description="The actual code content")
    description: str | None = Field(default=None, description="Auto-generated description of what the code does")
    language: str = Field(default="python", max_length=20)
    executed_successfully: bool | None = Field(default=None)


class CodeBlockCreate(CodeBlockBase):
    """Properties to receive on code block creation."""
    conversation_id: uuid.UUID
    tags: list[str] = Field(default=[], sa_column=Column(JSON))
    imports: list[str] = Field(default=[], sa_column=Column(JSON))
    functions_defined: list[str] = Field(default=[], sa_column=Column(JSON))
    variables_created: list[str] = Field(default=[], sa_column=Column(JSON))


class CodeBlockUpdate(SQLModel):
    """Properties to receive on code block update."""
    description: str | None = None
    executed_successfully: bool | None = None
    tags: list[str] | None = None


class CodeBlock(CodeBlockBase, table=True):
    """Database model for code blocks - CORE FEATURE."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Metadata for search and analysis
    imports: list[str] = Field(default=[], sa_column=Column(JSON))
    functions_defined: list[str] = Field(default=[], sa_column=Column(JSON))
    variables_created: list[str] = Field(default=[], sa_column=Column(JSON))
    tags: list[str] = Field(default=[], sa_column=Column(JSON))
    
    # Versioning support
    version: int = Field(default=1)
    parent_version_id: uuid.UUID | None = Field(
        default=None, 
        foreign_key="codeblock.id",
        description="Reference to parent version for version tracking"
    )


class CodeBlockPublic(CodeBlockBase):
    """Properties to return via API."""
    id: uuid.UUID
    conversation_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    imports: list[str]
    functions_defined: list[str]
    variables_created: list[str]
    tags: list[str]
    version: int
    parent_version_id: uuid.UUID | None


class CodeBlocksPublic(SQLModel):
    """List of code blocks to return via API."""
    data: list[CodeBlockPublic]
    count: int


class CodeBlockSearch(SQLModel):
    """Search parameters for code blocks."""
    query: str | None = None
    tags: list[str] | None = None
    language: str | None = None
    has_imports: list[str] | None = None
    has_functions: list[str] | None = None
    executed_successfully: bool | None = None
    conversation_id: uuid.UUID | None = None