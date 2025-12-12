"""
Google Fonts Service
Core service for managing local Google Fonts cache
"""
import os
import httpx
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, and_, case

from common.logger import get_logger
from models.fonts import (
    FontFamily,
    FontVariant,
    FontSubset,
    FontAxis,
    FontColorCapability,
    FontCategoryRef,
    FontUsageLog,
)

logger = get_logger(__name__)


class GoogleFontsService:
    """
    Service for managing local Google Fonts cache.
    
    Provides methods for:
    - Searching and filtering fonts
    - Getting font details
    - Logging font usage
    - Managing featured/recommended fonts
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.api_key = os.getenv("GOOGLE_FONTS_API_KEY")
        self.api_version = os.getenv("GOOGLE_FONTS_API_VERSION", "v1")
    
    async def search_fonts(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        subset: Optional[str] = None,
        is_variable: Optional[bool] = None,
        has_italic: Optional[bool] = None,
        min_weight: Optional[int] = None,
        max_weight: Optional[int] = None,
        is_featured: Optional[bool] = None,
        is_recommended: Optional[bool] = None,
        sort_by: str = "popularity",
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[FontFamily], int]:
        """
        Search fonts with filtering, sorting, and pagination.
        
        Args:
            query: Search term for font name
            category: Filter by category (serif, sans-serif, etc.)
            subset: Filter by required subset support
            is_variable: Filter for variable fonts only
            has_italic: Filter for fonts with italic
            min_weight: Filter by minimum weight available
            max_weight: Filter by maximum weight available
            is_featured: Featured fonts only
            is_recommended: Recommended fonts only
            sort_by: Sort order (popularity, name, date)
            page: Page number (1-based)
            page_size: Items per page
            
        Returns:
            Tuple of (fonts list, total count)
        """
        try:
            # Build base query
            base_query = self.db.query(FontFamily).filter(
                FontFamily.IsDeleted == False,
                FontFamily.IsActive == True,
                FontFamily.SyncStatus == 'Active'
            )
            
            # Apply filters
            if query:
                search_term = query.lower()
                base_query = base_query.filter(
                    FontFamily.FamilyNameNormalized.like(f'%{search_term}%')
                )
            
            if category:
                base_query = base_query.filter(FontFamily.Category == category)
            
            if subset:
                # Map subset to column
                subset_filters = {
                    'latin': FontFamily.SupportsLatin == True,
                    'cyrillic': FontFamily.SupportsCyrillic == True,
                    'greek': FontFamily.SupportsGreek == True,
                    'arabic': FontFamily.SupportsArabic == True,
                    'hebrew': FontFamily.SupportsHebrew == True,
                    'asian': FontFamily.SupportsAsian == True,
                }
                if subset in subset_filters:
                    base_query = base_query.filter(subset_filters[subset])
            
            if is_variable is not None:
                base_query = base_query.filter(FontFamily.IsVariableFont == is_variable)
            
            if has_italic is not None:
                base_query = base_query.filter(FontFamily.HasItalic == has_italic)
            
            if min_weight is not None:
                base_query = base_query.filter(FontFamily.MinWeight <= min_weight)
            
            if max_weight is not None:
                base_query = base_query.filter(FontFamily.MaxWeight >= max_weight)
            
            if is_featured is not None:
                base_query = base_query.filter(FontFamily.IsFeatured == is_featured)
            
            if is_recommended is not None:
                base_query = base_query.filter(FontFamily.IsRecommended == is_recommended)
            
            # Get total count
            total_count = base_query.count()
            
            # Apply sorting
            # Note: Using case() for SQL Server compatibility (NULLS LAST not supported)
            if sort_by == 'popularity':
                base_query = base_query.order_by(
                    case((FontFamily.PopularityRank.is_(None), 1), else_=0),
                    FontFamily.PopularityRank.asc(),
                    FontFamily.FamilyName.asc()
                )
            elif sort_by == 'name':
                base_query = base_query.order_by(FontFamily.FamilyName.asc())
            elif sort_by == 'date':
                base_query = base_query.order_by(FontFamily.LastModifiedDate.desc())
            elif sort_by == 'featured':
                base_query = base_query.order_by(
                    FontFamily.IsFeatured.desc(),
                    case((FontFamily.DisplayOrder.is_(None), 1), else_=0),
                    FontFamily.DisplayOrder.asc(),
                    FontFamily.FamilyName.asc()
                )
            else:
                base_query = base_query.order_by(FontFamily.FamilyName.asc())
            
            # Apply pagination
            offset = (page - 1) * page_size
            fonts = base_query.offset(offset).limit(page_size).all()
            
            logger.info(f"Font search: found {total_count} fonts, returning page {page}")
            
            return fonts, total_count
            
        except Exception as e:
            logger.error(f"Error searching fonts: {str(e)}", exc_info=True)
            raise
    
    async def get_font_by_id(self, font_family_id: int) -> Optional[FontFamily]:
        """
        Get complete font details by ID.
        
        Includes variants, subsets, axes, and color capabilities.
        Note: Relationships are loaded automatically via selectin lazy loading.
        """
        try:
            font = self.db.query(FontFamily).filter(
                FontFamily.FontFamilyID == font_family_id,
                FontFamily.IsDeleted == False
            ).first()
            
            return font
            
        except Exception as e:
            logger.error(f"Error getting font by ID: {str(e)}", exc_info=True)
            raise
    
    async def get_font_by_name(self, family_name: str) -> Optional[FontFamily]:
        """Get font by family name."""
        try:
            font = self.db.query(FontFamily).filter(
                FontFamily.FamilyNameNormalized == family_name.lower(),
                FontFamily.IsDeleted == False
            ).first()
            
            return font
            
        except Exception as e:
            logger.error(f"Error getting font by name: {str(e)}", exc_info=True)
            raise
    
    async def get_popular_fonts(
        self,
        limit: int = 20,
        category: Optional[str] = None
    ) -> List[FontFamily]:
        """Get most popular fonts."""
        try:
            query = self.db.query(FontFamily).filter(
                FontFamily.IsDeleted == False,
                FontFamily.IsActive == True,
                FontFamily.SyncStatus == 'Active'
            )
            
            if category:
                query = query.filter(FontFamily.Category == category)
            
            # SQL Server compatible NULLS LAST
            fonts = query.order_by(
                case((FontFamily.PopularityRank.is_(None), 1), else_=0),
                FontFamily.PopularityRank.asc()
            ).limit(limit).all()
            
            return fonts
            
        except Exception as e:
            logger.error(f"Error getting popular fonts: {str(e)}", exc_info=True)
            raise
    
    async def get_featured_fonts(self) -> List[FontFamily]:
        """Get curated featured fonts."""
        try:
            fonts = self.db.query(FontFamily).filter(
                FontFamily.IsDeleted == False,
                FontFamily.IsActive == True,
                FontFamily.IsFeatured == True
            ).order_by(
                # SQL Server compatible NULLS LAST
                case((FontFamily.DisplayOrder.is_(None), 1), else_=0),
                FontFamily.DisplayOrder.asc(),
                FontFamily.FamilyName.asc()
            ).all()
            
            return fonts
            
        except Exception as e:
            logger.error(f"Error getting featured fonts: {str(e)}", exc_info=True)
            raise
    
    async def get_font_categories(self) -> List[Dict[str, Any]]:
        """Get all font categories with counts."""
        try:
            # Get categories from reference table
            categories = self.db.query(FontCategoryRef).filter(
                FontCategoryRef.IsActive == True
            ).order_by(FontCategoryRef.DisplayOrder).all()
            
            # Get counts for each category
            category_counts = self.db.query(
                FontFamily.Category,
                func.count(FontFamily.FontFamilyID).label('count')
            ).filter(
                FontFamily.IsDeleted == False,
                FontFamily.IsActive == True,
                FontFamily.SyncStatus == 'Active'
            ).group_by(FontFamily.Category).all()
            
            count_map = {c.Category: c.count for c in category_counts}
            
            result = []
            for cat in categories:
                result.append({
                    'category_code': cat.CategoryCode,
                    'category_name': cat.CategoryName,
                    'description': cat.Description,
                    'icon_class': cat.IconClass,
                    'display_order': cat.DisplayOrder,
                    'font_count': count_map.get(cat.CategoryCode, 0)
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting font categories: {str(e)}", exc_info=True)
            raise
    
    async def log_font_usage(
        self,
        font_family_id: int,
        context: str,
        action: str,
        user_id: Optional[int] = None,
        company_id: Optional[int] = None,
        font_variant_id: Optional[int] = None,
        context_entity_type: Optional[str] = None,
        context_entity_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> None:
        """Log font usage for analytics."""
        try:
            usage_log = FontUsageLog(
                FontFamilyID=font_family_id,
                FontVariantID=font_variant_id,
                UsageContext=context,
                ActionType=action,
                UserID=user_id,
                CompanyID=company_id,
                ContextEntityType=context_entity_type,
                ContextEntityID=context_entity_id,
                IPAddress=ip_address,
                UserAgent=user_agent
            )
            
            self.db.add(usage_log)
            
            # Increment usage count on font family
            font = self.db.query(FontFamily).filter(
                FontFamily.FontFamilyID == font_family_id
            ).first()
            
            if font:
                font.UsageCount = (font.UsageCount or 0) + 1
                font.UpdatedDate = datetime.utcnow()
            
            self.db.commit()
            
            logger.debug(f"Logged font usage: font={font_family_id}, context={context}, action={action}")
            
        except Exception as e:
            logger.error(f"Error logging font usage: {str(e)}", exc_info=True)
            self.db.rollback()
            raise
    
    async def get_sync_status(self) -> Dict[str, Any]:
        """Get last sync status and metrics."""
        try:
            from models.fonts import FontSyncLog
            
            # Get last sync
            last_sync = self.db.query(FontSyncLog).order_by(
                FontSyncLog.SyncStartTime.desc()
            ).first()
            
            # Get font counts
            total_fonts = self.db.query(func.count(FontFamily.FontFamilyID)).filter(
                FontFamily.IsDeleted == False,
                FontFamily.IsActive == True
            ).scalar()
            
            active_fonts = self.db.query(func.count(FontFamily.FontFamilyID)).filter(
                FontFamily.IsDeleted == False,
                FontFamily.IsActive == True,
                FontFamily.SyncStatus == 'Active'
            ).scalar()
            
            variable_fonts = self.db.query(func.count(FontFamily.FontFamilyID)).filter(
                FontFamily.IsDeleted == False,
                FontFamily.IsActive == True,
                FontFamily.IsVariableFont == True
            ).scalar()
            
            return {
                'last_sync': {
                    'sync_id': last_sync.FontSyncLogID if last_sync else None,
                    'start_time': last_sync.SyncStartTime.isoformat() if last_sync else None,
                    'end_time': last_sync.SyncEndTime.isoformat() if last_sync and last_sync.SyncEndTime else None,
                    'status': last_sync.SyncStatus if last_sync else None,
                    'fonts_added': last_sync.FontsAdded if last_sync else 0,
                    'fonts_updated': last_sync.FontsUpdated if last_sync else 0,
                    'trigger_type': last_sync.TriggerType if last_sync else None,
                } if last_sync else None,
                'font_counts': {
                    'total': total_fonts,
                    'active': active_fonts,
                    'variable': variable_fonts,
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting sync status: {str(e)}", exc_info=True)
            raise
    
    async def set_font_featured(
        self,
        font_family_id: int,
        is_featured: bool,
        display_order: Optional[int] = None
    ) -> FontFamily:
        """Set font as featured or unfeatured."""
        try:
            font = self.db.query(FontFamily).filter(
                FontFamily.FontFamilyID == font_family_id
            ).first()
            
            if not font:
                raise ValueError(f"Font not found: {font_family_id}")
            
            font.IsFeatured = is_featured
            if display_order is not None:
                font.DisplayOrder = display_order
            font.UpdatedDate = datetime.utcnow()
            font.UpdatedBy = 'ADMIN'
            
            self.db.commit()
            
            logger.info(f"Set font {font_family_id} featured={is_featured}")
            
            return font
            
        except Exception as e:
            logger.error(f"Error setting font featured: {str(e)}", exc_info=True)
            self.db.rollback()
            raise
    
    async def set_font_recommended(
        self,
        font_family_id: int,
        is_recommended: bool
    ) -> FontFamily:
        """Set font as recommended or not recommended."""
        try:
            font = self.db.query(FontFamily).filter(
                FontFamily.FontFamilyID == font_family_id
            ).first()
            
            if not font:
                raise ValueError(f"Font not found: {font_family_id}")
            
            font.IsRecommended = is_recommended
            font.UpdatedDate = datetime.utcnow()
            font.UpdatedBy = 'ADMIN'
            
            self.db.commit()
            
            logger.info(f"Set font {font_family_id} recommended={is_recommended}")
            
            return font
            
        except Exception as e:
            logger.error(f"Error setting font recommended: {str(e)}", exc_info=True)
            self.db.rollback()
            raise

