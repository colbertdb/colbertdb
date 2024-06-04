""" Pydantic models app. """

from typing import List, Optional
from pydantic import BaseModel

from colbertdb.core.models.pydantic_models import Document


class ConnectResponse(BaseModel):
    """
    Pydantic model for a token.
    """

    access_token: str


class ConnectRequest(BaseModel):
    """
    Pydantic model for a connect request.
    """

    api_key: Optional[str] = None


class CreateCollectionDocument(BaseModel):
    """
    Pydantic model for creating a collection.
    """

    content: str
    metadata: Optional[dict] = None


class ListCollectionsResponse(BaseModel):
    """
    Pydantic model for the response of listing collections.
    """

    collections: List[str]


class GetCollectionResponse(BaseModel):
    """
    Pydantic model for the response of getting a collection.
    """

    exists: bool


class OperationResponse(BaseModel):
    """
    Pydantic model for the response of an operation.
    """

    status: str
    message: str


class CreateCollectionsOptions(BaseModel):
    """
    Pydantic model for options for creating a collection.
    """

    force_create: Optional[bool] = False


class CreateCollectionRequest(BaseModel):
    """
    Pydantic model for creating a collection.
    """

    class Config:
        arbitrary_types_allowed = True

    name: str
    documents: list[CreateCollectionDocument]
    options: Optional[CreateCollectionsOptions] = CreateCollectionsOptions()


class AddToCollectionRequest(BaseModel):
    """
    Pydantic model for creating a collection.
    """

    documents: list[CreateCollectionDocument]


class SearchResponse(BaseModel):
    """
    Pydantic model for the response of creating a collection.
    """

    documents: List[Document]


class SearchOptions(BaseModel):
    """
    Pydantic model for search options.
    """

    top_k: Optional[int] = 10


class SearchCollectionRequest(BaseModel):
    """
    Pydantic model for searching a collection.
    """

    k: Optional[int] = None
    query: str


class DeleteDocumentsRequest(BaseModel):
    """
    Pydantic model for deleting documents.
    """

    document_ids: List[str]


class CreateStoreRequest(BaseModel):
    """
    Pydantic model for creating a store.
    """

    name: str


class CreateStoreResponse(BaseModel):
    """
    Pydantic model for the response of creating a store.
    """

    name: str
    api_key: str


class GetStoreResponse(BaseModel):
    """
    Pydantic model for the response of getting a store.
    """

    name: str
    api_key: str
