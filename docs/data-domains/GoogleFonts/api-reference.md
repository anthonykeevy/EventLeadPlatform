# Google Fonts Domain - API Reference

Complete API reference for the Google Fonts caching and custom font upload endpoints.

## Base URL

```
/api/fonts
```

## Authentication

- **Public endpoints**: No authentication required (font listing, search)
- **Authenticated endpoints**: Require valid JWT token
- **Admin endpoints**: Require `system_admin` or `company_admin` role

---

## Environment Configuration

Add the following to your `.env` file:

```env
# Google Fonts API Configuration
# Get your API key from: https://console.cloud.google.com/apis/credentials
# Enable "Web Fonts Developer API" in your Google Cloud project
GOOGLE_FONTS_API_KEY=your_api_key_here
GOOGLE_FONTS_API_VERSION=v2
```

---

## Endpoints

### Public Endpoints

#### List Fonts

```http
GET /api/fonts
```

Get paginated list of fonts with filtering and sorting.

**Query Parameters:**

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `query` | string | Search term for font name | - |
| `category` | string | Filter by category (serif, sans-serif, display, handwriting, monospace) | - |
| `subset` | string | Filter by required subset (latin, cyrillic, arabic, etc.) | - |
| `is_variable` | boolean | Variable fonts only | - |
| `has_italic` | boolean | Fonts with italic variants | - |
| `is_featured` | boolean | Featured fonts only | - |
| `sort_by` | string | Sort order: popularity, name, date, featured | popularity |
| `page` | integer | Page number (1-based) | 1 |
| `page_size` | integer | Items per page (1-100) | 20 |

**Response:**

```json
{
  "fonts": [
    {
      "font_family_id": 1,
      "google_font_id": "Roboto",
      "family_name": "Roboto",
      "category": "sans-serif",
      "version": "v30",
      "is_variable_font": true,
      "min_weight": 100,
      "max_weight": 900,
      "has_italic": true,
      "total_variants": 12,
      "total_subsets": 7,
      "menu_file_url": "https://fonts.gstatic.com/...",
      "popularity_rank": 1,
      "usage_count": 150,
      "is_featured": true,
      "is_recommended": true,
      "variant_list": "100,300,400,500,700,900,100italic,..."
    }
  ],
  "total": 1500,
  "page": 1,
  "page_size": 20,
  "total_pages": 75
}
```

---

#### Get Featured Fonts

```http
GET /api/fonts/featured
```

Get curated featured fonts for quick selection.

**Response:** Array of `FontFamilySummary` objects

---

#### Get Font Categories

```http
GET /api/fonts/categories
```

Get all font categories with font counts.

**Response:**

```json
[
  {
    "category_code": "sans-serif",
    "category_name": "Sans Serif",
    "description": "Modern, clean fonts without decorative strokes.",
    "icon_class": "icon-font-sans",
    "display_order": 2,
    "font_count": 450
  }
]
```

---

#### Get Popular Fonts

```http
GET /api/fonts/popular?limit=20&category=sans-serif
```

Get most popular fonts.

**Query Parameters:**

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `limit` | integer | Number of fonts (1-50) | 20 |
| `category` | string | Filter by category | - |

---

#### Get Font Details

```http
GET /api/fonts/{font_family_id}
```

Get complete font family details including variants, subsets, and axes.

**Response:**

```json
{
  "font_family_id": 1,
  "google_font_id": "Roboto",
  "family_name": "Roboto",
  "category": "sans-serif",
  "sub_category": null,
  "version": "v30",
  "version_number": 30,
  "last_modified_date": "2024-01-15",
  "menu_file_url": "https://fonts.gstatic.com/...",
  "specimen_url": null,
  "is_variable_font": true,
  "has_color_capabilities": false,
  "min_weight": 100,
  "max_weight": 900,
  "has_italic": true,
  "has_regular": true,
  "supports_latin": true,
  "supports_cyrillic": true,
  "supports_greek": true,
  "supports_arabic": false,
  "supports_hebrew": false,
  "supports_asian": false,
  "total_subsets": 7,
  "total_variants": 12,
  "popularity_rank": 1,
  "usage_count": 150,
  "is_recommended": true,
  "is_featured": true,
  "license_type": "Open Font License",
  "designer": "Christian Robertson",
  "foundry": "Google",
  "last_sync_date": "2025-12-01T12:00:00Z",
  "variants": [
    {
      "font_variant_id": 1,
      "variant_name": "regular",
      "weight": 400,
      "weight_name": "Regular",
      "is_italic": false,
      "ttf_file_url": "https://fonts.gstatic.com/...",
      "display_order": 0,
      "is_default": true
    }
  ],
  "subsets": [
    {
      "font_subset_id": 1,
      "subset_code": "latin",
      "subset_name": "Latin",
      "subset_group": "Latin",
      "is_extended": false
    }
  ],
  "axes": [
    {
      "font_axis_id": 1,
      "axis_tag": "wght",
      "axis_name": "Weight",
      "min_value": 100,
      "max_value": 900,
      "default_value": 400,
      "is_standard": true,
      "css_property": "font-weight"
    }
  ]
}
```

---

#### Get Font by Name

```http
GET /api/fonts/by-name/{family_name}
```

Get font by family name (URL-encoded).

---

### Authenticated Endpoints

#### Log Font Usage

```http
POST /api/fonts/{font_family_id}/usage
Authorization: Bearer {token}
```

Log font usage for analytics.

**Request Body:**

```json
{
  "context": "FormBuilder",
  "action": "Applied",
  "font_variant_id": 1,
  "context_entity_type": "Form",
  "context_entity_id": 123
}
```

**Valid `context` values:** FormBuilder, TemplateCreation, Preview, Export, Settings

**Valid `action` values:** Selected, Applied, Previewed, Removed, Downloaded

---

### Custom Font Endpoints

#### Upload Custom Font

```http
POST /api/fonts/custom
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

Upload a custom corporate font with validation and deduplication.

**Form Data:**

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `file` | file | Font file (TTF, OTF, WOFF, WOFF2) | Yes |
| `display_name` | string | Custom display name | No |
| `category` | string | Font category | No (default: sans-serif) |

**Features:**
- Validates font file structure using fonttools
- Extracts metadata (name, version, glyphs, scripts)
- Hash-based deduplication (same file = link to existing)
- Per-company display name aliases

**Response (new font):**

```json
{
  "status": "created",
  "is_duplicate": false,
  "font_family_id": 1234,
  "font_variant_id": 5678,
  "font_file_id": 9012,
  "company_font_id": 3456,
  "display_name": "MyBrandFont",
  "message": "Font uploaded successfully."
}
```

**Response (duplicate font - linked):**

```json
{
  "status": "linked",
  "is_duplicate": true,
  "font_family_id": 1234,
  "company_font_id": 7890,
  "display_name": "OurCompanyFont",
  "message": "Font already exists. Company linked with custom display name."
}
```

---

#### List Company Fonts

```http
GET /api/fonts/custom?include_google_fonts=true
Authorization: Bearer {token}
```

Get all fonts accessible by the current company with effective display names.

**Query Parameters:**

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `include_google_fonts` | boolean | Include Google Fonts | true |

**Response:**

```json
{
  "fonts": [
    {
      "font_family_id": 1234,
      "display_name": "OurBrandFont",
      "internal_name": "OpenSans-Regular",
      "original_name": "Open Sans",
      "font_source": "Custom",
      "category": "sans-serif",
      "is_variable_font": false,
      "min_weight": 400,
      "max_weight": 400,
      "has_italic": false,
      "total_variants": 1,
      "is_owner": true,
      "is_shared": false,
      "license_type": "Owned",
      "license_expiry_date": null,
      "company_font_id": 5678
    }
  ],
  "custom_font_count": 5,
  "google_font_count": 1500,
  "total": 1505
}
```

---

#### Update Display Name

```http
PUT /api/fonts/custom/{company_font_id}/name
Authorization: Bearer {token}
```

Update a company's display name for a font.

**Request Body:**

```json
{
  "display_name": "NewBrandFontName"
}
```

---

#### Revoke Font Access

```http
DELETE /api/fonts/custom/{company_font_id}
Authorization: Bearer {token}
```

Revoke a company's access to a custom font.

---

#### Stream Font File

```http
GET /api/fonts/file/{font_variant_id}
Authorization: Bearer {token}
```

Stream font file for preview or download.

Returns the font file with appropriate content-type headers and 1-year cache.

---

### Admin Endpoints

#### Trigger Font Sync

```http
POST /api/fonts/sync
Authorization: Bearer {token}
```

Manually trigger font synchronization with Google Fonts API.

**Required Role:** `system_admin` or `company_admin`

**Response:**

```json
{
  "success": true,
  "sync_id": 123,
  "total_fonts_in_api": 1500,
  "fonts_added": 10,
  "fonts_updated": 25,
  "fonts_deprecated": 0,
  "fonts_unchanged": 1465,
  "variants_processed": 3500,
  "subsets_processed": 8000,
  "axes_processed": 200,
  "duration_seconds": 45.2,
  "api_response_time_ms": 1500
}
```

---

#### Get Sync Status

```http
GET /api/fonts/sync/status
```

Get last sync status and font counts.

**Response:**

```json
{
  "last_sync": {
    "sync_id": 123,
    "sync_start_time": "2025-12-01T12:00:00Z",
    "sync_end_time": "2025-12-01T12:00:45Z",
    "status": "Success",
    "fonts_added": 10,
    "fonts_updated": 25
  },
  "font_counts": {
    "total": 1500,
    "active": 1480,
    "deprecated": 20,
    "by_category": {
      "serif": 350,
      "sans-serif": 450,
      "display": 400,
      "handwriting": 200,
      "monospace": 100
    }
  }
}
```

---

#### Set Font Featured

```http
PUT /api/fonts/{font_family_id}/featured
Authorization: Bearer {token}
```

Set font as featured or unfeatured.

**Required Role:** `system_admin` or `company_admin`

**Request Body:**

```json
{
  "is_featured": true,
  "display_order": 1
}
```

---

#### Set Font Recommended

```http
PUT /api/fonts/{font_family_id}/recommended
Authorization: Bearer {token}
```

Set font as recommended or not recommended.

**Required Role:** `system_admin` or `company_admin`

**Request Body:**

```json
{
  "is_recommended": true
}
```

---

## Error Responses

All endpoints return standard error responses:

```json
{
  "detail": "Error message here"
}
```

**Common HTTP Status Codes:**

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters or font file |
| 401 | Unauthorized - Missing or invalid token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Font not found |
| 413 | Payload Too Large - Font file > 10MB |
| 500 | Internal Server Error |

---

## Data Types

### FontSource

| Value | Description |
|-------|-------------|
| `Google` | Font from Google Fonts API |
| `Custom` | Custom uploaded font |
| `System` | System/platform font |

### Category

| Value | Description |
|-------|-------------|
| `serif` | Traditional fonts with serifs |
| `sans-serif` | Modern fonts without serifs |
| `display` | Decorative fonts for headlines |
| `handwriting` | Script/handwritten fonts |
| `monospace` | Fixed-width fonts |

### LicenseType

| Value | Description |
|-------|-------------|
| `Owned` | Company owns/uploaded the font |
| `Shared` | Font shared from another company |
| `Platform` | Platform-provided (Google Fonts) |
| `Trial` | Trial/temporary license |

