import pytest
from fastapi import HTTPException, status
from colbertdb.server.services.auth import verify_token, create_access_token


def test_verify_token_valid_token():
    token = create_access_token(data={"api_key": "secret-key"})
    result = verify_token(f"Bearer {token}")
    assert result == "OK"


def test_verify_token_invalid_token():
    token = "Bearer invalid_token"
    with pytest.raises(HTTPException) as exc:
        verify_token(token)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Could not validate credentials"
