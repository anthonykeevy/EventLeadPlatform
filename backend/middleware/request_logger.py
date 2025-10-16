"""
Request Logging Middleware
Automatically logs all API requests to log.ApiRequest table
"""
import time
import uuid
import json
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.background import BackgroundTask
from sqlalchemy.orm import Session

from common.database import SessionLocal
from common.request_context import set_request_context, clear_request_context
from common.log_filters import sanitize_query_params
from models.log.api_request import ApiRequest


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that automatically logs all API requests.
    
    Features:
    - Generates unique RequestID (UUID4) for each request
    - Captures request details: Method, Path, QueryParams, StatusCode, DurationMs
    - Extracts UserID and CompanyID from request.state (set by JWT middleware)
    - Extracts IPAddress and UserAgent from request headers
    - Logs to log.ApiRequest table asynchronously (non-blocking)
    - Adds X-Request-ID header to response for client tracking
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and log details.
        
        Args:
            request: FastAPI request object
            call_next: Next middleware/route handler in chain
            
        Returns:
            Response with X-Request-ID header added
        """
        # Generate unique RequestID
        request_id = str(uuid.uuid4())
        
        # Extract client info
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        # Set request context (available throughout request lifecycle)
        set_request_context(
            request_id=request_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Start timing
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Extract user context (set by JWT middleware if authenticated)
        user_id = getattr(request.state, "user_id", None)
        company_id = getattr(request.state, "company_id", None)
        
        # Prepare log data
        log_data = {
            "request_id": request_id,
            "method": request.method,
            "path": str(request.url.path),
            "query_params": sanitize_query_params(str(request.url.query)) if request.url.query else None,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "user_id": user_id,
            "company_id": company_id,
            "ip_address": ip_address,
            "user_agent": user_agent,
        }
        
        # Schedule background task to log to database (non-blocking)
        background_task = BackgroundTask(log_api_request, log_data)
        response.background = background_task
        
        # Add RequestID to response headers (for client tracking)
        response.headers["X-Request-ID"] = request_id
        
        # Clear request context after response (cleanup)
        clear_request_context()
        
        return response


def log_api_request(log_data: dict) -> None:
    """
    Log API request to database (runs in background).
    
    Args:
        log_data: Dictionary containing request details
    """
    db: Session = SessionLocal()
    try:
        api_request = ApiRequest(
            RequestID=log_data["request_id"],
            Method=log_data["method"],
            Path=log_data["path"],
            QueryParams=log_data["query_params"],
            StatusCode=log_data["status_code"],
            DurationMs=log_data["duration_ms"],
            UserID=log_data["user_id"],
            CompanyID=log_data["company_id"],
            IPAddress=log_data["ip_address"],
            UserAgent=log_data["user_agent"],
        )
        
        db.add(api_request)
        db.commit()
    except Exception as e:
        # Log error but don't fail the request
        print(f"Error logging API request: {str(e)}")
        db.rollback()
    finally:
        db.close()

