"""
Global Exception Handler
Catches all unhandled exceptions and logs to log.ApplicationError table
"""
import traceback
import json
from typing import Union
from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from common.database import SessionLocal
from common.request_context import get_current_request_context
from common.log_filters import sanitize_stack_trace
from models.log.application_error import ApplicationError


async def global_exception_handler(
    request: Request,
    exc: Union[Exception, HTTPException]
) -> JSONResponse:
    """
    Global exception handler for all unhandled errors including HTTPExceptions.
    
    Implements Story 0.2 requirements:
    - AC-0.2.3: Catches ALL unhandled errors (including HTTPException)
    - AC-0.2.4: Logs to log.ApplicationError with stack traces
    - AC-0.2.8: Automatic logging - no manual intervention needed
    
    Features:
    - Catches all unhandled exceptions (base Exception class)
    - Catches all HTTPException (4xx/5xx errors from endpoints)
    - Extracts error details: ErrorType, ErrorMessage, StackTrace
    - Includes request context: RequestID, Path, Method, UserID, CompanyID
    - Logs to log.ApplicationError table
    - Returns standardized error response to client
    - Filters sensitive data from stack traces
    
    Args:
        request: FastAPI request object
        exc: Exception or HTTPException that was raised
        
    Returns:
        JSONResponse with standardized error format
    """
    # Get request context (includes RequestID)
    context = get_current_request_context()
    request_id = context.request_id if context else None
    
    # Determine if this is an HTTPException (controlled error) or system error
    is_http_exception = isinstance(exc, HTTPException)
    
    # Extract error details
    error_type = type(exc).__name__
    error_message = str(exc.detail) if is_http_exception else str(exc)
    stack_trace = None if is_http_exception else traceback.format_exc()
    
    # Determine severity
    if is_http_exception:
        # HTTPException are usually validation/business logic errors (less severe)
        severity = "WARNING" if exc.status_code < 500 else "ERROR"
    else:
        # Unhandled exceptions are critical system errors
        severity = "CRITICAL" if "Critical" in error_type or "Fatal" in error_type else "ERROR"
    
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
            StackTrace=sanitize_stack_trace(stack_trace) if stack_trace else None,
            Severity=severity,
            Path=str(request.url.path),
            Method=request.method,
            UserID=user_id,
            CompanyID=company_id,
            IPAddress=ip_address,
            UserAgent=user_agent,
            AdditionalData=json.dumps({
                "query_params": str(request.url.query) if request.url.query else None,
                "status_code": exc.status_code if is_http_exception else 500,
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
    
    # Return appropriate error response based on exception type
    if is_http_exception:
        # Preserve original HTTP status code and detail (FastAPI standard)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,  # FastAPI standard field
                "requestId": request_id,
            },
        )
    else:
        # Generic 500 error for unhandled exceptions
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "An unexpected error occurred. Our team has been notified.",
                "requestId": request_id,
            },
        )

