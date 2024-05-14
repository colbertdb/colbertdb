"""This module contains the FastAPI server for the ColbertDB API."""

from fastapi import APIRouter, HTTPException
from typing import Dict

from colbertdb.core.models.collection import Collection
from colbertdb.server.models import (
    CreateCollectionRequest,
    SearchCollectionRequest,
    SearchResponse,
    AddToCollectionRequest,
    OperationResponse,
    DeleteDocumentsRequest,
)


collections_router = APIRouter(prefix="/collections")


@collections_router.post("/", response_model=OperationResponse)
def create_collection(request: CreateCollectionRequest) -> OperationResponse:
    """Create a collection in the specified store.

    Args:
        collection (CreateCollection): The collection details.

    Returns:
        str: Status of the operation.
    """
    try:
        Collection.create(name=request.name, collection=request.documents)
        return OperationResponse(
            status="success", message="Collection created successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@collections_router.post(
    "/{collection_name}/documents", response_model=OperationResponse
)
def add_documents(request: AddToCollectionRequest, collection_name: str):
    """Add documents to a collection.

    Args:
        collection (AddToCollection): The documents to add.
        collection_name (str): The name of the collection.

    Returns:
        str: Status of the operation.
    """
    try:
        loaded_collection = Collection.load(name=collection_name)
        loaded_collection.add_to_index(collection=request.documents)
        return OperationResponse(
            status="success", message="Collection updated successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@collections_router.post("/{collection_name}/search", response_model=SearchResponse)
def search_collection(
    collection_name: str, request: SearchCollectionRequest
) -> SearchResponse:
    """Search a collection.

    Args:
        collection_name (str): The name of the collection.
        search (SearchCollection): The search query.

    Returns:
        SearchResponse: The search results.
    """
    try:
        collection = Collection.load(name=collection_name)
        docs = collection.search(query=request.query)
        return SearchResponse(documents=docs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@collections_router.delete("/{collection_name}", response_model=OperationResponse)
def delete_collection(collection_name: str):
    """Delete a collection in the specified store.

    Args:
        collection_name (str): The name of the collection.

    Returns:
        str: Status of the operation.
    """
    try:
        collection = Collection.load(name=collection_name)
        return OperationResponse(
            status="success", message="Collection deleted successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@collections_router.delete(
    "/{collection_name}/documents", response_model=OperationResponse
)
def delete_documents(collection_name: str, request: DeleteDocumentsRequest):
    pass
