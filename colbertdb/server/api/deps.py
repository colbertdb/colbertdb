"""API dependencies."""

import os
from typing import Annotated

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer
from colbertdb.core.models.store import Store
from colbertdb.server.core.config import settings
from colbertdb.server.services.api_key_manager import api_key_manager


header_schema = APIKeyHeader(name="x-api-key")
jwt_schema = HTTPBearer()


def verify_store(store_name: str, api_key: str = Depends(header_schema)) -> Store:
    """Get the store from the API key."""
    if os.getenv("AUTH_MODE") == "no_auth":
        return Store(name=store_name)
    store = api_key_manager.get_store_by_api_key(api_key)
    if not store:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if store != store_name:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return Store(name=store)


def get_store_from_access_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(jwt_schema)]
):
    """Get the store from the access token."""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        store_name: str = payload.get("store")
        if store_name is None:
            print("store_name is None")
            raise credentials_exception
        store = Store(name=store_name)
        if not store.exists():
            raise credentials_exception
        return Store(name=store_name)
    except JWTError as e:
        raise credentials_exception from e


def verify_management_api_key(
    api_key: str = Depends(header_schema),
):
    """Verify the management API key."""
    if api_key != settings.MANAGEMENT_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
