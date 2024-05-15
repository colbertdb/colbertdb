""" Models for the server. """

from typing import Optional, List
from pydantic import BaseModel

from colbertdb.core.models.pydantic_models import Document


class CreateCollectionDocument(BaseModel):
    """
    Pydantic model for creating a collection.
    """

    content: str
    metadata: Optional[dict] = None


class OperationResponse(BaseModel):
    """
    Pydantic model for the response of an operation.
    """

    status: str
    message: str


class CreateCollectionRequest(BaseModel):
    """
    Pydantic model for creating a collection.
    """

    name: str
    documents: list[CreateCollectionDocument]
    options: Optional[dict] = None


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

    ids: List[str]


class ConnectResponse(BaseModel):
    """
    Pydantic model for a token.
    """

    access_token: str


class ConnectRequest(BaseModel):
    """
    Pydantic model for a connect request.
    """

    api_token: str
