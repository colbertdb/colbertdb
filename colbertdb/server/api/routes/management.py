from fastapi import APIRouter, Depends, status

from colbertdb.core.models.store import Store
from colbertdb.server.models import (
    CreateStoreRequest,
    CreateStoreResponse,
    GetStoreResponse,
)
from colbertdb.server.api.deps import verify_management_api_key

router = APIRouter()


@router.post(
    "/stores",
    response_model=CreateStoreResponse,
    dependencies=[Depends(verify_management_api_key)],
)
def create_store(request: CreateStoreRequest):
    """Create a store."""
    store = Store(name=request.name).create()
    return {"name": store.name, "api_key": store.api_key}


@router.get(
    "/stores/{store_name}",
    response_model=GetStoreResponse,
    dependencies=[Depends(verify_management_api_key)],
)
def get_store(store_name: str):
    """Get a store."""
    store = Store.get(name=store_name)
    if not store:
        return status.HTTP_404_NOT_FOUND
    return {"name": store.name, "api_key": store.api_key}
