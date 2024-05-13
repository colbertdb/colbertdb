"""This module contains the FastAPI server for the ColbertDB API."""
from fastapi import FastAPI

from llama_index.readers.web import SimpleWebPageReader
from colbertdb.core.models.collection import Collection


if __name__ == "__main__":
    docs = SimpleWebPageReader(html_to_text=True).load_data(["https://radar.com/documentation/geofences"])
    collection = Collection.create(documents=[doc.text for doc in docs], name="radar_docs")