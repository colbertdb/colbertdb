"""This module contains the Store class, which represents a store in ColbertDB."""

import os

from typing import List, Optional
from pathlib import Path
from colbertdb.server.core.config import settings
from colbertdb.server.services.file_ops import (
    load_mappings,
    save_mappings,
    dir_exists,
)
from colbertdb.server.services.auth import generate_api_key


class Store:
    """A class representing a store in ColbertDB."""

    def __init__(self, name: str = "default", api_key: Optional[str] = None):
        self.name = name
        self.api_key = api_key

    @classmethod
    def get(cls, name: str) -> "Store":
        """Get a store by name."""
        mapping = load_mappings()
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
        store_index_path = Path(
            f"{settings.DATA_DIR}/{self.name}/indexes/{collection_name}"
        )
        return store_index_path.exists()

    def exists(self) -> bool:
        """Check if a store exists."""
        return dir_exists(f"{settings.DATA_DIR}/{self.name}")

    def create(self) -> str:
        """Create a store and register it with a new or provided API key."""
        print(f"Creating store: {self.name}")
        store_path = f"{settings.DATA_DIR}/{self.name}"
        os.makedirs(store_path, exist_ok=True)

        # Load existing mappings
        mappings = load_mappings()

        if self.api_key:
            if self.api_key in mappings and mappings[self.api_key] != self.name:
                raise ValueError(
                    "Provided API key is already associated with another store."
                )
            mappings[self.api_key] = self.name
        else:
            # Generate a new API key if not provided
            self.api_key = generate_api_key()
            mappings[self.api_key] = self.name

        # Save the updated mappings
        save_mappings(mappings)

        return self
