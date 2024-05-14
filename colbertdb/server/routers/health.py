
from fastapi import APIRouter, Depends

from colbertdb.server.services.auth import verify_token

health_router = APIRouter()

@health_router.get("/health")
def health(token: str = Depends(verify_token)): # pylint: disable=unused-argument
    """Health check endpoint."""
    return {"status": "ok"}
