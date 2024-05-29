"""This module contains the FastAPI server for the ColbertDB API."""

from fastapi import APIRouter, Depends, HTTPException

from colbertdb.core.models.collection import Collection
from colbertdb.core.models.store import Store
from colbertdb.server.models import (
    CreateCollectionRequest,
    SearchCollectionRequest,
    SearchResponse,
    AddToCollectionRequest,
    OperationResponse,
    DeleteDocumentsRequest,
    ListCollectionsResponse,
    GetCollectionResponse,
)
from colbertdb.server.api.deps import get_store_from_access_token

router = APIRouter()


@router.get("/", response_model=ListCollectionsResponse)
def get_collections(store: Store = Depends(get_store_from_access_token)):
    """Get all collections in the specified store.

    Returns:
        str: Status of the operation.
    """
    try:
        collections = store.list_collections()
        return ListCollectionsResponse(collections=collections)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/{collection_name}", response_model=GetCollectionResponse)
def get_collection(
    collection_name: str, store: Store = Depends(get_store_from_access_token)
):
    """Get all collections in the specified store.

    Returns:
        str: Status of the operation.
    """
    try:
        exists = store.collection_exists(collection_name=collection_name)
        return GetCollectionResponse(exists=exists)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/", response_model=OperationResponse)
def create_collection(
    request: CreateCollectionRequest,
    store: Store = Depends(get_store_from_access_token),
) -> OperationResponse:
    """Create a collection in the specified store.

    Args:
        collection (CreateCollection): The collection details.

    Returns:
        str: Status of the operation.
    """
    try:
        Collection.create(
            name=request.name, collection=request.documents, store_name=store.name
        )
        return OperationResponse(
            status="success", message="Collection created successfully."
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/{collection_name}/documents", response_model=OperationResponse)
def add_documents(
    request: AddToCollectionRequest,
    collection_name: str,
    store: Store = Depends(get_store_from_access_token),
):
    """Add documents to a collection.

    Args:
        collection (AddToCollection): The documents to add.
        collection_name (str): The name of the collection.

    Returns:
        str: Status of the operation.
    """
    try:
        loaded_collection = Collection.load(name=collection_name, store_name=store.name)
        loaded_collection.add_to_index(collection=request.documents)
        return OperationResponse(
            status="success", message="Collection updated successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/{collection_name}/search", response_model=SearchResponse)
def search_collection(
    collection_name: str,
    request: SearchCollectionRequest,
    store: Store = Depends(get_store_from_access_token),
) -> SearchResponse:
    """Search a collection.

    Args:
        collection_name (str): The name of the collection.
        search (SearchCollection): The search query.

    Returns:
        SearchResponse: The search results.
    """
    try:
        collection = Collection.load(name=collection_name, store_name=store.nam)
        docs = collection.search(query=request.query, k=request.k)
        return SearchResponse(documents=docs)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/{collection_name}", response_model=OperationResponse)
def delete_collection(
    collection_name: str, store: Store = Depends(get_store_from_access_token)
):
    """Delete a collection in the specified store.

    Args:
        collection_name (str): The name of the collection.

    Returns:
        str: Status of the operation.
    """
    try:
        collection = Collection.load(name=collection_name, store_name=store.name)
        collection.delete()
        return OperationResponse(
            status="success", message="Collection deleted successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/{collection_name}/delete", response_model=OperationResponse)
def delete_documents(
    collection_name: str,
    request: DeleteDocumentsRequest,
    store: Store = Depends(get_store_from_access_token),
):
    """Delete a collection in the specified store.

    Args:
        collection_name (str): The name of the collection.

    Returns:
        str: Status of the operation.
    """
    try:
        collection = Collection.load(name=collection_name, store_name=store.name)
        collection.delete_from_index(document_ids=request.document_ids)
        return OperationResponse(
            status="success", message="Collection deleted successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
