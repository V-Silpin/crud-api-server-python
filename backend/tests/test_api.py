import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crud_item():
    # Create
    data = {"id": 101, "name": "pytest", "description": "test desc", "price": 9.99}
    resp = client.post("/items/", json=data)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Course created successfully!"

    # Read
    resp = client.get("/items/")
    assert resp.status_code == 200
    items = resp.json()
    assert any(item["id"] == 101 for item in items)

    # Update
    update = {"id": 101, "name": "pytest2", "description": "desc2", "price": 19.99}
    resp = client.put("/items/101", json=update)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Course updated successfully!"

    # Delete
    resp = client.delete("/items/101")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Course deleted successfully!"

    # Confirm deletion
    resp = client.get("/items/")
    assert not any(item["id"] == 101 for item in resp.json())
