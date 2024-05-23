"""Document models"""
from typing import Union
from pydantic import BaseModel


class Document(BaseModel):
    """Document class"""
    id: Union[str, None]
    content: str
    metadata: Union[dict, None]