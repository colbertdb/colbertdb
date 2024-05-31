""" Tests for the APIKeyManager class """

from unittest.mock import MagicMock, patch
import pytest

from colbertdb.server.services.api_key_manager import APIKeyManager


@pytest.fixture
def mock_save_mappings():
    return MagicMock()


@pytest.fixture
def mock_load_mappings():
    return MagicMock()


def test_init_api_key_manager(mock_load_mappings):
    mock_load_mappings.return_value = {}
    with patch(
        "colbertdb.server.services.api_key_manager.load_mappings", mock_load_mappings
    ):
        manager = APIKeyManager()
        assert manager.api_keys == {}
        assert manager.lock is not None
        mock_load_mappings.assert_called_once()


def test_generate_api_key():
    manager = APIKeyManager()
    api_key = manager.generate_api_key()
    assert isinstance(api_key, str)
    assert len(api_key) == 43


def test_get_store_by_api_key(mock_load_mappings):
    manager = APIKeyManager()
    store_name = "example_store"
    api_key = manager.generate_api_key()

    # Mock the load_mappings to return a predefined mapping
    mock_load_mappings.return_value = {api_key: store_name}

    with patch(
        "colbertdb.server.services.api_key_manager.load_mappings", mock_load_mappings
    ):
        manager._load_api_keys()  # Ensure the internal state is loaded correctly
        retrieved_store_name = manager.get_store_by_api_key(api_key)

    assert retrieved_store_name == store_name


def test_register_store(mock_load_mappings, mock_save_mappings):
    mock_load_mappings.return_value = {}
    with patch(
        "colbertdb.server.services.api_key_manager.load_mappings", mock_load_mappings
    ):
        with patch(
            "colbertdb.server.services.api_key_manager.save_mappings",
            mock_save_mappings,
        ):
            manager = APIKeyManager()
            assert manager.api_keys == {}
            store_name = "example_store"
            api_key = manager.register_store(store_name)
    #
    assert api_key in manager.api_keys
    assert manager.api_keys[api_key] == store_name
    mock_save_mappings.assert_called_once()
    assert mock_load_mappings.call_count == 2  # once on init, once on register_store
