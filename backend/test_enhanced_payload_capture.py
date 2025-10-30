#!/usr/bin/env python3
"""
Test Enhanced Payload Capture
Test the new ASGI middleware that captures request/response payloads
"""
import asyncio
import json
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

# Import our enhanced ASGI middleware
from middleware.enhanced_request_logger import EnhancedRequestLoggingMiddleware

# Create a test FastAPI app
app = FastAPI()

# Add the enhanced ASGI middleware
app.add_middleware(EnhancedRequestLoggingMiddleware)

@app.post("/api/test-payload-capture")
async def test_payload_endpoint(request: Request):
    """Test endpoint that returns the request body"""
    body = await request.body()
    return {
        "message": "Payload capture test successful",
        "received_data": json.loads(body) if body else None,
        "body_length": len(body)
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint (should be excluded from payload logging)"""
    return {"status": "healthy"}

def test_enhanced_payload_capture():
    """Test the enhanced payload capture system"""
    print("Testing Enhanced Payload Capture (ASGI Middleware)")
    print("=" * 60)
    
    with TestClient(app) as client:
        # Test 1: POST request with payload (should be logged)
        print("\n1. Testing POST request with payload...")
        test_data = {
            "test_field": "test_value",
            "numbers": [1, 2, 3],
            "nested": {"key": "value"},
            "description": "This payload should be captured in the logs"
        }
        
        response = client.post(
            "/api/test-payload-capture",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test 2: Health check (should be excluded from payload logging)
        print("\n2. Testing health check (excluded endpoint)...")
        response = client.get("/api/health")
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test 3: Large payload (should be truncated)
        print("\n3. Testing large payload (should be truncated)...")
        large_data = {
            "large_field": "x" * 15000,  # 15KB payload
            "description": "This payload should be truncated at 10KB"
        }
        
        response = client.post(
            "/api/test-payload-capture",
            json=large_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        print("\nEnhanced payload capture tests completed!")
        print("\nNote: Check the log.ApiRequest table to see:")
        print("  - RequestPayload: Should contain the request body")
        print("  - ResponsePayload: Should contain the response body")
        print("  - Headers: Should contain non-sensitive headers")
        print("  - Truncation indicators for large payloads")

if __name__ == "__main__":
    test_enhanced_payload_capture()
