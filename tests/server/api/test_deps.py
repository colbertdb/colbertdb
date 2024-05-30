"""Tests for the API dependencies."""

from unittest.mock import patch
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
import pytest
from colbertdb.server.api.deps import verify_store, get_store_from_access_token
from colbertdb.server.services.auth import create_access_token


def test_verify_store():
    """Test that a valid store and API key returns the store."""
    with patch(
        "colbertdb.server.services.api_key_manager.api_key_manager.get_store_by_api_key",
        return_value="default",
    ):
        store = verify_store(store_name="default", api_key="supersecret")
        assert store.name == "default"


def test_verify_store_invalid_api_key():
    """Test that an invalid API key raises an HTTPException."""
    with patch(
        "colbertdb.server.services.file_ops.load_mappings",
        return_value={"supersecret": "default"},
    ):
        with pytest.raises(HTTPException) as e:
            verify_store("default", "superdupersecret")


def test_verify_store_invalid_store_key():
    """Test that an invalid store key raises an HTTPException."""
    with patch(
        "colbertdb.server.services.file_ops.load_mappings",
        return_value={"supersecret": "default"},
    ):
        with pytest.raises(HTTPException) as e:
            verify_store("defaul", "supersecret")


def test_get_store_from_access_token():
    """Test that a valid access token returns the store."""
    with patch(
        "colbertdb.server.services.file_ops.load_mappings",
        return_value={"supersecret": "test"},
    ):
        with patch("colbertdb.core.models.store.Store.exists", return_value=True):
            token = create_access_token({"store": "default"})
            credentials = HTTPAuthorizationCredentials(
                scheme="Bearer", credentials=token
            )
            store = get_store_from_access_token(credentials)
            assert store.name == "default"


def test_get_store_from_access_token_invalid_token():
    """Test that an invalid access token raises an HTTPException."""
    with patch(
        "colbertdb.server.services.file_ops.load_mappings",
        return_value={"supersecret": "test"},
    ):
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer", credentials="badtoken"
        )
        with pytest.raises(HTTPException) as e:
            get_store_from_access_token(credentials)


def test_get_store_from_access_token_invalid_store():
    """Test that an invalid access token raises an HTTPException."""
    with patch(
        "colbertdb.server.services.file_ops.load_mappings",
        return_value={"supersecret": "default"},
    ):
        token = create_access_token({"store": "idontexist"})
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        with pytest.raises(HTTPException) as e:
            get_store_from_access_token(credentials)
