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
