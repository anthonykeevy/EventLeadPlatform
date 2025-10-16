"""
Request Context Management
Uses Python contextvars for async-safe request-scoped data storage
"""
from contextvars import ContextVar
from typing import Optional
from dataclasses import dataclass


@dataclass
class RequestContext:
    """
    Request-scoped context data available throughout the request lifecycle.
    
    Attributes:
        request_id: Unique request identifier (UUID4)
        user_id: Authenticated user ID (None for anonymous requests)
        company_id: User's active company ID (None for anonymous requests)
        ip_address: Client IP address
        user_agent: Client user agent string
    """
    request_id: str
    user_id: Optional[int] = None
    company_id: Optional[int] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


# Context variable for request-scoped data (async-safe)
_request_context: ContextVar[Optional[RequestContext]] = ContextVar(
    "request_context", default=None
)


def set_request_context(
    request_id: str,
    user_id: Optional[int] = None,
    company_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> None:
    """
    Set request context for the current async context.
    
    Called by middleware at the start of each request.
    
    Args:
        request_id: Unique request identifier
        user_id: Authenticated user ID (optional)
        company_id: User's company ID (optional)
        ip_address: Client IP address (optional)
        user_agent: Client user agent (optional)
    """
    context = RequestContext(
        request_id=request_id,
        user_id=user_id,
        company_id=company_id,
        ip_address=ip_address,
        user_agent=user_agent
    )
    _request_context.set(context)


def get_current_request_context() -> Optional[RequestContext]:
    """
    Get the current request context.
    
    Returns None if no context is set (e.g., outside request lifecycle).
    
    Returns:
        RequestContext or None
    """
    return _request_context.get()


def update_request_context(
    user_id: Optional[int] = None,
    company_id: Optional[int] = None
) -> None:
    """
    Update user context after authentication.
    
    Called by JWT middleware to add user/company IDs to existing context.
    
    Args:
        user_id: Authenticated user ID
        company_id: User's active company ID
    """
    context = _request_context.get()
    if context is None:
        raise RuntimeError("No request context set - cannot update")
    
    if user_id is not None:
        context.user_id = user_id
    if company_id is not None:
        context.company_id = company_id


def clear_request_context() -> None:
    """
    Clear the current request context.
    
    Called at the end of request lifecycle (cleanup).
    """
    _request_context.set(None)

