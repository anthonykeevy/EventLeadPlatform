"""
Font Schemas
Pydantic models for font API requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal


# =====================================================================
# Request Schemas
# =====================================================================

class FontSearchParams(BaseModel):
    """Parameters for font search."""
    query: Optional[str] = Field(None, description="Search term for font name")
    category: Optional[str] = Field(None, description="Filter by category")
    subset: Optional[str] = Field(None, description="Filter by required subset")
    is_variable: Optional[bool] = Field(None, description="Variable fonts only")
    has_italic: Optional[bool] = Field(None, description="Fonts with italic")
    min_weight: Optional[int] = Field(None, ge=100, le=900, description="Minimum weight")
    max_weight: Optional[int] = Field(None, ge=100, le=900, description="Maximum weight")
    is_featured: Optional[bool] = Field(None, description="Featured fonts only")
    is_recommended: Optional[bool] = Field(None, description="Recommended fonts only")
    sort_by: str = Field("popularity", description="Sort order")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")


class FontUsageRequest(BaseModel):
    """Request to log font usage."""
    context: str = Field(..., description="Usage context (FormBuilder, Preview, etc.)")
    action: str = Field(..., description="Action type (Selected, Applied, Previewed)")
    font_variant_id: Optional[int] = Field(None, description="Specific variant used")
    context_entity_type: Optional[str] = Field(None, description="Entity type (Form, Template)")
    context_entity_id: Optional[int] = Field(None, description="Entity ID")


class SetFontFeaturedRequest(BaseModel):
    """Request to set font as featured."""
    is_featured: bool = Field(..., description="Featured status")
    display_order: Optional[int] = Field(None, description="Display order")


class SetFontRecommendedRequest(BaseModel):
    """Request to set font as recommended."""
    is_recommended: bool = Field(..., description="Recommended status")


# =====================================================================
# Response Schemas
# =====================================================================

class FontVariantResponse(BaseModel):
    """Font variant response."""
    font_variant_id: int
    variant_name: str
    weight: int
    weight_name: Optional[str]
    is_italic: bool
    ttf_file_url: Optional[str]
    display_order: int
    is_default: bool

    class Config:
        from_attributes = True


class FontSubsetResponse(BaseModel):
    """Font subset response."""
    font_subset_id: int
    subset_code: str
    subset_name: str
    subset_group: Optional[str]
    is_extended: bool

    class Config:
        from_attributes = True


class FontAxisResponse(BaseModel):
    """Font axis response (for variable fonts)."""
    font_axis_id: int
    axis_tag: str
    axis_name: str
    min_value: Decimal
    max_value: Decimal
    default_value: Optional[Decimal]
    is_standard: bool
    css_property: Optional[str]

    class Config:
        from_attributes = True


class FontFamilySummaryResponse(BaseModel):
    """Font family summary for list views."""
    font_family_id: int
    google_font_id: Optional[str]  # NULL for custom fonts
    family_name: str
    category: str
    version: str
    is_variable_font: bool
    min_weight: Optional[int]
    max_weight: Optional[int]
    has_italic: bool
    total_variants: int
    total_subsets: int
    menu_file_url: Optional[str]
    popularity_rank: Optional[int]
    usage_count: int
    is_featured: bool
    is_recommended: bool
    variant_list: Optional[str]

    class Config:
        from_attributes = True


class FontFamilyDetailResponse(BaseModel):
    """Complete font family details."""
    font_family_id: int
    google_font_id: Optional[str]  # NULL for custom fonts
    family_name: str
    category: str
    sub_category: Optional[str]
    version: str
    version_number: Optional[int]
    last_modified_date: date
    menu_file_url: Optional[str]
    specimen_url: Optional[str]
    is_variable_font: bool
    has_color_capabilities: bool
    min_weight: Optional[int]
    max_weight: Optional[int]
    has_italic: bool
    has_regular: bool
    supports_latin: bool
    supports_cyrillic: bool
    supports_greek: bool
    supports_arabic: bool
    supports_hebrew: bool
    supports_asian: bool
    total_subsets: int
    total_variants: int
    variant_list: Optional[str]
    popularity_rank: Optional[int]
    usage_count: int
    is_recommended: bool
    is_featured: bool
    display_order: Optional[int]
    license_type: Optional[str]
    license_url: Optional[str]
    designer: Optional[str]
    designer_url: Optional[str]
    foundry: Optional[str]
    last_sync_date: datetime
    variants: List[FontVariantResponse]
    subsets: List[FontSubsetResponse]
    axes: List[FontAxisResponse]

    class Config:
        from_attributes = True


class FontListResponse(BaseModel):
    """Paginated font list response."""
    fonts: List[FontFamilySummaryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class FontCategoryResponse(BaseModel):
    """Font category with count."""
    category_code: str
    category_name: str
    description: Optional[str]
    icon_class: Optional[str]
    display_order: int
    font_count: int


class SyncStatusResponse(BaseModel):
    """Sync status response."""
    last_sync: Optional[dict]
    font_counts: dict


class SyncResultResponse(BaseModel):
    """Sync result response."""
    success: bool
    sync_id: Optional[int]
    total_fonts_in_api: Optional[int]
    fonts_added: Optional[int]
    fonts_updated: Optional[int]
    fonts_deprecated: Optional[int]
    fonts_unchanged: Optional[int]
    variants_processed: Optional[int]
    subsets_processed: Optional[int]
    axes_processed: Optional[int]
    duration_seconds: Optional[float]
    api_response_time_ms: Optional[int]
    error: Optional[str]


class FontUsageResponse(BaseModel):
    """Font usage log response."""
    success: bool
    message: str


# =====================================================================
# Custom Font Schemas
# =====================================================================

class CustomFontUploadRequest(BaseModel):
    """Request for custom font upload."""
    display_name: Optional[str] = Field(None, description="Custom display name for the font")
    category: str = Field("sans-serif", description="Font category")


class CustomFontDisplayNameRequest(BaseModel):
    """Request to update display name."""
    display_name: str = Field(..., min_length=1, max_length=200, description="New display name")


class CustomFontResponse(BaseModel):
    """Custom font upload response."""
    status: str  # 'created' or 'linked'
    is_duplicate: bool
    font_family_id: int
    font_variant_id: Optional[int] = None
    font_file_id: Optional[int] = None
    company_font_id: int
    display_name: str
    message: str


class CompanyFontResponse(BaseModel):
    """Company font with effective display name."""
    font_family_id: int
    display_name: str  # Effective display name (override or original)
    internal_name: Optional[str]
    original_name: str
    font_source: str  # 'Google', 'Custom', 'System'
    category: str
    is_variable_font: bool
    min_weight: Optional[int]
    max_weight: Optional[int]
    has_italic: bool
    total_variants: int
    is_owner: bool
    is_shared: bool
    license_type: Optional[str]
    license_expiry_date: Optional[date] = None
    company_font_id: Optional[int]

    class Config:
        from_attributes = True


class CompanyFontListResponse(BaseModel):
    """List of company fonts."""
    fonts: List[CompanyFontResponse]
    custom_font_count: int
    google_font_count: int
    total: int


class FontFileStreamResponse(BaseModel):
    """Font file metadata for streaming."""
    font_variant_id: int
    file_format: str
    file_size_bytes: int
    mime_type: str
    original_filename: Optional[str]


# =====================================================================
# Extended Font Schemas (for frontend with context)
# =====================================================================

class FontFamilySummaryWithContextResponse(BaseModel):
    """Font family summary with company context."""
    font_family_id: int
    google_font_id: Optional[str]  # NULL for custom fonts
    family_name: str
    display_name: str  # Effective display name for company
    font_source: str  # 'Google', 'Custom', 'System'
    category: str
    version: str
    is_variable_font: bool
    min_weight: Optional[int]
    max_weight: Optional[int]
    has_italic: bool
    total_variants: int
    total_subsets: int
    menu_file_url: Optional[str]
    popularity_rank: Optional[int]
    usage_count: int
    is_featured: bool
    is_recommended: bool
    variant_list: Optional[str]
    # Company context
    is_company_font: bool  # TRUE if company has specific access
    is_owner: bool
    company_font_id: Optional[int]

    class Config:
        from_attributes = True

