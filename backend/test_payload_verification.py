#!/usr/bin/env python3
"""
Test payload capture verification
"""
import requests
import json

def test_payload_verification():
    """Test payload capture with detailed verification"""
    base_url = "http://localhost:8000"
    
    print("Payload Capture Verification Test")
    print("=" * 40)
    
    # Test with a POST request that should capture payload
    test_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "test_field": "This is a test payload to verify capture",
        "nested_data": {
            "key1": "value1",
            "key2": "value2"
        }
    }
    
    print(f"Sending POST request with payload:")
    print(json.dumps(test_data, indent=2))
    print()
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Response Status: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"RequestID: {response.headers.get('X-Request-ID', 'Not found')}")
        
        print("\n" + "=" * 40)
        print("Check the application console for debug output!")
        print("You should see:")
        print("- [DEBUG] RequestID: ...")
        print("- [DEBUG] Method: POST /api/auth/login")
        print("- [DEBUG] Config capture_payloads: True")
        print("- [DEBUG] Attempting to capture request payload...")
        print("- [DEBUG] Request payload captured: YES")
        print("- [DEBUG] Request payload preview: ...")
        print("- [DEBUG] Logging to database...")
        print("- [DEBUG] ✅ Log record inserted successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_payload_verification()