"""ColbertDB models."""
from pydantic import BaseModel


class Document(BaseModel):
    """
    Document model
    """
    id: str
    text: str
    metadata: dict


class IndexCreate(BaseModel):
    """
    Index model
    """
    name: str