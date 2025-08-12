"""File model for Red Panda - CSV file uploads and management."""
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.models.user import User


class FileBase(SQLModel):
    """Base file model with shared properties."""
    filename: str = Field(max_length=255, description="Original filename")
    mime_type: str = Field(max_length=100, description="MIME type of the file")
    size_bytes: int = Field(description="File size in bytes")


class FileCreate(FileBase):
    """Properties to receive on file creation."""
    storage_path: str = Field(max_length=500, description="Path where file is stored")
    file_metadata: dict = Field(default={}, sa_column=Column(JSON))


class FileUpdate(SQLModel):
    """Properties to receive on file update."""
    filename: str | None = Field(default=None, max_length=255)
    file_metadata: dict | None = None


class File(FileBase, table=True):
    """Database model for uploaded files."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(
        foreign_key="user.id", 
        nullable=False, 
        ondelete="CASCADE",
        description="Owner of the file"
    )
    storage_path: str = Field(max_length=500, description="Path where file is stored")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Metadata for CSV files (columns, row count, etc.)
    file_metadata: dict = Field(
        default={}, 
        sa_column=Column(JSON),
        description="File metadata (e.g., CSV columns, row count)"
    )
    
    # Relationships
    user: "User" = Relationship(back_populates="files")


class FilePublic(FileBase):
    """Properties to return via API."""
    id: uuid.UUID
    user_id: uuid.UUID
    uploaded_at: datetime
    file_metadata: dict


class FilesPublic(SQLModel):
    """List of files to return via API."""
    data: list[FilePublic]
    count: int


class FileMetadata(SQLModel):
    """CSV file metadata structure."""
    columns: list[str] = Field(default=[], description="Column names")
    row_count: int = Field(default=0, description="Number of rows")
    column_types: dict[str, str] = Field(default={}, description="Column data types")
    file_size_mb: float = Field(default=0.0, description="File size in MB")
    preview_rows: list[dict] | None = Field(default=None, description="First few rows as preview")