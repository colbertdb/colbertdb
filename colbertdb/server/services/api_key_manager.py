"""This module contains the APIKeyManager class, which manages the API keys for the stores."""

import json
import secrets
import threading
from pathlib import Path
from typing import Dict, Optional
from colbertdb.server.services.file_ops import ensure_stores_file_exists
from colbertdb.server.core.config import settings

STORES_PATH = Path(settings.DATA_DIR) / settings.STORES_FILE


class APIKeyManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.api_keys: Dict[str, str] = {}
        self._load_api_keys()

    def _load_api_keys(self):
        """Load the store mappings from the stores.json file."""
        with self.lock:
            ensure_stores_file_exists()
            with open(STORES_PATH, "r", encoding="utf-8") as file:
                self.api_keys = json.load(file)

    def _save_api_keys(self):
        """Save the store mappings to the stores.json file."""
        with self.lock:
            with open(STORES_PATH, "w", encoding="utf-8") as file:
                json.dump(self.api_keys, file)

    def generate_api_key(self, length: int = 32) -> str:
        """Generate a secure API key."""
        return secrets.token_urlsafe(length)

    def get_store_by_api_key(self, api_key: str) -> Optional[str]:
        """Retrieve the store name associated with the given API key."""
        with self.lock:
            return self.api_keys.get(api_key)

    def register_store(self, store_name: str, api_key: Optional[str] = None) -> str:
        """Register a new store with an API key and refresh the cache."""
        with self.lock:
            if (
                api_key
                and api_key in self.api_keys
                and self.api_keys[api_key] != store_name
            ):
                raise ValueError(
                    "Provided API key is already associated with another store."
                )

            if not api_key:
                api_key = self.generate_api_key()

            self.api_keys[api_key] = store_name
            self._save_api_keys()
            self._load_api_keys()  # Refresh the cache
            return api_key


# Initialize the API key manager
api_key_manager = APIKeyManager()
