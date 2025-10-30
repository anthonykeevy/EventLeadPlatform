#!/usr/bin/env python3
"""
Test script for Enhanced Request Logging Middleware
Tests payload capture functionality
"""
import requests
import json
import time

def test_enhanced_logger():
    """Test the enhanced logger with various requests"""
    base_url = "http://localhost:8000"
    
    print("Testing Enhanced Request Logging Middleware")
    print("=" * 50)
    
    # Test 1: Health check (should be excluded from payload logging)
    print("\n1. Testing health check (excluded endpoint)...")
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Login request (should capture payload)
    print("\n3. Testing login request (should capture payload)...")
    try:
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Database test endpoint
    print("\n4. Testing database endpoint...")
    try:
        response = requests.get(f"{base_url}/api/test-database")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\nTest completed! Check the database for logged requests.")
    print("   Run: python enhanced_diagnostic_logs.py --limit 5")

if __name__ == "__main__":
    test_enhanced_logger()
