"""API routes for user settings and API key management."""
from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.api.deps import CurrentUser, SessionDep
from app.services.llm_service import llm_service, LLMProvider

router = APIRouter(prefix="/settings", tags=["settings"])


class APIKeyRequest(BaseModel):
    """Request model for setting API key."""
    provider: LLMProvider
    api_key: str


class APIKeyResponse(BaseModel):
    """Response model for API key operations."""
    provider: str
    is_valid: bool
    message: str


class APIKeysStatus(BaseModel):
    """Status of all API keys."""
    openai: bool
    anthropic: bool


@router.post("/api-keys", response_model=APIKeyResponse)
async def set_api_key(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    request: APIKeyRequest,
) -> Any:
    """Set and validate an API key for a provider."""
    # Validate the API key
    is_valid = await llm_service.validate_api_key(request.provider, request.api_key)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid API key. Please check your key and try again.",
        )
    
    # Encrypt and store the API key
    current_user.api_keys = llm_service.set_user_api_key(
        current_user, request.provider, request.api_key
    )
    
    # Save to database
    session.add(current_user)
    session.commit()
    
    return APIKeyResponse(
        provider=request.provider.value,
        is_valid=True,
        message=f"API key for {request.provider.value} successfully saved.",
    )


@router.get("/api-keys/status", response_model=APIKeysStatus)
def get_api_keys_status(
    *,
    current_user: CurrentUser,
) -> Any:
    """Get status of configured API keys (without revealing the keys)."""
    return APIKeysStatus(
        openai=LLMProvider.OPENAI.value in (current_user.api_keys or {}),
        anthropic=LLMProvider.ANTHROPIC.value in (current_user.api_keys or {}),
    )


@router.delete("/api-keys/{provider}")
def delete_api_key(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    provider: LLMProvider,
) -> Any:
    """Delete an API key for a provider."""
    if not current_user.api_keys or provider.value not in current_user.api_keys:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No API key found for {provider.value}",
        )
    
    del current_user.api_keys[provider.value]
    session.add(current_user)
    session.commit()
    
    return {"message": f"API key for {provider.value} deleted successfully."}


@router.get("/api-usage")
def get_api_usage(
    *,
    current_user: CurrentUser,
) -> Any:
    """Get API usage statistics for the current user."""
    return current_user.api_usage or {}