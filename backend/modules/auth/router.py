"""
Authentication Router
Handles user signup, email verification, login, and password reset endpoints
"""
import os
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import select

from common.database import get_db
from common.password_validator import validate_password_strength
from modules.auth.schemas import (
    SignupRequest,
    SignupResponse,
    VerifyEmailRequest,
    VerifyEmailResponse,
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RefreshResponse,
    PasswordResetRequestSchema,
    PasswordResetRequestResponse,
    PasswordResetConfirmSchema,
    PasswordResetConfirmResponse,
    ErrorResponse
)
from modules.auth.user_service import (
    create_user, verify_user_email, get_user_by_email, create_user_with_invitation
)
from modules.auth.token_service import (
    generate_verification_token,
    validate_token,
    mark_token_used,
    store_refresh_token,
    validate_refresh_token,
    mark_refresh_token_used,
    generate_password_reset_token,
    validate_password_reset_token,
    mark_password_reset_token_used,
    invalidate_user_password_reset_tokens
)
from modules.auth.jwt_service import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token_type,
    extract_user_id
)
from common.security import verify_password, hash_password
from models.user_company import UserCompany
from models.ref.user_company_role import UserCompanyRole
from jose import JWTError  # type: ignore
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
    Supports invitation-based signup for team members.
    
    **Standard Flow:**
    1. Validate email uniqueness
    2. Validate password strength
    3. Hash password with bcrypt
    4. Create user (EmailVerified=false, IsActive=false)
    5. Generate verification token
    6. Send verification email (async)
    7. Log auth event
    8. Return success response
    
    **Invitation Flow (AC-1.7.5, AC-1.7.6):**
    1. Validate invitation token
    2. Verify email matches invitation
    3. Create user (immediately activated)
    4. Create UserCompany relationship
    5. Mark invitation as accepted
    6. Issue JWT with role and company_id
    7. Return success with access token
    
    **Password Requirements:**
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """
    try:
        # Check if this is invitation-based signup (AC-1.7.5, AC-1.7.6)
        if request_data.invitation_token:
            # 1. Validate password strength
            password_errors = validate_password_strength(request_data.password)
            if password_errors:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Password does not meet security requirements: {'; '.join(password_errors)}"
                )
            
            # 2. Create user with invitation (auto-accepts invitation)
            user, invitation, user_company = await create_user_with_invitation(
                db=db,
                email=request_data.email,
                password=request_data.password,
                first_name=request_data.first_name,
                last_name=request_data.last_name,
                invitation_token=request_data.invitation_token
            )
            
            logger.info(
                f"User created with invitation: UserID={user.UserID}, "
                f"CompanyID={user_company.CompanyID}, InvitationID={invitation.UserInvitationID}"
            )
            
            # 3. Get role for JWT
            role = db.execute(
                select(UserCompanyRole).where(
                    UserCompanyRole.UserCompanyRoleID == user_company.UserCompanyRoleID
                )
            ).scalar_one()
            
            # 4. Issue JWT with role and company_id (AC-1.7.8)
            access_token = create_access_token(
                user_id=int(user.UserID),  # type: ignore
                email=str(user.Email),  # type: ignore
                role=str(role.RoleCode),  # type: ignore
                company_id=int(user_company.CompanyID)  # type: ignore
            )
            
            refresh_token = create_refresh_token(
                user_id=int(user.UserID)  # type: ignore
            )
            
            # 5. Store refresh token
            store_refresh_token(db, int(user.UserID), refresh_token)  # type: ignore
            
            # 6. Log auth event
            log_auth_event(
                db=db,
                user_id=int(user.UserID),  # type: ignore
                event_type="SIGNUP_WITH_INVITATION",
                success=True,
                details={
                    "email": str(user.Email),  # type: ignore
                    "first_name": str(user.FirstName),  # type: ignore
                    "last_name": str(user.LastName),  # type: ignore
                    "company_id": int(user_company.CompanyID),  # type: ignore
                    "role": str(role.RoleCode)  # type: ignore
                },
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent")
            )
            
            logger.info(
                f"Invitation signup complete: UserID={user.UserID}, JWT issued, "
                f"onboarding skipped"
            )
            
            # 7. Return success with access token (no email verification needed)
            return SignupResponse(
                success=True,
                message="Signup successful! You can now access your team.",
                data={
                    "user_id": int(user.UserID),  # type: ignore
                    "email": str(user.Email),  # type: ignore
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "company_id": int(user_company.CompanyID),  # type: ignore
                    "role": str(role.RoleCode)  # type: ignore
                }
            )
        
        # Standard signup flow (no invitation)
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
# Login Endpoint
# ============================================================================

@router.post(
    "/login",
    response_model=LoginResponse,
    responses={
        200: {"description": "Login successful, tokens returned"},
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
        403: {"model": ErrorResponse, "description": "Account not verified or inactive"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def login(
    request_data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    **Public endpoint for user login.**
    
    Authenticates user and returns JWT access and refresh tokens.
    
    **Flow:**
    1. Find user by email
    2. Verify password with bcrypt (timing-safe)
    3. Check EmailVerified = true
    4. Check IsActive = true
    5. Get user's role and company (if exists)
    6. Generate JWT access token (1 hour expiry)
    7. Generate JWT refresh token (7 days expiry)
    8. Store refresh token in database
    9. Log login event
    10. Return both tokens
    
    **Security:**
    - Timing-safe password comparison
    - Same error message for invalid email/password (prevents email enumeration)
    - Separate errors for unverified/inactive accounts
    - Login events logged for audit trail
    
    **Tokens:**
    - Access token: Short-lived (1 hour), used for API requests
    - Refresh token: Long-lived (7 days), used to get new access tokens
    """
    try:
        # 1. Find user by email
        user = get_user_by_email(db, request_data.email)
        
        # 2. Verify password (timing-safe comparison)
        # Use same error for invalid email/password to prevent email enumeration
        if not user or not verify_password(request_data.password, user.PasswordHash):
            log_auth_event(
                db=db,
                user_id=user.UserID if user else None,
                event_type="LOGIN_FAILED",
                success=False,
                details={"reason": "Invalid credentials", "email": request_data.email},
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent")
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # 3. Check email verified
        if not user.EmailVerified:
            log_auth_event(
                db=db,
                user_id=user.UserID,
                event_type="LOGIN_FAILED",
                success=False,
                details={"reason": "Email not verified"},
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent")
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please verify your email before logging in. Check your inbox for the verification link."
            )
        
        # 4. Check account active
        if not user.IsActive:
            log_auth_event(
                db=db,
                user_id=user.UserID,
                event_type="LOGIN_FAILED",
                success=False,
                details={"reason": "Account inactive"},
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent")
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account has been deactivated. Please contact support."
            )
        
        # 5. Get user's role and company (if exists)
        user_company = db.query(UserCompany).filter(
            UserCompany.UserID == user.UserID,
            UserCompany.IsPrimaryCompany == True
        ).first()
        
        # If no primary company, get any active company
        if not user_company:
            user_company = db.query(UserCompany).filter(
                UserCompany.UserID == user.UserID
            ).first()
        
        # Extract role and company_id
        role = None
        company_id = None
        if user_company:
            # Get role name from UserCompanyRole
            if user_company.user_company_role:
                role = user_company.user_company_role.RoleName
            company_id = user_company.CompanyID
        
        # 6. Generate tokens
        access_token = create_access_token(
            user_id=user.UserID,
            email=user.Email,
            role=role,
            company_id=company_id
        )
        
        refresh_token = create_refresh_token(user_id=user.UserID)
        
        # 7. Store refresh token in database
        store_refresh_token(db, user.UserID, refresh_token, expiry_days=7)
        
        # 8. Log success
        log_auth_event(
            db=db,
            user_id=user.UserID,
            event_type="LOGIN_SUCCESS",
            success=True,
            details={"email": user.Email, "has_company": company_id is not None},
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        
        logger.info(f"User login successful: UserID={user.UserID}, Email={user.Email}")
        
        # 9. Return tokens
        return LoginResponse(
            success=True,
            message="Login successful",
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": 3600  # 1 hour in seconds
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login. Please try again later."
        )


# ============================================================================
# Token Refresh Endpoint
# ============================================================================

@router.post(
    "/refresh",
    response_model=RefreshResponse,
    responses={
        200: {"description": "Token refreshed successfully"},
        401: {"model": ErrorResponse, "description": "Invalid or expired refresh token"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def refresh_token_endpoint(
    request_data: RefreshRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    **Public endpoint for token refresh.**
    
    Exchanges refresh token for a new access token.
    
    **Flow:**
    1. Decode and verify refresh token JWT
    2. Verify token type is "refresh"
    3. Validate token exists in database
    4. Check token not expired, not used, not revoked
    5. Get fresh user data and company/role
    6. Generate new access token
    7. Log refresh event
    8. Return new access token
    
    **Security:**
    - Refresh tokens are stored in database (can be revoked)
    - Tokens validated for expiry and usage
    - Fresh user data fetched (reflects permission changes)
    
    **Note:**
    - Refresh token is NOT marked as used (can be reused until expiry)
    - For one-time use policy, uncomment mark_refresh_token_used()
    """
    try:
        # 1. Decode refresh token JWT
        try:
            payload = decode_token(request_data.refresh_token)
        except JWTError as e:
            logger.warning(f"Invalid refresh token JWT: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
        
        # 2. Verify token type
        if not verify_token_type(payload, "refresh"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type. Expected refresh token."
            )
        
        # 3. Validate token in database
        token_record = validate_refresh_token(db, request_data.refresh_token)
        
        if not token_record:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
        
        # 4. Get fresh user data
        user_id = extract_user_id(payload)
        user = get_user_by_email(db, payload["email"]) if "email" in payload else None
        
        if not user or user.UserID != user_id:
            # Fallback: get user by ID
            from modules.auth.user_service import get_user_by_id
            user = get_user_by_id(db, user_id)
        
        if not user or not user.IsActive or not user.EmailVerified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found, inactive, or email not verified"
            )
        
        # 5. Get updated role/company info
        user_company = db.query(UserCompany).filter(
            UserCompany.UserID == user.UserID,
            UserCompany.IsPrimaryCompany == True
        ).first()
        
        if not user_company:
            user_company = db.query(UserCompany).filter(
                UserCompany.UserID == user.UserID
            ).first()
        
        role = None
        company_id = None
        if user_company:
            if user_company.user_company_role:
                role = user_company.user_company_role.RoleName
            company_id = user_company.CompanyID
        
        # 6. Generate new access token
        access_token = create_access_token(
            user_id=user.UserID,
            email=user.Email,
            role=role,
            company_id=company_id
        )
        
        # 7. Optional: Mark refresh token as used (one-time use policy)
        # Uncomment if you want refresh tokens to be single-use:
        # mark_refresh_token_used(db, token_record)
        
        # 8. Log refresh event
        log_auth_event(
            db=db,
            user_id=user.UserID,
            event_type="TOKEN_REFRESH",
            success=True,
            details={"email": user.Email},
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        
        logger.info(f"Token refresh successful: UserID={user.UserID}")
        
        # 9. Return new access token
        return RefreshResponse(
            success=True,
            message="Token refreshed successfully",
            data={
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": 3600
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during token refresh. Please try again later."
        )


# ============================================================================
# Password Reset Endpoints
# ============================================================================

@router.post(
    "/password-reset/request",
    response_model=PasswordResetRequestResponse,
    status_code=status.HTTP_200_OK,
    tags=["Authentication"],
    summary="Request password reset",
    description="Request a password reset link. Returns success regardless of email existence (security)"
)
async def password_reset_request(
    request_data: PasswordResetRequestSchema,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Request password reset link via email.
    
    **Security Note**: Always returns success message regardless of whether
    the email exists in the system. This prevents email enumeration attacks.
    
    **Flow**:
    1. Validate email format
    2. Find user by email (if exists)
    3. Generate password reset token (1-hour expiry)
    4. Send email with reset link
    5. Log auth event
    6. Return success (don't reveal if email exists)
    
    **Rate Limiting**: Consider implementing rate limiting to prevent abuse.
    """
    try:
        # Find user by email (silently fail if not exists - security)
        user = get_user_by_email(db, request_data.email)
        
        if user:
            # Generate password reset token
            token = generate_password_reset_token(db, user.UserID)
            
            # Get email service
            email_service = get_email_service()
            
            # Get frontend URL for reset link
            frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
            reset_link = f"{frontend_url}/reset-password?token={token}"
            
            # Send password reset email (async in background)
            background_tasks.add_task(
                email_service.send_password_reset_email,
                to=user.Email,
                user_name=f"{user.FirstName} {user.LastName}",
                reset_link=reset_link
            )
            
            # Log auth event
            log_auth_event(
                db=db,
                user_id=user.UserID,
                event_type="PASSWORD_RESET_REQUESTED",
                success=True,
                details={"email": user.Email},
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent")
            )
            
            logger.info(f"Password reset requested: UserID={user.UserID}, Email={user.Email}")
        else:
            # Email doesn't exist - log attempt but don't reveal
            logger.info(f"Password reset requested for non-existent email: {request_data.email}")
        
        # Always return success message (security: don't leak email existence)
        return PasswordResetRequestResponse(
            success=True,
            message="If the email exists, a password reset link has been sent."
        )
        
    except Exception as e:
        logger.error(f"Password reset request error: {str(e)}", exc_info=True)
        # Still return success to avoid leaking information
        return PasswordResetRequestResponse(
            success=True,
            message="If the email exists, a password reset link has been sent."
        )


@router.post(
    "/password-reset/confirm",
    response_model=PasswordResetConfirmResponse,
    status_code=status.HTTP_200_OK,
    tags=["Authentication"],
    summary="Confirm password reset",
    description="Reset password using token from email"
)
async def password_reset_confirm(
    request_data: PasswordResetConfirmSchema,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Confirm password reset and set new password.
    
    **Flow**:
    1. Validate token (exists, not expired, not used)
    2. Validate new password strength
    3. Hash new password with bcrypt
    4. Update user's password
    5. Mark token as used
    6. Invalidate any remaining reset tokens
    7. Log auth event
    8. Return success
    
    **Security**:
    - Tokens expire after 1 hour
    - Tokens can only be used once
    - Password strength validated
    - Old tokens invalidated after successful reset
    """
    try:
        # 1. Validate token
        token = validate_password_reset_token(db, request_data.token)
        
        if not token:
            # Token invalid, expired, or already used
            log_auth_event(
                db=db,
                user_id=None,
                event_type="PASSWORD_RESET_FAILED",
                success=False,
                details={"reason": "Invalid or expired token"},
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent")
            )
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired password reset token"
            )
        
        # 2. Validate new password strength
        password_errors = validate_password_strength(request_data.new_password)
        if password_errors:
            log_auth_event(
                db=db,
                user_id=token.UserID,
                event_type="PASSWORD_RESET_FAILED",
                success=False,
                details={"reason": "Weak password", "errors": password_errors},
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent")
            )
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password does not meet security requirements: {', '.join(password_errors)}"
            )
        
        # 3. Get user
        from models.user import User
        user = db.query(User).filter(User.UserID == token.UserID).first()
        
        if not user:
            logger.error(f"User not found for password reset token: UserID={token.UserID}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found"
            )
        
        # 4. Hash new password
        new_password_hash = hash_password(request_data.new_password)
        
        # 5. Update user's password
        user.PasswordHash = new_password_hash
        user.UpdatedDate = datetime.utcnow()
        
        # 6. Mark token as used
        mark_password_reset_token_used(db, token)
        
        # 7. Invalidate any other unused reset tokens for this user
        invalidate_user_password_reset_tokens(db, user.UserID)
        
        db.commit()
        
        # 8. Log successful password reset
        log_auth_event(
            db=db,
            user_id=user.UserID,
            event_type="PASSWORD_RESET_COMPLETED",
            success=True,
            details={"email": user.Email},
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        
        logger.info(f"Password reset successful: UserID={user.UserID}, Email={user.Email}")
        
        # 9. Return success
        return PasswordResetConfirmResponse(
            success=True,
            message="Password reset successfully. You can now log in with your new password."
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Password reset confirm error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during password reset. Please try again later."
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
        "endpoints": [
            "/api/auth/signup",
            "/api/auth/verify-email",
            "/api/auth/login",
            "/api/auth/refresh",
            "/api/auth/password-reset/request",
            "/api/auth/password-reset/confirm"
        ]
    }

