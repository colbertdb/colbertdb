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


## Getting Started

```
git clone https://github.com/colbertdb/colbertdb.git
cd colbertdb
docker compose up --build
```

## ColBERTdb API Documentation

### COLLECTIONS

**Title:** FastAPI
**Version:** 0.1.0
**Base URL:** `/collections`

#### Get Collections

**Endpoint:** `GET /`
**Summary:** Get all collections in the specified store.
**Responses:**
- **200:** Successful Response (ListCollectionsResponse)

#### Create Collection

**Endpoint:** `POST /`
**Summary:** Create a collection in the specified store.
**Request Body:**
- **Content-Type:** application/json
- **Schema:** CreateCollectionRequest
**Responses:**
- **200:** Successful Response (OperationResponse)
- **422:** Validation Error (HTTPValidationError)

#### Get Collection

**Endpoint:** `GET /{collection_name}`
**Summary:** Get details of a specific collection.
**Parameters:**
- **collection_name** (path): string
**Responses:**
- **200:** Successful Response (GetCollectionResponse)
- **422:** Validation Error (HTTPValidationError)

#### Delete Collection

**Endpoint:** `DELETE /{collection_name}`
**Summary:** Delete a specific collection.
**Parameters:**
- **collection_name** (path): string
**Responses:**
- **200:** Successful Response (OperationResponse)
- **422:** Validation Error (HTTPValidationError)

#### Add Documents

**Endpoint:** `POST /{collection_name}/documents`
**Summary:** Add documents to a specific collection.
**Parameters:**
- **collection_name** (path): string
**Request Body:**
- **Content-Type:** application/json
- **Schema:** AddToCollectionRequest
**Responses:**
- **200:** Successful Response (OperationResponse)
- **422:** Validation Error (HTTPValidationError)

#### Search Collection

**Endpoint:** `POST /{collection_name}/search`
**Summary:** Search a specific collection.
**Parameters:**
- **collection_name** (path): string
**Request Body:**
- **Content-Type:** application/json
- **Schema:** SearchCollectionRequest
**Responses:**
- **200:** Successful Response (SearchResponse)
- **422:** Validation Error (HTTPValidationError)

#### Delete Documents

**Endpoint:** `POST /{collection_name}/delete`
**Summary:** Delete documents from a specific collection.
**Parameters:**
- **collection_name** (path): string
**Request Body:**
- **Content-Type:** application/json
- **Schema:** DeleteDocumentsRequest
**Responses:**
- **200:** Successful Response (OperationResponse)
- **422:** Validation Error (HTTPValidationError)

### Schemas

#### AddToCollectionRequest

- **documents** (array of CreateCollectionDocument)

#### CreateCollectionDocument

- **content** (string)
- **metadata** (object, nullable)

#### CreateCollectionRequest

- **name** (string)
- **documents** (array of CreateCollectionDocument)
- **options** (object, nullable)

#### DeleteDocumentsRequest

- **document_ids** (array of string)

#### Document

- **content** (string)
- **document_id** (string, nullable)
- **score** (number, nullable)
- **rank** (integer, nullable)
- **passage_id** (integer, nullable)
- **metadata** (object)

#### GetCollectionResponse

- **exists** (boolean)

#### HTTPValidationError

- **detail** (array of ValidationError)

#### ListCollectionsResponse

- **collections** (array of string)

#### OperationResponse

- **status** (string)
- **message** (string)

#### SearchCollectionRequest

- **k** (integer, nullable)
- **query** (string)

#### SearchResponse

- **documents** (array of Document)

#### ValidationError

- **loc** (array of string or integer)
- **msg** (string)
- **type** (string)


### CLIENT

**Title:** FastAPI
**Version:** 0.1.0
**Base URL:** `/client`

#### Connect

**Endpoint:** `POST /connect`
**Summary:** Connect to the server.
**Request Body:**
- **Content-Type:** application/json
- **Schema:** ConnectRequest
**Responses:**
- **200:** Successful Response (ConnectResponse)
- **422:** Validation Error (HTTPValidationError)

### Schemas

#### ConnectRequest

- **api_key** (string): The API key for authentication.

#### ConnectResponse

- **access_token** (string): The access token for authentication.

#### HTTPValidationError

- **detail** (array of ValidationError)

#### ValidationError

- **loc** (array of string or integer)
- **msg** (string)
- **type** (string)