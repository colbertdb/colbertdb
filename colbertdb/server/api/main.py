"""Main API router for the FastAPI application."""

from fastapi import APIRouter
from colbertdb.server.api.routes import collections, client, management

api_router = APIRouter()

api_router.include_router(prefix="/collections", router=collections.router)
api_router.include_router(prefix="/client", router=client.router)
api_router.include_router(prefix="/management", router=management.router)
