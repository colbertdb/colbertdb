"""This module contains the FastAPI server for the ColbertDB API."""

from fastapi import FastAPI
from colbertdb.server.apps.client import client_app
from colbertdb.server.apps.collections import collections_app


app = FastAPI()
app.mount("/client", client_app)
app.mount("/collections", collections_app)


@app.get("/health")
def health():
    """
    Health check endpoint.
    """
    return {"status": "ok"}
