
# KILIMANI PROJECT API DOMUMENTATION

## BASE URL
### [GET] /  
**Description:** Returns a welcome message.

**Successful Response:**
```json
{
    "message": "Welcome to the kilimani project api!"
}
```

---

### [POST] /auth/register  
**Description:** Registers a new user and creates a default organization.

**Request Body:**
```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "firstname": "string",
    "lastname": "string",
    "phone": "string",
    "roles": "string (optional)"
}
```

**Successful Response:**  
Returns the payload below with a 201 success status code.
```json
{
    "status": "success",
    "message": "Registration successful",
    "data": {
        "user": {
            "userid": "string",
            "username": "string",
            "email": "string",
            "firstname": "string",
            "lastname": "string",
            "phone": "string",
            "roles": "string"
        }
    }
}
```

**Unsuccessful Registration Response:**
```json
{
    "status": "Bad request",
    "message": "Registration unsuccessful",
    "statusCode": 400
}
```

---

### [POST] /auth/login  
**Description:** Authenticates a user and returns a token.

**Request Body:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Successful Response:**  
Returns the payload below with a 200 success status code.
```json
{
    "status": "success",
    "message": "Login successful",
    "data": {
        "accessToken": "eyJh..."
    }
}
```

**Unsuccessful Login Response:**
```json
{
    "status": "Bad request",
    "message": "Login unsuccessful",
    "statusCode": 400
}
```

---

### [POST] /posts  
**Description:** Creates a new post.

**Request Body:**
```json
{
    "title": "string",
    "content": "string"
}
```

**Successful Response:**  
Returns the payload below with a 201 success status code.
```json
{
    "status": "success",
    "message": "Post created successfully",
    "data": {
        "post": {
            "id": "string",
            "title": "string",
            "content": "string",
            "created_at": "string"
        }
    }
}
```

**Unsuccessful Response:**
```json
{
    "status": "Bad request",
    "message": "Post creation unsuccessful",
    "statusCode": 400
}
```

---

### [GET] /posts/<id>  
**Description:** Retrieves a post by ID.

**Successful Response:**  
Returns the payload below with a 200 success status code.
```json
{
    "status": "success",
    "data": {
        "post": {
            "id": "string",
            "title": "string",
            "content": "string",
            "created_at": "string"
        }
    }
}
```

**Unsuccessful Response:**
```json
{
    "status": "Not found",
    "message": "Post not found",
    "statusCode": 404
}
```

---

### [PUT] /posts/<id>  
**Description:** Updates an existing post.

**Request Body:**
```json
{
    "title": "string",
    "content": "string"
}
```

**Successful Response:**  
Returns the payload below with a 200 success status code.
```json
{
    "status": "success",
    "message": "Post updated successfully",
    "data": {
        "post": {
            "id": "string",
            "title": "string",
            "content": "string",
            "updated_at": "string"
        }
    }
}
```

**Unsuccessful Response:**
```json
{
    "status": "Bad request",
    "message": "Post update unsuccessful",
    "statusCode": 400
}
```

---

### [DELETE] /posts/<id>  
**Description:** Deletes a post by ID.

**Successful Response:**  
Returns the payload below with a 200 success status code.
```json
{
    "status": "success",
    "message": "Post deleted successfully"
}
```

**Unsuccessful Response:**
```json
{
    "status": "Not found",
    "message": "Post not found",
    "statusCode": 404
}
```

---

### [POST] /comments  
**Description:** Creates a new comment.

**Request Body:**
```json
{
    "post_id": "string",
    "content": "string"
}
```

**Successful Response:**  
Returns the payload below with a 201 success status code.
```json
{
    "status": "success",
    "message": "Comment created successfully",
    "data": {
        "comment": {
            "id": "string",
            "post_id": "string",
            "content": "string",
            "created_at": "string"
        }
    }
}
```

**Unsuccessful Response:**
```json
{
    "status": "Bad request",
    "message": "Comment creation unsuccessful",
    "statusCode": 400
}
```

---

### [GET] /posts/<id>/comments  
**Description:** Retrieves all comments for a post.

**Successful Response:**  
Returns the payload below with a 200 success status code.
```json
{
    "status": "success",
    "data": {
        "comments": [
            {
                "id": "string",
                "post_id": "string",
                "content": "string",
                "created_at": "string"
            }
        ]
    }
}
```

**Unsuccessful Response:**
```json
{
    "status": "Not found",
    "message": "Post not found",
    "statusCode": 404
}
```

---

### [POST] /polls  
**Description:** Creates a new poll.

**Request Body:**
```json
{
    "question": "string",
    "options": ["string"]
}
```

**Successful Response:**  
Returns the payload below with a 201 success status code.
```json
{
    "status": "success",
    "message": "Poll created successfully",
    "data": {
        "poll": {
            "id": "string",
            "question": "string",
            "options": ["string"],
            "created_at": "string"
        }
    }
}
```

**Unsuccessful Response:**
```json
{
    "status": "Bad request",
    "message": "Poll creation unsuccessful",
    "statusCode": 400
}
```

---

### [GET] /polls/<id>  
**Description:** Retrieves a poll by ID.

**Successful Response:**  
Returns the payload below with a 200 success status code.
```json
{
    "status": "success",
    "data": {
        "poll": {
            "id": "string",
            "question": "string",
            "options": ["string"],
            "created_at": "string"
        }
    }
}
```

**Unsuccessful Response:**
```json
{
    "status": "Not found",
    "message": "Poll not found",
    "statusCode": 404
}
```

---

### [POST] /events  
**Description:** Creates a new event.

**Request Body:**
```json
{
    "title": "string",
    "description": "string",
    "date": "string (ISO 8601)"
}
```

**Successful Response:**  
Returns the payload below with a 201 success status code.
```json
{
    "status": "success",
    "message": "Event created successfully",
    "data": {
        "event": {
            "id": "string",
            "title": "string",
            "description": "string",
            "date": "string (ISO 8601)",
            "created_at": "string"
        }
    }
}
```

**Unsuccessful Response:**
```json
{
    "status": "Bad request",
    "message": "Event creation unsuccessful",
    "statusCode": 400
}
```

---

### [GET] /events  
**Description:** Retrieves all events.

**Successful Response:**  
Returns the payload below with a 200 success status code.
```json
{
    "status": "success",
    "data": {
        "events": [
            {
                "id": "string",
                "title": "string",
                "description": "string",
                "date": "string (ISO 8601)",
                "created_at": "string"
            }
        ]
    }
}
```

---

### [POST] /highalertareas  
**Description:** Creates a new high alert area.

**Request Body:**
```json
{
    "location": "string",
    "details": "string"
}
```

**Successful Response:**  
Returns the payload below with a 201 success status code.
```json
{
    "status": "success",
    "message": "High alert area created successfully",
    "data": {
        "high_alert_area": {
            "id": "string",
            "location": "string",
            "details": "string",
            "created_at": "string"
        }
    }
}
```

**Unsuccessful Response:**
```json
{
    "status": "Bad request",
    "message": "High alert area creation unsuccessful",
    "statusCode": 400
}
```