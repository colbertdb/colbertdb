"""Test the ColbertDB API store endpoints."""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from colbertdb.core.models.store import Store
from colbertdb.server.main import app
from colbertdb.server.core.config import settings
from colbertdb.server.models import CreateStoreRequest

client = TestClient(app)


@pytest.fixture
def api_client():
    return TestClient(app)


def test_create_store(
    api_client,
):
    """Test creating a store."""
    settings.MANAGEMENT_API_KEY = "mock_management_api_key"
    mock_store = Store(name="test_store", api_key="mock_api")
    with patch("colbertdb.core.models.store.Store.create", return_value="mock_api_key"):
        with patch("colbertdb.core.models.store.Store") as MockStore:
            MockStore.return_value = mock_store
            mock_store.create.return_value = Store(
                name="test_store", api_key="mock_api_key"
            )

            request = CreateStoreRequest(name="test_store")
            response = api_client.post(
                f"{settings.API_V1_STR}/management/stores",
                json=request.dict(),
                headers={"X-MANAGEMENT-API-KEY": "mock_management_api_key"},
            )

            assert response.status_code == 200
            assert response.json() == {"name": "test_store", "api_key": "mock_api_key"}
            request = CreateStoreRequest(name="test_store")
            response = api_client.post(
                f"{settings.API_V1_STR}/management/stores",
                json=request.dict(),
                headers={"X-MANAGEMENT-API-KEY": "mock_management_api_key_bad"},
            )

            assert response.status_code == 401


def test_get_store(api_client):
    """Test getting a store."""
    settings.MANAGEMENT_API_KEY = "mock_management_api_key"
    mock_store = MagicMock()
    with patch("colbertdb.core.models.store.Store.get", return_value=mock_store):
        mock_store.name = "test_store"
        mock_store.api_key = "mock_api_key"

        response = api_client.get(
            f"{settings.API_V1_STR}/management/stores/test_store",
            headers={"X-MANAGEMENT-API-KEY": "mock_management_api_key"},
        )

        assert response.status_code == 200
        assert response.json() == {"name": "test_store", "api_key": "mock_api_key"}

    with patch("colbertdb.core.models.store.Store.get", return_value=None):
        response = api_client.get(
            f"{settings.API_V1_STR}/stores/non_existent_store",
            headers={"X-MANAGEMENT-API-KEY": "mock_management_api_key"},
        )

        assert response.status_code == 404
