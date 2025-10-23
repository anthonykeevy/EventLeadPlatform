"""
JWT Authentication Middleware
Validates JWT tokens and injects current user into request state
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import HTTPException, status
from jose import JWTError  # type: ignore
from typing import Callable

from modules.auth.jwt_service import decode_token
from modules.auth.models import CurrentUser
from common.request_context import update_request_context


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to validate JWT tokens and inject current user.
    
    For protected endpoints:
    1. Extracts Authorization header
    2. Validates Bearer token format
    3. Decodes and verifies JWT
    4. Stores CurrentUser in request.state.user
    5. Updates request context for logging
    
    For public endpoints:
    - Skips authentication entirely
    
    Error Handling:
    - 401: Missing, invalid, or expired token
    - Includes clear error messages
    """
    
    # Public endpoints that don't require authentication
    PUBLIC_PATHS = [
        "/api/auth/signup",
        "/api/auth/login",
        "/api/auth/verify-email",
        "/api/auth/refresh",
        "/api/auth/password-reset/request",
        "/api/auth/password-reset/validate",  # Token validation (Story 1.15)
        "/api/auth/password-reset/confirm",
        "/docs",
        "/openapi.json",
        "/redoc",
        "/api/health",
        "/api/test-database",
        "/",  # Root endpoint
    ]
    
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """
        Process each request through JWT authentication.
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware/endpoint in chain
            
        Returns:
            HTTP response
            
        Raises:
            HTTPException: 401 if authentication fails
        """
        # Skip authentication for public endpoints
        if self._is_public_path(request.url.path):
            return await call_next(request)
        
        # Extract Authorization header
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authorization header",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Validate Bearer token format
        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format. Expected 'Bearer <token>'",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Extract token
        token = auth_header.replace("Bearer ", "")
        
        # Decode and validate token
        try:
            payload = decode_token(token)
        except JWTError as e:
            # Handle specific JWT errors
            error_message = str(e)
            if "expired" in error_message.lower():
                detail = "Token has expired"
            elif "signature" in error_message.lower():
                detail = "Invalid token signature"
            else:
                detail = "Invalid token"
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=detail,
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Verify token type is 'access'
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type. Expected access token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Extract user claims from JWT payload
        try:
            user_id = int(payload["sub"])
            email = payload["email"]
            role = payload.get("role")
            company_id = payload.get("company_id")
        except (KeyError, ValueError) as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token payload: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Store user info in request state
        request.state.user = CurrentUser(
            user_id=user_id,
            email=email,
            role=role,
            company_id=company_id
        )
        
        # Update request context for logging (Story 0.2 integration)
        try:
            update_request_context(
                user_id=user_id,
                company_id=company_id
            )
        except RuntimeError:
            # Request context not yet initialized - that's okay, not critical for auth
            pass
        
        # Continue to endpoint
        response = await call_next(request)
        return response
    
    def _is_public_path(self, path: str) -> bool:
        """
        Check if path is public (doesn't require authentication).
        
        Args:
            path: Request URL path
            
        Returns:
            True if path is public, False otherwise
        """
        # Special case: exact match for root path
        if path == "/" or path == "":
            return True
        
        # For other paths, check if they start with any public path
        # But exclude root "/" from the list to avoid matching everything
        for public_path in self.PUBLIC_PATHS:
            if public_path == "/":
                continue  # Already handled above
            if path.startswith(public_path):
                return True
        
        return False

