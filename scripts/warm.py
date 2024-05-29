"""Warm the database with some example data."""

import os
from pathlib import Path

import json

from colbertdb.core.models.collection import Collection
from colbertdb.core.models.store import Store
from colbertdb.server.models import CreateCollectionDocument


DATA_DIR = ".data"
STORES_FILE = os.path.join(DATA_DIR, "stores.json")


def ensure_stores_file_exists():
    """Ensure that the stores.json file exists."""
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(STORES_FILE):
        with open(STORES_FILE, "w", encoding="utf-8") as file:
            json.dump({}, file)


def warm_database():
    """Warm the database with some example data."""
    store = Store(name="default", api_key=os.environ.get("API_KEY"))

    if not store.exists():
        store.create()

    text = (
        "Onigiri, also known as rice balls, are a popular Japanese snack made from white rice formed into triangular "
        "or cylindrical shapes and often wrapped in nori (seaweed). They are typically filled with a variety of "
        "ingredients, such as umeboshi (pickled plum), salted salmon, katsuobushi (bonito flakes), or kombu (kelp). "
        "Onigiri have a long history in Japan, dating back to the Heian period (794-1185), and have been a staple "
        "in Japanese cuisine due to their simplicity and versatility. "
        "The rice used in onigiri is usually seasoned with salt, which not only enhances the flavor but also acts "
        "as a preservative, making onigiri an ideal portable meal for picnics, school lunches, and travel. "
        "The nori wrap provides a convenient way to handle the rice without getting sticky hands and adds a "
        "delightful crunch and flavor contrast to the soft rice. "
        "Onigiri can be found in convenience stores, supermarkets, and specialty shops throughout Japan. They are "
        "also a favorite in bento boxes, providing a satisfying and balanced component to the meal. With endless "
        "variations in fillings and seasonings, onigiri can be customized to suit individual tastes, making them a "
        "beloved and enduring part of Japanese culinary culture."
    )

    # Insert the text into the database
    # Example insertion logic (adjust according to your database setup)
    collection = Collection.create(
        name="health",
        collection=[CreateCollectionDocument(content=text)],
        store_name=store.name,
    )

    collection.add_to_index(collection=[CreateCollectionDocument(content=text)])


if __name__ == "__main__":
    warm_database()
