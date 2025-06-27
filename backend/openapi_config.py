"""
OpenAPI configuration and utilities for the CRUD API Server.
Includes curl snippets and response examples.
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from typing import Dict, Any
import json

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

# Example response schemas for better documentation with curl snippets
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
                },
                "examples": {
                    "successful_creation": {
                        "summary": "Successful course creation",
                        "description": "Example of a successful course creation response",
                        "value": {
                            "message": "Course created successfully!",
                            "course": {
                                "id": 1,
                                "name": "Python Programming",
                                "description": "Learn Python from basics to advanced",
                                "price": 99.99
                            }
                        }
                    },
                    "web_development_course": {
                        "summary": "Web Development Course",
                        "description": "Example of creating a web development course",
                        "value": {
                            "message": "Course created successfully!",
                            "course": {
                                "id": 2,
                                "name": "Full Stack Web Development",
                                "description": "Complete MERN stack development course",
                                "price": 149.99
                            }
                        }
                    }
                }
            }
        }
    },
    "courses_list": {
        "description": "List of all courses",
        "content": {
            "application/json": {
                "example": [
                    {
                        "id": 1,
                        "name": "Python Programming",
                        "description": "Learn Python from basics to advanced",
                        "price": 99.99
                    },
                    {
                        "id": 2,
                        "name": "Full Stack Web Development",
                        "description": "Complete MERN stack development course",
                        "price": 149.99
                    }
                ],
                "examples": {
                    "multiple_courses": {
                        "summary": "Multiple courses",
                        "description": "Example response with multiple courses",
                        "value": [
                            {
                                "id": 1,
                                "name": "Python Programming",
                                "description": "Learn Python from basics to advanced",
                                "price": 99.99
                            },
                            {
                                "id": 2,
                                "name": "Full Stack Web Development",
                                "description": "Complete MERN stack development course",
                                "price": 149.99
                            },
                            {
                                "id": 3,
                                "name": "Data Science with Python",
                                "description": "Machine learning and data analysis",
                                "price": 199.99
                            }
                        ]
                    },
                    "empty_list": {
                        "summary": "No courses",
                        "description": "Response when no courses exist",
                        "value": []
                    }
                }
            }
        }
    },
    "course_updated": {
        "description": "Course updated successfully",
        "content": {
            "application/json": {
                "example": {
                    "message": "Course updated successfully!",
                    "course": {
                        "id": 1,
                        "name": "Advanced Python Programming",
                        "description": "Learn Python from basics to expert level",
                        "price": 129.99
                    }
                }
            }
        }
    },
    "course_deleted": {
        "description": "Course deleted successfully",
        "content": {
            "application/json": {
                "example": {
                    "message": "Course deleted successfully!"
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

def generate_curl_examples():
    """Generate curl command examples for all endpoints."""
    base_url = "http://localhost:8000/api/v1"
    
    curl_examples = {
        "create_course": {
            "description": "Create a new course",
            "curl": f'''curl -X POST "{base_url}/items/" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "id": 1,
    "name": "Python Programming",
    "description": "Learn Python from basics to advanced",
    "price": 99.99
  }}'
''',
            "response": '''{
  "message": "Course created successfully!",
  "course": {
    "id": 1,
    "name": "Python Programming",
    "description": "Learn Python from basics to advanced",
    "price": 99.99
  }
}'''
        },
        "get_all_courses": {
            "description": "Get all courses",
            "curl": f'''curl -X GET "{base_url}/items/" \\
  -H "Accept: application/json"
''',
            "response": '''[
  {
    "id": 1,
    "name": "Python Programming",
    "description": "Learn Python from basics to advanced",
    "price": 99.99
  },
  {
    "id": 2,
    "name": "Full Stack Web Development",
    "description": "Complete MERN stack development course",
    "price": 149.99
  }
]'''
        },
        "update_course": {
            "description": "Update an existing course",
            "curl": f'''curl -X PUT "{base_url}/items/1" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "name": "Advanced Python Programming",
    "price": 129.99
  }}'
''',
            "response": '''{
  "message": "Course updated successfully!",
  "course": {
    "id": 1,
    "name": "Advanced Python Programming",
    "description": "Learn Python from basics to advanced",
    "price": 129.99
  }
}'''
        },
        "delete_course": {
            "description": "Delete a course",
            "curl": f'''curl -X DELETE "{base_url}/items/1" \\
  -H "Accept: application/json"
''',
            "response": '''{
  "message": "Course deleted successfully!"
}'''
        }
    }
    
    return curl_examples
