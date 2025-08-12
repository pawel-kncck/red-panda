from fastapi import APIRouter

from app.api.routes import (
    login,
    private,
    users,
    utils,
    conversations,
    code_blocks,
    messages,
    files,
)
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(conversations.router)
api_router.include_router(code_blocks.router)
api_router.include_router(messages.router)
api_router.include_router(files.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
