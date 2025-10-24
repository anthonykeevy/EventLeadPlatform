"""
User Management Router
Endpoints for user profile management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from common.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser
from models.company import Company
from models.ref.user_company_role import UserCompanyRole
from schemas.user import (
    UpdateUserDetailsSchema, UpdateUserDetailsResponse, UserProfileResponse,
    SwitchCompanyRequest, SwitchCompanyResponse, UserCompanyInfo, RelationshipInfo
)
from .service import update_user_details, get_user_profile, get_user_companies_with_relationship_context
from .switch_service import CompanySwitchService
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
        db.rollback()  # Rollback on validation error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating user details: {str(e)}", exc_info=True)
        db.rollback()  # Rollback on any error
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


# ============================================================================
# Multi-Company Support Endpoints (Story 1.7)
# ============================================================================

@router.get(
    "/me/companies",
    response_model=List[UserCompanyInfo],
    summary="List user's companies",
    description="Get all companies the user belongs to, including relationship context."
)
async def list_my_companies(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[UserCompanyInfo]:
    """
    List all companies user belongs to, enriched with relationship context.
    AC-1.11.1, AC-1.11.3, AC-1.11.8
    """
    try:
        enriched_companies = await get_user_companies_with_relationship_context(db, current_user.user_id)
        
        result = []
        for item in enriched_companies:
            uc = item['user_company']
            company = db.get(Company, uc.CompanyID)
            role = db.get(UserCompanyRole, uc.UserCompanyRoleID)

            relationship_info = None
            if item.get('relationship'):
                relationship_info = RelationshipInfo(**item['relationship'])

            result.append(UserCompanyInfo(
                company_id=uc.CompanyID,
                company_name=company.CompanyName,
                role=role.RoleCode,
                is_primary=uc.IsPrimaryCompany,
                joined_at=uc.JoinedDate,
                relationship=relationship_info
            ))
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing user's companies: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list companies"
        )


@router.post(
    "/me/switch-company",
    response_model=SwitchCompanyResponse,
    summary="Switch active company",
    description="Switch to a different company the user belongs to"
)
async def switch_active_company(
    request: SwitchCompanyRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> SwitchCompanyResponse:
    """
    Switch user's active company context (AC-1.11.4).
    
    Issues new JWT with updated company_id and corresponding role.
    """
    try:
        switch_service = CompanySwitchService(db)
        
        result = switch_service.switch_company(
            user_id=current_user.user_id,
            target_company_id=request.company_id
        )
        
        return SwitchCompanyResponse(**result)
        
    except ValueError as e:
        logger.warning(f"Invalid company switch: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error switching company: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to switch company"
        )

