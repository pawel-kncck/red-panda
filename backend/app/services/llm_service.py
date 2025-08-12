"""LLM Service for handling OpenAI and Anthropic API interactions."""
import json
from typing import AsyncGenerator, Optional, Dict, Any, List
from enum import Enum
import logging

from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from fastapi import HTTPException
from pydantic import BaseModel

from app.core.security import decrypt_api_key, encrypt_api_key
from app.models.user import User

logger = logging.getLogger(__name__)


class LLMProvider(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class ChatMessage(BaseModel):
    """Chat message for LLM interaction."""
    role: str  # "user", "assistant", "system"
    content: str


class LLMConfig(BaseModel):
    """Configuration for LLM requests."""
    provider: LLMProvider = LLMProvider.OPENAI
    model: str = "gpt-4-turbo-preview"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = True


class LLMService:
    """Service for handling LLM interactions."""
    
    def __init__(self):
        self.openai_client: Optional[AsyncOpenAI] = None
        self.anthropic_client: Optional[AsyncAnthropic] = None
    
    def get_user_api_key(self, user: User, provider: LLMProvider) -> Optional[str]:
        """Get and decrypt user's API key for a provider."""
        encrypted_key = user.api_keys.get(provider.value)
        if not encrypted_key:
            return None
        
        try:
            return decrypt_api_key(encrypted_key)
        except Exception as e:
            logger.error(f"Failed to decrypt API key: {e}")
            return None
    
    def set_user_api_key(self, user: User, provider: LLMProvider, api_key: str) -> Dict[str, str]:
        """Encrypt and store user's API key."""
        encrypted_key = encrypt_api_key(api_key)
        
        if not user.api_keys:
            user.api_keys = {}
        
        user.api_keys[provider.value] = encrypted_key
        return user.api_keys
    
    async def validate_api_key(self, provider: LLMProvider, api_key: str) -> bool:
        """Validate an API key by making a test request."""
        try:
            if provider == LLMProvider.OPENAI:
                client = AsyncOpenAI(api_key=api_key)
                # Make a minimal request to validate the key
                await client.models.list()
                return True
            
            elif provider == LLMProvider.ANTHROPIC:
                client = AsyncAnthropic(api_key=api_key)
                # Anthropic doesn't have a simple list endpoint, so we'll try a minimal completion
                await client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1,
                    messages=[{"role": "user", "content": "Hi"}],
                )
                return True
            
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            return False
        
        return False
    
    def get_client(self, user: User, provider: LLMProvider):
        """Get or create an LLM client for the user."""
        api_key = self.get_user_api_key(user, provider)
        if not api_key:
            raise HTTPException(
                status_code=400,
                detail=f"No API key configured for {provider.value}. Please add your API key in settings.",
            )
        
        if provider == LLMProvider.OPENAI:
            return AsyncOpenAI(api_key=api_key)
        elif provider == LLMProvider.ANTHROPIC:
            return AsyncAnthropic(api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    async def create_chat_completion(
        self,
        user: User,
        messages: List[ChatMessage],
        config: LLMConfig,
    ) -> str:
        """Create a non-streaming chat completion."""
        client = self.get_client(user, config.provider)
        
        message_dicts = [{"role": msg.role, "content": msg.content} for msg in messages]
        
        try:
            if config.provider == LLMProvider.OPENAI:
                response = await client.chat.completions.create(
                    model=config.model,
                    messages=message_dicts,
                    temperature=config.temperature,
                    max_tokens=config.max_tokens,
                    stream=False,
                )
                return response.choices[0].message.content or ""
            
            elif config.provider == LLMProvider.ANTHROPIC:
                # Anthropic requires system message to be separate
                system_message = None
                user_messages = []
                
                for msg in message_dicts:
                    if msg["role"] == "system":
                        system_message = msg["content"]
                    else:
                        # Convert "assistant" to "assistant" and "user" to "user"
                        user_messages.append({
                            "role": msg["role"],
                            "content": msg["content"],
                        })
                
                response = await client.messages.create(
                    model=config.model,
                    messages=user_messages,
                    system=system_message,
                    temperature=config.temperature,
                    max_tokens=config.max_tokens or 4096,
                )
                return response.content[0].text
            
        except Exception as e:
            logger.error(f"Chat completion failed: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"LLM request failed: {str(e)}",
            )
    
    async def create_chat_stream(
        self,
        user: User,
        messages: List[ChatMessage],
        config: LLMConfig,
    ) -> AsyncGenerator[str, None]:
        """Create a streaming chat completion."""
        client = self.get_client(user, config.provider)
        
        message_dicts = [{"role": msg.role, "content": msg.content} for msg in messages]
        
        try:
            if config.provider == LLMProvider.OPENAI:
                stream = await client.chat.completions.create(
                    model=config.model,
                    messages=message_dicts,
                    temperature=config.temperature,
                    max_tokens=config.max_tokens,
                    stream=True,
                )
                
                async for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            
            elif config.provider == LLMProvider.ANTHROPIC:
                # Prepare messages for Anthropic
                system_message = None
                user_messages = []
                
                for msg in message_dicts:
                    if msg["role"] == "system":
                        system_message = msg["content"]
                    else:
                        user_messages.append({
                            "role": msg["role"],
                            "content": msg["content"],
                        })
                
                async with client.messages.stream(
                    model=config.model,
                    messages=user_messages,
                    system=system_message,
                    temperature=config.temperature,
                    max_tokens=config.max_tokens or 4096,
                ) as stream:
                    async for text in stream.text_stream:
                        yield text
        
        except Exception as e:
            logger.error(f"Chat stream failed: {e}")
            yield f"Error: {str(e)}"
    
    def update_usage_tracking(self, user: User, provider: LLMProvider, tokens_used: int) -> None:
        """Update user's API usage tracking."""
        if not user.api_usage:
            user.api_usage = {}
        
        if provider.value not in user.api_usage:
            user.api_usage[provider.value] = {
                "total_tokens": 0,
                "total_requests": 0,
            }
        
        user.api_usage[provider.value]["total_tokens"] += tokens_used
        user.api_usage[provider.value]["total_requests"] += 1


# Global instance
llm_service = LLMService()