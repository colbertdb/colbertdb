"""Test the ColbertDB API routes."""

from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient
from colbertdb.server.main import app
from colbertdb.server.models import CreateCollectionDocument, DeleteDocumentsRequest
from colbertdb.server.core.config import settings
from colbertdb.server.services.auth import create_access_token

client = TestClient(app)


@pytest.fixture
def api_client():
    """Create a test client for the API."""
    return TestClient(app)


def test_get_collections(api_client):
    """Test retrieving all collections in a store."""
    with patch(
        "colbertdb.server.services.file_ops.load_mappings",
        return_value={"supersecret": "test"},
    ):
        with patch(
            "colbertdb.core.models.store.Store.list_collections",
            return_value=["collection1", "collection2"],
        ):
            with patch("colbertdb.core.models.store.Store.exists", return_value=True):
                token = create_access_token({"store": "test"})
                response = api_client.get(
                    f"{settings.API_V1_STR}/collections",
                    headers={"Authorization": f"Bearer {token}"},
                )

                assert response.status_code == 200
                assert response.json() == {
                    "collections": ["collection1", "collection2"]
                }


def test_get_collection(api_client):
    """Test retrieving all collections in a store."""
    with patch(
        "colbertdb.server.services.file_ops.load_mappings",
        return_value={"supersecret": "test"},
    ):
        with patch("colbertdb.core.models.store.Store.exists", return_value=True):
            token = create_access_token({"store": "test"})
            response = api_client.get(
                f"{settings.API_V1_STR}/collections/test",
                headers={"Authorization": f"Bearer {token}"},
            )

            assert response.status_code == 200


def test_create_collection(api_client):
    """Test creating a collection in a store."""
    with patch(
        "colbertdb.server.services.file_ops.load_mappings",
        return_value={"supersecret": "test"},
    ):
        with patch("colbertdb.core.models.store.Store.exists", return_value=True):
            with patch(
                "colbertdb.core.models.collection.Collection.create"
            ) as mock_create:
                with patch(
                    "colbertdb.server.api.deps.verify_store"
                ) as mock_verify_store:
                    mock_store = MagicMock()
                    mock_verify_store.return_value = mock_store

                    token = create_access_token({"store": "test"})
                    response = api_client.post(
                        f"{settings.API_V1_STR}/collections",
                        json={"name": "test", "documents": [{"content": "foo"}]},
                        headers={"Authorization": f"Bearer {token}"},
                    )

                    assert response.status_code == 200
                    assert response.json() == {
                        "status": "success",
                        "message": "Collection created successfully.",
                    }
                    mock_create.assert_called_once_with(
                        name="test",
                        collection=[
                            CreateCollectionDocument(content="foo", metadata=None)
                        ],
                        store_name="test",
                    )


def test_add_documents(api_client):
    """Test adding documents to a collection in a store."""
    with patch(
        "colbertdb.server.services.file_ops.load_mappings",
        return_value={"supersecret": "test"},
    ):
        with patch("colbertdb.core.models.store.Store.exists", return_value=True):
            with patch("colbertdb.core.models.collection.Collection.load") as mock_load:
                mock_collection = MagicMock()
                mock_load.return_value = mock_collection

                token = create_access_token({"store": "test"})
                response = api_client.post(
                    f"{settings.API_V1_STR}/collections/test/documents",
                    json={"documents": [{"content": "foo"}]},
                    headers={"Authorization": f"Bearer {token}"},
                )

                assert response.status_code == 200
                assert response.json() == {
                    "status": "success",
                    "message": "Collection updated successfully.",
                }
                mock_load.assert_called_once_with(name="test", store_name="test")
                mock_collection.add_to_index.assert_called_once_with(
                    collection=[CreateCollectionDocument(content="foo", metadata=None)]
                )


def test_delete_collection(api_client):
    """Test deleting a collection in a store."""

    with patch(
        "colbertdb.server.services.file_ops.load_mappings",
        return_value={"supersecret": "test"},
    ):
        with patch("colbertdb.core.models.store.Store.exists", return_value=True):
            with patch("colbertdb.core.models.collection.Collection.load") as mock_load:
                mock_collection = MagicMock()
                mock_load.return_value = mock_collection

                token = create_access_token({"store": "test"})
                response = api_client.delete(
                    f"{settings.API_V1_STR}/collections/test_collection",
                    headers={"Authorization": f"Bearer {token}"},
                )

                assert response.status_code == 200
                assert response.json() == {
                    "status": "success",
                    "message": "Collection deleted successfully.",
                }
                mock_load.assert_called_once_with(
                    name="test_collection", store_name="test"
                )
                mock_collection.delete.assert_called_once()


def test_delete_documents(api_client):
    """Test deleting documents from a collection in a store."""

    delete_request = DeleteDocumentsRequest(document_ids=["1", "2", "3"])
    with patch(
        "colbertdb.server.services.file_ops.load_mappings",
        return_value={"supersecret": "test"},
    ):
        with patch("colbertdb.core.models.store.Store.exists", return_value=True):
            with patch("colbertdb.core.models.collection.Collection.load") as mock_load:
                mock_collection = MagicMock()
                mock_load.return_value = mock_collection

                token = create_access_token({"store": "test"})
                response = api_client.post(
                    f"{settings.API_V1_STR}/collections/test_collection/delete",
                    json=delete_request.dict(),
                    headers={"Authorization": f"Bearer {token}"},
                )

                assert response.status_code == 200
                assert response.json() == {
                    "status": "success",
                    "message": "Collection deleted successfully.",
                }
                mock_load.assert_called_once_with(
                    name="test_collection", store_name="test"
                )
                mock_collection.delete_from_index.assert_called_once_with(
                    document_ids=["1", "2", "3"]
                )
