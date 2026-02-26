"""
JWT Authentication Middleware
Validates JWT tokens and injects current user into request state
"""
import hashlib
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import status, HTTPException
from jose import JWTError  # type: ignore
from typing import Callable

from modules.auth.jwt_service import decode_token
from modules.auth.models import CurrentUser
from common.request_context import update_request_context

logger = logging.getLogger(__name__)

def _token_fingerprint(token: str | None) -> str:
    if not token:
        return "missing"
    try:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()[:12]
    except Exception:
        return "unavailable"


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
        "/api/invitations/",  # View invitation details (Story 1.7, Story 1.16)
        "/api/config",  # Public configuration endpoint (Story 1.13)
        "/api/countries",  # Country validation endpoints (Story 1.20)
        "/api/companies/smart-search",  # ABR search for onboarding (Story 1.19)
        "/api/users/reference/",  # Theme reference endpoints (Story 2.2)
        "/api/public/", # External Approval and other public endpoints (Story 2.12)
        "/api/form-schema/",  # DefinitionJSON schema from DB (Story 5.3) - public for Form Builder init
        "/api/form-validate",  # Story 6.1 static validator for AI correction loop
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
            HTTPException: For authentication failures (401 Unauthorized)
                          These are caught by the global exception handler and logged to log.ApplicationError
        """
        # Skip authentication for OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
            return await call_next(request)
        
        is_public = self._is_public_path(request.url.path)
        
        from fastapi.responses import JSONResponse
        
        # Extract Authorization header
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            if is_public:
                return await call_next(request)
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing authorization header"},
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Validate Bearer token format
        if not auth_header.startswith("Bearer "):
            if is_public:
                return await call_next(request)
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authorization header format. Expected 'Bearer <token>'"},
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Extract token
        token = auth_header.replace("Bearer ", "")
        
        # Decode and validate token
        try:
            payload = decode_token(token)
        except JWTError as e:
            if is_public:
                return await call_next(request)
            # Handle specific JWT errors
            error_message = str(e)
            if "expired" in error_message.lower():
                detail = "Token has expired"
            elif "signature" in error_message.lower():
                detail = "Invalid token signature"
            else:
                detail = "Invalid token"
            
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": detail},
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Verify token type is 'access'
        if payload.get("type") != "access":
            if is_public:
                return await call_next(request)
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token type. Expected access token"},
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Extract user claims from JWT payload
        try:
            user_id = int(payload["sub"])
            email = payload["email"]
            role = payload.get("role")
            company_id = payload.get("company_id")
        except (KeyError, ValueError) as e:
            if is_public:
                return await call_next(request)
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": f"Invalid token payload: {str(e)}"},
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Store user info in request state
        request.state.user = CurrentUser(
            user_id=user_id,
            email=email,
            role=role,
            company_id=company_id
        )

        if request.url.path.startswith(("/api/forms", "/api/builder", "/api/auth/me", "/api/users/me")):
            logger.info(
                "Access token fingerprint: user_id=%s path=%s fingerprint=%s",
                user_id,
                request.url.path,
                _token_fingerprint(token)
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
        
        # Check specific dynamic public endpoints
        # Handle potential trailing slashes from some clients/proxies
        clean_path = path.rstrip("/")
        if clean_path.startswith("/api/assets/") and (clean_path.endswith("/content") or clean_path.endswith("/resolve")):
            return True
        
        # For other paths, check if they start with any public path
        # But exclude root "/" from the list to avoid matching everything
        for public_path in self.PUBLIC_PATHS:
            if public_path == "/":
                continue  # Already handled above
            if path.startswith(public_path):
                return True
        
        return False

