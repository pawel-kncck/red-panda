"""API routes for code block management."""
import uuid
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentUser, SessionDep
from app.crud_ops.code_block import (
    create_code_block,
    get_code_block,
    get_code_blocks,
    search_code_blocks,
    update_code_block,
    delete_code_block,
    get_code_blocks_by_conversation,
)
from app.models.code_block import (
    CodeBlockCreate,
    CodeBlockPublic,
    CodeBlocksPublic,
    CodeBlockUpdate,
)

router = APIRouter(prefix="/code-blocks", tags=["code-blocks"])


@router.post("/", response_model=CodeBlockPublic, status_code=status.HTTP_201_CREATED)
def create_new_code_block(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    code_block_in: CodeBlockCreate,
) -> Any:
    """Create new code block."""
    code_block = create_code_block(
        session=session,
        code_block_in=code_block_in,
        user_id=current_user.id,
    )
    return code_block


@router.get("/", response_model=CodeBlocksPublic)
def read_code_blocks(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    conversation_id: Optional[uuid.UUID] = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Retrieve code blocks for the current user."""
    code_blocks = get_code_blocks(
        session=session,
        user_id=current_user.id,
        conversation_id=conversation_id,
        skip=skip,
        limit=limit,
    )
    
    return CodeBlocksPublic(data=code_blocks, count=len(code_blocks))


@router.get("/search", response_model=CodeBlocksPublic)
def search_user_code_blocks(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    q: str = Query(default="", description="Search query"),
    language: Optional[str] = Query(default=None, description="Filter by language"),
    tags: Optional[list[str]] = Query(default=None, description="Filter by tags"),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Search code blocks with filters."""
    code_blocks = search_code_blocks(
        session=session,
        user_id=current_user.id,
        query=q,
        language=language,
        tags=tags,
        skip=skip,
        limit=limit,
    )
    
    return CodeBlocksPublic(data=code_blocks, count=len(code_blocks))


@router.get("/conversation/{conversation_id}", response_model=CodeBlocksPublic)
def read_conversation_code_blocks(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    conversation_id: uuid.UUID,
) -> Any:
    """Get all code blocks for a specific conversation."""
    code_blocks = get_code_blocks_by_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=current_user.id,
    )
    
    return CodeBlocksPublic(data=code_blocks, count=len(code_blocks))


@router.get("/{code_block_id}", response_model=CodeBlockPublic)
def read_code_block(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    code_block_id: uuid.UUID,
) -> Any:
    """Get specific code block by ID."""
    code_block = get_code_block(
        session=session,
        code_block_id=code_block_id,
        user_id=current_user.id,
    )
    if not code_block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code block not found",
        )
    return code_block


@router.patch("/{code_block_id}", response_model=CodeBlockPublic)
def update_existing_code_block(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    code_block_id: uuid.UUID,
    code_block_in: CodeBlockUpdate,
) -> Any:
    """Update a code block."""
    code_block = get_code_block(
        session=session,
        code_block_id=code_block_id,
        user_id=current_user.id,
    )
    if not code_block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code block not found",
        )
    
    code_block = update_code_block(
        session=session,
        db_code_block=code_block,
        code_block_in=code_block_in,
    )
    return code_block


@router.delete("/{code_block_id}")
def delete_existing_code_block(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    code_block_id: uuid.UUID,
) -> Any:
    """Delete a code block."""
    success = delete_code_block(
        session=session,
        code_block_id=code_block_id,
        user_id=current_user.id,
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code block not found",
        )
    return {"message": "Code block deleted successfully"}