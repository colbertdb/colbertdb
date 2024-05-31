"""This module contains the Store class, which represents a store in ColbertDB."""

from typing import List, Optional
from pathlib import Path
from colbertdb.server.core.config import settings
from colbertdb.server.services.file_ops import (
    load_mappings,
    dir_exists,
    ensure_stores_file_exists,
    make_dir,
)
from colbertdb.server.services.api_key_manager import api_key_manager


class Store:
    """A class representing a store in ColbertDB."""

    def __init__(self, name: str = "default", api_key: Optional[str] = None):
        self.name = name
        self.api_key = api_key

    @classmethod
    def get(cls, name: str) -> "Store":
        """Get a store by name."""
        mapping = load_mappings(Path(settings.DATA_DIR) / settings.STORES_FILE)
        for key, value in mapping.items():
            if value == name:
                return cls(name=name, api_key=key)

    def list_collections(self) -> List[str]:
        """List all collections in a store."""
        store_index_path = Path(f"{settings.DATA_DIR}/{self.name}/indexes")
        if not store_index_path.exists():
            return []
        return [x.name for x in store_index_path.iterdir() if x.is_dir()]

    def collection_exists(self, collection_name: str) -> bool:
        """Check if a collection exists in a store."""
        return dir_exists(f"{settings.DATA_DIR}/{self.name}/indexes/{collection_name}")

    def exists(self) -> bool:
        """Check if a store exists."""
        return dir_exists(f"{settings.DATA_DIR}/{self.name}")

    def create(self) -> str:
        """Create a store and register it with a new API key."""
        # Check if the store already exists
        if self.exists():
            raise ValueError(f"Store {self.name} already exists.")

        # make store directory
        make_dir(f"{settings.DATA_DIR}/{self.name}")

        # Register store and generate api key
        self.api_key = api_key_manager.register_store(self.name)

        return self


ensure_stores_file_exists()
