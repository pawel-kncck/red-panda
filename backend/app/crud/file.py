"""CRUD operations for File model."""
import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Session, select
from sqlalchemy import desc

from app.models.file import (
    File,
    FileCreate,
)


def create_file(
    *,
    session: Session,
    file_in: FileCreate,
    user_id: uuid.UUID,
    storage_path: str,
    file_metadata: dict,
) -> File:
    """Create a new file record."""
    db_file = File(
        **file_in.model_dump(),
        user_id=user_id,
        storage_path=storage_path,
        file_metadata=file_metadata,
        uploaded_at=datetime.utcnow(),
    )
    session.add(db_file)
    session.commit()
    session.refresh(db_file)
    return db_file


def get_file(
    *, session: Session, file_id: uuid.UUID, user_id: uuid.UUID
) -> Optional[File]:
    """Get a file by ID for a specific user."""
    statement = select(File).where(
        File.id == file_id,
        File.user_id == user_id,
    )
    return session.exec(statement).first()


def get_files(
    *,
    session: Session,
    user_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[File]:
    """Get all files for a user."""
    statement = (
        select(File)
        .where(File.user_id == user_id)
        .order_by(desc(File.uploaded_at))
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def delete_file(
    *, session: Session, file_id: uuid.UUID, user_id: uuid.UUID
) -> Optional[File]:
    """Delete a file and return it for cleanup."""
    file = get_file(session=session, file_id=file_id, user_id=user_id)
    if not file:
        return None
    
    session.delete(file)
    session.commit()
    return file