"""CRUD operations for CodeBlock model."""
import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Session, select, or_
from sqlalchemy import desc

from app.models.code_block import (
    CodeBlock,
    CodeBlockCreate,
    CodeBlockUpdate,
)


def create_code_block(
    *,
    session: Session,
    code_block_in: CodeBlockCreate,
    user_id: uuid.UUID,
) -> CodeBlock:
    """Create a new code block."""
    db_code_block = CodeBlock(
        **code_block_in.model_dump(),
        user_id=user_id,
        created_at=datetime.utcnow(),
    )
    session.add(db_code_block)
    session.commit()
    session.refresh(db_code_block)
    return db_code_block


def get_code_block(
    *, session: Session, code_block_id: uuid.UUID, user_id: uuid.UUID
) -> Optional[CodeBlock]:
    """Get a code block by ID for a specific user."""
    statement = select(CodeBlock).where(
        CodeBlock.id == code_block_id,
        CodeBlock.user_id == user_id,
    )
    return session.exec(statement).first()


def get_code_blocks(
    *,
    session: Session,
    user_id: uuid.UUID,
    conversation_id: Optional[uuid.UUID] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[CodeBlock]:
    """Get code blocks for a user, optionally filtered by conversation."""
    statement = select(CodeBlock).where(CodeBlock.user_id == user_id)
    
    if conversation_id:
        statement = statement.where(CodeBlock.conversation_id == conversation_id)
    
    statement = statement.order_by(desc(CodeBlock.created_at)).offset(skip).limit(limit)
    return list(session.exec(statement).all())


def search_code_blocks(
    *,
    session: Session,
    user_id: uuid.UUID,
    query: str,
    language: Optional[str] = None,
    tags: Optional[list[str]] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[CodeBlock]:
    """Search code blocks by content, description, or metadata."""
    statement = select(CodeBlock).where(CodeBlock.user_id == user_id)
    
    # Search in code content and description
    if query:
        statement = statement.where(
            or_(
                CodeBlock.code.contains(query),
                CodeBlock.description.contains(query),
            )
        )
    
    # Filter by language
    if language:
        statement = statement.where(CodeBlock.language == language)
    
    # Filter by tags (any tag match)
    if tags:
        # This requires a more complex query for JSON array contains
        # For now, we'll do a simple implementation
        for tag in tags:
            statement = statement.where(CodeBlock.tags.contains([tag]))
    
    statement = statement.order_by(desc(CodeBlock.created_at)).offset(skip).limit(limit)
    return list(session.exec(statement).all())


def update_code_block(
    *,
    session: Session,
    db_code_block: CodeBlock,
    code_block_in: CodeBlockUpdate,
) -> CodeBlock:
    """Update a code block."""
    code_block_data = code_block_in.model_dump(exclude_unset=True)
    
    for key, value in code_block_data.items():
        setattr(db_code_block, key, value)
    
    session.add(db_code_block)
    session.commit()
    session.refresh(db_code_block)
    return db_code_block


def delete_code_block(
    *, session: Session, code_block_id: uuid.UUID, user_id: uuid.UUID
) -> bool:
    """Delete a code block."""
    code_block = get_code_block(
        session=session, code_block_id=code_block_id, user_id=user_id
    )
    if not code_block:
        return False
    
    session.delete(code_block)
    session.commit()
    return True


def get_code_blocks_by_conversation(
    *,
    session: Session,
    conversation_id: uuid.UUID,
    user_id: uuid.UUID,
) -> list[CodeBlock]:
    """Get all code blocks for a specific conversation."""
    statement = (
        select(CodeBlock)
        .where(
            CodeBlock.conversation_id == conversation_id,
            CodeBlock.user_id == user_id,
        )
        .order_by(CodeBlock.created_at)
    )
    return list(session.exec(statement).all())