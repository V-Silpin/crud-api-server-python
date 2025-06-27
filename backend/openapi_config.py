"""
OpenAPI configuration and utilities for the CRUD API Server.
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from typing import Dict, Any

def custom_openapi(app: FastAPI) -> Dict[str, Any]:
    """
    Generate custom OpenAPI schema with additional metadata.
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="CRUD API Server - Course Management",
        version="1.0.0",
        description="""
        ## Course Management API
        
        This API provides full CRUD (Create, Read, Update, Delete) operations for managing courses.
        
        ### Features
        - ✅ Create new courses
        - 📖 Retrieve all courses
        - ✏️ Update existing courses
        - 🗑️ Delete courses
        
        ### Authentication
        Currently, this API does not require authentication, but it can be easily extended.
        
        ### Database
        Uses PostgreSQL as the backend database with SQLAlchemy ORM.
        
        ### Error Handling
        All endpoints include proper error handling with meaningful HTTP status codes.
        """,
        routes=app.routes,
        servers=[
            {
                "url": "http://localhost:8000",
                "description": "Development server"
            },
            {
                "url": "https://api.yourdomain.com",
                "description": "Production server"
            }
        ]
    )
    
    # Add custom extensions
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    # Add tags metadata
    openapi_schema["tags"] = [
        {
            "name": "courses",
            "description": "Operations with courses. Create, read, update and delete courses.",
            "externalDocs": {
                "description": "Course Management Guide",
                "url": "https://docs.yourdomain.com/courses"
            }
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Example response schemas for better documentation
EXAMPLE_RESPONSES = {
    "course_created": {
        "description": "Course created successfully",
        "content": {
            "application/json": {
                "example": {
                    "message": "Course created successfully!",
                    "course": {
                        "id": 1,
                        "name": "Python Programming",
                        "description": "Learn Python from basics to advanced",
                        "price": 99.99
                    }
                }
            }
        }
    },
    "course_not_found": {
        "description": "Course not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Course with ID 999 not found"
                }
            }
        }
    },
    "validation_error": {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "loc": ["body", "price"],
                            "msg": "ensure this value is greater than 0",
                            "type": "value_error.number.not_gt",
                            "ctx": {"limit_value": 0}
                        }
                    ]
                }
            }
        }
    }
}
