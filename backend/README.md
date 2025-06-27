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

See [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation (Swagger UI).

## How to Run (Standalone)

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Set up environment variables:**
   - Create a `.env` file with your database connection details if needed.
3. **Start the server:**
   ```sh
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

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