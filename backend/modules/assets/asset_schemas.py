"""
Asset Contracts - Story 5.1 (Background Asset Management)
Pydantic models defining asset metadata, placement, and resolver interfaces.

NOTE:
- Field names intentionally use camelCase to match frontend contracts.
- Data URLs must NOT be persisted in form definitions; validation should reject
  any background value starting with "data:" before save/export.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional, Protocol, Literal

from pydantic import BaseModel, Field


# =====================================================================
# Core Asset Metadata Contract (FE + BE parity)
# =====================================================================

class BackgroundAssetMetadata(BaseModel):
    """Canonical asset metadata shared across frontend and backend."""
    assetId: int = Field(..., description="Stable asset identifier (DB primary key)")
    assetKey: str = Field(..., description="Stable asset key for referencing assets in definitions")
    displayName: Optional[str] = Field(None, description="Human-friendly name (can differ from filename)")
    originalFilename: str = Field(..., description="Original uploaded filename")
    mimeType: str = Field(..., description="MIME type (e.g., image/png)")
    byteSize: int = Field(..., description="File size in bytes")
    widthPx: Optional[int] = Field(None, description="Pixel width of the asset")
    heightPx: Optional[int] = Field(None, description="Pixel height of the asset")
    checksumSha256: Optional[str] = Field(None, description="SHA-256 checksum for dedupe")
    createdAt: Optional[datetime] = Field(None, description="Asset creation timestamp (UTC)")
    updatedAt: Optional[datetime] = Field(None, description="Asset update timestamp (UTC)")


class BackgroundAssetUploadResponse(BaseModel):
    """Upload response with asset metadata."""
    asset: BackgroundAssetMetadata
    isDuplicate: bool = Field(False, description="True if deduped to an existing asset")


class AssetResolveResponse(BaseModel):
    """Runtime URL resolver response."""
    url: str = Field(..., description="Resolved runtime URL for asset access")


class BackgroundAssetListResponse(BaseModel):
    """List of background assets for the current user's company."""
    assets: list[BackgroundAssetMetadata] = Field(default_factory=list, description="Company background assets")


class AssetUpdateRequest(BaseModel):
    """Update asset metadata (Story 5.7)."""
    display_name: Optional[str] = Field(None, max_length=255, description="Display name for the asset")
    display_width_px: Optional[int] = Field(None, ge=320, le=1920, description="Terms modal width")
    display_height_px: Optional[int] = Field(None, ge=240, le=1080, description="Terms modal height")
    display_rotation_degrees: Optional[int] = Field(None, ge=0, le=359, description="PDF rotation 0,90,180,270")


# =====================================================================
# Terms Asset (Story 5.7)
# =====================================================================

class TermsAssetMetadata(BaseModel):
    """Terms asset metadata (PDF upload or URL)."""
    assetId: int = Field(..., description="Asset ID")
    assetKey: str = Field(..., description="Asset key for form references")
    displayName: Optional[str] = Field(None, description="Display name")
    sourceType: Literal["upload", "url"] = Field(..., description="PDF upload or URL")
    sourceUrl: Optional[str] = Field(None, description="URL when sourceType=url")
    mimeType: str = Field(..., description="application/pdf or text/url")
    byteSize: int = Field(0, description="File size (0 for URL)")
    embeddable: Optional[bool] = Field(None, description="True if URL can be embedded in iframe")
    termsDisplayMode: Optional[Literal["popup", "new_tab"]] = Field(
        None, description="popup=iframe; new_tab=link; null for PDF"
    )
    displayWidthPx: Optional[int] = Field(None, description="Preferred modal width for Terms popup")
    displayHeightPx: Optional[int] = Field(None, description="Preferred modal height for Terms popup")
    displayRotationDegrees: Optional[int] = Field(None, description="PDF rotation: 0, 90, 180, 270")
    createdAt: Optional[datetime] = Field(None)
    updatedAt: Optional[datetime] = Field(None)


class TermsAssetUpdateRequest(BaseModel):
    """Update Terms asset display settings."""
    display_name: Optional[str] = Field(None, max_length=255)
    display_width_px: Optional[int] = Field(None, ge=320, le=1920)
    display_height_px: Optional[int] = Field(None, ge=240, le=1080)
    display_rotation_degrees: Optional[int] = Field(None, ge=0, le=359)


class TermsAssetListResponse(BaseModel):
    """List of Terms assets for a company."""
    assets: list[TermsAssetMetadata] = Field(default_factory=list)
    defaultTermsAssetId: Optional[int] = Field(None, description="Asset ID used as default when multiple exist")


class SetDefaultTermsRequest(BaseModel):
    """Set company's default Terms asset."""
    assetId: int = Field(..., description="Asset ID to use as default; must be a Terms asset for this company")


class TermsUploadResponse(BaseModel):
    """Response after PDF upload."""
    asset: TermsAssetMetadata
    isDuplicate: bool = False


class TermsUrlAddRequest(BaseModel):
    """Add Terms by URL."""
    url: str = Field(..., min_length=10, max_length=2048)
    display_name: Optional[str] = Field(None, max_length=255)
    display_mode: Optional[Literal["popup", "new_tab"]] = Field(
        "popup",
        description="popup = iframe; new_tab = link opens in new tab",
    )


class TermsUrlValidateRequest(BaseModel):
    """Validate Terms URL (embedding)."""
    url: str = Field(..., min_length=10, max_length=2048)


class TermsUrlValidateResponse(BaseModel):
    """URL validation result (embedding)."""
    embeddable: bool = Field(..., description="Can be embedded in iframe")
    reason: Optional[str] = Field(None, description="Explanation when not embeddable")
    blocker_type: Optional[str] = Field(
        None,
        description="Type of blocker: embedding, reachability, content, unknown",
    )
    next_action: Optional[str] = Field(
        None,
        description="What the user can do next to use this URL",
    )


# =====================================================================
# Background Placement Contract (position, size, crop)
# =====================================================================

class BackgroundPosition(BaseModel):
    """Canvas position in pixels (allows negative offsets)."""
    x: float = Field(..., description="X position in canvas coordinates (px)")
    y: float = Field(..., description="Y position in canvas coordinates (px)")


class BackgroundSize(BaseModel):
    """Rendered size in pixels."""
    width: float = Field(..., description="Rendered width in pixels")
    height: float = Field(..., description="Rendered height in pixels")


class BackgroundCrop(BaseModel):
    """Crop rectangle in pixels (relative to the asset)."""
    x: float = Field(..., description="Crop X offset in pixels")
    y: float = Field(..., description="Crop Y offset in pixels")
    width: float = Field(..., description="Crop width in pixels")
    height: float = Field(..., description="Crop height in pixels")


class BackgroundPlacement(BaseModel):
    """Placement metadata for background assets."""
    position: BackgroundPosition
    size: BackgroundSize
    crop: Optional[BackgroundCrop] = None


# =====================================================================
# Background Definition Contract
# =====================================================================

class BackgroundDefinition(BaseModel):
    """
    Background definition for a form page.

    - For color backgrounds, value is a hex color string.
    - For image backgrounds, value may be a legacy URL, but preferred contract
      is the asset metadata + placement.
    """
    type: Literal["color", "image"]
    value: str = Field(..., description="Hex color or legacy URL (no Data URLs allowed)")
    asset: Optional[BackgroundAssetMetadata] = Field(
        None, description="Preferred asset reference for background images"
    )
    placement: Optional[BackgroundPlacement] = Field(
        None, description="Placement metadata for image backgrounds"
    )
    imageSize: Optional[Literal["cover", "contain", "tile", "auto"]] = Field(
        None, description="Legacy image sizing mode (CSS-style)"
    )
    imagePosition: Optional[str] = Field(
        None, description="Legacy image positioning (CSS-style)"
    )
    overlayColor: Optional[str] = Field(None, description="Overlay color (hex)")
    overlayOpacity: Optional[float] = Field(None, ge=0, le=1, description="Overlay opacity (0-1)")
    opacity: Optional[float] = Field(None, ge=0, le=1, description="Background opacity (0-1)")
    scale: Optional[float] = Field(None, description="Legacy scale factor")
    position: Optional[BackgroundPosition] = Field(
        None, description="Legacy position (use placement.position instead)"
    )


# =====================================================================
# Resolver Contract (interface only - no implementation)
# =====================================================================

class BackgroundAssetResolver(Protocol):
    """Resolve asset references into runtime URLs."""
    def resolve_url(
        self, asset: BackgroundAssetMetadata, placement: Optional[BackgroundPlacement] = None
    ) -> str:
        """Return a runtime URL for the provided asset reference."""
        ...
