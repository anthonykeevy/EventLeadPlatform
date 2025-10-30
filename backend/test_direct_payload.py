#!/usr/bin/env python3
"""
Direct Payload Test - Test payload capture with your actual application
"""
import requests
import json

def test_payload_capture():
    """Test payload capture with the running enhanced app"""
    print("Testing Payload Capture with Enhanced App")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Login request (should capture payload)
    print("\n1. Testing login request with payload...")
    login_data = {
        "email": "user2@test.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   Login successful!")
        else:
            print(f"   Login failed: {response.text}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Dashboard request (should capture response payload)
    print("\n2. Testing dashboard request...")
    try:
        response = requests.get(f"{base_url}/api/dashboard/kpis")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   Dashboard data retrieved!")
        else:
            print(f"   Dashboard failed: {response.text}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Health check (should be excluded from payload logging)
    print("\n3. Testing health check (excluded endpoint)...")
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 50)
    print("Payload capture test completed!")
    print("\nNow check your database:")
    print("1. Go to your SQL Server Management Studio")
    print("2. Query: SELECT TOP 5 RequestPayload, ResponsePayload, Headers FROM log.ApiRequest ORDER BY CreatedDate DESC")
    print("3. You should see:")
    print("   - RequestPayload: Login JSON data")
    print("   - ResponsePayload: Dashboard/API response data")
    print("   - Headers: Non-sensitive request headers")

if __name__ == "__main__":
    test_payload_capture()
