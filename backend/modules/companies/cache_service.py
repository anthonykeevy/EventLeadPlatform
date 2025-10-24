"""
ABR Search Cache Service

Provides caching functionality for ABR API search results to improve performance
and reduce API costs. Implements enterprise-grade caching with 30-day TTL.

Story 1.10: Enhanced ABR Search Implementation
AC-1.10.8: Enterprise-Grade Caching
AC-1.10.9: Cache Cleanup & Maintenance
AC-1.10.11: Success Rate Metrics
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, func, and_, desc

from models.cache.abr_search import ABRSearch
from common.logger import get_logger

logger = get_logger(__name__)


class CacheService:
    """
    ABR Search Cache Service
    
    Manages caching of ABR API search results with automatic expiry,
    analytics tracking, and cleanup functionality.
    
    Features:
    - 30-day TTL (compliance with ABR terms)
    - Hit count tracking for analytics
    - Automatic cache key normalization
    - Popular search tracking
    - Expired cache cleanup
    """
    
    def __init__(self, ttl_days: Optional[int] = None):
        """
        Initialize cache service
        
        Args:
            ttl_days: Time to live in days (default: 30 for ABR compliance)
        """
        self.ttl_days = ttl_days or int(os.getenv("ABR_CACHE_TTL_DAYS", "30"))
        
    def _normalize_search_key(self, search_type: str, search_value: str) -> str:
        """
        Normalize search key for consistent caching
        
        Args:
            search_type: Type of search ('ABN', 'ACN', 'Name')
            search_value: Raw search value
            
        Returns:
            Normalized search key
        """
        if search_type in ['ABN', 'ACN']:
            # Remove spaces and store digits only
            return ''.join(c for c in search_value if c.isdigit())
        else:  # Name search
            # Lowercase and trim whitespace
            return search_value.strip().lower()
    
    def _calculate_expiry_date(self) -> datetime:
        """Calculate cache expiry date (TTL from now)"""
        return datetime.utcnow() + timedelta(days=self.ttl_days)
    
    async def get_cached_search(
        self, 
        db: Session,
        search_type: str, 
        search_value: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get cached search results if available and not expired
        
        Args:
            db: Database session
            search_type: Type of search ('ABN', 'ACN', 'Name')
            search_value: Search value to look up
            
        Returns:
            List of cached results or None if not cached or expired
        """
        search_key = self._normalize_search_key(search_type, search_value)
        
        try:
            # Query for non-expired cache entries
            cached_entries = db.execute(
                select(ABRSearch)
                .where(
                    and_(
                        ABRSearch.SearchType == search_type,
                        ABRSearch.SearchValue == search_key,
                        ABRSearch.ExpiresAt > datetime.utcnow(),
                        ABRSearch.IsDeleted == False
                    )
                )
                .order_by(ABRSearch.ResultIndex)
            ).scalars().all()
            
            if not cached_entries:
                logger.debug(f"Cache miss: {search_type} search for '{search_value}'")
                return None
            
            # Update hit count and last hit timestamp for all entries
            for entry in cached_entries:
                entry.HitCount += 1  # type: ignore
                entry.LastHitAt = datetime.utcnow()  # type: ignore
            
            db.commit()
            
            # Parse and return results
            results = []
            for entry in cached_entries:
                try:
                    result = json.loads(entry.FullResponse)  # type: ignore
                    results.append(result)
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse cached result: {e}")
                    continue
            
            logger.info(
                f"Cache hit: {search_type} search for '{search_value}' "
                f"({len(results)} results, hit_count: {cached_entries[0].HitCount})"
            )
            
            return results if results else None
            
        except Exception as e:
            logger.error(f"Error retrieving cached search: {e}")
            db.rollback()
            return None
    
    async def cache_search_result(
        self,
        db: Session,
        search_type: str,
        search_value: str,
        results: List[Dict[str, Any]],
        user_id: Optional[int] = None,
        company_id: Optional[int] = None
    ) -> bool:
        """
        Cache search results with specified TTL
        
        Args:
            db: Database session
            search_type: Type of search ('ABN', 'ACN', 'Name')
            search_value: Search value that was searched
            results: List of search results to cache
            user_id: ID of user who performed search (optional)
            company_id: ID of company context (optional)
            
        Returns:
            True if caching successful, False otherwise
        """
        if not results:
            logger.debug(f"Skipping cache for empty results: {search_type} '{search_value}'")
            return False
        
        search_key = self._normalize_search_key(search_type, search_value)
        expires_at = self._calculate_expiry_date()
        
        try:
            # Delete any existing cache entries for this search
            db.execute(
                delete(ABRSearch).where(
                    and_(
                        ABRSearch.SearchType == search_type,
                        ABRSearch.SearchValue == search_key
                    )
                )
            )
            
            # Create new cache entries
            for index, result in enumerate(results):
                cache_entry = ABRSearch(
                    SearchType=search_type,
                    SearchValue=search_key,
                    ResultIndex=index,
                    ABN=result.get('abn'),
                    LegalEntityName=result.get('company_name'),
                    EntityType=result.get('entity_type'),
                    ABNStatus=result.get('status'),
                    GSTRegistered=result.get('gst_registered'),
                    FullResponse=json.dumps(result),
                    SearchDate=datetime.utcnow(),
                    ExpiresAt=expires_at,
                    HitCount=0,  # Will be incremented on cache hits
                    LastHitAt=None,
                    CreatedBy=user_id,
                    UserID=user_id,
                    CompanyID=company_id,
                    IsDeleted=False
                )
                
                db.add(cache_entry)
            
            db.commit()
            
            logger.info(
                f"Cached search results: {search_type} '{search_value}' "
                f"({len(results)} results, expires: {expires_at.strftime('%Y-%m-%d')})"
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error caching search results: {e}")
            db.rollback()
            return False
    
    async def get_cache_statistics(self, db: Session) -> Dict[str, Any]:
        """
        Get cache performance statistics
        
        Args:
            db: Database session
            
        Returns:
            Dictionary containing cache statistics
        """
        try:
            now = datetime.utcnow()
            
            # Total cached searches (unique search keys)
            total_searches = db.execute(
                select(func.count(func.distinct(
                    func.concat(ABRSearch.SearchType, ':', ABRSearch.SearchValue)
                )))
                .where(ABRSearch.IsDeleted == False)
            ).scalar() or 0
            
            # Total cache entries
            total_entries = db.execute(
                select(func.count(ABRSearch.SearchType))
                .where(ABRSearch.IsDeleted == False)
            ).scalar() or 0
            
            # Active (non-expired) entries
            active_entries = db.execute(
                select(func.count(ABRSearch.SearchType))
                .where(
                    and_(
                        ABRSearch.IsDeleted == False,
                        ABRSearch.ExpiresAt > now
                    )
                )
            ).scalar() or 0
            
            # Total hits
            total_hits = db.execute(
                select(func.sum(ABRSearch.HitCount))
                .where(ABRSearch.IsDeleted == False)
            ).scalar() or 0
            
            # Cache hit rate (hits per search)
            cache_hit_rate = (total_hits / max(total_searches, 1)) * 100
            
            # Popular searches (top 10 by hit count)
            popular_searches_query = db.execute(
                select(
                    ABRSearch.SearchType,
                    ABRSearch.SearchValue,
                    func.sum(ABRSearch.HitCount).label('total_hits'),
                    func.max(ABRSearch.LastHitAt).label('last_hit')
                )
                .where(
                    and_(
                        ABRSearch.IsDeleted == False,
                        ABRSearch.HitCount > 0
                    )
                )
                .group_by(ABRSearch.SearchType, ABRSearch.SearchValue)
                .order_by(desc('total_hits'))
                .limit(10)
            ).all()
            
            popular_searches = [
                {
                    "search_type": row.SearchType,
                    "search_key": row.SearchValue,
                    "hit_count": int(row.total_hits),
                    "last_hit": row.last_hit.isoformat() if row.last_hit else None
                }
                for row in popular_searches_query
            ]
            
            # Search type distribution
            search_type_stats = db.execute(
                select(
                    ABRSearch.SearchType,
                    func.count(func.distinct(ABRSearch.SearchValue)).label('unique_searches'),
                    func.sum(ABRSearch.HitCount).label('total_hits')
                )
                .where(ABRSearch.IsDeleted == False)
                .group_by(ABRSearch.SearchType)
            ).all()
            
            search_type_distribution = {
                row.SearchType: {
                    "unique_searches": int(row.unique_searches),
                    "total_hits": int(row.total_hits or 0)
                }
                for row in search_type_stats
            }
            
            # Estimated API cost savings (assuming 40% cache hit rate saves 40% of API costs)
            estimated_savings = min(cache_hit_rate, 40.0)  # Cap at 40% as per story target
            
            return {
                "total_cached_searches": int(total_searches),
                "total_cache_entries": int(total_entries),
                "active_cache_entries": int(active_entries),
                "expired_entries": int(total_entries - active_entries),
                "cache_hit_rate_percent": round(cache_hit_rate, 1),
                "total_cache_hits": int(total_hits),
                "average_hits_per_search": round(total_hits / max(total_searches, 1), 1),
                "popular_searches": popular_searches,
                "search_type_distribution": search_type_distribution,
                "estimated_api_cost_savings_percent": round(estimated_savings, 1),
                "cache_ttl_days": self.ttl_days,
                "generated_at": now.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating cache statistics: {e}")
            return {
                "error": "Failed to generate cache statistics",
                "generated_at": datetime.utcnow().isoformat()
            }
    
    async def cleanup_expired_cache(self, db: Session) -> Dict[str, Any]:
        """
        Clean up expired cache entries
        
        Args:
            db: Database session
            
        Returns:
            Dictionary with cleanup statistics
        """
        try:
            now = datetime.utcnow()
            
            # Find expired entries
            expired_count = db.execute(
                select(func.count(ABRSearch.SearchType))
                .where(
                    and_(
                        ABRSearch.ExpiresAt <= now,
                        ABRSearch.IsDeleted == False
                    )
                )
            ).scalar() or 0
            
            if expired_count == 0:
                logger.info("Cache cleanup: No expired entries found")
                return {
                    "expired_entries_found": 0,
                    "entries_deleted": 0,
                    "cleanup_date": now.isoformat()
                }
            
            # Soft delete expired entries (set IsDeleted = True)
            result = db.execute(
                ABRSearch.__table__.update()
                .where(
                    and_(
                        ABRSearch.ExpiresAt <= now,
                        ABRSearch.IsDeleted == False
                    )
                )
                .values(
                    IsDeleted=True,
                    UpdatedDate=now
                )
            )
            
            db.commit()
            
            deleted_count = result.rowcount
            
            logger.info(
                f"Cache cleanup completed: {deleted_count} expired entries deleted "
                f"(found {expired_count} expired entries)"
            )
            
            return {
                "expired_entries_found": int(expired_count),
                "entries_deleted": int(deleted_count),
                "cleanup_date": now.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error during cache cleanup: {e}")
            db.rollback()
            return {
                "error": "Cache cleanup failed",
                "expired_entries_found": 0,
                "entries_deleted": 0,
                "cleanup_date": datetime.utcnow().isoformat()
            }
    
    async def invalidate_cache(
        self,
        db: Session,
        search_type: Optional[str] = None,
        search_value: Optional[str] = None
    ) -> int:
        """
        Invalidate cache entries (mark as deleted)
        
        Args:
            db: Database session
            search_type: Specific search type to invalidate (optional)
            search_value: Specific search value to invalidate (optional)
            
        Returns:
            Number of cache entries invalidated
        """
        try:
            conditions = [ABRSearch.IsDeleted == False]
            
            if search_type:
                conditions.append(ABRSearch.SearchType == search_type)
                
            if search_value:
                search_key = self._normalize_search_key(search_type or 'Name', search_value)
                conditions.append(ABRSearch.SearchValue == search_key)
            
            result = db.execute(
                ABRSearch.__table__.update()
                .where(and_(*conditions))
                .values(
                    IsDeleted=True,
                    UpdatedDate=datetime.utcnow()
                )
            )
            
            db.commit()
            
            invalidated_count = result.rowcount
            
            logger.info(
                f"Cache invalidation: {invalidated_count} entries invalidated "
                f"(type: {search_type or 'ALL'}, value: {search_value or 'ALL'})"
            )
            
            return invalidated_count
            
        except Exception as e:
            logger.error(f"Error invalidating cache: {e}")
            db.rollback()
            return 0


# Module-level cache service instance (singleton pattern)
_cache_service: Optional[CacheService] = None


def get_cache_service() -> CacheService:
    """
    Get cache service instance (singleton)
    
    Returns:
        CacheService instance
    """
    global _cache_service
    
    if _cache_service is None:
        _cache_service = CacheService()
    
    return _cache_service
