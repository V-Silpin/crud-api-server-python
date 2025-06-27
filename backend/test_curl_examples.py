#!/usr/bin/env python3
"""
Test runner for curl examples.
Automatically tests all curl snippets against the running API.
Usage: python test_curl_examples.py
"""

import requests
import json
import time
import subprocess
import sys
from typing import Dict, Any, List

def test_api_endpoint(method: str, url: str, data: Dict = None, expected_status: int = 200) -> Dict[str, Any]:
    """Test a single API endpoint."""
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            return {"success": False, "error": f"Unsupported method: {method}"}
        
        return {
            "success": True,
            "status_code": response.status_code,
            "expected_status": expected_status,
            "status_match": response.status_code == expected_status,
            "response_data": response.json() if response.content else {},
            "response_text": response.text
        }
        
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection failed - is the server running?"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def check_server_running(base_url: str) -> bool:
    """Check if the API server is running."""
    try:
        response = requests.get(f"{base_url.replace('/api/v1', '')}/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

def run_curl_tests():
    """Run all curl example tests."""
    base_url = "http://localhost:8000/api/v1"
    
    print("🧪 CRUD API Curl Test Runner")
    print("=" * 50)
    
    # Check if server is running
    if not check_server_running(base_url):
        print("❌ Server is not running!")
        print("💡 Start the server with: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        return False
    
    print("✅ Server is running")
    print()
    
    # Test cases in logical order
    test_cases = [
        {
            "name": "Create Course - Python Programming",
            "method": "POST",
            "url": f"{base_url}/items/",
            "data": {
                "id": 1,
                "name": "Python Programming",
                "description": "Learn Python from basics to advanced",
                "price": 99.99
            },
            "expected_status": 201
        },
        {
            "name": "Create Course - Web Development",
            "method": "POST", 
            "url": f"{base_url}/items/",
            "data": {
                "id": 2,
                "name": "Full Stack Web Development",
                "description": "Complete MERN stack development course",
                "price": 149.99
            },
            "expected_status": 201
        },
        {
            "name": "Get All Courses",
            "method": "GET",
            "url": f"{base_url}/items/",
            "expected_status": 200
        },
        {
            "name": "Update Course - Change Price",
            "method": "PUT",
            "url": f"{base_url}/items/1",
            "data": {
                "price": 129.99
            },
            "expected_status": 200
        },
        {
            "name": "Update Course - Full Update",
            "method": "PUT",
            "url": f"{base_url}/items/2",
            "data": {
                "name": "Advanced Full Stack Development",
                "description": "Master full stack development with advanced concepts",
                "price": 199.99
            },
            "expected_status": 200
        },
        {
            "name": "Get All Courses (After Updates)",
            "method": "GET",
            "url": f"{base_url}/items/",
            "expected_status": 200
        },
        {
            "name": "Delete Course",
            "method": "DELETE",
            "url": f"{base_url}/items/1",
            "expected_status": 200
        },
        {
            "name": "Get All Courses (After Delete)",
            "method": "GET",
            "url": f"{base_url}/items/",
            "expected_status": 200
        }
    ]
    
    # Error test cases
    error_test_cases = [
        {
            "name": "Create Course - Invalid Price (Negative)",
            "method": "POST",
            "url": f"{base_url}/items/",
            "data": {
                "id": 999,
                "name": "Invalid Course",
                "description": "This should fail",
                "price": -10.0
            },
            "expected_status": 422
        },
        {
            "name": "Create Course - Missing Fields",
            "method": "POST",
            "url": f"{base_url}/items/",
            "data": {
                "name": "Incomplete Course"
            },
            "expected_status": 422
        },
        {
            "name": "Update Non-existent Course",
            "method": "PUT",
            "url": f"{base_url}/items/999",
            "data": {
                "name": "Non-existent Course"
            },
            "expected_status": 500  # Might be 404 depending on implementation
        }
    ]
    
    # Run main tests
    print("🔧 Running Main API Tests")
    print("-" * 30)
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['name']}")
        
        result = test_api_endpoint(
            method=test['method'],
            url=test['url'],
            data=test.get('data'),
            expected_status=test['expected_status']
        )
        
        if result['success']:
            if result['status_match']:
                print(f"  ✅ PASS - Status: {result['status_code']}")
                passed += 1
                
                # Print response for GET requests
                if test['method'] == 'GET':
                    response_data = result['response_data']
                    if isinstance(response_data, list):
                        print(f"     📊 Returned {len(response_data)} courses")
                    else:
                        print(f"     📊 Response: {json.dumps(response_data, indent=6)[:100]}...")
                        
            else:
                print(f"  ❌ FAIL - Expected: {result['expected_status']}, Got: {result['status_code']}")
                print(f"     Response: {result['response_text'][:200]}...")
                failed += 1
        else:
            print(f"  ❌ ERROR - {result['error']}")
            failed += 1
        
        print()
        time.sleep(0.5)  # Small delay between requests
    
    # Run error tests
    print("🚨 Running Error Handling Tests")
    print("-" * 30)
    
    for i, test in enumerate(error_test_cases, 1):
        print(f"Error Test {i}: {test['name']}")
        
        result = test_api_endpoint(
            method=test['method'],
            url=test['url'],
            data=test.get('data'),
            expected_status=test['expected_status']
        )
        
        if result['success']:
            if result['status_code'] in [422, 404, 500]:  # Expected error codes
                print(f"  ✅ PASS - Properly handled error: {result['status_code']}")
                passed += 1
            else:
                print(f"  ⚠️  UNEXPECTED - Expected error, got: {result['status_code']}")
                failed += 1
        else:
            print(f"  ❌ ERROR - {result['error']}")
            failed += 1
        
        print()
        time.sleep(0.5)
    
    # Summary
    print("📊 Test Summary")
    print("=" * 50)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%" if (passed+failed) > 0 else "No tests run")
    
    if failed == 0:
        print("\n🎉 All tests passed! Your API is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check the output above for details.")
    
    return failed == 0

def generate_curl_commands():
    """Generate actual curl commands for manual testing."""
    base_url = "http://localhost:8000/api/v1"
    
    commands = [
        f"# Create a course\ncurl -X POST \"{base_url}/items/\" -H \"Content-Type: application/json\" -d '{{\"id\": 1, \"name\": \"Python Programming\", \"description\": \"Learn Python\", \"price\": 99.99}}'",
        f"# Get all courses\ncurl -X GET \"{base_url}/items/\" -H \"Accept: application/json\"",
        f"# Update a course\ncurl -X PUT \"{base_url}/items/1\" -H \"Content-Type: application/json\" -d '{{\"price\": 129.99}}'",
        f"# Delete a course\ncurl -X DELETE \"{base_url}/items/1\" -H \"Accept: application/json\""
    ]
    
    print("📋 Manual Curl Commands")
    print("=" * 50)
    for cmd in commands:
        print(cmd)
        print()

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Run automated tests")
    print("2. Show manual curl commands")
    print("3. Both")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice in ["1", "3"]:
        success = run_curl_tests()
        if not success:
            sys.exit(1)
    
    if choice in ["2", "3"]:
        print("\n")
        generate_curl_commands()
