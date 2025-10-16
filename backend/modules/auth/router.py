"""
Authentication Router
Handles user signup, email verification, login, and password reset endpoints
"""
import os
import logging
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status, Request
from sqlalchemy.orm import Session

from common.database import get_db
from common.password_validator import validate_password_strength
from modules.auth.schemas import (
    SignupRequest,
    SignupResponse,
    VerifyEmailRequest,
    VerifyEmailResponse,
    ErrorResponse
)
from modules.auth.user_service import create_user, verify_user_email, get_user_by_email
from modules.auth.token_service import generate_verification_token, validate_token, mark_token_used
from modules.auth.audit_service import (
    log_auth_event,
    log_user_creation,
    log_email_verification
)
from services.email_service import get_email_service

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Get frontend URL from environment
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


# ============================================================================
# Signup Endpoint
# ============================================================================

@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User created successfully, verification email sent"},
        400: {"model": ErrorResponse, "description": "Validation error (duplicate email, weak password)"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def signup(
    request_data: SignupRequest,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    **Public endpoint for user signup.**
    
    Creates a new user account with email verification required.
    
    **Flow:**
    1. Validate email uniqueness
    2. Validate password strength
    3. Hash password with bcrypt
    4. Create user (EmailVerified=false, IsActive=false)
    5. Generate verification token
    6. Send verification email (async)
    7. Log auth event
    8. Return success response
    
    **Password Requirements:**
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    
    **After Signup:**
    - User receives verification email
    - User must click link in email to activate account
    - Unverified users cannot log in
    """
    try:
        # 1. Check email uniqueness
        existing_user = get_user_by_email(db, request_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered. Please use a different email or try logging in."
            )
        
        # 2. Validate password strength
        password_errors = validate_password_strength(request_data.password)
        if password_errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password does not meet security requirements: {'; '.join(password_errors)}"
            )
        
        # 3. Create user
        user = create_user(
            db=db,
            email=request_data.email,
            password=request_data.password,
            first_name=request_data.first_name,
            last_name=request_data.last_name
        )
        
        logger.info(f"User created successfully: UserID={user.UserID}, Email={user.Email}")
        
        # 4. Generate verification token
        token = generate_verification_token(db, user.UserID, expiry_hours=24)
        
        # 5. Send verification email (async, non-blocking)
        email_service = get_email_service()
        verification_url = f"{FRONTEND_URL}/verify-email?token={token}"
        
        background_tasks.add_task(
            email_service.send_email,
            to=user.Email,
            subject="Verify Your Email - EventLead Platform",
            template_name="email_verification",
            template_vars={
                "user_name": user.FirstName,
                "verification_url": verification_url,
                "expiry_hours": 24,
                "unsubscribe_url": f"{FRONTEND_URL}/unsubscribe",
                "support_url": f"{FRONTEND_URL}/support"
            },
            email_type="email_verification",
            user_id=user.UserID
        )
        
        # 6. Log auth event
        log_auth_event(
            db=db,
            user_id=user.UserID,
            event_type="SIGNUP",
            success=True,
            details={
                "email": user.Email,
                "first_name": user.FirstName,
                "last_name": user.LastName
            },
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        
        # 7. Log user creation audit
        log_user_creation(db, user.UserID, user.Email)
        
        logger.info(f"Signup complete: UserID={user.UserID}, verification email queued")
        
        # 8. Return success response
        return SignupResponse(
            success=True,
            message="Signup successful! Please check your email to verify your account.",
            data={
                "user_id": user.UserID,
                "email": user.Email
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        logger.error(f"Signup error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during signup. Please try again later."
        )


# ============================================================================
# Email Verification Endpoint
# ============================================================================

@router.post(
    "/verify-email",
    response_model=VerifyEmailResponse,
    responses={
        200: {"description": "Email verified successfully, account activated"},
        400: {"model": ErrorResponse, "description": "Invalid, expired, or used token"},
        404: {"model": ErrorResponse, "description": "Token or user not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def verify_email(
    request_data: VerifyEmailRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    **Public endpoint for email verification.**
    
    Validates the verification token and activates the user account.
    
    **Flow:**
    1. Find token in database
    2. Validate token (not expired, not used)
    3. Find associated user
    4. Activate user (EmailVerified=true, IsActive=true)
    5. Mark token as used
    6. Log verification event
    7. Return success response
    
    **Token Requirements:**
    - Token must exist
    - Token must not be expired (< 24 hours old)
    - Token must not have been used before
    
    **After Verification:**
    - User can now log in
    - Token cannot be reused
    """
    try:
        # 1. Validate token
        token_record = validate_token(db, request_data.token)
        
        if not token_record:
            # Check if token exists at all
            from models.user_email_verification_token import UserEmailVerificationToken
            existing_token = db.query(UserEmailVerificationToken).filter(
                UserEmailVerificationToken.Token == request_data.token
            ).first()
            
            if not existing_token:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Invalid verification token. Please check the link in your email."
                )
            elif existing_token.IsUsed:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This verification token has already been used. You can now log in."
                )
            else:
                # Token expired
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Verification token has expired. Please request a new verification email."
                )
        
        # 2. Verify user email and activate account
        user = verify_user_email(db, token_record.UserID)
        
        logger.info(f"Email verified: UserID={user.UserID}, Email={user.Email}")
        
        # 3. Mark token as used
        mark_token_used(db, token_record)
        
        # 4. Log verification event
        log_auth_event(
            db=db,
            user_id=user.UserID,
            event_type="EMAIL_VERIFICATION",
            success=True,
            details={"email": user.Email},
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        
        # 5. Log email verification audit
        log_email_verification(db, user.UserID)
        
        logger.info(f"Email verification complete: UserID={user.UserID}")
        
        # 6. Return success response
        return VerifyEmailResponse(
            success=True,
            message="Email verified successfully! You can now log in to your account.",
            data={
                "user_id": user.UserID,
                "email": user.Email
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Email verification error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during email verification. Please try again later."
        )


# ============================================================================
# Health Check (for testing router is registered)
# ============================================================================

@router.get(
    "/health",
    response_model=dict,
    tags=["Health"]
)
async def auth_health():
    """Simple health check for auth module"""
    return {
        "status": "healthy",
        "module": "authentication",
        "endpoints": ["/api/auth/signup", "/api/auth/verify-email"]
    }

