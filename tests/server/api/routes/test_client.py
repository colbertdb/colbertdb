"""Test the client routes."""

from unittest.mock import patch

from fastapi.testclient import TestClient
import pytest

from colbertdb.server.main import app
from colbertdb.server.core.config import settings


@pytest.fixture
def client():
    return TestClient(app)


def test_client_connect(client):
    """Test connecting to the server."""
    with patch(
        "colbertdb.server.services.api_key_manager.api_key_manager.get_store_by_api_key",
        return_value="test_store",
    ):
        with patch("colbertdb.server.api.routes.client.Store") as mock_store:
            with patch(
                "colbertdb.server.api.routes.client.create_access_token"
            ) as mock_create_access_token:
                mock_create_access_token.return_value = "test_token"
                mock_store.return_value = {"name": "test_store"}

                response = client.post(
                    f"{settings.API_V1_STR}/client/connect/test_store",
                    headers={"X-API-Key": "supersecret"},
                )
                assert response.status_code == 200
                assert response.json() == {"access_token": "test_token"}
