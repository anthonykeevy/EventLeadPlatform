"""
Role-Based Access Control (RBAC)
Decorators and helper functions for role-based authorization
"""
from functools import wraps
from fastapi import HTTPException, status, Request
from typing import Union, List, Callable, Any

from modules.auth.models import CurrentUser


def require_role(roles: Union[str, List[str]]) -> Callable:
    """
    Decorator to require specific role(s) for endpoint access.
    
    Checks if the current user (from request.state.user) has one of the
    specified roles. Returns 403 Forbidden if role doesn't match.
    
    Args:
        roles: Single role string or list of allowed roles
        
    Returns:
        Decorated function that enforces role requirement
        
    Raises:
        HTTPException: 401 if not authenticated, 403 if wrong role
        
    Usage:
        # Single role
        @router.get("/admin")
        @require_role("company_admin")
        async def admin_endpoint(
            request: Request,
            current_user: CurrentUser = Depends(get_current_user)
        ):
            return {"message": "Admin access granted"}
        
        # Multiple roles
        @router.get("/dashboard")
        @require_role(["company_admin", "company_user"])
        async def dashboard(
            request: Request,
            current_user: CurrentUser = Depends(get_current_user)
        ):
            return {"message": "Dashboard access granted"}
    """
    # Normalize to list
    if isinstance(roles, str):
        roles = [roles]
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Extract request from kwargs (FastAPI injects it)
            request = kwargs.get("request")
            if not request:
                # Try to find Request in args
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Request object not found. Ensure endpoint accepts 'request: Request' parameter."
                )
            
            # Get current user from request state
            if not hasattr(request.state, "user"):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            
            user = request.state.user
            
            # Check if user has role assigned
            if not user.role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User does not have any role assigned"
                )
            
            # Check if user's role matches required roles
            if user.role not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Required role: {', '.join(roles)}"
                )
            
            # Call original function
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


# Helper functions for role and authorization checks

def has_role(user: CurrentUser, role: str) -> bool:
    """
    Check if user has a specific role.
    
    Args:
        user: CurrentUser instance
        role: Role name to check
        
    Returns:
        True if user has the role, False otherwise
        
    Example:
        if has_role(current_user, "company_admin"):
            # User is company admin
            pass
    """
    return user.role == role


def is_company_admin(user: CurrentUser) -> bool:
    """
    Check if user is a company admin.
    
    Args:
        user: CurrentUser instance
        
    Returns:
        True if user is company_admin, False otherwise
        
    Example:
        if is_company_admin(current_user):
            # Grant admin privileges
            pass
    """
    return user.role == "company_admin"


def belongs_to_company(user: CurrentUser, company_id: int) -> bool:
    """
    Check if user belongs to a specific company.
    
    Args:
        user: CurrentUser instance
        company_id: Company ID to check
        
    Returns:
        True if user belongs to the company, False otherwise
        
    Example:
        if not belongs_to_company(current_user, requested_company_id):
            raise HTTPException(status_code=403, detail="Access denied")
    """
    return user.company_id == company_id


def require_company_access(user: CurrentUser, company_id: int) -> None:
    """
    Require user to belong to specific company, raise 403 if not.
    
    Helper function for endpoints that access company-specific resources.
    Enforces multi-tenant data isolation.
    
    Args:
        user: CurrentUser instance
        company_id: Required company ID
        
    Raises:
        HTTPException: 403 if user doesn't belong to company
        
    Example:
        @router.get("/companies/{company_id}/data")
        async def get_company_data(
            company_id: int,
            current_user: CurrentUser = Depends(get_current_user)
        ):
            require_company_access(current_user, company_id)
            # Proceed with data access
            pass
    """
    if not belongs_to_company(user, company_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You do not have permission to access this company's resources."
        )

