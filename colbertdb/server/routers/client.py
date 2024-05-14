""" Module containing the client router. """
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, status
from jose import  jwt
from colbertdb.server.models import Token

from colbertdb.server.services.auth import (ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM,
                                            API_AUTH_TOKEN, SECRET_KEY, NO_AUTH)

client_router = APIRouter()

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create an access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@client_router.post("/client/connect", response_model=Token)
async def connect(api_token: str):
    """Connect to the server."""
    if NO_AUTH:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"api_token": "no_auth"})
        return {"access_token": access_token, "token_type": "bearer"}

    if api_token == API_AUTH_TOKEN:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"api_token": api_token}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token",
        headers={"WWW-Authenticate": "Bearer"},
    )

