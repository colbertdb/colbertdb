from typing import Optional
from pydantic import BaseModel


class Document(BaseModel):
    """
    Pydantic model for a document.
    """
    id: Optional[str] = None
    text: str
    metadata: Optional[dict] = None

class Collection(BaseModel):
    """
    Pydantic model for a collection.
    """
    documents: list[Document]


class CreateCollection(BaseModel):
    """
    Pydantic model for creating a collection.
    """
    name: str
    documents: list[Document]
    options: Optional[dict] = None

class SearchOptions(BaseModel):
    """
    Pydantic model for search options.
    """
    top_k: Optional[int] = 10

class SearchCollection(BaseModel):
    """
    Pydantic model for searching a collection.
    """
    query: str
