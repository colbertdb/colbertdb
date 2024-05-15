import os
from fastapi.testclient import TestClient
from unittest.mock import patch
from colbertdb.server.main import app

client = TestClient(app)


def test_connect_no_auth():
    response = client.post("/client/connect", json={"api_token": "any_token"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_connect_with_valid_token():
    response = client.post("/client/connect", json={"api_token": "valid_token"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_connect_with_invalid_token():
    os.environ["AUTH_MODE"] = "auth"
    response = client.post("/client/connect", json={"api_token": "invalid_token"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API token"
    os.environ["AUTH_MODE"] = "no_auth"
