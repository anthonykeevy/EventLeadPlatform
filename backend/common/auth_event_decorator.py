"""
Auth Event Logging Decorator
Automatically logs authentication events (signup, login, etc.) to log.AuthEvent

Implements Story 0.2 principle: No manual logging required
"""
from functools import wraps
from typing import Callable, Optional
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session

from modules.auth.audit_service import log_auth_event


def log_auth_attempts(event_type_success: str, event_type_failed: str):
    """
    Decorator to automatically log authentication events.
    
    Implements Story 0.2 AC-0.2.8: No manual logging required
    
    Features:
    - Automatically logs SUCCESS events when endpoint completes normally
    - Automatically logs FAILED events when HTTPException is raised
    - Captures user context (UserID, IPAddress, UserAgent)
    - Works with both sync and async endpoints
    
    Args:
        event_type_success: Event type for successful auth (e.g., "SIGNUP_SUCCESS")
        event_type_failed: Event type for failed auth (e.g., "SIGNUP_FAILED")
        
    Usage:
        @log_auth_attempts("SIGNUP_SUCCESS", "SIGNUP_FAILED")
        async def signup(request_data: SignupRequest, request: Request, db: Session):
            user = create_user(...)
            return SignupResponse(...)
    
    Example:
        When signup succeeds:
            - Creates log.AuthEvent with EventType="SIGNUP_SUCCESS"
            - Includes UserID (if created), RequestID, IPAddress, UserAgent
            
        When signup fails (e.g., duplicate email):
            - Creates log.AuthEvent with EventType="SIGNUP_FAILED"
            - Includes failure reason in details JSON
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Extract request and db from function arguments
            request: Optional[Request] = kwargs.get('request')
            db: Optional[Session] = kwargs.get('db')
            
            # Get request context
            ip_address = request.client.host if request and request.client else None
            user_agent = request.headers.get("user-agent") if request else None
            
            try:
                # Execute the endpoint function
                result = await func(*args, **kwargs)
                
                # Log SUCCESS event
                if db:
                    # Try to extract user_id from result (if it's a signup/login response)
                    user_id = None
                    if hasattr(result, 'data') and isinstance(result.data, dict):
                        user_id = result.data.get('user_id')
                    
                    log_auth_event(
                        db=db,
                        user_id=user_id,
                        event_type=event_type_success,
                        success=True,
                        details={},
                        ip_address=ip_address,
                        user_agent=user_agent
                    )
                
                return result
                
            except HTTPException as e:
                # Log FAILED event
                if db:
                    log_auth_event(
                        db=db,
                        user_id=None,
                        event_type=event_type_failed,
                        success=False,
                        details={
                            "reason": str(e.detail),
                            "status_code": e.status_code
                        },
                        ip_address=ip_address,
                        user_agent=user_agent
                    )
                
                # Re-raise the exception (will be caught by global exception handler)
                raise
            
            except Exception as e:
                # Log FAILED event for unexpected errors
                if db:
                    log_auth_event(
                        db=db,
                        user_id=None,
                        event_type=event_type_failed,
                        success=False,
                        details={
                            "reason": f"Unexpected error: {type(e).__name__}",
                            "error_message": str(e)
                        },
                        ip_address=ip_address,
                        user_agent=user_agent
                    )
                
                # Re-raise the exception (will be caught by global exception handler)
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Similar implementation for sync functions
            # (Most FastAPI endpoints are async, so this is a fallback)
            request: Optional[Request] = kwargs.get('request')
            db: Optional[Session] = kwargs.get('db')
            
            ip_address = request.client.host if request and request.client else None
            user_agent = request.headers.get("user-agent") if request else None
            
            try:
                result = func(*args, **kwargs)
                
                if db:
                    user_id = None
                    if hasattr(result, 'data') and isinstance(result.data, dict):
                        user_id = result.data.get('user_id')
                    
                    log_auth_event(
                        db=db,
                        user_id=user_id,
                        event_type=event_type_success,
                        success=True,
                        details={},
                        ip_address=ip_address,
                        user_agent=user_agent
                    )
                
                return result
                
            except HTTPException as e:
                if db:
                    log_auth_event(
                        db=db,
                        user_id=None,
                        event_type=event_type_failed,
                        success=False,
                        details={
                            "reason": str(e.detail),
                            "status_code": e.status_code
                        },
                        ip_address=ip_address,
                        user_agent=user_agent
                    )
                raise
            
            except Exception as e:
                if db:
                    log_auth_event(
                        db=db,
                        user_id=None,
                        event_type=event_type_failed,
                        success=False,
                        details={
                            "reason": f"Unexpected error: {type(e).__name__}",
                            "error_message": str(e)
                        },
                        ip_address=ip_address,
                        user_agent=user_agent
                    )
                raise
        
        # Return async wrapper if function is async, otherwise sync wrapper
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator



