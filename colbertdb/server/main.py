"""This module contains the FastAPI server for the ColbertDB API."""

from fastapi import FastAPI

from colbertdb.server.api.main import api_router
from colbertdb.server.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
def health():
    """
    Health check endpoint.
    """
    return {"status": "ok"}
