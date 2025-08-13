"""API routes for file management."""
import uuid
from typing import Any

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.api.deps import CurrentUser, SessionDep
from app.crud_ops.file import (
    create_file,
    get_file,
    get_files,
    delete_file,
)
from app.models.file import (
    FileCreate,
    FilePublic,
    FilesPublic,
)
from app.services.file_service import FileService

router = APIRouter(prefix="/files", tags=["files"])
file_service = FileService()


@router.post("/upload", response_model=FilePublic, status_code=status.HTTP_201_CREATED)
async def upload_file(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    file: UploadFile = File(...),
) -> Any:
    """Upload a file (CSV or other)."""
    # Validate file size (50MB max)
    if file.size and file.size > 50 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large. Maximum size is 50MB.",
        )
    
    # Save file and extract metadata
    try:
        storage_path, metadata = await file_service.save_upload_file(
            upload_file=file,
            user_id=current_user.id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}",
        )
    
    # Create database record
    file_create = FileCreate(
        filename=file.filename,
        mime_type=file.content_type or "application/octet-stream",
        size_bytes=file.size or 0,
    )
    
    db_file = create_file(
        session=session,
        file_in=file_create,
        user_id=current_user.id,
        storage_path=storage_path,
        file_metadata=metadata,
    )
    
    return db_file


@router.get("/", response_model=FilesPublic)
def read_files(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Retrieve all files for the current user."""
    files = get_files(
        session=session,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )
    
    return FilesPublic(data=files, count=len(files))


@router.get("/{file_id}", response_model=FilePublic)
def read_file(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    file_id: uuid.UUID,
) -> Any:
    """Get specific file metadata by ID."""
    file = get_file(
        session=session,
        file_id=file_id,
        user_id=current_user.id,
    )
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    return file


@router.get("/{file_id}/content")
def read_file_content(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    file_id: uuid.UUID,
    max_rows: int = 1000,
) -> Any:
    """Get file content (for CSV files, returns parsed data)."""
    file = get_file(
        session=session,
        file_id=file_id,
        user_id=current_user.id,
    )
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    
    content = file_service.get_file_content(
        file_path=file.storage_path,
        max_rows=max_rows,
    )
    
    if content is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File content not found on disk",
        )
    
    return content


@router.delete("/{file_id}")
def delete_uploaded_file(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    file_id: uuid.UUID,
) -> Any:
    """Delete a file and its data."""
    db_file = delete_file(
        session=session,
        file_id=file_id,
        user_id=current_user.id,
    )
    
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    
    # Delete physical file
    file_service.delete_file(db_file.storage_path)
    
    return {"message": "File deleted successfully"}