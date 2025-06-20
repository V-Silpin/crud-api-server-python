from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.ops import PostgresOps
from typing import List, Dict, Any

router = APIRouter()

db = PostgresOps()

class Course(BaseModel):
    id: int
    name: str
    description: str
    price: float
    

@router.post("/items/", response_model=Course)
def create_item(item: Course):
    try:
        db.insert_data("items", [item.id, item.name, item.description])
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/items/", response_model=List[Course])
def read_items():
    try:
        rows = db.fetch_data("items")
        return [Course(id=row[0], name=row[1], description=row[2]) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/items/{item_id}", response_model=Course)
def update_item(item_id: int, item: Course):
    try:
        db.update_data(
            "items",
            {"name = %s": item.name, "description = %s": item.description},
            {"id = %s": item_id}
        )
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    try:
        db.delete_data("items", {"id = %s": item_id})
        return {"detail": "Course deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
