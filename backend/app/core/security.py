from datetime import datetime, timedelta, timezone
from typing import Any
from cryptography.fernet import Fernet
import base64
import hashlib

import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_encryption_key() -> bytes:
    """Generate a consistent encryption key from SECRET_KEY."""
    # Use SHA256 to create a consistent 32-byte key from SECRET_KEY
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_api_key(api_key: str) -> str:
    """Encrypt an API key for storage."""
    fernet = Fernet(get_encryption_key())
    encrypted = fernet.encrypt(api_key.encode())
    return base64.urlsafe_b64encode(encrypted).decode()


def decrypt_api_key(encrypted_key: str) -> str:
    """Decrypt an API key from storage."""
    fernet = Fernet(get_encryption_key())
    encrypted_bytes = base64.urlsafe_b64decode(encrypted_key.encode())
    decrypted = fernet.decrypt(encrypted_bytes)
    return decrypted.decode()
