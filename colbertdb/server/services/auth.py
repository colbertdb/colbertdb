from datetime import datetime, timedelta, timezone

from jose import jwt
import secrets

from colbertdb.server.core.config import settings


# Configuration


def create_access_token(data: dict):
    """Create an access token."""
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def generate_api_key(length: int = 32) -> str:
    """Generate a secure API key."""
    return secrets.token_urlsafe(length)
