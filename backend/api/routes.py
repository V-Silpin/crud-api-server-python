from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from db.ops import PostgresOps
from typing import List, Dict, Any, Optional
import os

router = APIRouter()

# Initialize database connection with environment variable support
try:
    # Check if DATABASE_URL is provided (common in CI/CD environments)
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        db = PostgresOps(database_url=database_url)
    else:
        db = PostgresOps()
    
    # Create table if it doesn't exist
    db.create_table("items", ["id", "name", "description", "price"])
except Exception as e:
    print(f"Warning: Database connection failed: {e}")
    print("Some endpoints may not work properly without a database connection.")
    db = None

class CourseBase(BaseModel):
    name: str = Field(..., description="The name of the course", example="Python Programming")
    description: str = Field(..., description="Course description", example="Learn Python from basics to advanced")
    price: float = Field(..., gt=0, description="Course price in USD", example=99.99)

class Course(CourseBase):
    id: int = Field(..., description="Unique identifier for the course", example=1)

class CourseCreate(CourseBase):
    id: int = Field(..., description="Unique identifier for the course", example=1)

class CourseUpdate(BaseModel):
    name: Optional[str] = Field(None, description="The name of the course", example="Python Programming")
    description: Optional[str] = Field(None, description="Course description", example="Learn Python from basics to advanced")
    price: Optional[float] = Field(None, gt=0, description="Course price in USD", example=99.99)

class CourseResponse(BaseModel):
    message: str
    course: Course

class MessageResponse(BaseModel):
    message: str
    

@router.post("/items/", response_model=CourseResponse, status_code=201,
            responses={
                201: {
                    "description": "Course created successfully",
                    "content": {
                        "application/json": {
                            "examples": {
                                "python_course": {
                                    "summary": "Python Programming Course",
                                    "description": "Example of creating a Python course",
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
                                "web_dev_course": {
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
                422: {
                    "description": "Validation Error",
                    "content": {
                        "application/json": {
                            "examples": {
                                "invalid_price": {
                                    "summary": "Invalid Price",
                                    "description": "Price must be greater than 0",
                                    "value": {
                                        "detail": [
                                            {
                                                "loc": ["body", "price"],
                                                "msg": "ensure this value is greater than 0",
                                                "type": "value_error.number.not_gt",
                                                "ctx": {"limit_value": 0}
                                            }
                                        ]
                                    }
                                },
                                "missing_fields": {
                                    "summary": "Missing Required Fields",
                                    "description": "Required fields are missing",
                                    "value": {
                                        "detail": [
                                            {
                                                "loc": ["body", "name"],
                                                "msg": "field required",
                                                "type": "value_error.missing"
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    }
                }
            })
def create_item(
    item: CourseCreate,
    summary="Create a new course",
    description="Create a new course with the provided details"
):
    """
    Create a new course with all the information:
    
    - **id**: Unique identifier for the course
    - **name**: Course name
    - **description**: Detailed course description
    - **price**: Course price (must be greater than 0)
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection not available")
    
    try:
        db.insert_data("items", [item.id, item.name, item.description, item.price])
        course = Course(id=item.id, name=item.name, description=item.description, price=item.price)
        return CourseResponse(message="Course created successfully!", course=course)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/items/", response_model=List[Course],
           responses={
               200: {
                   "description": "List of all courses",
                   "content": {
                       "application/json": {
                           "examples": {
                               "multiple_courses": {
                                   "summary": "Multiple Courses",
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
                                   "summary": "Empty Course List",
                                   "description": "Response when no courses exist",
                                   "value": []
                               },
                               "single_course": {
                                   "summary": "Single Course",
                                   "description": "Response with only one course",
                                   "value": [
                                       {
                                           "id": 1,
                                           "name": "Python Programming",
                                           "description": "Learn Python from basics to advanced",
                                           "price": 99.99
                                       }
                                   ]
                               }
                           }
                       }
                   }
               }
           })
def read_items(
    summary="Get all courses",
    description="Retrieve a list of all available courses"
):
    """
    Retrieve all courses from the database.
    
    Returns a list of courses with their details.
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection not available")
    
    try:
        courses = db.fetch_data("items")
        return courses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/items/{item_id}", response_model=CourseResponse)
def update_item(
    item_id: int,
    item: CourseUpdate,
    summary="Update a course",
    description="Update an existing course by ID"
):
    """
    Update a course with new information:
    
    - **item_id**: The ID of the course to update
    - **name**: New course name (optional)
    - **description**: New course description (optional)
    - **price**: New course price (optional, must be greater than 0)
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection not available")
    
    try:
        update_data = {}
        if item.name is not None:
            update_data["name"] = item.name
        if item.description is not None:
            update_data["description"] = item.description
        if item.price is not None:
            update_data["price"] = item.price
            
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
            
        db.update_data("items", update_data, {"id": item_id})
        
        # Fetch updated course
        updated_courses = db.fetch_data("items")
        updated_course = next((c for c in updated_courses if c["id"] == item_id), None)
        
        if not updated_course:
            raise HTTPException(status_code=404, detail="Course not found")
            
        course = Course(**updated_course)
        return CourseResponse(message="Course updated successfully!", course=course)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/items/{item_id}", response_model=MessageResponse)
def delete_item(
    item_id: int,
    summary="Delete a course",
    description="Delete a course by ID"
):
    """
    Delete a course from the database.
    
    - **item_id**: The ID of the course to delete
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection not available")
    
    try:
        db.delete_data("items", {"id": item_id})
        return MessageResponse(message="Course deleted successfully!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
