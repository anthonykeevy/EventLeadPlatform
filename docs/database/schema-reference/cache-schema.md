# `cache` Schema - External API Cache

**Schema Purpose:** Cache for external API results (safe to delete/rebuild)  
**Table Count:** 1  
**Retention:** 30-90 days, then delete  
**Backup Priority:** LOW (can be rebuilt from source APIs)  
**Write Volume:** Medium

---

## Schema Overview

The `cache` schema stores results from external API calls to improve performance and reduce costs. Unlike other schemas, cache data is **NOT source of truth** and can be safely deleted or truncated.

**Key Characteristics:**
- **Ephemeral:** Safe to delete (can be rebuilt from source APIs)
- **Performance optimization:** Reduces latency and external API costs
- **TTL-based expiration:** Rows auto-expire after configurable period (30-90 days)
- **No audit trail:** Cache updates don't need audit logging
- **Relaxed constraints:** Fewer foreign keys (cache is independent)

---

## Table Overview

| # | Table | Purpose | Cache Duration | API Cost Savings |
|---|-------|---------|----------------|------------------|
| 1 | `ABRSearch` | ABR (Australian Business Register) API results | 90 days | ~$0.10 per search avoided |

**Future Cache Tables (Not in Epic 1):**
- `Geocoding` - Address geocoding results (Google Maps API)
- `EmailValidation` - Email validation API results (ZeroBounce, Hunter.io)
- `CreditCardValidation` - Card BIN lookup results (Stripe)

---

## 1. `cache.ABRSearch` - ABR API Results Cache

**Purpose:** Cache Australian Business Register (ABR) API search results for company validation

**Background:**
- ABR API provides company details by ABN, ACN, or Name
- API response time: 500-2000ms (external service)
- API cost: Potentially rate-limited or paid tiers
- Company details rarely change (cache for 90 days is safe)

**Primary Key:** Composite `(SearchType, SearchValue)`

**Key Columns:**
- `SearchType` (NVARCHAR(20)) - Type of search: 'ABN', 'ACN', 'Name'
- `SearchValue` (NVARCHAR(255)) - Search term (ABN number, ACN number, or company name)
- `ABN` (NVARCHAR(11)) - Australian Business Number (result)
- `ACN` (NVARCHAR(9)) - Australian Company Number (result, NULL for non-companies)
- `LegalEntityName` (NVARCHAR(255)) - Official registered name
- `BusinessNames` (NVARCHAR(MAX)) - JSON array of trading names
- `EntityType` (NVARCHAR(100)) - Type of entity (e.g., 'Australian Private Company', 'Sole Trader')
- `ABNStatus` (NVARCHAR(50)) - Status ('Active', 'Cancelled')
- `GSTRegistered` (BIT) - Is entity GST registered?
- `FullResponse` (NVARCHAR(MAX)) - Full JSON response from ABR API (for future reference)
- `SearchDate` (DATETIME2) - When this search was performed (for TTL expiration)
- `ExpiresAt` (DATETIME2) - When cache entry expires (SearchDate + 90 days)
- `IsDeleted` (BIT, default 0) - Soft delete flag

**Unique Constraints:**
- `PK_ABRSearch` (composite): `(SearchType, SearchValue)` - One cache entry per search

**Indexes:**
- `IX_ABRSearch_ABN` (lookup by ABN)
- `IX_ABRSearch_ExpiresAt` (cleanup expired entries)
- `IX_ABRSearch_SearchDate` (analytics on search frequency)

**Query Patterns:**

**Check Cache Before API Call:**
```python
# Service layer: Check cache first
async def search_company_by_abn(abn: str) -> CompanyDetails:
    # Check cache
    cached = db.query(ABRSearch).filter(
        ABRSearch.search_type == 'ABN',
        ABRSearch.search_value == abn,
        ABRSearch.expires_at > datetime.utcnow(),
        ABRSearch.is_deleted == False
    ).first()
    
    if cached:
        # Cache hit! Return cached data
        return CompanyDetails.from_cache(cached)
    
    # Cache miss - call ABR API
    abr_response = await call_abr_api(abn)
    
    # Store in cache
    cache_entry = ABRSearch(
        search_type='ABN',
        search_value=abn,
        abn=abr_response.abn,
        legal_entity_name=abr_response.entity_name,
        # ... other fields
        full_response=json.dumps(abr_response),
        search_date=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(days=90)
    )
    db.add(cache_entry)
    db.commit()
    
    return CompanyDetails.from_abr_response(abr_response)
```

**Cleanup Expired Cache:**
```sql
-- Delete expired cache entries (scheduled job)
DELETE FROM cache.ABRSearch 
WHERE ExpiresAt < GETUTCDATE();
```

**Cache Statistics:**
```sql
-- Cache hit rate (last 7 days)
SELECT 
    SearchType,
    COUNT(*) as TotalSearches,
    SUM(CASE WHEN SearchDate >= DATEADD(DAY, -7, GETUTCDATE()) THEN 1 ELSE 0 END) as RecentSearches,
    AVG(DATEDIFF(DAY, SearchDate, GETUTCDATE())) as AvgAgeInDays
FROM cache.ABRSearch
WHERE IsDeleted = 0
GROUP BY SearchType;
```

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: cache.ABRSearch)

---

## Cache Design Patterns

### **1. Composite Primary Key (Multi-Search Support)**

**Reason:** Support multiple search types (ABN, ACN, Name) in same table

```sql
-- Composite PK allows same value to be searched different ways
(SearchType='ABN', SearchValue='12345678901')   -- Search by ABN
(SearchType='ACN', SearchValue='123456789')     -- Search by ACN
(SearchType='Name', SearchValue='Acme Corp')    -- Search by Name
```

**Alternative (Rejected):** Separate tables per search type
- ❌ More tables to manage
- ❌ Duplicate data (ABN search and ACN search may return same company)

---

### **2. Full JSON Response Storage**

**Purpose:** Store complete API response for future reference

```json
{
  "Abn": "12345678901",
  "AbnStatus": "Active",
  "EntityName": "ACME PTY LTD",
  "EntityType": {
    "EntityTypeCode": "PRV",
    "EntityDescription": "Australian Private Company"
  },
  "Gst": {
    "EffectiveFrom": "2020-01-01",
    "EffectiveTo": "0001-01-01"
  },
  "BusinessName": [
    { "OrganisationName": "Acme Corp" },
    { "OrganisationName": "Acme Industries" }
  ],
  "MainBusinessPhysicalAddress": {...}
}
```

**Benefits:**
- Future-proof (can extract new fields without re-calling API)
- Audit trail (see exactly what ABR returned)
- Debugging (compare current data vs original response)

---

### **3. TTL-Based Expiration**

**Pattern:** Each cache entry has `ExpiresAt` timestamp

```python
# Insert with expiration
expires_at = datetime.utcnow() + timedelta(days=90)  # 90-day TTL

# Query ignores expired entries
WHERE expires_at > datetime.utcnow()

# Scheduled job cleans up
DELETE WHERE expires_at < datetime.utcnow()
```

**Why 90 days?**
- Company details rarely change
- Balance between freshness and cost savings
- Configurable per cache type (email validation: 30 days, geocoding: 365 days)

---

### **4. Soft Delete (Not Hard Delete)**

**Reason:** May need to analyze cache history

```sql
-- Soft delete (preserve for analytics)
UPDATE cache.ABRSearch 
SET IsDeleted = 1 
WHERE ABN = '12345678901';

-- Queries ignore soft-deleted
WHERE IsDeleted = 0
```

---

## Cache vs Database Tables

**When to use Cache:**
- ✅ Data comes from external API (ABR, Google Maps, email validation)
- ✅ Data is expensive to fetch (slow, costs money, rate-limited)
- ✅ Data rarely changes (safe to cache for days/weeks)
- ✅ Safe to delete and rebuild (not source of truth)

**When to use Regular Table:**
- ❌ Data is source of truth (user accounts, companies, forms)
- ❌ Data changes frequently (user profile, form submissions)
- ❌ Data must be permanent (audit trail, compliance)
- ❌ Data has business logic (foreign keys, triggers)

---

## Performance Considerations

### **Read Performance**

**Cache Hit Scenario:**
```
User searches ABN → Check cache (5ms) → Return cached data
Total: 5ms (vs 500-2000ms API call)
```

**Cache Miss Scenario:**
```
User searches ABN → Check cache (5ms) → Call ABR API (500-2000ms) → Store in cache (5ms) → Return
Total: 510-2010ms (subsequent searches: 5ms)
```

**Cache Hit Rate:**
- Target: 70-80% (7-8 out of 10 searches hit cache)
- Measured: Track `SearchDate` frequency per ABN

### **Write Performance**

- Write volume: MEDIUM (only cache misses write)
- Write pattern: INSERT only (no UPDATEs)
- Index strategy: Minimal (only essential indexes)

### **Storage Growth**

**Estimate:**
- 100 companies × 3 search types (ABN, ACN, Name) = 300 cache entries
- 1KB per entry (including JSON) = 300 KB
- **Conclusion:** Negligible storage cost

---

## Security & Privacy

### **No PII in Cache**

**Good:** Company details are public information (ABR is public registry)
- ABN, company name, entity type = PUBLIC
- Safe to cache without privacy concerns

**Bad Example (DON'T DO THIS):**
```python
# ❌ DON'T cache user-specific searches
cache.ABRSearch(
    search_value=abn,
    searched_by_user_id=user_id,  # ❌ Links cache to user (privacy issue)
    user_email=user_email          # ❌ PII in cache
)
```

**Correct:**
```python
# ✅ Cache is anonymous (no user tracking)
cache.ABRSearch(
    search_value=abn,
    # No user_id, no email = anonymous cache
)
```

---

## Monitoring & Alerting

### **Cache Health Metrics**

1. **Cache Hit Rate:**
   ```sql
   SELECT 
       SearchType,
       COUNT(DISTINCT SearchValue) as UniqueSearches,
       COUNT(*) as TotalSearches,
       AVG(CASE WHEN SearchDate >= DATEADD(DAY, -1, GETUTCDATE()) THEN 1 ELSE 0 END) as RecentActivity
   FROM cache.ABRSearch
   GROUP BY SearchType;
   ```

2. **Cache Age Distribution:**
   ```sql
   SELECT 
       CASE 
           WHEN DATEDIFF(DAY, SearchDate, GETUTCDATE()) < 7 THEN '0-7 days'
           WHEN DATEDIFF(DAY, SearchDate, GETUTCDATE()) < 30 THEN '7-30 days'
           WHEN DATEDIFF(DAY, SearchDate, GETUTCDATE()) < 90 THEN '30-90 days'
           ELSE '90+ days'
       END as CacheAge,
       COUNT(*) as EntryCount
   FROM cache.ABRSearch
   WHERE IsDeleted = 0
   GROUP BY 
       CASE 
           WHEN DATEDIFF(DAY, SearchDate, GETUTCDATE()) < 7 THEN '0-7 days'
           WHEN DATEDIFF(DAY, SearchDate, GETUTCDATE()) < 30 THEN '7-30 days'
           WHEN DATEDIFF(DAY, SearchDate, GETUTCDATE()) < 90 THEN '30-90 days'
           ELSE '90+ days'
       END;
   ```

3. **ABR API Call Frequency:**
   ```sql
   -- Track API calls (cache misses)
   SELECT 
       CAST(SearchDate AS DATE) as Date,
       COUNT(*) as APICalls
   FROM cache.ABRSearch
   WHERE SearchDate >= DATEADD(DAY, -30, GETUTCDATE())
   GROUP BY CAST(SearchDate AS DATE)
   ORDER BY Date DESC;
   ```

### **Alerts**

- Cache hit rate < 50% → May need longer TTL
- ABR API calls > 100/hour → May need rate limiting
- Cache size > 10,000 entries → May need cleanup

---

## Future Enhancements

### **Additional Cache Tables (Post-MVP)**

**`cache.Geocoding` - Address geocoding results:**
```sql
CREATE TABLE [cache].[Geocoding] (
    GeocodingID BIGINT IDENTITY(1,1) PRIMARY KEY,
    Address NVARCHAR(500) NOT NULL,
    Latitude DECIMAL(10, 8) NOT NULL,
    Longitude DECIMAL(11, 8) NOT NULL,
    FormattedAddress NVARCHAR(500) NOT NULL,
    FullResponse NVARCHAR(MAX),  -- JSON from Google Maps API
    SearchDate DATETIME2 NOT NULL,
    ExpiresAt DATETIME2 NOT NULL,
    CONSTRAINT UQ_Geocoding_Address UNIQUE (Address)
);
```

**`cache.EmailValidation` - Email validation results:**
```sql
CREATE TABLE [cache].[EmailValidation] (
    EmailValidationID BIGINT IDENTITY(1,1) PRIMARY KEY,
    Email NVARCHAR(255) NOT NULL,
    IsValid BIT NOT NULL,
    IsCatchAll BIT NOT NULL,
    IsDisposable BIT NOT NULL,
    Score INT NOT NULL,  -- 0-100 quality score
    FullResponse NVARCHAR(MAX),
    SearchDate DATETIME2 NOT NULL,
    ExpiresAt DATETIME2 NOT NULL,
    CONSTRAINT UQ_EmailValidation_Email UNIQUE (Email)
);
```

---

## Related Documentation

**Architecture:**
- `docs/solution-architecture.md` - Database Architecture section
- `docs/architecture/decisions/ADR-001-database-schema-organization.md`
- `docs/data-domains/company-validation-implementation.md` - ABR integration

**Database:**
- `docs/database/REBUILD-PLAN-SUMMARY.md`
- `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` - Full SQL definitions

**External APIs:**
- ABR API Documentation: https://abr.business.gov.au/json/
- Geoscape API: https://geoscape.com.au/

---

**Winston** 🏗️  
*"Cache is a performance optimization. Treat it like temporary scaffolding."*

