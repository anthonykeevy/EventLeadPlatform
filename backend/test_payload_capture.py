"""
Comprehensive Test Script for Payload Capture
Run this to diagnose and verify the middleware is working.
"""

import asyncio
import json
import httpx
import time
from datetime import datetime

async def run_tests():
    """Run comprehensive tests"""
    
    print("\n" + "="*80)
    print("RUNNING PAYLOAD CAPTURE TESTS")
    print("="*80 + "\n")
    
    # Give the server a moment to start
    await asyncio.sleep(1)
    
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        
        # Test 1: Simple POST
        print("\nTest 1: Simple POST request")
        print("-" * 60)
        response = await client.post(
            "/api/test-database",
            content=b"Simple text payload",
            headers={"Content-Type": "text/plain"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test 2: JSON POST to auth endpoint
        print("\nTest 2: JSON POST to auth endpoint")
        print("-" * 60)
        test_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "test_field": "This is a test payload to verify capture"
        }
        response = await client.post(
            "/api/auth/login",
            json=test_data
        )
        print(f"Status: {response.status_code}")
        try:
            print(f"Response: {response.json()}")
        except:
            print(f"Response: {response.text}")
        
        # Test 3: Health check (excluded endpoint)
        print("\nTest 3: Health check (should be excluded)")
        print("-" * 60)
        response = await client.get("/api/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test 4: Large payload
        print("\nTest 4: Large payload (should truncate)")
        print("-" * 60)
        large_data = {
            "data": "x" * 100000,  # 100KB of data
            "metadata": "This is a large payload test",
            "timestamp": datetime.now().isoformat()
        }
        response = await client.post(
            "/api/test-database",
            json=large_data
        )
        print(f"Status: {response.status_code}")
        print(f"Response keys: {list(response.json().keys())}")
        
        # Test 5: GET request (no body)
        print("\nTest 5: GET request (no body)")
        print("-" * 60)
        response = await client.get("/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    
    print("\n" + "="*80)
    print("ALL TESTS COMPLETED")
    print("="*80 + "\n")
    
    print("Next Steps:")
    print("   1. Check the console output above for detailed debug logs")
    print("   2. Query the database to verify payloads were saved:")
    print("      SELECT TOP 10 * FROM log.ApiRequest ORDER BY CreatedDate DESC")
    print("   3. Verify RequestPayload and ResponsePayload are NOT NULL")
    print("\n")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("STARTING PAYLOAD CAPTURE TESTS")
    print("="*80 + "\n")
    
    asyncio.run(run_tests())
