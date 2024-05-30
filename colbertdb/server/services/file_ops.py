"""This module contains functions for reading and writing to the stores file."""

import os
from typing import Dict
import json
from pathlib import Path
from colbertdb.server.core.config import settings


def ensure_stores_file_exists():
    """Ensure that the stores file exists."""
    Path(settings.DATA_DIR).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(settings.STORES_FILE):
        with open(settings.STORES_FILE, "w", encoding="utf-8") as file:
            json.dump({}, file)


def load_mappings() -> Dict[str, str]:
    """Load the store mappings from the stores file."""
    try:
        with open(settings.STORES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_mappings(mappings: Dict[str, str]):
    """Save the store mappings to the stores file."""
    with open(settings.STORES_FILE, "w", encoding="utf-8") as file:
        json.dump(mappings, file)


def dir_exists(path: str):
    """Check if a path exists."""
    path = Path(path)
    return path.is_dir()


ensure_stores_file_exists()
