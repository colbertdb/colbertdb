""" This file contains the pydantic models for the core module"""

from typing import Optional
from pydantic import BaseModel


class Document(BaseModel):
    """A document in a collection."""

    content: str
    document_id: Optional[int]
    score: Optional[float]
    rank: Optional[int]
    document_id: Optional[str]
    passage_id: Optional[str]
    metadata: Optional[dict] = {}
