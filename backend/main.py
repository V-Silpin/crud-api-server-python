from fastapi import FastAPI
from api.routes import router
from openapi_config import custom_openapi
import uvicorn

app = FastAPI(
    title="CRUD API Server",
    description="A FastAPI application for managing courses with full CRUD operations",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Set custom OpenAPI schema
app.openapi = lambda: custom_openapi(app)

app.include_router(router, prefix="/api/v1", tags=["courses"])

def main():
    print("Hello from crud-api-server-python!")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
