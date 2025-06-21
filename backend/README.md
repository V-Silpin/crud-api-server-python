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

- `POST /items/` — Create a new course
- `GET /items/` — List all courses
- `PUT /items/{item_id}` — Update a course
- `DELETE /items/{item_id}` — Delete a course

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