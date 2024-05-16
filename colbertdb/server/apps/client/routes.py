""" Module containing the client router. """

import os
from fastapi import APIRouter, HTTPException, status
from colbertdb.server.apps.client.models import ConnectRequest, ConnectResponse
from colbertdb.server.services.auth import create_access_token
from colbertdb.server.stores.api_keys import CLIENT_API_KEY

client_router = APIRouter()


@client_router.post("/connect", response_model=ConnectResponse)
async def connect(request: ConnectRequest):
    """Connect to the server."""
    auth_mode = os.environ.get("AUTH_MODE", "no_auth")
    if auth_mode == "no_auth":
        access_token = create_access_token(data={"api_key": "no_auth"})
        return {"access_token": access_token}

    if request.api_key == CLIENT_API_KEY:
        access_token = create_access_token(data={"api_key": request.api_key})
        return {"access_token": access_token}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token",
        headers={"WWW-Authenticate": "Bearer"},
    )
