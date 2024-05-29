""" Module containing the client router. """

from fastapi import APIRouter, Depends
from colbertdb.server.api.deps import verify_store
from colbertdb.server.models import ConnectResponse
from colbertdb.server.services.auth import create_access_token
from colbertdb.core.models.store import Store

router = APIRouter()


@router.post("/connect/{store_name}", response_model=ConnectResponse)
async def connect(store: Store = Depends(verify_store)):
    """Connect to the server."""
    token = create_access_token({"store": store.name})
    return ConnectResponse(token=token)
