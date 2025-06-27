#!/usr/bin/env python3
"""
Generate curl snippets and response examples from FastAPI OpenAPI schema.
Usage: python generate_curl_snippets.py
"""

import json
import os
from pathlib import Path

def generate_curl_snippets():
    """Generate comprehensive curl snippets with responses."""
    
    base_url = "http://localhost:8000/api/v1"
    
    snippets = {
        "CRUD API Server - Curl Examples": {
            "description": "Complete set of curl commands for the Course Management API",
            "base_url": base_url,
            "examples": [
                {
                    "name": "Create a New Course",
                    "method": "POST",
                    "endpoint": "/items/",
                    "description": "Create a new course with all required details",
                    "curl": f"""curl -X POST "{base_url}/items/" \\
  -H "Content-Type: application/json" \\
  -H "Accept: application/json" \\
  -d '{{
    "id": 1,
    "name": "Python Programming",
    "description": "Learn Python from basics to advanced level",
    "price": 99.99
  }}'""",
                    "expected_response": {
                        "status_code": 201,
                        "body": {
                            "message": "Course created successfully!",
                            "course": {
                                "id": 1,
                                "name": "Python Programming", 
                                "description": "Learn Python from basics to advanced level",
                                "price": 99.99
                            }
                        }
                    }
                },
                {
                    "name": "Get All Courses",
                    "method": "GET", 
                    "endpoint": "/items/",
                    "description": "Retrieve a list of all available courses",
                    "curl": f"""curl -X GET "{base_url}/items/" \\
  -H "Accept: application/json" \\
  -H "Content-Type: application/json" """,
                    "expected_response": {
                        "status_code": 200,
                        "body": [
                            {
                                "id": 1,
                                "name": "Python Programming",
                                "description": "Learn Python from basics to advanced level",
                                "price": 99.99
                            },
                            {
                                "id": 2,
                                "name": "Full Stack Web Development",
                                "description": "Complete MERN stack development course",
                                "price": 149.99
                            }
                        ]
                    }
                },
                {
                    "name": "Update a Course",
                    "method": "PUT",
                    "endpoint": "/items/{item_id}",
                    "description": "Update an existing course by ID (partial update supported)",
                    "curl": f"""curl -X PUT "{base_url}/items/1" \\
  -H "Content-Type: application/json" \\
  -H "Accept: application/json" \\
  -d '{{
    "name": "Advanced Python Programming",
    "description": "Master Python with advanced concepts and best practices",
    "price": 129.99
  }}'""",
                    "expected_response": {
                        "status_code": 200,
                        "body": {
                            "message": "Course updated successfully!",
                            "course": {
                                "id": 1,
                                "name": "Advanced Python Programming",
                                "description": "Master Python with advanced concepts and best practices",
                                "price": 129.99
                            }
                        }
                    }
                },
                {
                    "name": "Partial Update a Course",
                    "method": "PUT",
                    "endpoint": "/items/{item_id}",
                    "description": "Update only specific fields of a course",
                    "curl": f"""curl -X PUT "{base_url}/items/1" \\
  -H "Content-Type: application/json" \\
  -H "Accept: application/json" \\
  -d '{{
    "price": 79.99
  }}'""",
                    "expected_response": {
                        "status_code": 200,
                        "body": {
                            "message": "Course updated successfully!",
                            "course": {
                                "id": 1,
                                "name": "Advanced Python Programming",
                                "description": "Master Python with advanced concepts and best practices",
                                "price": 79.99
                            }
                        }
                    }
                },
                {
                    "name": "Delete a Course",
                    "method": "DELETE",
                    "endpoint": "/items/{item_id}",
                    "description": "Delete a course by ID",
                    "curl": f"""curl -X DELETE "{base_url}/items/1" \\
  -H "Accept: application/json" """,
                    "expected_response": {
                        "status_code": 200,
                        "body": {
                            "message": "Course deleted successfully!"
                        }
                    }
                }
            ]
        },
        "Error Examples": {
            "description": "Common error scenarios and their responses",
            "examples": [
                {
                    "name": "Validation Error - Invalid Price",
                    "method": "POST",
                    "endpoint": "/items/",
                    "description": "What happens when price is invalid (negative or zero)",
                    "curl": f"""curl -X POST "{base_url}/items/" \\
  -H "Content-Type: application/json" \\
  -H "Accept: application/json" \\
  -d '{{
    "id": 1,
    "name": "Python Programming",
    "description": "Learn Python programming",
    "price": -10.00
  }}'""",
                    "expected_response": {
                        "status_code": 422,
                        "body": {
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
                },
                {
                    "name": "Course Not Found",
                    "method": "PUT",
                    "endpoint": "/items/{item_id}",
                    "description": "Trying to update a non-existent course",
                    "curl": f"""curl -X PUT "{base_url}/items/999" \\
  -H "Content-Type: application/json" \\
  -H "Accept: application/json" \\
  -d '{{
    "name": "Non-existent Course"
  }}'""",
                    "expected_response": {
                        "status_code": 404,
                        "body": {
                            "detail": "Course not found"
                        }
                    }
                },
                {
                    "name": "Missing Required Fields",
                    "method": "POST",
                    "endpoint": "/items/",
                    "description": "What happens when required fields are missing",
                    "curl": f"""curl -X POST "{base_url}/items/" \\
  -H "Content-Type: application/json" \\
  -H "Accept: application/json" \\
  -d '{{
    "name": "Incomplete Course"
  }}'""",
                    "expected_response": {
                        "status_code": 422,
                        "body": {
                            "detail": [
                                {
                                    "loc": ["body", "id"],
                                    "msg": "field required",
                                    "type": "value_error.missing"
                                },
                                {
                                    "loc": ["body", "description"],
                                    "msg": "field required",
                                    "type": "value_error.missing"
                                },
                                {
                                    "loc": ["body", "price"],
                                    "msg": "field required",
                                    "type": "value_error.missing"
                                }
                            ]
                        }
                    }
                }
            ]
        }
    }
    
    return snippets

def save_curl_snippets_to_file():
    """Save curl snippets to a markdown file."""
    snippets = generate_curl_snippets()
    
    output_file = "curl_examples.md"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# CRUD API Server - Curl Examples\n\n")
        f.write("This document contains comprehensive curl examples for the Course Management API.\n\n")
        f.write("## Base URL\n")
        f.write(f"```\n{snippets['CRUD API Server - Curl Examples']['base_url']}\n```\n\n")
        
        # Write main examples
        f.write("## API Examples\n\n")
        for example in snippets['CRUD API Server - Curl Examples']['examples']:
            f.write(f"### {example['name']}\n\n")
            f.write(f"**Method:** `{example['method']}`  \n")
            f.write(f"**Endpoint:** `{example['endpoint']}`\n\n")
            f.write(f"{example['description']}\n\n")
            
            f.write("**Curl Command:**\n")
            f.write("```bash\n")
            f.write(example['curl'])
            f.write("\n```\n\n")
            
            f.write("**Expected Response:**\n")
            f.write(f"Status Code: `{example['expected_response']['status_code']}`\n")
            f.write("```json\n")
            f.write(json.dumps(example['expected_response']['body'], indent=2))
            f.write("\n```\n\n")
            f.write("---\n\n")
        
        # Write error examples
        f.write("## Error Scenarios\n\n")
        for example in snippets['Error Examples']['examples']:
            f.write(f"### {example['name']}\n\n")
            f.write(f"**Method:** `{example['method']}`  \n")
            f.write(f"**Endpoint:** `{example['endpoint']}`\n\n")
            f.write(f"{example['description']}\n\n")
            
            f.write("**Curl Command:**\n")
            f.write("```bash\n")
            f.write(example['curl'])
            f.write("\n```\n\n")
            
            f.write("**Expected Response:**\n")
            f.write(f"Status Code: `{example['expected_response']['status_code']}`\n")
            f.write("```json\n")
            f.write(json.dumps(example['expected_response']['body'], indent=2))
            f.write("\n```\n\n")
            f.write("---\n\n")
        
        # Add testing tips
        f.write("## Testing Tips\n\n")
        f.write("1. **Start the server first:**\n")
        f.write("   ```bash\n")
        f.write("   uvicorn main:app --reload --host 0.0.0.0 --port 8000\n")
        f.write("   ```\n\n")
        f.write("2. **Test in order:** Create → Read → Update → Delete\n\n")
        f.write("3. **Check responses:** Each example includes the expected response format\n\n")
        f.write("4. **Error testing:** Try the error scenarios to understand validation\n\n")
        f.write("5. **Interactive docs:** Visit http://localhost:8000/docs for a web interface\n\n")
    
    print(f"✅ Curl examples saved to '{output_file}'")
    return output_file

def save_curl_snippets_to_json():
    """Save curl snippets to a JSON file for programmatic use."""
    snippets = generate_curl_snippets()
    
    output_file = "curl_examples.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(snippets, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Curl examples saved to '{output_file}'")
    return output_file

if __name__ == "__main__":
    print("🔧 Generating curl snippets and response examples...")
    
    # Save to both markdown and JSON formats
    md_file = save_curl_snippets_to_file()
    json_file = save_curl_snippets_to_json()
    
    print(f"\n📁 Files created:")
    print(f"  📝 {md_file} - Human-readable examples")
    print(f"  📊 {json_file} - Machine-readable format")
    print(f"\n📖 Open {md_file} to see all curl examples with responses!")
