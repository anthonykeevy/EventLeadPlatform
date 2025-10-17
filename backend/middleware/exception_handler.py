"""
Global Exception Handler
Catches all unhandled exceptions and logs to log.ApplicationError table
"""
import traceback
import json
from typing import Union
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from backend.common.database import SessionLocal
from backend.common.request_context import get_current_request_context
from backend.common.log_filters import sanitize_stack_trace
from backend.models.log.application_error import ApplicationError


async def global_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """
    Global exception handler for all unhandled errors.
    
    Features:
    - Catches all unhandled exceptions
    - Extracts error details: ErrorType, ErrorMessage, StackTrace
    - Includes request context: RequestID, Path, Method, UserID, CompanyID
    - Logs to log.ApplicationError table
    - Returns standardized error response to client
    - Filters sensitive data from stack traces
    
    Args:
        request: FastAPI request object
        exc: Exception that was raised
        
    Returns:
        JSONResponse with standardized error format
    """
    # Get request context (includes RequestID)
    context = get_current_request_context()
    request_id = context.request_id if context else None
    
    # Extract error details
    error_type = type(exc).__name__
    error_message = str(exc)
    stack_trace = traceback.format_exc()
    
    # Determine severity (default to ERROR)
    severity = "ERROR"
    if "Critical" in error_type or "Fatal" in error_type:
        severity = "CRITICAL"
    
    # Extract user context from request.state (set by JWT middleware)
    user_id = getattr(request.state, "user_id", None)
    company_id = getattr(request.state, "company_id", None)
    
    # Extract client info
    ip_address = context.ip_address if context else None
    user_agent = context.user_agent if context else None
    
    # Log error to database (synchronous - we want to ensure it's logged)
    db: Session = SessionLocal()
    try:
        application_error = ApplicationError(
            RequestID=request_id,
            ErrorType=error_type,
            ErrorMessage=error_message,
            StackTrace=sanitize_stack_trace(stack_trace),
            Severity=severity,
            Path=str(request.url.path),
            Method=request.method,
            UserID=user_id,
            CompanyID=company_id,
            IPAddress=ip_address,
            UserAgent=user_agent,
            AdditionalData=json.dumps({
                "query_params": str(request.url.query) if request.url.query else None,
            }),
        )
        
        db.add(application_error)
        db.commit()
    except Exception as log_error:
        # Failed to log error - print to console
        print(f"Failed to log application error: {str(log_error)}")
        db.rollback()
    finally:
        db.close()
    
    # Return user-friendly error response
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": error_type,
            "message": "An unexpected error occurred. Our team has been notified.",
            "details": {
                "requestId": request_id,
                "timestamp": None,  # Could add timestamp if needed
            }
        },
    )

