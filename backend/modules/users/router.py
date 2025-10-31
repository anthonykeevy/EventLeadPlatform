"""
User Management Router
Endpoints for user profile management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from pydantic import BaseModel, Field

from common.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser
from models.company import Company
from models.ref.user_company_role import UserCompanyRole
from schemas.user import (
    UpdateUserDetailsSchema, UpdateUserDetailsResponse, UserProfileResponse,
    SwitchCompanyRequest, SwitchCompanyResponse, UserCompanyInfo, RelationshipInfo,
    UserProfileUpdateSchema, EnhancedUserProfileResponse, ReferenceOptionResponse,
    IndustryAssociationSchema, IndustryAssociationResponse
)
from .service import (
    update_user_details, get_user_profile, get_user_companies_with_relationship_context,
    update_user_profile_enhancements, get_user_industries, add_user_industry,
    update_user_industry, remove_user_industry
)
from .switch_service import CompanySwitchService
from common.logger import get_logger

from models.ref.theme_preference import ThemePreference
from models.ref.layout_density import LayoutDensity
from models.ref.font_size import FontSize
from models.ref.industry import Industry

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


# ============================================================================
# Epic 2: Enhanced User Profile Endpoints
# ============================================================================

@router.put(
    "/me/profile/enhancements",
    response_model=UpdateUserDetailsResponse,
    status_code=status.HTTP_200_OK,
    summary="Update user profile enhancements",
    description="Update authenticated user's bio, theme preferences, layout density, and font size"
)
async def update_my_profile_enhancements(
    request: UserProfileUpdateSchema,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UpdateUserDetailsResponse:
    """
    Update user profile enhancements (Epic 2).
    
    Requires authentication. Updates:
    - Bio (optional, max 500 characters)
    - Theme preference (optional)
    - Layout density (optional)
    - Font size (optional)
    
    All fields are optional for partial updates.
    Logs changes to audit.UserAudit.
    """
    try:
        # Log incoming request
        logger.info(f"Profile enhancement update request: UserID={current_user.user_id}, "
                   f"theme_preference_id={request.theme_preference_id}, "
                   f"layout_density_id={request.layout_density_id}, "
                   f"font_size_id={request.font_size_id}, "
                   f"bio={'*' * len(request.bio) if request.bio else None}")
        
        await update_user_profile_enhancements(
            db=db,
            user_id=current_user.user_id,
            bio=request.bio,
            theme_preference_id=request.theme_preference_id,
            layout_density_id=request.layout_density_id,
            font_size_id=request.font_size_id
        )
        
        logger.info(f"Profile enhancement update completed successfully for UserID={current_user.user_id}")
        
        return UpdateUserDetailsResponse(
            success=True,
            message="Profile enhancements updated successfully",
            user_id=current_user.user_id
        )
        
    except ValueError as e:
        logger.warning(f"Invalid profile enhancement update: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating profile enhancements: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile enhancements"
        )


@router.get(
    "/me/profile/enhanced",
    response_model=EnhancedUserProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get enhanced user profile",
    description="Get authenticated user's complete profile with Epic 2 enhancements"
)
async def get_my_enhanced_profile(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> EnhancedUserProfileResponse:
    """
    Get current user's enhanced profile with Epic 2 fields.
    
    Returns full profile including:
    - Basic user info (email, name, phone)
    - Epic 2 enhancements (bio, theme, density, font size)
    - Industry associations
    
    Requires authentication.
    """
    try:
        # Get user - use expire/refresh to ensure we get latest data from database
        # This ensures we get the latest theme preferences even if cached
        user = await get_user_profile(db, current_user.user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Expire and refresh user object to ensure we get latest data from database
        # This ensures we get the latest theme preferences even if cached in session
        db.expire(user)
        db.refresh(user)
        
        # Get industry associations
        user_industries = await get_user_industries(db, current_user.user_id)
        industries_list = []
        
        for ui in user_industries:
            industry = db.get(Industry, ui.IndustryID)
            if industry:
                industries_list.append(IndustryAssociationResponse(
                    user_industry_id=int(ui.UserIndustryID),
                    industry_id=int(industry.IndustryID),
                    industry_name=str(industry.IndustryName),
                    industry_code=str(industry.IndustryCode),
                    is_primary=bool(ui.IsPrimary),
                    sort_order=int(ui.SortOrder)
                ))
        
        # Build response
        response = EnhancedUserProfileResponse(
            user_id=int(user.UserID),
            email=str(user.Email),
            first_name=str(user.FirstName),
            last_name=str(user.LastName),
            phone=str(user.Phone) if user.Phone else None,
            bio=str(user.Bio) if user.Bio else None,
            role_title=str(user.RoleTitle) if user.RoleTitle else None,
            is_email_verified=bool(user.IsEmailVerified),
            industries=industries_list
        )
        
        # Add theme preference if set
        if user.ThemePreferenceID:
            theme = db.get(ThemePreference, user.ThemePreferenceID)
            if theme:
                logger.info(f"Returning theme preference: UserID={user.UserID}, "
                           f"ThemePreferenceID={user.ThemePreferenceID}, "
                           f"ThemeCode={theme.ThemeCode}, ThemeName={theme.ThemeName}")
                response.theme_preference = ReferenceOptionResponse(
                    id=int(theme.ThemePreferenceID),
                    code=str(theme.ThemeCode),
                    name=str(theme.ThemeName),
                    description=str(theme.Description),
                    css_class=str(theme.CSSClass),
                    base_font_size=None
                )
        else:
            logger.info(f"No theme preference set: UserID={user.UserID}, ThemePreferenceID={user.ThemePreferenceID}")
        
        # Add layout density if set
        if user.LayoutDensityID:
            density = db.get(LayoutDensity, user.LayoutDensityID)
            if density:
                response.layout_density = ReferenceOptionResponse(
                    id=int(density.LayoutDensityID),
                    code=str(density.DensityCode),
                    name=str(density.DensityName),
                    description=str(density.Description),
                    css_class=str(density.CSSClass),
                    base_font_size=None
                )
        
        # Add font size if set
        if user.FontSizeID:
            font_size = db.get(FontSize, user.FontSizeID)
            if font_size:
                response.font_size = ReferenceOptionResponse(
                    id=int(font_size.FontSizeID),
                    code=str(font_size.SizeCode),
                    name=str(font_size.SizeName),
                    description=str(font_size.Description),
                    css_class=str(font_size.CSSClass),
                    base_font_size=str(font_size.BaseFontSize)
                )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting enhanced profile: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get enhanced profile"
        )


@router.get(
    "/me/industries",
    response_model=List[IndustryAssociationResponse],
    status_code=status.HTTP_200_OK,
    summary="Get user industries",
    description="Get all industry associations for the authenticated user"
)
async def get_my_industries(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[IndustryAssociationResponse]:
    """
    Get user's industry associations.
    
    Returns list of industries with:
    - Industry details (ID, name, code)
    - Primary/secondary designation
    - Sort order
    
    Requires authentication.
    """
    try:
        user_industries = await get_user_industries(db, current_user.user_id)
        industries_list = []
        
        for ui in user_industries:
            industry = db.get(Industry, ui.IndustryID)
            if industry:
                industries_list.append(IndustryAssociationResponse(
                    user_industry_id=int(ui.UserIndustryID),
                    industry_id=int(industry.IndustryID),
                    industry_name=str(industry.IndustryName),
                    industry_code=str(industry.IndustryCode),
                    is_primary=bool(ui.IsPrimary),
                    sort_order=int(ui.SortOrder)
                ))
        
        return industries_list
        
    except Exception as e:
        logger.error(f"Error getting user industries: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user industries"
        )


@router.post(
    "/me/industries",
    response_model=IndustryAssociationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add industry association",
    description="Add a new industry to the authenticated user"
)
async def add_my_industry(
    request: IndustryAssociationSchema,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> IndustryAssociationResponse:
    """
    Add an industry association to the current user.
    
    Validates that:
    - User and industry exist
    - No duplicate association
    - Only one primary industry (auto-updates if setting new primary)
    
    Requires authentication.
    """
    try:
        user_industry = await add_user_industry(
            db=db,
            user_id=current_user.user_id,
            industry_id=request.industry_id,
            is_primary=request.is_primary,
            sort_order=request.sort_order
        )
        
        industry = db.get(Industry, user_industry.IndustryID)
        if not industry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Industry not found"
            )
        
        return IndustryAssociationResponse(
            user_industry_id=int(user_industry.UserIndustryID),
            industry_id=int(industry.IndustryID),
            industry_name=str(industry.IndustryName),
            industry_code=str(industry.IndustryCode),
            is_primary=bool(user_industry.IsPrimary),
            sort_order=int(user_industry.SortOrder)
        )
        
    except ValueError as e:
        logger.warning(f"Invalid industry association: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error adding industry: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add industry"
        )


@router.put(
    "/me/industries/{user_industry_id}",
    response_model=IndustryAssociationResponse,
    status_code=status.HTTP_200_OK,
    summary="Update industry association",
    description="Update an existing industry association (e.g., set as primary, change sort order)"
)
async def update_my_industry(
    user_industry_id: int,
    request: IndustryAssociationSchema,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> IndustryAssociationResponse:
    """
    Update an industry association.
    
    Can update:
    - Primary/secondary designation
    - Sort order
    
    Requires authentication and ownership.
    """
    try:
        user_industry = await update_user_industry(
            db=db,
            user_industry_id=user_industry_id,
            user_id=current_user.user_id,
            is_primary=request.is_primary,
            sort_order=request.sort_order
        )
        
        industry = db.get(Industry, user_industry.IndustryID)
        if not industry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Industry not found"
            )
        
        return IndustryAssociationResponse(
            user_industry_id=int(user_industry.UserIndustryID),
            industry_id=int(industry.IndustryID),
            industry_name=str(industry.IndustryName),
            industry_code=str(industry.IndustryCode),
            is_primary=bool(user_industry.IsPrimary),
            sort_order=int(user_industry.SortOrder)
        )
        
    except ValueError as e:
        logger.warning(f"Invalid industry update: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating industry: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update industry"
        )


@router.delete(
    "/me/industries/{user_industry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove industry association",
    description="Remove an industry association from the authenticated user (soft delete)"
)
async def remove_my_industry(
    user_industry_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove an industry association.
    
    Soft deletes the association (marks as deleted).
    Requires authentication and ownership.
    """
    try:
        await remove_user_industry(
            db=db,
            user_industry_id=user_industry_id,
            user_id=current_user.user_id
        )
        
    except ValueError as e:
        logger.warning(f"Invalid industry removal: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error removing industry: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove industry"
        )


# ============================================================================
# Epic 2: Reference Data Endpoints
# ============================================================================

@router.get(
    "/reference/themes",
    response_model=List[ReferenceOptionResponse],
    status_code=status.HTTP_200_OK,
    summary="Get theme preferences",
    description="Get all available theme preference options"
)
async def get_themes(
    db: Session = Depends(get_db)
) -> List[ReferenceOptionResponse]:
    """
    Get all available theme preferences.
    
    Returns:
    - Light Theme
    - Dark Theme
    - High-Contrast Theme
    - System Default Theme
    
    No authentication required.
    """
    try:
        stmt = select(ThemePreference).where(
            ThemePreference.IsActive == True
        ).order_by(ThemePreference.SortOrder.asc())
        
        themes = db.execute(stmt).scalars().all()
        
        return [
            ReferenceOptionResponse(
                id=int(theme.ThemePreferenceID),
                code=str(theme.ThemeCode),
                name=str(theme.ThemeName),
                description=str(theme.Description),
                css_class=str(theme.CSSClass),
                base_font_size=None
            )
            for theme in themes
        ]
        
    except Exception as e:
        logger.error(f"Error getting themes: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get themes"
        )


@router.get(
    "/reference/layout-densities",
    response_model=List[ReferenceOptionResponse],
    status_code=status.HTTP_200_OK,
    summary="Get layout densities",
    description="Get all available layout density options"
)
async def get_layout_densities(
    db: Session = Depends(get_db)
) -> List[ReferenceOptionResponse]:
    """
    Get all available layout densities.
    
    Returns:
    - Compact
    - Comfortable
    - Spacious
    
    No authentication required.
    """
    try:
        stmt = select(LayoutDensity).where(
            LayoutDensity.IsActive == True
        ).order_by(LayoutDensity.SortOrder.asc())
        
        densities = db.execute(stmt).scalars().all()
        
        return [
            ReferenceOptionResponse(
                id=int(density.LayoutDensityID),
                code=str(density.DensityCode),
                name=str(density.DensityName),
                description=str(density.Description),
                css_class=str(density.CSSClass),
                base_font_size=None
            )
            for density in densities
        ]
        
    except Exception as e:
        logger.error(f"Error getting layout densities: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get layout densities"
        )


@router.get(
    "/reference/font-sizes",
    response_model=List[ReferenceOptionResponse],
    status_code=status.HTTP_200_OK,
    summary="Get font sizes",
    description="Get all available font size options"
)
async def get_font_sizes(
    db: Session = Depends(get_db)
) -> List[ReferenceOptionResponse]:
    """
    Get all available font sizes.
    
    Returns:
    - Small (14px)
    - Medium (16px)
    - Large (18px)
    
    No authentication required.
    """
    try:
        stmt = select(FontSize).where(
            FontSize.IsActive == True
        ).order_by(FontSize.SortOrder.asc())
        
        font_sizes = db.execute(stmt).scalars().all()
        
        return [
            ReferenceOptionResponse(
                id=int(font_size.FontSizeID),
                code=str(font_size.SizeCode),
                name=str(font_size.SizeName),
                description=str(font_size.Description),
                css_class=str(font_size.CSSClass),
                base_font_size=str(font_size.BaseFontSize)
            )
            for font_size in font_sizes
        ]
        
    except Exception as e:
        logger.error(f"Error getting font sizes: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get font sizes"
        )


class IndustryOptionResponse(BaseModel):
    """Response schema for industry options"""
    id: int = Field(..., description="Industry ID")
    code: str = Field(..., description="Industry code")
    name: str = Field(..., description="Industry name")
    description: str = Field(..., description="Industry description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 5,
                "code": "tech",
                "name": "Technology",
                "description": "Technology and software industry"
            }
        }


@router.get(
    "/reference/industries",
    response_model=List[IndustryOptionResponse],
    status_code=status.HTTP_200_OK,
    summary="Get industries",
    description="Get all available industry options"
)
async def get_industries(
    db: Session = Depends(get_db)
) -> List[IndustryOptionResponse]:
    """
    Get all available industries.
    
    Returns list of all active industries for user selection.
    
    No authentication required.
    """
    try:
        stmt = select(Industry).where(
            Industry.IsActive == True
        ).order_by(Industry.SortOrder.asc())
        
        industries = db.execute(stmt).scalars().all()
        
        return [
            IndustryOptionResponse(
                id=int(industry.IndustryID),
                code=str(industry.IndustryCode),
                name=str(industry.IndustryName),
                description=str(industry.Description)
            )
            for industry in industries
        ]
        
    except Exception as e:
        logger.error(f"Error getting industries: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get industries"
        )

