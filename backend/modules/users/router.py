"""
User Management Router
Endpoints for user profile management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from common.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser
from .schemas import UpdateUserDetailsSchema, UpdateUserDetailsResponse, UserProfileResponse
from .service import update_user_details, get_user_profile
from common.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post(
    "/me/details",
    response_model=UpdateUserDetailsResponse,
    status_code=status.HTTP_200_OK,
    summary="Update user profile details",
    description="Update authenticated user's phone number, timezone, and job title"
)
async def update_my_details(
    request: UpdateUserDetailsSchema,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UpdateUserDetailsResponse:
    """
    Update user profile details (AC-1.5.1, AC-1.5.2, AC-1.5.10).
    
    Requires authentication. Updates:
    - Phone number (optional)
    - Timezone (validated against ref.Timezone)
    - Job title (optional)
    
    Logs changes to audit.UserAudit.
    """
    try:
        await update_user_details(
            db=db,
            user_id=current_user.user_id,
            phone=request.phone,
            timezone_identifier=request.timezone_identifier,
            role_title=request.role_title
        )
        
        return UpdateUserDetailsResponse(
            success=True,
            message="User details updated successfully",
            user_id=current_user.user_id
        )
        
    except ValueError as e:
        logger.warning(f"Invalid user details update: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating user details: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user details"
        )


@router.get(
    "/me",
    response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Get authenticated user's profile information"
)
async def get_my_profile(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserProfileResponse:
    """
    Get current user's profile.
    
    Requires authentication.
    """
    try:
        user = await get_user_profile(db, current_user.user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserProfileResponse(
            user_id=int(user.UserID),  # type: ignore
            email=str(user.Email),  # type: ignore
            first_name=str(user.FirstName),  # type: ignore
            last_name=str(user.LastName),  # type: ignore
            phone=str(user.Phone) if user.Phone else None,  # type: ignore
            timezone_identifier=str(user.TimezoneIdentifier),  # type: ignore
            role_title=str(user.RoleTitle) if user.RoleTitle else None,  # type: ignore
            is_email_verified=bool(user.IsEmailVerified),  # type: ignore
            onboarding_complete=bool(user.OnboardingComplete),  # type: ignore
            onboarding_step=int(user.OnboardingStep)  # type: ignore
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user profile: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user profile"
        )

