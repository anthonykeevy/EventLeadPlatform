"""
Fonts Router
API endpoints for Google Fonts management and custom corporate font uploads
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional, List
import math
import io

from common.database import get_db
from common.logger import get_logger
from modules.auth.dependencies import get_current_user, get_current_user_optional
from modules.auth.models import CurrentUser
from services.fonts import GoogleFontsService, FontSyncService, CustomFontService, InvalidFontError
from .schemas import (
    FontSearchParams,
    FontUsageRequest,
    SetFontFeaturedRequest,
    SetFontRecommendedRequest,
    FontFamilySummaryResponse,
    FontFamilyDetailResponse,
    FontListResponse,
    FontCategoryResponse,
    FontVariantResponse,
    FontSubsetResponse,
    FontAxisResponse,
    SyncStatusResponse,
    SyncResultResponse,
    FontUsageResponse,
    # Custom font schemas
    CustomFontUploadRequest,
    CustomFontDisplayNameRequest,
    CustomFontResponse,
    CompanyFontResponse,
    CompanyFontListResponse,
    FontFileStreamResponse,
    FontFamilySummaryWithContextResponse,
)

logger = get_logger(__name__)

router = APIRouter(prefix="/api/fonts", tags=["fonts"])


# =====================================================================
# Helper Functions
# =====================================================================

def _font_to_summary(font) -> FontFamilySummaryResponse:
    """Convert FontFamily model to summary response."""
    return FontFamilySummaryResponse(
        font_family_id=font.FontFamilyID,
        google_font_id=font.GoogleFontID or "",  # Handle NULL for custom fonts
        family_name=font.FamilyName,
        category=font.Category,
        version=font.Version,
        is_variable_font=font.IsVariableFont,
        min_weight=font.MinWeight,
        max_weight=font.MaxWeight,
        has_italic=font.HasItalic,
        total_variants=font.TotalVariants,
        total_subsets=font.TotalSubsets,
        menu_file_url=font.MenuFileUrl,
        popularity_rank=font.PopularityRank,
        usage_count=font.UsageCount,
        is_featured=font.IsFeatured,
        is_recommended=font.IsRecommended,
        variant_list=font.VariantList
    )


def _font_to_summary_with_context(font_data: dict) -> FontFamilySummaryWithContextResponse:
    """Convert font dict with company context to response."""
    return FontFamilySummaryWithContextResponse(**font_data)


def _company_font_to_response(font_data: dict) -> CompanyFontResponse:
    """Convert company font dict to response."""
    return CompanyFontResponse(**font_data)


def _font_to_detail(font) -> FontFamilyDetailResponse:
    """Convert FontFamily model to detail response with relationships."""
    variants = [
        FontVariantResponse(
            font_variant_id=v.FontVariantID,
            variant_name=v.VariantName,
            weight=v.Weight,
            weight_name=v.WeightName,
            is_italic=v.IsItalic,
            ttf_file_url=v.TtfFileUrl,
            display_order=v.DisplayOrder,
            is_default=v.IsDefault
        )
        for v in font.variants.filter_by(IsDeleted=False).order_by('DisplayOrder').all()
    ]
    
    subsets = [
        FontSubsetResponse(
            font_subset_id=s.FontSubsetID,
            subset_code=s.SubsetCode,
            subset_name=s.SubsetName,
            subset_group=s.SubsetGroup,
            is_extended=s.IsExtended
        )
        for s in font.subsets.filter_by(IsActive=True).order_by('DisplayOrder').all()
    ]
    
    axes = [
        FontAxisResponse(
            font_axis_id=a.FontAxisID,
            axis_tag=a.AxisTag,
            axis_name=a.AxisName,
            min_value=a.MinValue,
            max_value=a.MaxValue,
            default_value=a.DefaultValue,
            is_standard=a.IsStandard,
            css_property=a.CssProperty
        )
        for a in font.axes.filter_by(IsActive=True).order_by('DisplayOrder').all()
    ]
    
    return FontFamilyDetailResponse(
        font_family_id=font.FontFamilyID,
        google_font_id=font.GoogleFontID,
        family_name=font.FamilyName,
        category=font.Category,
        sub_category=font.SubCategory,
        version=font.Version,
        version_number=font.VersionNumber,
        last_modified_date=font.LastModifiedDate,
        menu_file_url=font.MenuFileUrl,
        specimen_url=font.SpecimenUrl,
        is_variable_font=font.IsVariableFont,
        has_color_capabilities=font.HasColorCapabilities,
        min_weight=font.MinWeight,
        max_weight=font.MaxWeight,
        has_italic=font.HasItalic,
        has_regular=font.HasRegular,
        supports_latin=font.SupportsLatin,
        supports_cyrillic=font.SupportsCyrillic,
        supports_greek=font.SupportsGreek,
        supports_arabic=font.SupportsArabic,
        supports_hebrew=font.SupportsHebrew,
        supports_asian=font.SupportsAsian,
        total_subsets=font.TotalSubsets,
        total_variants=font.TotalVariants,
        variant_list=font.VariantList,
        popularity_rank=font.PopularityRank,
        usage_count=font.UsageCount,
        is_recommended=font.IsRecommended,
        is_featured=font.IsFeatured,
        display_order=font.DisplayOrder,
        license_type=font.LicenseType,
        license_url=font.LicenseUrl,
        designer=font.Designer,
        designer_url=font.DesignerUrl,
        foundry=font.Foundry,
        last_sync_date=font.LastSyncDate,
        variants=variants,
        subsets=subsets,
        axes=axes
    )


# =====================================================================
# Public Endpoints (No Auth Required)
# =====================================================================

@router.get(
    "",
    response_model=FontListResponse,
    summary="List fonts",
    description="Get paginated list of fonts with optional filtering and sorting"
)
async def list_fonts(
    query: Optional[str] = Query(None, description="Search term for font name"),
    category: Optional[str] = Query(None, description="Filter by category (serif, sans-serif, etc.)"),
    subset: Optional[str] = Query(None, description="Filter by required subset (latin, cyrillic, etc.)"),
    is_variable: Optional[bool] = Query(None, description="Variable fonts only"),
    has_italic: Optional[bool] = Query(None, description="Fonts with italic variants"),
    is_featured: Optional[bool] = Query(None, description="Featured fonts only"),
    sort_by: str = Query("popularity", description="Sort order: popularity, name, date, featured"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
) -> FontListResponse:
    """
    List fonts with filtering and pagination.
    
    This is a public endpoint - no authentication required.
    """
    try:
        service = GoogleFontsService(db)
        
        fonts, total = await service.search_fonts(
            query=query,
            category=category,
            subset=subset,
            is_variable=is_variable,
            has_italic=has_italic,
            is_featured=is_featured,
            sort_by=sort_by,
            page=page,
            page_size=page_size
        )
        
        font_responses = [_font_to_summary(f) for f in fonts]
        total_pages = math.ceil(total / page_size) if total > 0 else 1
        
        return FontListResponse(
            fonts=font_responses,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
        
    except Exception as e:
        logger.error(f"Error listing fonts: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list fonts"
        )


@router.get(
    "/featured",
    response_model=List[FontFamilySummaryResponse],
    summary="Get featured fonts",
    description="Get curated featured fonts for quick selection"
)
async def get_featured_fonts(
    db: Session = Depends(get_db)
) -> List[FontFamilySummaryResponse]:
    """Get curated featured fonts."""
    try:
        service = GoogleFontsService(db)
        fonts = await service.get_featured_fonts()
        
        return [_font_to_summary(f) for f in fonts]
        
    except Exception as e:
        logger.error(f"Error getting featured fonts: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get featured fonts"
        )


@router.get(
    "/categories",
    response_model=List[FontCategoryResponse],
    summary="Get font categories",
    description="Get all font categories with font counts"
)
async def get_font_categories(
    db: Session = Depends(get_db)
) -> List[FontCategoryResponse]:
    """Get all font categories with counts."""
    try:
        service = GoogleFontsService(db)
        categories = await service.get_font_categories()
        
        return [FontCategoryResponse(**cat) for cat in categories]
        
    except Exception as e:
        logger.error(f"Error getting font categories: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get font categories"
        )


@router.get(
    "/popular",
    response_model=List[FontFamilySummaryResponse],
    summary="Get popular fonts",
    description="Get most popular fonts"
)
async def get_popular_fonts(
    limit: int = Query(20, ge=1, le=50, description="Number of fonts to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
) -> List[FontFamilySummaryResponse]:
    """Get most popular fonts."""
    try:
        service = GoogleFontsService(db)
        fonts = await service.get_popular_fonts(limit=limit, category=category)
        
        return [_font_to_summary(f) for f in fonts]
        
    except Exception as e:
        logger.error(f"Error getting popular fonts: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get popular fonts"
        )


@router.get(
    "/{font_family_id}",
    response_model=FontFamilyDetailResponse,
    summary="Get font details",
    description="Get complete font family details including variants, subsets, and axes"
)
async def get_font_details(
    font_family_id: int,
    db: Session = Depends(get_db)
) -> FontFamilyDetailResponse:
    """Get complete font family details."""
    try:
        service = GoogleFontsService(db)
        font = await service.get_font_by_id(font_family_id)
        
        if not font:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Font not found: {font_family_id}"
            )
        
        return _font_to_detail(font)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting font details: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get font details"
        )


@router.get(
    "/by-name/{family_name:path}",
    response_model=FontFamilyDetailResponse,
    summary="Get font by name",
    description="Get font by family name"
)
async def get_font_by_name(
    family_name: str,
    db: Session = Depends(get_db)
) -> FontFamilyDetailResponse:
    """Get font by family name."""
    try:
        service = GoogleFontsService(db)
        font = await service.get_font_by_name(family_name)
        
        if not font:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Font not found: {family_name}"
            )
        
        return _font_to_detail(font)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting font by name: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get font by name"
        )


# =====================================================================
# Authenticated Endpoints
# =====================================================================

@router.post(
    "/{font_family_id}/usage",
    response_model=FontUsageResponse,
    summary="Log font usage",
    description="Log font usage for analytics"
)
async def log_font_usage(
    font_family_id: int,
    request: FontUsageRequest,
    req: Request,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> FontUsageResponse:
    """Log font usage for analytics."""
    try:
        service = GoogleFontsService(db)
        
        # Get client info
        ip_address = req.client.host if req.client else None
        user_agent = req.headers.get('user-agent')
        
        await service.log_font_usage(
            font_family_id=font_family_id,
            context=request.context,
            action=request.action,
            user_id=current_user.user_id,
            company_id=current_user.company_id,
            font_variant_id=request.font_variant_id,
            context_entity_type=request.context_entity_type,
            context_entity_id=request.context_entity_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return FontUsageResponse(
            success=True,
            message="Font usage logged successfully"
        )
        
    except Exception as e:
        logger.error(f"Error logging font usage: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to log font usage"
        )


# =====================================================================
# Admin Endpoints
# =====================================================================

@router.post(
    "/sync",
    response_model=SyncResultResponse,
    summary="Trigger font sync",
    description="Manually trigger font synchronization with Google Fonts API (admin only)"
)
async def trigger_sync(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> SyncResultResponse:
    """
    Manually trigger font synchronization.
    
    Requires system_admin or company_admin role.
    """
    try:
        # Check for admin role
        if current_user.role not in ['system_admin', 'company_admin']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        service = FontSyncService(db)
        result = await service.execute_sync(
            trigger_type="Manual",
            triggered_by=f"User:{current_user.user_id}"
        )
        
        return SyncResultResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error triggering sync: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to trigger sync"
        )


@router.get(
    "/sync/status",
    response_model=SyncStatusResponse,
    summary="Get sync status",
    description="Get last sync status and font counts"
)
async def get_sync_status(
    db: Session = Depends(get_db)
) -> SyncStatusResponse:
    """Get last sync status and metrics."""
    try:
        service = GoogleFontsService(db)
        status_data = await service.get_sync_status()
        
        return SyncStatusResponse(**status_data)
        
    except Exception as e:
        logger.error(f"Error getting sync status: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get sync status"
        )


@router.put(
    "/{font_family_id}/featured",
    response_model=FontFamilySummaryResponse,
    summary="Set font featured status",
    description="Set font as featured or unfeatured (admin only)"
)
async def set_font_featured(
    font_family_id: int,
    request: SetFontFeaturedRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> FontFamilySummaryResponse:
    """Set font as featured or unfeatured."""
    try:
        # Check for admin role
        if current_user.role not in ['system_admin', 'company_admin']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        service = GoogleFontsService(db)
        font = await service.set_font_featured(
            font_family_id=font_family_id,
            is_featured=request.is_featured,
            display_order=request.display_order
        )
        
        return _font_to_summary(font)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting font featured: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to set font featured"
        )


@router.put(
    "/{font_family_id}/recommended",
    response_model=FontFamilySummaryResponse,
    summary="Set font recommended status",
    description="Set font as recommended or not recommended (admin only)"
)
async def set_font_recommended(
    font_family_id: int,
    request: SetFontRecommendedRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> FontFamilySummaryResponse:
    """Set font as recommended or not recommended."""
    try:
        # Check for admin role
        if current_user.role not in ['system_admin', 'company_admin']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        service = GoogleFontsService(db)
        font = await service.set_font_recommended(
            font_family_id=font_family_id,
            is_recommended=request.is_recommended
        )
        
        return _font_to_summary(font)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting font recommended: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to set font recommended"
        )


# =====================================================================
# Custom Font Endpoints
# =====================================================================

@router.post(
    "/custom",
    response_model=CustomFontResponse,
    summary="Upload custom font",
    description="Upload a custom corporate font with validation and deduplication"
)
async def upload_custom_font(
    file: UploadFile = File(..., description="Font file (TTF, OTF, WOFF, WOFF2)"),
    display_name: Optional[str] = Form(None, description="Custom display name"),
    category: str = Form("sans-serif", description="Font category"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> CustomFontResponse:
    """
    Upload a custom corporate font.
    
    Features:
    - Validates font file structure using fonttools
    - Extracts metadata (name, version, glyphs, scripts)
    - Hash-based deduplication (same file = link to existing)
    - Per-company display name aliases
    
    Supported formats: TTF, OTF, WOFF, WOFF2
    """
    try:
        # Validate file size (max 10MB)
        MAX_SIZE = 10 * 1024 * 1024
        file_bytes = await file.read()
        
        if len(file_bytes) > MAX_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Font file too large. Maximum size is {MAX_SIZE // (1024*1024)}MB"
            )
        
        if len(file_bytes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty file uploaded"
            )
        
        service = CustomFontService(db)
        result = await service.upload_font(
            file_bytes=file_bytes,
            original_filename=file.filename or "unknown.ttf",
            company_id=current_user.company_id,
            user_id=current_user.user_id,
            display_name=display_name,
            category=category
        )
        
        return CustomFontResponse(**result)
        
    except InvalidFontError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid font file: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading custom font: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload font"
        )


@router.get(
    "/custom",
    response_model=CompanyFontListResponse,
    summary="List company fonts",
    description="Get all fonts accessible by the current company"
)
async def list_company_fonts(
    include_google_fonts: bool = Query(True, description="Include Google Fonts in response"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> CompanyFontListResponse:
    """
    List all fonts accessible by the current company.
    
    Returns fonts with effective display names (company overrides applied).
    """
    try:
        service = CustomFontService(db)
        fonts = await service.get_company_fonts(
            company_id=current_user.company_id,
            include_google_fonts=include_google_fonts
        )
        
        font_responses = [_company_font_to_response(f) for f in fonts]
        
        custom_count = sum(1 for f in fonts if f["font_source"] in ("Custom", "System"))
        google_count = sum(1 for f in fonts if f["font_source"] == "Google")
        
        return CompanyFontListResponse(
            fonts=font_responses,
            custom_font_count=custom_count,
            google_font_count=google_count,
            total=len(fonts)
        )
        
    except Exception as e:
        logger.error(f"Error listing company fonts: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list company fonts"
        )


@router.put(
    "/custom/{company_font_id}/name",
    response_model=CompanyFontResponse,
    summary="Update display name",
    description="Update a company's display name for a font"
)
async def update_font_display_name(
    company_font_id: int,
    request: CustomFontDisplayNameRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> CompanyFontResponse:
    """
    Update a company's display name for a font.
    
    This allows companies to use custom names like "BrandFont" for any font they have access to.
    """
    try:
        service = CustomFontService(db)
        company_font = await service.update_display_name(
            company_font_id=company_font_id,
            new_display_name=request.display_name,
            user_id=current_user.user_id
        )
        
        # Get font family details
        fonts = await service.get_company_fonts(
            company_id=current_user.company_id,
            include_google_fonts=False
        )
        
        # Find the updated font
        for f in fonts:
            if f["company_font_id"] == company_font_id:
                return _company_font_to_response(f)
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company font not found: {company_font_id}"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating font display name: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update display name"
        )


@router.delete(
    "/custom/{company_font_id}",
    summary="Revoke font access",
    description="Revoke a company's access to a custom font"
)
async def revoke_font_access(
    company_font_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Revoke a company's access to a custom font.
    
    This does not delete the font, just removes the company's access.
    """
    try:
        service = CustomFontService(db)
        await service.revoke_font_access(
            company_font_id=company_font_id,
            user_id=current_user.user_id
        )
        
        return {"success": True, "message": "Font access revoked"}
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error revoking font access: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke font access"
        )


@router.get(
    "/file/{font_variant_id}",
    summary="Stream font file",
    description="Stream font file for preview/download"
)
async def get_font_file(
    font_variant_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> StreamingResponse:
    """
    Stream font file for preview or download.
    
    Returns the font file with appropriate content-type headers.
    """
    try:
        service = CustomFontService(db)
        font_file = await service.get_font_file(font_variant_id)
        
        if not font_file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Font file not found for variant: {font_variant_id}"
            )
        
        # Create streaming response
        return StreamingResponse(
            io.BytesIO(font_file.FileData),
            media_type=font_file.MimeType,
            headers={
                "Content-Disposition": f'inline; filename="{font_file.OriginalFileName or "font." + font_file.FileFormat}"',
                "Content-Length": str(font_file.FileSizeBytes),
                "Cache-Control": "public, max-age=31536000",  # Cache for 1 year
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting font file: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get font file"
        )

