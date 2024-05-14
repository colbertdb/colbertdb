""" Models for the server. """

from typing import Optional, List
from pydantic import BaseModel

from colbertdb.core.models.pydantic_models import Document


class OperationResponse(BaseModel):
    """
    Pydantic model for the response of an operation.
    """

    status: str
    message: str


class Collection(BaseModel):
    """
    Pydantic model for a collection.
    """

    documents: list[Document]


class CreateCollectionRequest(BaseModel):
    """
    Pydantic model for creating a collection.
    """

    name: str
    documents: list[Document]
    options: Optional[dict] = None


class AddToCollectionRequest(BaseModel):
    """
    Pydantic model for creating a collection.
    """

    documents: list[Document]


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

    query: str


class DeleteDocumentsRequest(BaseModel):
    ids: List[str]


class Token(BaseModel):
    """
    Pydantic model for a token.
    """

    access_token: str
    token_type: str
