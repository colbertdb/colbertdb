# ColBERTdb

ColBERTdb is an open-source database designed for efficient information retrieval using [ColBERT](https://github.com/stanford-futuredata/ColBERT) and [PLAID](https://arxiv.org/abs/2205.09707). Inspired by and heavily sourced from [RAGatouille](https://github.com/bclavie/RAGatouille/blob/main/ragatouille/models/colbert.py), ColBERTdb aims to simplify the complex process of document chunking, embedding, and indexing for retrieval-augmented generation (RAG) applications. This project emerged from the significant improvements observed when switching from a traditional vector database to a ColBERT-based index.

## Motivation

The motivation behind ColBERTdb is three-fold:

- **More Relevant Information Retrieval:** Switching from a vector database to a ColBERT-based index yielded significant improvements in information retrieval for a project. This highlighted the potential benefits of ColBERT-based indexing over traditional methods.

- **Developer-Friendly Interface:** Setting up document chunking, embedding, and indexing can be challenging and error-prone. ColBERTdb provides a simple interface with intelligent defaults, making it easier for developers to integrate powerful information retrieval capabilities into their applications.

- **Reduced Dependency on External Model Providers:** Owning the embedding model means no reliance on external embedding APIs and the ability to fine-tune the underlying model to your specific domain for even better retrieval relevancy.

## Features

- **ColBERT and PLAID Indexing:** Leverages state-of-the-art ColBERT and PLAID strategies for efficient and accurate information retrieval.
- **Simple API:** Easy-to-use REST API for managing collections, adding documents, and performing searches.
- **Intelligent Defaults:** Pre-configured settings for document chunking, embedding, and indexing, ensuring optimal performance with minimal configuration.
- **FastAPI Integration:** Built using FastAPI, providing a modern, fast, and robust web framework.
- **Python Client:** A Python client, [pycolbertdb](https://github.com/colbertdb/pycolbertdb.git), is available for seamless integration.

## Running ColBERTdb

The Docker image uses a CUDA base image and will utilize GPUs if available. It is recommended to run ColBERTdb on hardware with GPUs as indexing documents is prohibitively slow using CPUs.

```sh
docker build . -t colbertdb:latest
docker run colbertdb:latest
```

## API Documentation

Access the API documentation at the following URLs:

- Client API Documentation: http://localhost:8080/client/docs
- Collections API Documentation: http://localhost:8080/collections/docs
