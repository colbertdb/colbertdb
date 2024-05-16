""" This module contains the FastAPI application for the client API."""

from fastapi import FastAPI

from colbertdb.server.apps.client.routes import client_router

client_app = FastAPI(root_path="/client")
client_app.include_router(client_router)
