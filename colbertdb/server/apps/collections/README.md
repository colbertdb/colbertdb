# FastAPI Documentation

## Overview

This is the API documentation for FastAPI, version 0.1.0.

## Server

- Base URL: `/collections`

## Endpoints

### Get Collections

**GET** `/`

#### Summary

Get all collections in the specified store.

#### Description

This endpoint retrieves all collections in the specified store.

#### Responses

- **200 Successful Response**

  The response will be a JSON object containing the list of collections.

  Example:

  ```json
  {
    "collections": ["collection1", "collection2"]
  }
  ```

### Create Collection

**POST** `/`

#### Summary

Create a collection in the specified store.

#### Description

This endpoint allows the creation of a collection in the specified store.

#### Request Body

The request body must be a JSON object containing the following properties:

- **name** (string, required): The name of the collection.
- **documents** (array of `CreateCollectionDocument`, required): The documents to add to the collection.
- **options** (object or null, optional): Additional options for the collection.

Example:

```json
{
  "name": "new_collection",
  "documents": [
    {
      "content": "document content",
      "metadata": {}
    }
  ],
  "options": {}
}
```

#### Responses

- **200 Successful Response**

  The response will be a JSON object indicating the status of the operation.

  Example:

  ```json
  {
    "status": "success",
    "message": "Collection created"
  }
  ```

- **422 Validation Error**

  The response will be a JSON object containing details about the validation error.

  Example:

  ```json
  {
    "detail": [
      {
        "loc": ["body", "name"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }
  ```

### Get Collection

**GET** `/{collection_name}`

#### Summary

Get a collection by name.

#### Description

This endpoint retrieves a collection by its name.

#### Parameters

- **collection_name** (string, required): The name of the collection.

#### Responses

- **200 Successful Response**

  The response will be a JSON object containing the details of the collection.

  Example:

  ```json
  {
    "exists": true
  }
  ```

- **422 Validation Error**

  The response will be a JSON object containing details about the validation error.

  Example:

  ```json
  {
    "detail": [
      {
        "loc": ["path", "collection_name"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }
  ```

### Delete Collection

**DELETE** `/{collection_name}`

#### Summary

Delete a collection by name.

#### Description

This endpoint allows the deletion of a collection by its name.

#### Parameters

- **collection_name** (string, required): The name of the collection.

#### Responses

- **200 Successful Response**

  The response will be a JSON object indicating the status of the operation.

  Example:

  ```json
  {
    "status": "success",
    "message": "Collection deleted"
  }
  ```

- **422 Validation Error**

  The response will be a JSON object containing details about the validation error.

  Example:

  ```json
  {
    "detail": [
      {
        "loc": ["path", "collection_name"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }
  ```

### Add Documents

**POST** `/{collection_name}/documents`

#### Summary

Add documents to a collection.

#### Description

This endpoint allows adding documents to a collection.

#### Parameters

- **collection_name** (string, required): The name of the collection.

#### Request Body

The request body must be a JSON object containing the following properties:

- **documents** (array of `CreateCollectionDocument`, required): The documents to add to the collection.

Example:

```json
{
  "documents": [
    {
      "content": "document content",
      "metadata": {}
    }
  ]
}
```

#### Responses

- **200 Successful Response**

  The response will be a JSON object indicating the status of the operation.

  Example:

  ```json
  {
    "status": "success",
    "message": "Documents added"
  }
  ```

- **422 Validation Error**

  The response will be a JSON object containing details about the validation error.

  Example:

  ```json
  {
    "detail": [
      {
        "loc": ["path", "collection_name"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }
  ```

### Search Collection

**POST** `/{collection_name}/search`

#### Summary

Search a collection.

#### Description

This endpoint allows searching within a collection.

#### Parameters

- **collection_name** (string, required): The name of the collection.

#### Request Body

The request body must be a JSON object containing the following properties:

- **query** (string, required): The search query.
- **k** (integer or null, optional): The number of results to return.

Example:

```json
{
  "query": "search term",
  "k": 10
}
```

#### Responses

- **200 Successful Response**

  The response will be a JSON object containing the search results.

  Example:

  ```json
  {
    "documents": [
      {
        "content": "document content",
        "score": 0.9,
        "metadata": {}
      }
    ]
  }
  ```

- **422 Validation Error**

  The response will be a JSON object containing details about the validation error.

  Example:

  ```json
  {
    "detail": [
      {
        "loc": ["path", "collection_name"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }
  ```

### Delete Documents

**POST** `/{collection_name}/delete`

#### Summary

Delete documents from a collection.

#### Description

This endpoint allows the deletion of documents from a collection.

#### Parameters

- **collection_name** (string, required): The name of the collection.

#### Request Body

The request body must be a JSON object containing the following properties:

- **document_ids** (array of string, required): The IDs of the documents to delete.

Example:

```json
{
  "document_ids": ["doc1", "doc2"]
}
```

#### Responses

- **200 Successful Response**

  The response will be a JSON object indicating the status of the operation.

  Example:

  ```json
  {
    "status": "success",
    "message": "Documents deleted"
  }
  ```

- **422 Validation Error**

  The response will be a JSON object containing details about the validation error.

  Example:

  ```json
  {
    "detail": [
      {
        "loc": ["path", "collection_name"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }
  ```

## Components

### Schemas

#### AddToCollectionRequest

- **Description**: Pydantic model for adding documents to a collection.
- **Properties**:
  - **documents** (array of `CreateCollectionDocument`, required): The documents to add.

#### CreateCollectionDocument

- **Description**: Pydantic model for a document in a collection.
- **Properties**:
  - **content** (string, required): The content of the document.
  - **metadata** (object or null, optional): Additional metadata for the document.

#### CreateCollectionRequest

- **Description**: Pydantic model for creating a collection.
- **Properties**:
  - **name** (string, required): The name of the collection.
  - **documents** (array of `CreateCollectionDocument`, required): The documents to add to the collection.
  - **options** (object or null, optional): Additional options for the collection.

#### DeleteDocumentsRequest

- **Description**: Pydantic model for deleting documents.
- **Properties**:
  - **document_ids** (array of string, required): The IDs of the documents to delete.

#### Document

- **Description**: A document in a collection.
- **Properties**:
  - **content** (string, required): The content of the document.
  - **document_id** (string or null, optional): The ID of the document.
  - **score** (number or null, optional): The score of the document.
  - **rank** (integer or null, optional): The rank of the document.
  - **passage_id** (integer or null, optional): The passage ID of the document.
  - **metadata** (object, optional): Additional metadata for the document.

#### GetCollectionResponse

- **Description**: Pydantic model for the response of getting a collection.
- **Properties**:
  - **exists** (boolean, required): Indicates whether the collection exists.

#### HTTPValidationError

- **Description**: Model for HTTP validation errors.
- **Properties**:
  - **detail** (array of `ValidationError`): Details of the validation error.

#### ListCollectionsResponse

- **Description**: Pydantic model for the response of listing collections.
- **Properties**:
  - **collections** (array of string, required): The list of collections.

#### OperationResponse

- **Description**: Pydantic model for the response of an operation.
- **Properties**:
  - **status** (string, required

): The status of the operation.
  - **message** (string, required): A message describing the operation.

#### SearchCollectionRequest

- **Description**: Pydantic model for searching a collection.
- **Properties**:
  - **query** (string, required): The search query.
  - **k** (integer or null, optional): The number of results to return.

#### SearchResponse

- **Description**: Pydantic model for the response of searching a collection.
- **Properties**:
  - **documents** (array of `Document`, required): The search results.

#### ValidationError

- **Description**: Model for a validation error.
- **Properties**:
  - **loc** (array of string or integer, required): Location of the error.
  - **msg** (string, required): Error message.
  - **type** (string, required): Error type.
