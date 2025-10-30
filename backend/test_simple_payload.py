#!/usr/bin/env python3
"""
Simple test to verify payload capture is working
"""
import requests
import json
import time

def test_simple_payload():
    """Test with a simple payload to verify capture"""
    print("Testing Simple Payload Capture...")
    
    base_url = "http://localhost:8000"
    
    # Test with a simple login payload
    login_data = {
        "email": "test@example.com",
        "password": "testpassword",
        "test_payload": "This should be captured"
    }
    
    print(f"Sending login data: {login_data}")
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        # Wait a moment for logging to complete
        time.sleep(1)
        
        print("\nNow check the database manually to see if RequestPayload was captured...")
        print("Run: python enhanced_diagnostic_logs.py")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_simple_payload()
