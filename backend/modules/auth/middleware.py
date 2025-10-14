"""
Authentication Middleware - Epic 1
JWT token validation and role-based access control
"""
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
from .service import AuthService

security = HTTPBearer()

class AuthMiddleware:
    """Authentication middleware for Epic 1"""
    
    @staticmethod
    async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
        """Extract and validate current user from JWT token"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = AuthService.verify_token(credentials.credentials)
            if payload is None:
                raise credentials_exception
            
            # Validate token type
            if payload.get("type") != "access":
                raise credentials_exception
            
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
                
            return {
                "user_id": user_id,
                "email": payload.get("email"),
                "role": payload.get("role"),
                "company_id": payload.get("company_id")
            }
        except Exception:
            raise credentials_exception
    
    @staticmethod
    async def require_company_admin(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        """Require company admin role"""
        if current_user.get("role") != "company_admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Company admin access required"
            )
        return current_user
    
    @staticmethod
    async def require_company_user(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        """Require company user role or higher"""
        if current_user.get("role") not in ["company_admin", "company_user"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Company user access required"
            )
        return current_user
    
    @staticmethod
    async def inject_company_context(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        """Inject company context for multi-tenant isolation"""
        company_id = current_user.get("company_id")
        if not company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No company context available"
            )
        return current_user
