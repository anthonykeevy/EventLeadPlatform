"""
Simple test to verify middleware is working
"""

import requests
import json

def test_simple():
    """Test simple endpoints"""
    
    print("Testing simple endpoints...")
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Simple POST to test-database
    print("\n3. Testing POST to test-database...")
    try:
        response = requests.post("http://localhost:8000/api/test-database", 
                               json={"test": "data"}, 
                               timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_simple()
