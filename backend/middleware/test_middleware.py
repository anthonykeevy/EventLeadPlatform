"""
Simple test middleware to verify middleware registration works
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class TestMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        print("\n[TEST MIDDLEWARE] Constructor called!")
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        print(f"\n[TEST MIDDLEWARE] Dispatch called for {request.method} {request.url.path}")
        response = await call_next(request)
        print(f"[TEST MIDDLEWARE] Response status: {response.status_code}")
        return response
