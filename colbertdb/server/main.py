"""This module contains the FastAPI server for the ColbertDB API."""

from fastapi import FastAPI

from colbertdb.server.routers.client import client_router
from colbertdb.server.routers.collections import collections_router
from colbertdb.server.routers.health import health_router

# Dummy API token store
api_tokens = {"valid_api_token_123": "client1"}

app = FastAPI()

app.include_router(health_router)
app.include_router(client_router)
app.include_router(collections_router)
