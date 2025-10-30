"""
Test auth endpoint to verify payload capture
"""

import requests
import json
import time

def test_auth_payload():
    """Test auth endpoint with payload capture"""
    
    print("Testing auth endpoint for payload capture...")
    
    # Test data
    test_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "test_field": "This is a test payload to verify capture"
    }
    
    print(f"\nSending POST to /api/auth/login with data:")
    print(json.dumps(test_data, indent=2))
    
    try:
        response = requests.post(
            "http://localhost:8000/api/auth/login", 
            json=test_data,
            timeout=10
        )
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"Response Body: {json.dumps(response_json, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
            
    except requests.exceptions.Timeout:
        print("Request timed out - this might indicate the middleware is hanging")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_auth_payload()
