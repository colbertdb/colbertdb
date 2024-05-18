""" Pydantic models for the client app. """

from typing import Optional
from pydantic import BaseModel


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
