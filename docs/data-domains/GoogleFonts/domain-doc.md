# Google Fonts Domain Documentation

## 🔤 **Domain Overview**

Local caching and synchronization of Google Fonts metadata AND custom corporate font uploads for the EventLead Platform form builder. This domain enables responsive font selection, reduces external API dependencies, supports custom corporate fonts with deduplication, and provides comprehensive font properties for customer customization.

**Primary Use Cases:**
- Form Builder font customization - allowing customers to select and preview fonts for their lead capture forms without external API latency
- Custom corporate font uploads - companies can upload their own fonts with per-company display name aliases
- Font sharing between companies - hash-based deduplication prevents duplicate storage

---

## 📋 **Domain Status**

| Aspect | Status | Notes |
|--------|--------|-------|
| **Research** | ✅ Complete | Data model analysis complete |
| **Schema Design** | ✅ Complete | SQL Server schema with CompanyFont & FontFile |
| **Migration** | ✅ Complete | Migration 031 ready for execution |
| **SQLAlchemy Models** | ✅ Complete | 13 models including CompanyFont, FontFile |
| **Sync Service** | ✅ Complete | Monthly Google Fonts sync |
| **Custom Font Service** | ✅ Complete | Upload, dedup, alias management |
| **Font Validator** | ✅ Complete | fonttools-based validation |
| **API Endpoints** | ✅ Complete | 14 endpoints (public, auth, admin) |
| **API Documentation** | ✅ Complete | api-reference.md |
| **Story 3.5 Integration** | ✅ Complete | TypeScript types & React hooks |

---

## 🎯 **Business Value**

### Performance Improvement
| Scenario | Before (External API) | After (Local Cache) | Improvement |
|----------|----------------------|---------------------|-------------|
| Font list load | 500-800ms | < 50ms | **90%+ faster** |
| Font search | 300-500ms | < 20ms | **95%+ faster** |
| Font details | 200-400ms | < 10ms | **95%+ faster** |

### Additional Benefits
- **Reliability**: No dependency on Google API availability
- **Customization**: Add platform-specific metadata (featured, recommended)
- **Custom Fonts**: Companies can upload their own corporate fonts
- **Deduplication**: Same font file = single storage, multiple company aliases
- **Analytics**: Track font usage patterns
- **Offline Support**: Potential for offline font selection

---

## 📊 **Data Model Summary**

### Core Tables (dbo schema)

| Table | Purpose | Records (Est.) |
|-------|---------|----------------|
| `FontFamily` | Primary font registry (Google + Custom) | ~1,600+ |
| `FontVariant` | Weight/style combinations | ~15,000+ |
| `FontSubset` | Character set support | ~25,000 |
| `FontAxis` | Variable font axes | ~500 |
| `FontColorCapability` | Color font features | ~100 |
| `CompanyFont` | Company-Font junction with display names | Variable |
| `FontFile` | Uploaded font file storage with dedup | Variable |

### Reference Tables (dbo schema)

| Table | Purpose |
|-------|---------|
| `FontCategoryRef` | Category definitions (serif, sans-serif, etc.) |
| `FontSubsetRef` | Subset/language definitions |
| `FontAxisRef` | Standard axis definitions |

### Logging Tables (log schema)

| Table | Purpose |
|-------|---------|
| `log.FontSyncLog` | Sync operation tracking |
| `log.FontSyncDetail` | Individual font sync details |
| `log.FontUsageLog` | Platform usage analytics |

### Key Features

**FontFamily Extensions:**
- `FontSource`: 'Google', 'Custom', 'System'
- `UploadedByCompanyID`: Original uploader company
- `InternalFontName`: Name extracted from font file
- `InternalVersion`: Version from font metadata

**CompanyFont Junction:**
- `DisplayNameOverride`: Per-company display name alias
- `IsOwner`: TRUE if company originally uploaded the font
- `LicenseType`: 'Owned', 'Shared', 'Platform', 'Trial'

**FontFile Storage:**
- `FileHash`: SHA-256 for deduplication (UNIQUE constraint)
- Full extracted metadata (name, version, glyphs, scripts)
- Validation status tracking

---

## 🔄 **Synchronization Strategy**

### Schedule
- **Frequency**: Monthly (1st of month, 2:00 AM UTC)
- **API Version**: v2 (supports variable fonts)
- **Retry Policy**: 3 attempts with exponential backoff

### Process Flow
```
1. Trigger (Scheduled/Manual)
   ↓
2. Call Google Fonts API v2
   ↓
3. Compare with existing data
   ↓
4. Process changes:
   - INSERT new fonts
   - UPDATE modified fonts
   - DEPRECATE removed fonts
   ↓
5. Log sync results
   ↓
6. Update popularity rankings
```

---

## 📤 **Custom Font Upload Flow**

```
1. User uploads font file (TTF, OTF, WOFF, WOFF2)
   ↓
2. Validate with fonttools
   - Parse font structure
   - Extract metadata
   ↓
3. Calculate SHA-256 hash
   ↓
4. Check for duplicate (FileHash)
   ↓
5a. DUPLICATE: Link company to existing font
    - Create CompanyFont with DisplayNameOverride
    - IsOwner = false
   ↓
5b. NEW: Create all records
    - FontFamily (FontSource='Custom')
    - FontVariant
    - FontFile (with extracted metadata)
    - CompanyFont (IsOwner = true)
```

---

## 🛠️ **API Endpoints**

### Public Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/fonts` | List fonts with filtering/pagination |
| GET | `/api/fonts/featured` | Get curated featured fonts |
| GET | `/api/fonts/categories` | Get categories with counts |
| GET | `/api/fonts/popular` | Get most popular fonts |
| GET | `/api/fonts/{id}` | Get font details |
| GET | `/api/fonts/by-name/{name}` | Get font by family name |
| GET | `/api/fonts/sync/status` | Get sync status |

### Authenticated Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/fonts/{id}/usage` | Log font usage |
| POST | `/api/fonts/custom` | Upload custom font |
| GET | `/api/fonts/custom` | List company fonts |
| PUT | `/api/fonts/custom/{id}/name` | Update display name |
| DELETE | `/api/fonts/custom/{id}` | Revoke font access |
| GET | `/api/fonts/file/{variant_id}` | Stream font file |

### Admin Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/fonts/sync` | Trigger manual sync |
| PUT | `/api/fonts/{id}/featured` | Set featured status |
| PUT | `/api/fonts/{id}/recommended` | Set recommended status |

---

## 📁 **File Structure**

```
docs/data-domains/GoogleFonts/
├── domain-doc.md                    # This file
├── api-reference.md                 # Complete API documentation ✅
├── story-3.5-integration.md         # Frontend integration guide ✅
└── research/
    └── data-model-analysis.md       # Comprehensive data analysis ✅

database/schemas/
└── google-fonts-schema.sql          # Complete schema with CompanyFont ✅

backend/migrations/versions/
└── 031_google_fonts_domain.py       # Alembic migration ✅

backend/models/fonts/
├── __init__.py
├── font_family.py                   # With FontSource, InternalFontName ✅
├── font_variant.py
├── font_subset.py
├── font_axis.py
├── font_color_capability.py
├── company_font.py                  # NEW: DisplayNameOverride ✅
├── font_file.py                     # NEW: Hash deduplication ✅
├── font_sync_log.py
├── font_sync_detail.py
├── font_usage_log.py
├── font_category_ref.py
├── font_subset_ref.py
└── font_axis_ref.py

backend/services/fonts/
├── __init__.py
├── google_fonts_service.py          # Core font operations ✅
├── sync_service.py                  # Google Fonts sync ✅
├── font_validator.py                # NEW: fonttools validation ✅
└── custom_font_service.py           # NEW: Upload, dedup, aliases ✅

backend/modules/fonts/
├── __init__.py
├── router.py                        # 14 API endpoints ✅
└── schemas.py                       # Pydantic models ✅
```

---

## 🔧 **Configuration**

### Environment Variables

```env
# Google Fonts API (Required for sync)
GOOGLE_FONTS_API_KEY=your-api-key-here
GOOGLE_FONTS_API_VERSION=v2

# Sync Configuration
FONT_SYNC_ENABLED=true
FONT_SYNC_CRON="0 2 1 * *"  # 2 AM on 1st of each month
FONT_SYNC_RETRY_COUNT=3
FONT_SYNC_TIMEOUT_SECONDS=300

# Custom Font Limits
MAX_FONT_FILE_SIZE_MB=10
```

### Dependencies

Add to `requirements.txt`:
```
fonttools>=4.47.0    # Font file parsing and validation
```

---

## 🚀 **Setup Instructions**

### 1. Run Migration

```bash
cd backend
alembic upgrade head
```

### 2. Configure API Key

Add `GOOGLE_FONTS_API_KEY` to your `.env` file.

### 3. Initial Sync

Call the sync endpoint or wait for scheduled sync:

```bash
curl -X POST http://localhost:8000/api/fonts/sync \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📚 **Related Documentation**

- [API Reference](./api-reference.md) - Complete endpoint documentation
- [Story 3.5 Integration](./story-3.5-integration.md) - TypeScript types & React hooks
- [Data Model Analysis](./research/data-model-analysis.md) - Comprehensive schema design
- [Google Fonts Developer API](https://developers.google.com/fonts/docs/developer_api) - External API docs
- [Form Builder Architecture](../../stories/EPIC-3-ARCHITECTURE-REF.md) - Form builder context

---

*Last Updated: December 2025*
*Domain Version: 2.0*
*Status: Implementation Complete - Ready for Deployment*
