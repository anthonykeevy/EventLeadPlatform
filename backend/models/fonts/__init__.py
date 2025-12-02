"""
Google Fonts Domain Models
Local caching of Google Fonts metadata AND custom corporate font uploads for the Form Builder
"""

from .font_family import FontFamily
from .font_variant import FontVariant
from .font_subset import FontSubset
from .font_axis import FontAxis
from .font_color_capability import FontColorCapability
from .font_sync_log import FontSyncLog
from .font_sync_detail import FontSyncDetail
from .font_usage_log import FontUsageLog
from .font_category_ref import FontCategoryRef
from .font_subset_ref import FontSubsetRef
from .font_axis_ref import FontAxisRef
from .company_font import CompanyFont
from .font_file import FontFile

__all__ = [
    # Core tables (dbo schema)
    "FontFamily",
    "FontVariant",
    "FontSubset",
    "FontAxis",
    "FontColorCapability",
    # Company-Font relationship (dbo schema)
    "CompanyFont",
    # Font file storage (dbo schema)
    "FontFile",
    # Log tables (log schema)
    "FontSyncLog",
    "FontSyncDetail",
    "FontUsageLog",
    # Reference tables (dbo schema)
    "FontCategoryRef",
    "FontSubsetRef",
    "FontAxisRef",
]

