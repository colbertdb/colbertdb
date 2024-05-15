""" This module contains the FastAPI application for the client API."""

import os
from fastapi import FastAPI, Request

from colbertdb.server.apps.collections.routes import collections_router
from colbertdb.server.services.auth import verify_token

collections_app = FastAPI(openapi_prefix="/collections")


@collections_app.middleware("http")
def authenticate_request(request: Request, call_next):
    """Authenticate the request."""
    if os.getenv("AUTH_MODE", "no_auth") == "no_auth":
        print("NO AUTH")
        return call_next(request)
    # Check the token
    print("AUTH")
    jwt_token = request.headers.get("Authorization")
    verify_token(jwt_token)
    return call_next(request)


collections_app.include_router(collections_router)
