"""
Authentication Module
Handles user signup, email verification, login, password reset, and JWT tokens
"""
try:
    from .router import router as auth_router
except ImportError:
    # Fallback for when running from backend directory
    from modules.auth.router import router as auth_router

__all__ = ["auth_router"]

