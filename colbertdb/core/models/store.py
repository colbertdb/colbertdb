import os

from typing import List
from pathlib import Path


class Store:
    def __init__(self, name: str = "default"):
        self.name = name

    def list_collections(self) -> List[str]:
        """List all collections in a store."""
        store_index_path = Path(f".data/{self.name}/indexes")
        if not store_index_path.exists():
            return []
        return [x.name for x in store_index_path.iterdir() if x.is_dir()]

    def collection_exists(self, collection_name: str) -> bool:
        """Check if a collection exists in a store."""
        store_index_path = Path(f".data/{self.name}/indexes/{collection_name}")
        return store_index_path.exists()

    def exists(self) -> bool:
        """Check if a store exists."""
        store_path = Path(f".data/{self.name}")
        return store_path.exists()

    def create(self):
        """Create a store."""
        print(f"Creating store: {self.name}")
        store_path = f".data/{self.name}"
        os.makedirs(store_path)
