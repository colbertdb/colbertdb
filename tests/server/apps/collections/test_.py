# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=redefined-outer-name
from unittest.mock import patch, Mock

import pytest
from fastapi.testclient import TestClient
from colbertdb.server.main import app

client = TestClient(app)

documents = [
    {"content": f"This is doc{i}", "metadata": {"external_id": i}} for i in range(10)
]

search_response = [
    {
        "document_id": str(i),
        "content": f"This is doc{i}",
        "metadata": {"external_id": i},
        "score": 0.5,
        "rank": 1,
        "passage_id": i,
    }
    for i in range(4)
]


def sort_dict(d):
    """
    Convert a dictionary to a sorted list of tuples for comparison.
    """
    return sorted((k, sort_dict(v) if isinstance(v, dict) else v) for k, v in d.items())


def lists_are_equal(list1, list2):
    """
    Compare two lists of dictionaries.
    """
    list1_sorted = sorted(sort_dict(d) for d in list1)
    list2_sorted = sorted(sort_dict(d) for d in list2)
    return list1_sorted == list2_sorted


@pytest.fixture
def mock_collection():
    return Mock()


@patch("colbertdb.core.models.collection.Collection.create")
def test_create_collection(mock_collection_create):
    response = client.post(
        "/collections",
        json={"name": "my_collection", "documents": documents},
        headers={"Authorization": "Bearer token"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Collection created successfully.",
    }
    assert mock_collection_create.called


@patch("colbertdb.core.models.collection.Collection.load")
def test_add_documents(mock_load, mock_collection):
    mock_load.return_value = mock_collection
    response = client.post(
        "/collections/my_collection/documents",
        json={"documents": documents},
        headers={"Authorization": "Bearer token"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Collection updated successfully.",
    }
    assert mock_load.called
    assert mock_collection.add_to_index.called


@patch("colbertdb.core.models.collection.Collection.load")
def test_search_collection(mock_load, mock_collection):
    mock_collection.search.return_value = search_response
    mock_load.return_value = mock_collection
    response = client.post(
        "/collections/my_collection/search",
        json={"query": "keyword"},
        headers={"Authorization": "Bearer token"},
    )
    assert response.status_code == 200
    assert lists_are_equal(response.json()["documents"], search_response)
    assert mock_collection.search.called


@patch("colbertdb.core.models.collection.Collection.load")
def test_delete_collection(mock_load, mock_collection):
    mock_load.return_value = mock_collection
    response = client.delete(
        "/collections/my_collection", headers={"Authorization": "Bearer token"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Collection deleted successfully.",
    }
    assert mock_load.called
