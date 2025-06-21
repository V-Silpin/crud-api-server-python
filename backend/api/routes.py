from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.ops import PostgresOps
from typing import List, Dict, Any

router = APIRouter()

db = PostgresOps()

db.create_table("items", ["id", "name", "description", "price"])

class Course(BaseModel):
    id: int
    name: str
    description: str
    price: float
    

@router.post("/items/")
def create_item(item: Course):
    try:
        db.insert_data("items", [item.id, item.name, item.description, item.price])
        return {"message": "Course created successfully!", "course": item.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/items/")
def read_items():
    try:
        courses = db.fetch_data("items")
        return courses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/items/{item_id}")
def update_item(item_id: int, item: Course):
    try:
        db.update_data(
            "items",
            {"name": item.name, "description": item.description, "price": item.price},
            {"id": item_id}
        )
        return {"message": "Course updated successfully!", "course": item.dict()}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    try:
        db.delete_data("items", {"id": item_id})
        return {"message": "Course deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
