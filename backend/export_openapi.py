#!/usr/bin/env python3
"""
Script to export OpenAPI schema from FastAPI application.
Usage: python export_openapi.py
"""

import json
from main import app

def export_openapi_schema():
    """Export the OpenAPI schema to a JSON file."""
    openapi_schema = app.openapi()
    
    # Save to file
    with open("openapi_schema.json", "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
    
    print("✅ OpenAPI schema exported to 'openapi_schema.json'")
    print(f"📋 Title: {openapi_schema['info']['title']}")
    print(f"📝 Version: {openapi_schema['info']['version']}")
    print(f"🔗 Endpoints: {len(openapi_schema['paths'])} paths found")
    
    # Print available endpoints
    print("\n📍 Available endpoints:")
    for path, methods in openapi_schema['paths'].items():
        for method in methods.keys():
            if method != 'parameters':  # Skip parameters
                print(f"  {method.upper()} {path}")

if __name__ == "__main__":
    export_openapi_schema()
