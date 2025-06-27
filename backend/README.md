# Backend API - CRUD API Server Python

This backend is part of a full-stack CRUD application for managing courses. It is built with **FastAPI** and uses **PostgreSQL** for data storage. The backend exposes a RESTful API for creating, reading, updating, and deleting course records, and is designed to work seamlessly with the React frontend.

## Tech Stack
- **Python 3.11+**
- **FastAPI** (web framework)
- **SQLAlchemy** (ORM)
- **PostgreSQL** (database)
- **Uvicorn** (ASGI server)
- **Docker** (for containerization)

## API Endpoints

- `POST /api/v1/items/` — Create a new course
- `GET /api/v1/items/` — List all courses
- `PUT /api/v1/items/{item_id}` — Update a course
- `DELETE /api/v1/items/{item_id}` — Delete a course

## OpenAPI Documentation

FastAPI automatically generates OpenAPI (Swagger) documentation for your API:

- **Interactive API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative Documentation (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI JSON Schema**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

### Exporting OpenAPI Schema

To export the OpenAPI schema to a JSON file:

```sh
python export_openapi.py
```

This will create an `openapi_schema.json` file with your complete API specification.

### Generating Client Code

You can generate client libraries in various programming languages from your OpenAPI schema:

1. **Install the OpenAPI Generator CLI:**
   ```sh
   npm install @openapitools/openapi-generator-cli -g
   ```

2. **Generate a client (Python example):**
   ```sh
   python generate_client.py python
   ```

3. **List supported languages:**
   ```sh
   python generate_client.py --list
   ```

### Curl Examples and Testing

Generate comprehensive curl snippets with response examples:

```sh
# Generate curl examples in markdown and JSON format
python generate_curl_snippets.py
```

This creates:
- `curl_examples.md` - Human-readable examples with responses
- `curl_examples.json` - Machine-readable format

**Test your API with automated curl tests:**

```sh
# Run automated tests against your running API
python test_curl_examples.py
```

**Quick curl examples:**

```bash
# Create a course
curl -X POST "http://localhost:8000/api/v1/items/" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "name": "Python Programming",
    "description": "Learn Python from basics to advanced",
    "price": 99.99
  }'

# Get all courses
curl -X GET "http://localhost:8000/api/v1/items/" \
  -H "Accept: application/json"

# Update a course
curl -X PUT "http://localhost:8000/api/v1/items/1" \
  -H "Content-Type: application/json" \
  -d '{"price": 129.99}'

# Delete a course
curl -X DELETE "http://localhost:8000/api/v1/items/1" \
  -H "Accept: application/json"
```

See [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation (Swagger UI).

## How to Run (Standalone)

1. **Set up environment variables:**
   ```sh
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your database configuration
   # Required variables:
   # DB_NAME=your_database_name
   # DB_HOST=localhost
   # DB_USER=your_username  
   # DB_PASS=your_password
   # DB_PORT=5432
   #
   # Or use a single DATABASE_URL:
   # DATABASE_URL=postgresql://username:password@localhost:5432/database
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Start the server:**
   ```sh
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Environment Variables

The application supports two ways to configure the database connection:

### Option 1: Individual Environment Variables
```bash
DB_NAME=postgres          # Database name
DB_HOST=localhost         # Database host
DB_USER=postgres          # Database username
DB_PASS=postgres          # Database password
DB_PORT=5432             # Database port
```

### Option 2: Database URL (Recommended for Production)
```bash
DATABASE_URL=postgresql://username:password@host:port/database
```

**Note:** If both are provided, `DATABASE_URL` takes precedence.

### Default Values
If environment variables are not set, the following defaults are used:
- DB_NAME: `postgres`
- DB_HOST: `localhost`
- DB_USER: `postgres`
- DB_PASS: `postgres`
- DB_PORT: `5432`

## How to Run Tests

1. **Install test dependencies:**
   ```sh
   pip install uv && uv init
   ```
   (You should already have `fastapi` and `sqlalchemy` from the main requirements.)

2. **Run all tests:**
   ```sh
   pytest tests/
   ```

- Unit tests for database logic are in `tests/test_db_ops.py` and `tests/test_unit.py`.
- API/integration tests for endpoints are in `tests/test_api.py` (uses FastAPI's TestClient).

> **Note:** Ensure your database is running and environment variables are set before running tests.

## Interacting with the API

- Use the React frontend to add, view, edit, and delete courses.
- Alternatively, use [Postman](https://www.postman.com/) or `curl` to interact with the API directly.

## Project Structure

- Main FastAPI app: `main.py`
- API routes: `api/routes.py`
- Database operations: `db/ops.py`

## Development Notes
- The backend is designed to be run as part of a Docker Compose stack, but can also be run standalone for development.
- For full-stack development, see the main project `README.md` for instructions on running the entire stack with Docker Compose.