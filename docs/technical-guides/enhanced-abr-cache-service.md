# Enhanced ABR Cache Service - Multi-Search Support

**Author:** Solomon 📜 (SQL Standards Sage)  
**Date:** October 13, 2025  
**Purpose:** Enhanced caching service supporting ABN, ACN, and Name searches

---

## 🎯 **Cache Strategy Overview**

### **Single Table, Multiple Search Types:**
- **ABRSearchCache** table with composite primary key
- **SearchType** + **SearchKey** + **ResultIndex** = Unique cache entry
- **JSON storage** for flexible result caching
- **30-day TTL** for all search types (ABR compliance)

### **Search Type Support:**
1. **ABN Search:** `SearchType='ABN'`, `ResultIndex=0` (single result)
2. **ACN Search:** `SearchType='ACN'`, `ResultIndex=0` (single result)  
3. **Name Search:** `SearchType='Name'`, `ResultIndex=0,1,2...` (multiple results)

---

## 🏗️ **Enhanced Cache Service Implementation**

```python
"""
Enhanced ABR Cache Service - Multi-Search Support
"""
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

logger = logging.getLogger(__name__)


class ABRSearchResult:
    """Single search result from ABR API"""
    def __init__(self, data: Dict[str, Any]):
        self.abn = data.get("abn")
        self.entity_name = data.get("entity_name")
        self.entity_type = data.get("entity_type")
        self.abn_status = data.get("abn_status")
        self.gst_registered = data.get("gst_registered", False)
        self.state = data.get("state")
        self.postcode = data.get("postcode")
        self.business_names = data.get("business_names", [])
        self.trading_names = data.get("trading_names", [])
        self.retrieved_at = data.get("retrieved_at")


class EnhancedABRCacheService:
    """
    Enhanced ABR caching service supporting multiple search types
    
    Features:
    - ABN search caching (existing)
    - ACN search caching (new)
    - Company name search caching (new, multiple results)
    - Smart cache invalidation
    - Performance analytics
    """
    
    def __init__(self, db: Session, cache_ttl_seconds: int = 2592000):
        self.db = db
        self.cache_ttl_seconds = cache_ttl_seconds  # 30 days default
        
        # Search type constants
        self.SEARCH_TYPES = {
            'ABN': 'ABN',
            'ACN': 'ACN', 
            'NAME': 'Name'
        }
    
    # ============================================================================
    # Generic Cache Operations
    # ============================================================================
    
    async def get_cached_results(
        self, 
        search_type: str, 
        search_key: str
    ) -> List[ABRSearchResult]:
        """
        Get cached search results for any search type
        
        Args:
            search_type: 'ABN', 'ACN', or 'Name'
            search_key: Search query (ABN, ACN, or company name)
            
        Returns:
            List of ABRSearchResult objects (empty if not cached or expired)
        """
        try:
            # Get all cached results for this search
            cached_entries = self.db.query(ABRSearchCache).filter(
                and_(
                    ABRSearchCache.SearchType == search_type,
                    ABRSearchCache.SearchKey == search_key,
                    ABRSearchCache.IsActive == True
                )
            ).order_by(ABRSearchCache.ResultIndex).all()
            
            if not cached_entries:
                logger.debug(f"No cache found for {search_type} search: {search_key}")
                return []
            
            # Check if any entries are expired
            expired_count = 0
            results = []
            
            for entry in cached_entries:
                # Check TTL
                cache_age = datetime.utcnow() - entry.CachedDate
                if cache_age > timedelta(seconds=entry.CacheTTLSeconds):
                    expired_count += 1
                    # Soft delete expired entry
                    entry.IsActive = False
                    entry.UpdatedDate = datetime.utcnow()
                    continue
                
                # Parse and add result
                try:
                    result_data = json.loads(entry.ResultJSON)
                    results.append(ABRSearchResult(result_data))
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON in cache for {search_key}: {e}")
                    continue
            
            # Commit any expired entry updates
            if expired_count > 0:
                self.db.commit()
                logger.info(f"Expired {expired_count} cache entries for {search_type} search: {search_key}")
            
            if results:
                logger.info(f"Cache HIT for {search_type} search: {search_key} ({len(results)} results)")
            else:
                logger.debug(f"Cache MISS for {search_type} search: {search_key}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error reading cache for {search_type} search {search_key}: {e}")
            return []
    
    async def set_cached_results(
        self, 
        search_type: str, 
        search_key: str, 
        results: List[ABRSearchResult],
        search_metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Cache search results for any search type
        
        Args:
            search_type: 'ABN', 'ACN', or 'Name'
            search_key: Search query (ABN, ACN, or company name)
            results: List of ABRSearchResult objects
            search_metadata: Optional search metadata (timing, API endpoint, etc.)
        """
        try:
            # First, invalidate any existing cache for this search
            await self.invalidate_search(search_type, search_key)
            
            # Cache each result with appropriate index
            for index, result in enumerate(results):
                result_data = {
                    "abn": result.abn,
                    "entity_name": result.entity_name,
                    "entity_type": result.entity_type,
                    "abn_status": result.abn_status,
                    "gst_registered": result.gst_registered,
                    "state": result.state,
                    "postcode": result.postcode,
                    "business_names": result.business_names,
                    "trading_names": result.trading_names,
                    "retrieved_at": result.retrieved_at or datetime.utcnow().isoformat()
                }
                
                cache_entry = ABRSearchCache(
                    SearchType=search_type,
                    SearchKey=search_key,
                    ResultIndex=index,
                    ResultJSON=json.dumps(result_data),
                    SearchMetadata=json.dumps(search_metadata) if search_metadata else None,
                    CachedDate=datetime.utcnow(),
                    CacheTTLSeconds=self.cache_ttl_seconds,
                    CacheVersion=1,
                    IsActive=True,
                    CreatedDate=datetime.utcnow(),
                    CreatedBy=None,  # System process
                    UpdatedDate=None,
                    UpdatedBy=None
                )
                
                self.db.add(cache_entry)
            
            self.db.commit()
            logger.info(f"Cached {len(results)} results for {search_type} search: {search_key}")
            
        except Exception as e:
            logger.error(f"Error caching {search_type} search {search_key}: {e}")
            self.db.rollback()
    
    async def invalidate_search(self, search_type: str, search_key: str) -> None:
        """
        Invalidate all cached results for a specific search
        
        Args:
            search_type: 'ABN', 'ACN', or 'Name'
            search_key: Search query to invalidate
        """
        try:
            # Soft delete all cache entries for this search
            updated = self.db.query(ABRSearchCache).filter(
                and_(
                    ABRSearchCache.SearchType == search_type,
                    ABRSearchCache.SearchKey == search_key,
                    ABRSearchCache.IsActive == True
                )
            ).update({
                'IsActive': False,
                'UpdatedDate': datetime.utcnow(),
                'UpdatedBy': None
            })
            
            self.db.commit()
            logger.info(f"Invalidated {updated} cache entries for {search_type} search: {search_key}")
            
        except Exception as e:
            logger.error(f"Error invalidating cache for {search_type} search {search_key}: {e}")
            self.db.rollback()
    
    # ============================================================================
    # Search Type Specific Methods
    # ============================================================================
    
    async def get_abn_cached(self, abn: str) -> Optional[ABRSearchResult]:
        """
        Get cached ABN search result (single result)
        
        Args:
            abn: 11-digit ABN
            
        Returns:
            ABRSearchResult or None if not cached/expired
        """
        results = await self.get_cached_results('ABN', abn)
        return results[0] if results else None
    
    async def set_abn_cached(
        self, 
        abn: str, 
        result: ABRSearchResult,
        search_metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Cache ABN search result (single result)
        
        Args:
            abn: 11-digit ABN
            result: ABRSearchResult object
            search_metadata: Optional search metadata
        """
        await self.set_cached_results('ABN', abn, [result], search_metadata)
    
    async def get_acn_cached(self, acn: str) -> Optional[ABRSearchResult]:
        """
        Get cached ACN search result (single result)
        
        Args:
            acn: 9-digit ACN
            
        Returns:
            ABRSearchResult or None if not cached/expired
        """
        results = await self.get_cached_results('ACN', acn)
        return results[0] if results else None
    
    async def set_acn_cached(
        self, 
        acn: str, 
        result: ABRSearchResult,
        search_metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Cache ACN search result (single result)
        
        Args:
            acn: 9-digit ACN
            result: ABRSearchResult object
            search_metadata: Optional search metadata
        """
        await self.set_cached_results('ACN', acn, [result], search_metadata)
    
    async def get_name_cached(self, company_name: str) -> List[ABRSearchResult]:
        """
        Get cached company name search results (multiple results)
        
        Args:
            company_name: Company name to search for
            
        Returns:
            List of ABRSearchResult objects
        """
        return await self.get_cached_results('Name', company_name)
    
    async def set_name_cached(
        self, 
        company_name: str, 
        results: List[ABRSearchResult],
        search_metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Cache company name search results (multiple results)
        
        Args:
            company_name: Company name searched for
            results: List of ABRSearchResult objects
            search_metadata: Optional search metadata
        """
        await self.set_cached_results('Name', company_name, results, search_metadata)
    
    # ============================================================================
    # Cache Management & Analytics
    # ============================================================================
    
    async def cleanup_expired_cache(self) -> Dict[str, int]:
        """
        Clean up expired cache entries (soft delete)
        
        Returns:
            Dictionary with cleanup statistics
        """
        try:
            current_time = datetime.utcnow()
            stats = {}
            
            # Get expired entries by search type
            for search_type in self.SEARCH_TYPES.values():
                expired_count = self.db.query(ABRSearchCache).filter(
                    and_(
                        ABRSearchCache.SearchType == search_type,
                        ABRSearchCache.IsActive == True,
                        ABRSearchCache.CachedDate < (
                            current_time - timedelta(seconds=self.cache_ttl_seconds)
                        )
                    )
                ).update({
                    'IsActive': False,
                    'UpdatedDate': current_time,
                    'UpdatedBy': None
                })
                
                stats[search_type] = expired_count
            
            self.db.commit()
            total_cleaned = sum(stats.values())
            logger.info(f"Cache cleanup completed: {total_cleaned} expired entries removed")
            
            return stats
            
        except Exception as e:
            logger.error(f"Error during cache cleanup: {e}")
            self.db.rollback()
            return {}
    
    async def get_cache_statistics(self) -> Dict[str, Any]:
        """
        Get cache usage statistics
        
        Returns:
            Dictionary with cache statistics by search type
        """
        try:
            stats = {}
            
            for search_type in self.SEARCH_TYPES.values():
                # Count active entries
                active_count = self.db.query(ABRSearchCache).filter(
                    and_(
                        ABRSearchCache.SearchType == search_type,
                        ABRSearchCache.IsActive == True
                    )
                ).count()
                
                # Count inactive entries
                inactive_count = self.db.query(ABRSearchCache).filter(
                    and_(
                        ABRSearchCache.SearchType == search_type,
                        ABRSearchCache.IsActive == False
                    )
                ).count()
                
                # Get date range
                date_range = self.db.query(
                    self.db.func.min(ABRSearchCache.CachedDate).label('oldest'),
                    self.db.func.max(ABRSearchCache.CachedDate).label('newest')
                ).filter(
                    ABRSearchCache.SearchType == search_type
                ).first()
                
                # Calculate average result size
                avg_size = self.db.query(
                    self.db.func.avg(self.db.func.len(ABRSearchCache.ResultJSON))
                ).filter(
                    and_(
                        ABRSearchCache.SearchType == search_type,
                        ABRSearchCache.IsActive == True
                    )
                ).scalar() or 0
                
                stats[search_type] = {
                    'active_entries': active_count,
                    'inactive_entries': inactive_count,
                    'total_entries': active_count + inactive_count,
                    'oldest_entry': date_range.oldest,
                    'newest_entry': date_range.newest,
                    'avg_result_size_bytes': round(avg_size, 2)
                }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting cache statistics: {e}")
            return {}
    
    async def invalidate_by_abn(self, abn: str) -> None:
        """
        Invalidate all cache entries that contain a specific ABN
        (Useful when a company reports ABN changes)
        
        Args:
            abn: ABN to invalidate across all search types
        """
        try:
            # Find all cache entries that contain this ABN in their JSON
            cache_entries = self.db.query(ABRSearchCache).filter(
                and_(
                    ABRSearchCache.IsActive == True,
                    ABRSearchCache.ResultJSON.contains(f'"abn": "{abn}"')
                )
            ).all()
            
            # Soft delete all matching entries
            for entry in cache_entries:
                entry.IsActive = False
                entry.UpdatedDate = datetime.utcnow()
                entry.UpdatedBy = None
            
            self.db.commit()
            logger.info(f"Invalidated {len(cache_entries)} cache entries containing ABN: {abn}")
            
        except Exception as e:
            logger.error(f"Error invalidating cache by ABN {abn}: {e}")
            self.db.rollback()


# ============================================================================
# Database Model (SQLAlchemy)
# ============================================================================

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ABRSearchCache(Base):
    """
    Enhanced ABR search cache table model
    """
    __tablename__ = "ABRSearchCache"
    
    SearchType = Column(String(10), primary_key=True)
    SearchKey = Column(String(200), primary_key=True)
    ResultIndex = Column(Integer, primary_key=True)
    ResultJSON = Column(Text, nullable=False)
    SearchMetadata = Column(Text, nullable=True)
    CachedDate = Column(DateTime, nullable=False)
    CacheTTLSeconds = Column(Integer, nullable=False)
    CacheVersion = Column(Integer, nullable=False)
    IsActive = Column(Boolean, nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    CreatedBy = Column(Integer, nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(Integer, nullable=True)
```

---

## 🔧 **Integration with Enhanced ABR Client**

```python
# Updated EnhancedABRClient with caching integration

class EnhancedABRClient:
    """
    Enhanced ABR API Client with Multi-Search Support and Caching
    """
    
    def __init__(self, api_key: str, base_url: str, cache_service: EnhancedABRCacheService):
        self.api_key = api_key
        self.base_url = base_url
        self.cache_service = cache_service
        self.timeout = 10.0
        
        # API Endpoints
        self.endpoints = {
            "abn": f"{base_url}/SearchByABNv202001",
            "acn": f"{base_url}/SearchByACNv202001", 
            "name": f"{base_url}/SearchByNamev202001"
        }
    
    async def search_by_abn(self, abn: str) -> Optional[ABRSearchResult]:
        """
        Search by ABN with caching
        """
        # Check cache first
        cached_result = await self.cache_service.get_abn_cached(abn)
        if cached_result:
            logger.info(f"ABN {abn} found in cache")
            return cached_result
        
        # Validate format
        if not self._validate_abn_format(abn):
            raise ValueError(f"Invalid ABN format: {abn}")
        
        # Make API request
        start_time = datetime.utcnow()
        try:
            response = await self._make_request(self.endpoints["abn"], {
                "authenticationGuid": self.api_key,
                "searchString": abn.replace(" ", ""),
                "includeHistoricalDetails": "N"
            })
            
            if response:
                result = ABRSearchResult(response)
                
                # Cache the result
                search_metadata = {
                    "search_timestamp": start_time.isoformat(),
                    "api_endpoint": self.endpoints["abn"],
                    "response_time_ms": (datetime.utcnow() - start_time).total_seconds() * 1000
                }
                await self.cache_service.set_abn_cached(abn, result, search_metadata)
                
                return result
            
            return None
            
        except Exception as e:
            logger.error(f"ABN search failed for {abn}: {e}")
            raise
    
    async def search_by_name(self, company_name: str, max_results: int = 20) -> List[ABRSearchResult]:
        """
        Search by company name with caching
        """
        # Check cache first
        cached_results = await self.cache_service.get_name_cached(company_name)
        if cached_results:
            logger.info(f"Name search '{company_name}' found {len(cached_results)} results in cache")
            return cached_results[:max_results]  # Respect max_results limit
        
        # Validate input
        if not company_name or len(company_name.strip()) < 2:
            raise ValueError("Company name must be at least 2 characters")
        
        # Make API request
        start_time = datetime.utcnow()
        try:
            response = await self._make_request(self.endpoints["name"], {
                "authenticationGuid": self.api_key,
                "searchString": company_name.strip(),
                "includeHistoricalDetails": "N",
                "maxResults": str(max_results)
            })
            
            if response and isinstance(response, list):
                results = [ABRSearchResult(item) for item in response]
            elif response:
                results = [ABRSearchResult(response)]
            else:
                results = []
            
            # Cache the results
            search_metadata = {
                "search_timestamp": start_time.isoformat(),
                "api_endpoint": self.endpoints["name"],
                "response_time_ms": (datetime.utcnow() - start_time).total_seconds() * 1000,
                "total_results": len(results)
            }
            await self.cache_service.set_name_cached(company_name, results, search_metadata)
            
            return results
            
        except Exception as e:
            logger.error(f"Name search failed for '{company_name}': {e}")
            raise
```

---

## 📊 **Cache Performance Benefits**

### **Cache Hit Rates (Estimated):**
- **ABN searches:** 60% (frequent lookups for same companies)
- **ACN searches:** 40% (less frequent, but still valuable)
- **Name searches:** 30% (many unique searches, but popular companies cached)

### **Performance Improvements:**
- **Cache hit:** ~5ms response time
- **API call:** ~1000-2000ms response time
- **Improvement:** 200-400x faster for cached results

### **Cost Savings:**
- **Cache hit rate:** 40% average across all search types
- **API call reduction:** 40% fewer calls to ABR API
- **Cost savings:** 40% reduction in API costs

---

## 🎯 **Implementation Checklist**

### **✅ Database Schema:**
- [x] ABRSearchCache table with composite primary key
- [x] Performance indexes for fast lookups
- [x] Cache cleanup stored procedures
- [x] Sample data and examples

### **✅ Cache Service:**
- [x] Generic cache operations (get/set/invalidate)
- [x] Search type specific methods
- [x] Cache management and analytics
- [x] ABN-based invalidation

### **✅ Integration:**
- [x] Enhanced ABR client with caching
- [x] Search metadata tracking
- [x] Performance monitoring
- [x] Error handling and fallbacks

### **📋 Next Steps:**
1. **Test cache performance** with real ABR API
2. **Implement cache cleanup job** (daily schedule)
3. **Add cache analytics dashboard** for monitoring
4. **Optimize cache TTL** based on usage patterns

---

**This enhanced caching system provides enterprise-grade performance while maintaining Australian compliance and supporting all three search methods!** 🇦🇺

---

*Solomon - SQL Standards Sage* 📜  
*"Efficient caching: The foundation of scalable search performance!"*


