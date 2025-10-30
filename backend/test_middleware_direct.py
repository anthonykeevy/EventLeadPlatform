#!/usr/bin/env python3
"""
Direct test of middleware functionality
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from middleware.request_logger import RequestLoggingMiddleware

# Create a test app
app = FastAPI()
app.add_middleware(RequestLoggingMiddleware)

@app.post("/test")
async def test_endpoint(request: Request):
    """Test endpoint that returns the request body"""
    body = await request.body()
    return {"received_body": body.decode('utf-8')}

def test_middleware():
    """Test middleware directly"""
    print("Testing Middleware Directly...")
    
    client = TestClient(app)
    
    # Test with a simple payload
    test_data = {"test": "payload", "number": 123}
    
    print(f"Sending test data: {test_data}")
    response = client.post("/test", json=test_data)
    
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")
    
    # Check if the request was logged
    print("\nChecking if request was logged...")
    try:
        from common.database import get_db
        with next(get_db()) as db:
            result = db.execute("""
                SELECT TOP 1 Method, Path, RequestPayload, ResponsePayload 
                FROM log.ApiRequest 
                WHERE Path = '/test' 
                ORDER BY CreatedDate DESC
            """).fetchone()
            
            if result:
                print(f"Found log entry:")
                print(f"  Method: {result.Method}")
                print(f"  Path: {result.Path}")
                print(f"  RequestPayload: {result.RequestPayload}")
                print(f"  ResponsePayload: {result.ResponsePayload}")
            else:
                print("No log entry found")
                
    except Exception as e:
        print(f"Error checking logs: {e}")

if __name__ == "__main__":
    test_middleware()
