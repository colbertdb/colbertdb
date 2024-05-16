from typing import List
from pathlib import Path


class Store:
    def __init__(self, name: str = "default"):
        self.name = name

    def list_collections(self) -> List[str]:
        """List all collections in a store."""
        store_index_path = f".data/{self.name}/indexes"
        store_index_path = Path(store_index_path)
        if not store_index_path.exists():
            return []
        return [x.name for x in store_index_path.iterdir() if x.is_dir()]

    def collection_exists(self, collection_name: str) -> bool:
        """Check if a collection exists in a store."""
        store_index_path = f".data/{self.name}/indexes/{collection_name}"
        store_index_path = Path(store_index_path)
        return store_index_path.exists()
