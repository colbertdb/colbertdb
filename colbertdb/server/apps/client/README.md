# FastAPI Documentation

## Overview

This is the API documentation for FastAPI, version 0.1.0.

## Server

- Base URL: `/client`

## Endpoints

### Connect

**POST** `/connect`

#### Summary

Connect to the server.

#### Description

This endpoint allows a client to connect to the server.

#### Request Body

The request body must be a JSON object containing the following properties:

- **api_key** (string or null, optional): The API key for authentication.

Example:

```json
{
  "api_key": "your_api_key"
}
```

#### Responses

- **200 Successful Response**

  The response will be a JSON object containing the following property:

  - **access_token** (string, required): The access token for authentication.

  Example:

  ```json
  {
    "access_token": "your_access_token"
  }
  ```

- **422 Validation Error**

  The response will be a JSON object containing details about the validation error.

  Example:

  ```json
  {
    "detail": [
      {
        "loc": ["body", "api_key"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }
  ```

## Components

### Schemas

#### ConnectRequest

- **Description**: Pydantic model for a connect request.
- **Properties**:
  - **api_key** (string or null, optional): The API key for authentication.

#### ConnectResponse

- **Description**: Pydantic model for a token.
- **Properties**:
  - **access_token** (string, required): The access token for authentication.

#### HTTPValidationError

- **Description**: Model for HTTP validation errors.
- **Properties**:
  - **detail** (array of `ValidationError`): Details of the validation error.

#### ValidationError

- **Description**: Model for a validation error.
- **Properties**:
  - **loc** (array of string or integer, required): Location of the error.
  - **msg** (string, required): Error message.
  - **type** (string, required): Error type.
```