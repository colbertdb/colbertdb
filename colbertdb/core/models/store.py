"""This module contains the Store class, which represents a store in ColbertDB."""

import os
import secrets
import json
from typing import List, Dict, Optional
from pathlib import Path

DATA_DIR = ".data"
STORES_FILE = os.path.join(DATA_DIR, "stores.json")


def ensure_stores_file_exists():
    """Ensure that the stores.json file exists."""
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(STORES_FILE):
        with open(STORES_FILE, "w", encoding="utf-8") as file:
            json.dump({}, file)


def load_mappings() -> Dict[str, str]:
    """Load the store mappings from the stores.json file."""
    try:
        with open(STORES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_mappings(mappings: Dict[str, str]):
    """Save the store mappings to the stores.json file."""
    with open(STORES_FILE, "w", encoding="utf-8") as file:
        json.dump(mappings, file)


def generate_api_key(length: int = 32) -> str:
    """Generate a secure API key."""
    return secrets.token_urlsafe(length)


class Store:
    """A class representing a store in ColbertDB."""

    def __init__(self, name: str = "default", api_key: Optional[str] = None):
        self.name = name
        self.api_key = api_key

    def list_collections(self) -> List[str]:
        """List all collections in a store."""
        store_index_path = Path(f"{DATA_DIR}/{self.name}/indexes")
        if not store_index_path.exists():
            return []
        return [x.name for x in store_index_path.iterdir() if x.is_dir()]

    def collection_exists(self, collection_name: str) -> bool:
        """Check if a collection exists in a store."""
        store_index_path = Path(f"{DATA_DIR}/{self.name}/indexes/{collection_name}")
        return store_index_path.exists()

    def exists(self) -> bool:
        """Check if a store exists."""
        store_path = Path(f"{DATA_DIR}/{self.name}")
        return store_path.exists()

    def create(self) -> str:
        """Create a store and register it with a new or provided API key."""
        print(f"Creating store: {self.name}")
        store_path = f"{DATA_DIR}/{self.name}"
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

        return self.api_key


ensure_stores_file_exists()
