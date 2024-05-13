"""This module contains the FastAPI server for the ColbertDB API."""
from typing import Any

from fastapi import FastAPI

from colbertdb.core.models.collection import Collection
from colbertdb.server.models import CreateCollection, SearchCollection

app = FastAPI()

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/{store_name}/collections")
def create_collection(collection: CreateCollection, store_name: str = "default"):
    """Create a collection in the specified store."""
    docs = [doc.text for doc in collection.documents]
    Collection.create(name=collection.name, documents=docs, store_name=store_name)


@app.post("/{store_name}/collections/{collection_name}/documents")
def add_documents():
    """Add documents to a collection."""



@app.post("/{store_name}/collections/{collection_name}/search")
def search_collection(store_name: str, collection_name: str, search: SearchCollection):
    """Search a collection."""
    collection = Collection.load(name=collection_name, store_name=store_name)
    docs = collection.search(query=search.query)


