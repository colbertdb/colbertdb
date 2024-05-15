from typing import Optional, Dict
from pydantic import BaseModel, Field


class Document(BaseModel):
    """A document in a collection."""

    text: str
    document_id: Optional[str] = None
    score: Optional[float] = None
    rank: Optional[int] = None
    passage_id: Optional[str] = None
    metadata: Dict = Field(default_factory=dict)
