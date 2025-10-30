#!/usr/bin/env python3
"""
Simple test to verify payload capture is working
"""
import requests
import json

def test_payload_capture():
    """Test payload capture with a simple POST request"""
    base_url = "http://localhost:8000"
    
    print("Testing Payload Capture")
    print("=" * 30)
    
    # Test with a simple POST request
    test_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "test_field": "This is a test payload to verify capture"
    }
    
    print(f"Sending POST request with payload: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Response Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        print(f"RequestID: {response.headers.get('X-Request-ID', 'Not found')}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_payload_capture()