"""
Authentication Dependencies
FastAPI dependencies for accessing current authenticated user
"""
from fastapi import Depends, HTTPException, status, Request
from typing import Optional

from modules.auth.models import CurrentUser


def get_current_user(request: Request) -> CurrentUser:
    """
    Dependency to get current authenticated user.
    
    Requires JWTAuthMiddleware to have run first.
    Use this dependency on protected endpoints that require authentication.
    
    Args:
        request: FastAPI request object
        
    Returns:
        CurrentUser model with user_id, email, role, company_id
        
    Raises:
        HTTPException: 401 if user not authenticated
        
    Example:
        @router.get("/api/users/me")
        async def get_profile(
            current_user: CurrentUser = Depends(get_current_user)
        ):
            return {"user_id": current_user.user_id}
    """
    if not hasattr(request.state, "user"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return request.state.user


def get_current_user_optional(request: Request) -> Optional[CurrentUser]:
    """
    Dependency to get current user if authenticated, else None.
    
    Use this for endpoints that work for both authenticated and anonymous users,
    but provide enhanced functionality for authenticated users.
    
    Args:
        request: FastAPI request object
        
    Returns:
        CurrentUser if authenticated, None otherwise
        
    Example:
        @router.get("/api/public-content")
        async def get_content(
            current_user: Optional[CurrentUser] = Depends(get_current_user_optional)
        ):
            if current_user:
                return {"content": "personalized", "user_id": current_user.user_id}
            return {"content": "public"}
    """
    if hasattr(request.state, "user"):
        return request.state.user
    return None

