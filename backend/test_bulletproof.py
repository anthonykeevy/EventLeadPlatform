#!/usr/bin/env python3
"""
Test the bulletproof request logger
"""
import requests
import json
import time

def test_bulletproof_logger():
    """Test the bulletproof logger"""
    base_url = "http://localhost:8000"
    
    print("Testing Bulletproof Request Logger")
    print("=" * 40)
    
    # Test 1: Health check (should be excluded)
    print("\n1. Testing health check (excluded endpoint)...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print(f"   RequestID: {response.headers.get('X-Request-ID', 'Not found')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print(f"   RequestID: {response.headers.get('X-Request-ID', 'Not found')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Login request (should capture payload)
    print("\n3. Testing login request (should capture payload)...")
    try:
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "test_field": "This is a test payload to verify capture"
        }
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        print(f"   RequestID: {response.headers.get('X-Request-ID', 'Not found')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\nTest completed! Check the console output for debug messages.")
    print("The bulletproof logger should show detailed debug output.")

if __name__ == "__main__":
    test_bulletproof_logger()
