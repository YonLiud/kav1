# WebSocket Message Protocol Template

This document defines the structure of messages exchanged between the frontend and backend.

## 1. **Request Message Format (Frontend → Backend)**

When the frontend sends a request to the backend, the message should follow this structure:

```json
{
  "type": "createUser",       // Command type or action (e.g., "createUser", "getUsers")
  "payload": {                // Data required for the action
    "name": "yossi"            // Example field, depending on the command type
  }
}
```

Request Fields:
* *type*: The type of request or action being requested (e.g., "createUser", "updateUser").

* *payload*: The data sent with the request. This can be any relevant data needed for the command (e.g., user information, parameters).

## 2. Response Message Format (Backend → Frontend)

Once the backend processes the request, it will respond with a message structured like this:

### Success Response

```json
{
  "status": "OK",           // Indicates the operation was successful
  "code": "CREATED",        // Specific code indicating the success type (e.g., "CREATED", "UPDATED")
  "msg": "User created",    // Human-readable message describing the result
  "data": {                 // Optional data specific to the result
    "id": 1,
    "name": "יוסי"
  }
}
```

### Error Response

If the operation encounters an error, the response will have this format:

```json
{
  "status": "ERROR",         // Indicates the operation failed
  "code": "USER_EXISTS",     // Specific error code (e.g., "USER_EXISTS", "VALIDATION_ERROR")
  "msg": "User already exists" // Human-readable error message
}
```

