# ColBERTdb
ColBERTdb is an open-source database designed for efficient information retrieval using [ColBERT](https://github.com/stanford-futuredata/ColBERT) and [PLAID](https://arxiv.org/abs/2205.09707). Inspired by and heavily sourced from [RAGatouille](https://github.com/bclavie/RAGatouille/blob/main/ragatouille/models/colbert.py), ColBERTdb aims to simplify the complex process of document chunking, embedding, and indexing for retrieval-augmented generation (RAG) applications. This project emerged from the significant improvements observed when switching from a traditional vector database to a ColBERT-based index.

## Motivation
The motivation behind ColBERTdb is three-fold:

- More relevant information retrieval: The switch from a vector database to a ColBERT-based index yielded improvements in information retrieval for a project I was working on. This highlighted the potential benefits of ColBERT-based indexing over traditional methods.

- Developer-Friendly Interface: Setting up document chunking, embedding, and indexing can be challenging and error-prone. ColBERTdb provides a simple interface with intelligent defaults, making it easier for developers to integrate powerful information retrieval capabilities into their applications.

- Reduced dependancy on external model providers: You own the embedding model which means 1) no calls to embedding apis 2) ability to find tune the underlying model to your specific domain for even better retrieval relevancy.

## Features
- ColBERT and PLAID Indexing: Leverages state-of-the-art ColBERT and PLAID strategies for efficient and accurate information retrieval.
- Simple API: Easy-to-use REST API for managing collections, adding documents, and performing searches.
- Intelligent Defaults: Pre-configured settings for document chunking, embedding, and indexing, ensuring optimal performance with minimal configuration.
- FastAPI Integration: Built using FastAPI, providing a modern, fast, and robust web framework.
- python client [pycoldbertdb](https://github.com/colbertdb/pycolbertdb.git)


## Run
From docker hub
```yaml
services:
  colbertdb:
    image: rsloanweave/colbertdb:latest
    container_name: colbertdb
    ports:
      - "8080:8080"
    environment:
      - AUTH_MODE=no_auth
    entrypoint: ["/bin/sh", "-c", "mkdir -p /src/.data && uvicorn colbertdb.server.main:app --host 0.0.0.0 --port 8080 --reload"]
    volumes:
      - ./.data:/src/.data
```
From source
```bash
git clone https://github.com/colbertdb/colbertdb.git
cd colbertdb
docker compose up --build
```

## API Docs
```
http://localhost:8080/client/docs
http://localhost:8080/collections/docs
```