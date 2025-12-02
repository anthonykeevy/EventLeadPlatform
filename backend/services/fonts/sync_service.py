"""
Font Sync Service
Synchronization service for Google Fonts API
"""
import os
import httpx
import re
from typing import Dict, Any, List, Optional, Set
from datetime import datetime, date
from sqlalchemy.orm import Session

from common.logger import get_logger
from models.fonts import (
    FontFamily,
    FontVariant,
    FontSubset,
    FontAxis,
    FontColorCapability,
    FontSyncLog,
    FontSyncDetail,
)

logger = get_logger(__name__)


class FontSyncService:
    """
    Service for synchronizing fonts from Google Fonts API.
    
    Handles:
    - Fetching font metadata from Google Fonts API
    - Comparing with existing database records
    - Adding new fonts
    - Updating changed fonts
    - Marking deprecated fonts
    - Logging all sync operations
    """
    
    GOOGLE_FONTS_API_URL = "https://www.googleapis.com/webfonts/v1/webfonts"
    
    # Standard font weight names
    WEIGHT_NAMES = {
        100: 'Thin',
        200: 'Extra Light',
        300: 'Light',
        400: 'Regular',
        500: 'Medium',
        600: 'Semi Bold',
        700: 'Bold',
        800: 'Extra Bold',
        900: 'Black',
    }
    
    # Standard font axes
    STANDARD_AXES = {'wght', 'wdth', 'ital', 'slnt', 'opsz'}
    
    def __init__(self, db: Session):
        self.db = db
        self.api_key = os.getenv("GOOGLE_FONTS_API_KEY")
        
        if not self.api_key:
            logger.warning("GOOGLE_FONTS_API_KEY not set - sync will fail")
    
    async def execute_sync(
        self,
        trigger_type: str = "Manual",
        triggered_by: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute font synchronization with Google Fonts API.
        
        Args:
            trigger_type: How sync was triggered (Scheduled, Manual, Webhook)
            triggered_by: User or system that triggered sync
            
        Returns:
            Sync results summary
        """
        sync_log = FontSyncLog(
            SyncStartTime=datetime.utcnow(),
            SyncStatus='Running',
            TriggerType=trigger_type,
            TriggeredBy=triggered_by,
            APIEndpoint=self.GOOGLE_FONTS_API_URL,
            APIVersion='v2'
        )
        self.db.add(sync_log)
        self.db.commit()
        
        try:
            logger.info(f"Starting font sync (trigger={trigger_type})")
            
            # Fetch fonts from Google API
            api_start = datetime.utcnow()
            api_response = await self._fetch_from_google_api()
            api_end = datetime.utcnow()
            
            sync_log.APIResponseTimeMs = int((api_end - api_start).total_seconds() * 1000)
            
            if not api_response or 'items' not in api_response:
                raise ValueError("Invalid API response - no items found")
            
            fonts_from_api = api_response['items']
            sync_log.TotalFontsInAPI = len(fonts_from_api)
            
            logger.info(f"Fetched {len(fonts_from_api)} fonts from Google API")
            
            # Get existing fonts from database
            existing_fonts = self._get_existing_fonts()
            existing_map = {f.GoogleFontID: f for f in existing_fonts}
            
            processed_ids: Set[str] = set()
            
            # Process each font from API
            for api_font in fonts_from_api:
                try:
                    google_id = self._generate_google_font_id(api_font['family'])
                    processed_ids.add(google_id)
                    
                    if google_id not in existing_map:
                        # New font
                        await self._insert_font(api_font, sync_log)
                        sync_log.FontsAdded += 1
                    else:
                        existing_font = existing_map[google_id]
                        if self._has_font_changed(existing_font, api_font):
                            # Updated font
                            await self._update_font(existing_font, api_font, sync_log)
                            sync_log.FontsUpdated += 1
                        else:
                            # Unchanged
                            sync_log.FontsUnchanged += 1
                            
                except Exception as font_error:
                    logger.error(f"Error processing font {api_font.get('family', 'unknown')}: {str(font_error)}")
                    self._log_sync_detail(
                        sync_log=sync_log,
                        google_font_id=self._generate_google_font_id(api_font.get('family', 'unknown')),
                        family_name=api_font.get('family'),
                        operation='Error',
                        error_message=str(font_error)
                    )
            
            # Handle removed fonts (in DB but not in API)
            for google_id, existing_font in existing_map.items():
                if google_id not in processed_ids and existing_font.SyncStatus == 'Active':
                    await self._deprecate_font(existing_font, sync_log)
                    sync_log.FontsDeprecated += 1
            
            # Complete sync
            sync_log.SyncStatus = 'Success'
            sync_log.SyncEndTime = datetime.utcnow()
            
            self.db.commit()
            
            result = {
                'success': True,
                'sync_id': sync_log.FontSyncLogID,
                'total_fonts_in_api': sync_log.TotalFontsInAPI,
                'fonts_added': sync_log.FontsAdded,
                'fonts_updated': sync_log.FontsUpdated,
                'fonts_deprecated': sync_log.FontsDeprecated,
                'fonts_unchanged': sync_log.FontsUnchanged,
                'variants_processed': sync_log.VariantsProcessed,
                'subsets_processed': sync_log.SubsetsProcessed,
                'axes_processed': sync_log.AxesProcessed,
                'duration_seconds': (sync_log.SyncEndTime - sync_log.SyncStartTime).total_seconds(),
                'api_response_time_ms': sync_log.APIResponseTimeMs,
            }
            
            logger.info(f"Font sync completed: {result}")
            
            return result
            
        except Exception as e:
            sync_log.SyncStatus = 'Failed'
            sync_log.SyncEndTime = datetime.utcnow()
            sync_log.ErrorMessage = str(e)
            sync_log.ErrorDetails = str(e.__class__.__name__)
            
            self.db.commit()
            
            logger.error(f"Font sync failed: {str(e)}", exc_info=True)
            
            return {
                'success': False,
                'sync_id': sync_log.FontSyncLogID,
                'error': str(e)
            }
    
    async def _fetch_from_google_api(self) -> Dict[str, Any]:
        """Fetch font data from Google Fonts API."""
        if not self.api_key:
            raise ValueError("GOOGLE_FONTS_API_KEY environment variable not set")
        
        params = {
            'key': self.api_key,
            'sort': 'popularity'
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(self.GOOGLE_FONTS_API_URL, params=params)
            response.raise_for_status()
            return response.json()
    
    def _get_existing_fonts(self) -> List[FontFamily]:
        """Get all existing fonts from database."""
        return self.db.query(FontFamily).filter(
            FontFamily.IsDeleted == False
        ).all()
    
    def _generate_google_font_id(self, family_name: str) -> str:
        """Generate a consistent Google Font ID from family name."""
        # Normalize family name to create ID
        return family_name.lower().replace(' ', '-')
    
    def _has_font_changed(self, existing: FontFamily, api_font: Dict[str, Any]) -> bool:
        """Check if font has changed since last sync."""
        # Compare version
        if existing.Version != api_font.get('version'):
            return True
        
        # Compare last modified date
        api_date = api_font.get('lastModified')
        if api_date:
            try:
                api_date_parsed = datetime.strptime(api_date, '%Y-%m-%d').date()
                if existing.LastModifiedDate != api_date_parsed:
                    return True
            except ValueError:
                pass
        
        # Compare variants count
        api_variants = api_font.get('variants', [])
        if existing.TotalVariants != len(api_variants):
            return True
        
        # Compare subsets count
        api_subsets = api_font.get('subsets', [])
        if existing.TotalSubsets != len(api_subsets):
            return True
        
        return False
    
    async def _insert_font(self, api_font: Dict[str, Any], sync_log: FontSyncLog) -> FontFamily:
        """Insert a new font from API data."""
        family_name = api_font['family']
        google_id = self._generate_google_font_id(family_name)
        
        # Parse variants
        variants = api_font.get('variants', ['regular'])
        files = api_font.get('files', {})
        subsets = api_font.get('subsets', ['latin'])
        axes = api_font.get('axes', [])
        
        # Determine font characteristics
        weights = self._parse_weights(variants)
        has_italic = any('italic' in v for v in variants)
        has_regular = 'regular' in variants or '400' in variants
        is_variable = len(axes) > 0
        
        # Parse last modified date
        last_modified = date.today()
        if api_font.get('lastModified'):
            try:
                last_modified = datetime.strptime(api_font['lastModified'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # Create font family
        font = FontFamily(
            GoogleFontID=google_id,
            FamilyName=family_name,
            FamilyNameNormalized=family_name.lower(),
            Category=api_font.get('category', 'sans-serif'),
            Version=api_font.get('version', 'v1'),
            VersionNumber=self._parse_version_number(api_font.get('version')),
            LastModifiedDate=last_modified,
            MenuFileUrl=api_font.get('menu'),
            IsVariableFont=is_variable,
            HasColorCapabilities=len(api_font.get('colorCapabilities', [])) > 0,
            MinWeight=min(weights) if weights else 400,
            MaxWeight=max(weights) if weights else 400,
            HasItalic=has_italic,
            HasRegular=has_regular,
            SupportsLatin='latin' in subsets,
            SupportsCyrillic='cyrillic' in subsets or 'cyrillic-ext' in subsets,
            SupportsGreek='greek' in subsets or 'greek-ext' in subsets,
            SupportsArabic='arabic' in subsets,
            SupportsHebrew='hebrew' in subsets,
            SupportsAsian=any(s in subsets for s in ['vietnamese', 'thai', 'korean', 'japanese', 'chinese-simplified', 'chinese-traditional']),
            TotalSubsets=len(subsets),
            TotalVariants=len(variants),
            VariantList=','.join(variants[:10]),  # Limit for storage
            SyncStatus='Active',
            CreatedBy='SYNC'
        )
        
        self.db.add(font)
        self.db.flush()  # Get the ID
        
        # Insert variants
        for idx, variant_name in enumerate(variants):
            weight, is_italic = self._parse_variant(variant_name)
            file_url = files.get(variant_name)
            
            variant = FontVariant(
                FontFamilyID=font.FontFamilyID,
                VariantName=variant_name,
                VariantNameNormalized=variant_name.lower(),
                Weight=weight,
                WeightName=self.WEIGHT_NAMES.get(weight),
                IsItalic=is_italic,
                TtfFileUrl=file_url,
                DisplayOrder=idx,
                IsDefault=variant_name == 'regular'
            )
            self.db.add(variant)
            sync_log.VariantsProcessed += 1
        
        # Insert subsets
        for idx, subset_code in enumerate(subsets):
            subset = FontSubset(
                FontFamilyID=font.FontFamilyID,
                SubsetCode=subset_code,
                SubsetName=self._get_subset_name(subset_code),
                SubsetGroup=self._get_subset_group(subset_code),
                IsExtended='-ext' in subset_code,
                DisplayOrder=idx
            )
            self.db.add(subset)
            sync_log.SubsetsProcessed += 1
        
        # Insert axes (for variable fonts)
        for idx, axis_data in enumerate(axes):
            axis = FontAxis(
                FontFamilyID=font.FontFamilyID,
                AxisTag=axis_data.get('tag', ''),
                AxisName=self._get_axis_name(axis_data.get('tag', '')),
                MinValue=axis_data.get('start', 0),
                MaxValue=axis_data.get('end', 0),
                IsStandard=axis_data.get('tag', '') in self.STANDARD_AXES,
                DisplayOrder=idx
            )
            self.db.add(axis)
            sync_log.AxesProcessed += 1
        
        # Insert color capabilities
        for cap_code in api_font.get('colorCapabilities', []):
            cap = FontColorCapability(
                FontFamilyID=font.FontFamilyID,
                CapabilityCode=cap_code,
                CapabilityName=cap_code
            )
            self.db.add(cap)
        
        # Log the addition
        self._log_sync_detail(
            sync_log=sync_log,
            font_family=font,
            operation='Added',
            new_version=font.Version
        )
        
        logger.debug(f"Inserted new font: {family_name}")
        
        return font
    
    async def _update_font(
        self,
        existing: FontFamily,
        api_font: Dict[str, Any],
        sync_log: FontSyncLog
    ) -> FontFamily:
        """Update an existing font with new API data."""
        previous_version = existing.Version
        
        # Parse new data
        variants = api_font.get('variants', ['regular'])
        files = api_font.get('files', {})
        subsets = api_font.get('subsets', ['latin'])
        axes = api_font.get('axes', [])
        
        weights = self._parse_weights(variants)
        has_italic = any('italic' in v for v in variants)
        has_regular = 'regular' in variants or '400' in variants
        is_variable = len(axes) > 0
        
        # Parse last modified date
        last_modified = existing.LastModifiedDate
        if api_font.get('lastModified'):
            try:
                last_modified = datetime.strptime(api_font['lastModified'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # Update font family
        existing.Version = api_font.get('version', existing.Version)
        existing.VersionNumber = self._parse_version_number(api_font.get('version'))
        existing.LastModifiedDate = last_modified
        existing.MenuFileUrl = api_font.get('menu', existing.MenuFileUrl)
        existing.IsVariableFont = is_variable
        existing.HasColorCapabilities = len(api_font.get('colorCapabilities', [])) > 0
        existing.MinWeight = min(weights) if weights else 400
        existing.MaxWeight = max(weights) if weights else 400
        existing.HasItalic = has_italic
        existing.HasRegular = has_regular
        existing.SupportsLatin = 'latin' in subsets
        existing.SupportsCyrillic = 'cyrillic' in subsets or 'cyrillic-ext' in subsets
        existing.SupportsGreek = 'greek' in subsets or 'greek-ext' in subsets
        existing.SupportsArabic = 'arabic' in subsets
        existing.SupportsHebrew = 'hebrew' in subsets
        existing.SupportsAsian = any(s in subsets for s in ['vietnamese', 'thai', 'korean', 'japanese', 'chinese-simplified', 'chinese-traditional'])
        existing.TotalSubsets = len(subsets)
        existing.TotalVariants = len(variants)
        existing.VariantList = ','.join(variants[:10])
        existing.LastSyncDate = datetime.utcnow()
        existing.SyncVersion = (existing.SyncVersion or 0) + 1
        existing.UpdatedDate = datetime.utcnow()
        existing.UpdatedBy = 'SYNC'
        
        # Update variants (delete old, insert new)
        self.db.query(FontVariant).filter(
            FontVariant.FontFamilyID == existing.FontFamilyID
        ).delete()
        
        for idx, variant_name in enumerate(variants):
            weight, is_italic = self._parse_variant(variant_name)
            file_url = files.get(variant_name)
            
            variant = FontVariant(
                FontFamilyID=existing.FontFamilyID,
                VariantName=variant_name,
                VariantNameNormalized=variant_name.lower(),
                Weight=weight,
                WeightName=self.WEIGHT_NAMES.get(weight),
                IsItalic=is_italic,
                TtfFileUrl=file_url,
                DisplayOrder=idx,
                IsDefault=variant_name == 'regular'
            )
            self.db.add(variant)
            sync_log.VariantsProcessed += 1
        
        # Update subsets
        self.db.query(FontSubset).filter(
            FontSubset.FontFamilyID == existing.FontFamilyID
        ).delete()
        
        for idx, subset_code in enumerate(subsets):
            subset = FontSubset(
                FontFamilyID=existing.FontFamilyID,
                SubsetCode=subset_code,
                SubsetName=self._get_subset_name(subset_code),
                SubsetGroup=self._get_subset_group(subset_code),
                IsExtended='-ext' in subset_code,
                DisplayOrder=idx
            )
            self.db.add(subset)
            sync_log.SubsetsProcessed += 1
        
        # Update axes
        self.db.query(FontAxis).filter(
            FontAxis.FontFamilyID == existing.FontFamilyID
        ).delete()
        
        for idx, axis_data in enumerate(axes):
            axis = FontAxis(
                FontFamilyID=existing.FontFamilyID,
                AxisTag=axis_data.get('tag', ''),
                AxisName=self._get_axis_name(axis_data.get('tag', '')),
                MinValue=axis_data.get('start', 0),
                MaxValue=axis_data.get('end', 0),
                IsStandard=axis_data.get('tag', '') in self.STANDARD_AXES,
                DisplayOrder=idx
            )
            self.db.add(axis)
            sync_log.AxesProcessed += 1
        
        # Update color capabilities
        self.db.query(FontColorCapability).filter(
            FontColorCapability.FontFamilyID == existing.FontFamilyID
        ).delete()
        
        for cap_code in api_font.get('colorCapabilities', []):
            cap = FontColorCapability(
                FontFamilyID=existing.FontFamilyID,
                CapabilityCode=cap_code,
                CapabilityName=cap_code
            )
            self.db.add(cap)
        
        # Log the update
        self._log_sync_detail(
            sync_log=sync_log,
            font_family=existing,
            operation='Updated',
            previous_version=previous_version,
            new_version=existing.Version,
            change_summary=f"Updated from {previous_version} to {existing.Version}"
        )
        
        logger.debug(f"Updated font: {existing.FamilyName}")
        
        return existing
    
    async def _deprecate_font(self, font: FontFamily, sync_log: FontSyncLog) -> None:
        """Mark a font as deprecated (removed from Google Fonts)."""
        font.SyncStatus = 'Deprecated'
        font.UpdatedDate = datetime.utcnow()
        font.UpdatedBy = 'SYNC'
        
        self._log_sync_detail(
            sync_log=sync_log,
            font_family=font,
            operation='Deprecated',
            previous_version=font.Version,
            change_summary="Font no longer available in Google Fonts API"
        )
        
        logger.info(f"Deprecated font: {font.FamilyName}")
    
    def _log_sync_detail(
        self,
        sync_log: FontSyncLog,
        operation: str,
        google_font_id: Optional[str] = None,
        family_name: Optional[str] = None,
        font_family: Optional[FontFamily] = None,
        previous_version: Optional[str] = None,
        new_version: Optional[str] = None,
        change_summary: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> None:
        """Log a sync detail record."""
        detail = FontSyncDetail(
            FontSyncLogID=sync_log.FontSyncLogID,
            FontFamilyID=font_family.FontFamilyID if font_family else None,
            GoogleFontID=google_font_id or (font_family.GoogleFontID if font_family else None),
            FamilyName=family_name or (font_family.FamilyName if font_family else None),
            Operation=operation,
            PreviousVersion=previous_version,
            NewVersion=new_version,
            ChangeSummary=change_summary,
            ErrorMessage=error_message
        )
        self.db.add(detail)
    
    def _parse_weights(self, variants: List[str]) -> List[int]:
        """Parse weight values from variant names."""
        weights = set()
        for variant in variants:
            weight, _ = self._parse_variant(variant)
            weights.add(weight)
        return list(weights)
    
    def _parse_variant(self, variant_name: str) -> tuple:
        """Parse variant name into weight and italic flag."""
        variant_lower = variant_name.lower()
        is_italic = 'italic' in variant_lower
        
        # Remove 'italic' suffix
        weight_str = variant_lower.replace('italic', '').strip()
        
        # Map common names to weights
        name_to_weight = {
            'thin': 100,
            'extralight': 200,
            'light': 300,
            'regular': 400,
            '': 400,
            'medium': 500,
            'semibold': 600,
            'bold': 700,
            'extrabold': 800,
            'black': 900,
        }
        
        if weight_str in name_to_weight:
            return name_to_weight[weight_str], is_italic
        
        # Try to parse as number
        try:
            weight = int(weight_str)
            if 100 <= weight <= 900:
                return weight, is_italic
        except ValueError:
            pass
        
        return 400, is_italic
    
    def _parse_version_number(self, version_str: Optional[str]) -> Optional[int]:
        """Parse version string to number (e.g., 'v30' -> 30)."""
        if not version_str:
            return None
        
        match = re.search(r'v?(\d+)', version_str)
        if match:
            return int(match.group(1))
        return None
    
    def _get_subset_name(self, subset_code: str) -> str:
        """Get display name for subset code."""
        names = {
            'latin': 'Latin',
            'latin-ext': 'Latin Extended',
            'cyrillic': 'Cyrillic',
            'cyrillic-ext': 'Cyrillic Extended',
            'greek': 'Greek',
            'greek-ext': 'Greek Extended',
            'vietnamese': 'Vietnamese',
            'arabic': 'Arabic',
            'hebrew': 'Hebrew',
            'devanagari': 'Devanagari',
            'thai': 'Thai',
            'korean': 'Korean',
            'japanese': 'Japanese',
            'chinese-simplified': 'Chinese Simplified',
            'chinese-traditional': 'Chinese Traditional',
        }
        return names.get(subset_code, subset_code.replace('-', ' ').title())
    
    def _get_subset_group(self, subset_code: str) -> str:
        """Get group for subset code."""
        groups = {
            'latin': 'Latin',
            'latin-ext': 'Latin',
            'cyrillic': 'Cyrillic',
            'cyrillic-ext': 'Cyrillic',
            'greek': 'Greek',
            'greek-ext': 'Greek',
            'arabic': 'Middle Eastern',
            'hebrew': 'Middle Eastern',
            'vietnamese': 'Asian',
            'thai': 'Asian',
            'korean': 'Asian',
            'japanese': 'Asian',
            'chinese-simplified': 'Asian',
            'chinese-traditional': 'Asian',
            'devanagari': 'Asian',
        }
        return groups.get(subset_code, 'Other')
    
    def _get_axis_name(self, axis_tag: str) -> str:
        """Get display name for axis tag."""
        names = {
            'wght': 'Weight',
            'wdth': 'Width',
            'ital': 'Italic',
            'slnt': 'Slant',
            'opsz': 'Optical Size',
            'GRAD': 'Grade',
            'XTRA': 'X-Height Extra',
            'YOPQ': 'Y Opaque',
            'CASL': 'Casual',
            'CRSV': 'Cursive',
            'FILL': 'Fill',
            'MONO': 'Monospace',
        }
        return names.get(axis_tag, axis_tag)

