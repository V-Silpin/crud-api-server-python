# CRUD API Server - Curl Examples

This document contains comprehensive curl examples for the Course Management API.

## Base URL
```
http://localhost:8000/api/v1
```

## API Examples

### Create a New Course

**Method:** `POST`  
**Endpoint:** `/items/`

Create a new course with all required details

**Curl Command:**
```bash
curl -X POST "http://localhost:8000/api/v1/items/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "id": 1,
    "name": "Python Programming",
    "description": "Learn Python from basics to advanced level",
    "price": 99.99
  }'
```

**Expected Response:**
Status Code: `201`
```json
{
  "message": "Course created successfully!",
  "course": {
    "id": 1,
    "name": "Python Programming",
    "description": "Learn Python from basics to advanced level",
    "price": 99.99
  }
}
```

---

### Get All Courses

**Method:** `GET`  
**Endpoint:** `/items/`

Retrieve a list of all available courses

**Curl Command:**
```bash
curl -X GET "http://localhost:8000/api/v1/items/" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" 
```

**Expected Response:**
Status Code: `200`
```json
[
  {
    "id": 1,
    "name": "Python Programming",
    "description": "Learn Python from basics to advanced level",
    "price": 99.99
  },
  {
    "id": 2,
    "name": "Full Stack Web Development",
    "description": "Complete MERN stack development course",
    "price": 149.99
  }
]
```

---

### Update a Course

**Method:** `PUT`  
**Endpoint:** `/items/{item_id}`

Update an existing course by ID (partial update supported)

**Curl Command:**
```bash
curl -X PUT "http://localhost:8000/api/v1/items/1" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "Advanced Python Programming",
    "description": "Master Python with advanced concepts and best practices",
    "price": 129.99
  }'
```

**Expected Response:**
Status Code: `200`
```json
{
  "message": "Course updated successfully!",
  "course": {
    "id": 1,
    "name": "Advanced Python Programming",
    "description": "Master Python with advanced concepts and best practices",
    "price": 129.99
  }
}
```

---

### Partial Update a Course

**Method:** `PUT`  
**Endpoint:** `/items/{item_id}`

Update only specific fields of a course

**Curl Command:**
```bash
curl -X PUT "http://localhost:8000/api/v1/items/1" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "price": 79.99
  }'
```

**Expected Response:**
Status Code: `200`
```json
{
  "message": "Course updated successfully!",
  "course": {
    "id": 1,
    "name": "Advanced Python Programming",
    "description": "Master Python with advanced concepts and best practices",
    "price": 79.99
  }
}
```

---

### Delete a Course

**Method:** `DELETE`  
**Endpoint:** `/items/{item_id}`

Delete a course by ID

**Curl Command:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/items/1" \
  -H "Accept: application/json" 
```

**Expected Response:**
Status Code: `200`
```json
{
  "message": "Course deleted successfully!"
}
```

---

## Error Scenarios

### Validation Error - Invalid Price

**Method:** `POST`  
**Endpoint:** `/items/`

What happens when price is invalid (negative or zero)

**Curl Command:**
```bash
curl -X POST "http://localhost:8000/api/v1/items/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "id": 1,
    "name": "Python Programming",
    "description": "Learn Python programming",
    "price": -10.00
  }'
```

**Expected Response:**
Status Code: `422`
```json
{
  "detail": [
    {
      "loc": [
        "body",
        "price"
      ],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt",
      "ctx": {
        "limit_value": 0
      }
    }
  ]
}
```

---

### Course Not Found

**Method:** `PUT`  
**Endpoint:** `/items/{item_id}`

Trying to update a non-existent course

**Curl Command:**
```bash
curl -X PUT "http://localhost:8000/api/v1/items/999" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "Non-existent Course"
  }'
```

**Expected Response:**
Status Code: `404`
```json
{
  "detail": "Course not found"
}
```

---

### Missing Required Fields

**Method:** `POST`  
**Endpoint:** `/items/`

What happens when required fields are missing

**Curl Command:**
```bash
curl -X POST "http://localhost:8000/api/v1/items/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "Incomplete Course"
  }'
```

**Expected Response:**
Status Code: `422`
```json
{
  "detail": [
    {
      "loc": [
        "body",
        "id"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": [
        "body",
        "description"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": [
        "body",
        "price"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Testing Tips

1. **Start the server first:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Test in order:** Create → Read → Update → Delete

3. **Check responses:** Each example includes the expected response format

4. **Error testing:** Try the error scenarios to understand validation

5. **Interactive docs:** Visit http://localhost:8000/docs for a web interface

