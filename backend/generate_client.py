#!/usr/bin/env python3
"""
Script to generate client code from OpenAPI schema.
Requires openapi-generator-cli to be installed.

Installation:
npm install @openapitools/openapi-generator-cli -g

Usage: python generate_client.py [language]
Example: python generate_client.py python
"""

import subprocess
import sys
import json
from pathlib import Path

def generate_client(language="python"):
    """Generate client code from OpenAPI schema."""
    
    # First, export the OpenAPI schema
    print("📤 Exporting OpenAPI schema...")
    try:
        from main import app
        openapi_schema = app.openapi()
        
        schema_file = "openapi_schema.json"
        with open(schema_file, "w", encoding="utf-8") as f:
            json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
        print(f"✅ Schema exported to {schema_file}")
    except Exception as e:
        print(f"❌ Error exporting schema: {e}")
        return
    
    # Generate client code
    output_dir = f"generated-client-{language}"
    
    print(f"🔧 Generating {language} client code...")
    
    try:
        cmd = [
            "openapi-generator-cli",
            "generate",
            "-i", schema_file,
            "-g", language,
            "-o", output_dir,
            "--additional-properties=packageName=crud_api_client"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Client code generated successfully in '{output_dir}' directory")
            print(f"📁 Check the '{output_dir}' folder for generated files")
        else:
            print(f"❌ Error generating client code:")
            print(result.stderr)
            
    except FileNotFoundError:
        print("❌ openapi-generator-cli not found!")
        print("📥 Install it with: npm install @openapitools/openapi-generator-cli -g")
    except Exception as e:
        print(f"❌ Error: {e}")

def list_supported_languages():
    """List supported languages for client generation."""
    try:
        result = subprocess.run(
            ["openapi-generator-cli", "list"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("🔧 Supported client languages:")
            lines = result.stdout.split('\n')
            for line in lines:
                if 'CLIENT generators:' in line:
                    start_printing = True
                    continue
                if start_printing and line.strip():
                    if 'SERVER generators:' in line:
                        break
                    print(f"  - {line.strip()}")
        else:
            print("❌ Could not list supported languages")
    except FileNotFoundError:
        print("❌ openapi-generator-cli not found!")
        print("📥 Install it with: npm install @openapitools/openapi-generator-cli -g")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--list":
            list_supported_languages()
        else:
            language = sys.argv[1]
            generate_client(language)
    else:
        print("🐍 Generating Python client by default...")
        generate_client("python")
