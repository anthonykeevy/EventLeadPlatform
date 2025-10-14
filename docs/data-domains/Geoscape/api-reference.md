# GeoScape API Reference

## Overview

This document provides comprehensive API reference for the GeoScape address validation and geocoding services. The API provides standardized endpoints for Australian address validation, search, and coordinate retrieval.

## Base URL

```
Production: https://jobtrackerdb-backend-au.azurewebsites.net
Development: http://localhost:8000
```

## Authentication

### API Key Authentication

All endpoints use simple API key authentication via the `Authorization` header:

```http
Authorization: {GEOSCAPE_API_KEY}
```

**Note**: No "Bearer" prefix required - use the API key directly.

### Rate Limits

- **Search Endpoints**: 100 requests per minute
- **Validation Endpoints**: 50 requests per minute
- **Coordinates Endpoints**: 30 requests per minute

### Error Responses

All endpoints return consistent error responses:

```json
{
  "error": "error_type",
  "message": "User-friendly error message",
  "details": {
    "technical_details": "for_developers_only"
  }
}
```

## Endpoints

### 1. Address Search (Autocomplete)

**Endpoint:** `GET /api/address/search`

**Description:** Provides address suggestions for autocomplete functionality.

**Query Parameters:**
- `q` (required): Address search query (min 3 characters)
- `country` (optional): Country code (default: "AU")
- `limit` (optional): Maximum suggestions (1-50, default: 10)

**Example Request:**
```http
GET /api/address/search?q=4 Milburn&country=AU&limit=10
```

**Example Response:**
```json
{
  "suggestions": [
    {
      "address": "4 MILBURN CCT, BOOLAROO NSW 2284",
      "id": "GNSW2284001",
      "data": {
        "streetNumber": "4",
        "streetName": "MILBURN",
        "streetType": "CCT",
        "suburb": "BOOLAROO",
        "state": "NSW",
        "postcode": "2284",
        "latitude": null,
        "longitude": null,
        "propertyType": null,
        "landArea": null,
        "floorArea": null
      },
      "confidence": 0.9
    }
  ],
  "total_count": 1,
  "query": "4 Milburn",
  "country": "AU"
}
```

**Error Codes:**
- `400`: Invalid query parameter (too short, invalid country)
- `500`: Internal server error
- `503`: Service temporarily unavailable

### 2. Address Validation

**Endpoint:** `POST /api/address/validate`

**Description:** Validates and geocodes a complete address.

**Request Body:**
```json
{
  "address": "4 Milburn Place, St Ives Chase NSW 2075",
  "property_id": "GNSW2075190",
  "country": "AU"
}
```

**Request Schema:**
```typescript
interface AddressValidationRequest {
  address: string;           // Full address string (required)
  property_id?: string;      // Geoscape property ID (optional)
  country: string;           // Country code (default: "AU")
}
```

**Example Response:**
```json
{
  "validated": true,
  "address": {
    "streetNumber": "4",
    "streetName": "Milburn",
    "streetType": "Place",
    "suburb": "St Ives Chase",
    "state": "NSW",
    "postcode": "2075",
    "country": "Australia",
    "latitude": -33.70131425995992,
    "longitude": 151.16600576829697,
    "formattedAddress": "4 MILBURN PLACE, ST IVES CHASE NSW 2075"
  },
  "metadata": {
    "propertyType": "Residential",
    "landArea": 650.0,
    "floorArea": 180.0,
    "demographics": {
      "population": 15000,
      "median_age": 35,
      "median_income": 85000
    },
    "validationDate": "2025-01-21T10:30:00Z",
    "validationSource": "geoscape"
  },
  "confidence_score": 0.98,
  "property_id": "GNSW2075190"
}
```

**Response Schema:**
```typescript
interface AddressValidationResponse {
  validated: boolean;        // Validation success
  address: {                 // Standardized address components
    streetNumber?: string;
    streetName: string;
    streetType?: string;
    suburb: string;
    state: string;
    postcode: string;
    country: string;
    latitude?: number;
    longitude?: number;
    formattedAddress: string;
  };
  metadata: {               // Additional property data
    propertyType?: string;
    landArea?: number;
    floorArea?: number;
    demographics?: object;
    validationDate: string;
    validationSource: string;
  };
  confidence_score: number; // 0.0 to 1.0
  property_id?: string;     // Geoscape property identifier
}
```

**Error Codes:**
- `400`: Invalid request body
- `422`: Validation error (invalid address format)
- `500`: Internal server error
- `503`: Service temporarily unavailable

### 3. Address Coordinates

**Endpoint:** `POST /api/address/coordinates`

**Description:** Retrieves precise coordinates for a given address.

**Request Body:**
```json
{
  "address": "4 Milburn Place, St Ives Chase NSW 2075",
  "property_id": "GNSW2075190",
  "country": "AU"
}
```

**Request Schema:**
```typescript
interface AddressCoordinatesRequest {
  address: string;           // Full address string (required)
  property_id?: string;      // Geoscape property ID (optional)
  country: string;           // Country code (default: "AU")
}
```

**Example Response:**
```json
{
  "success": true,
  "latitude": -33.70131425995992,
  "longitude": 151.16600576829697,
  "address": {
    "streetNumber": "4",
    "streetName": "Milburn",
    "streetType": "Place",
    "suburb": "St Ives Chase",
    "state": "NSW",
    "postcode": "2075",
    "latitude": -33.70131425995992,
    "longitude": 151.16600576829697
  },
  "property_id": "GNSW2075190",
  "confidence_score": 0.9
}
```

**Response Schema:**
```typescript
interface AddressCoordinatesResponse {
  success: boolean;          // Operation success
  latitude?: number;         // Latitude (15 decimal precision)
  longitude?: number;        // Longitude (15 decimal precision)
  address?: object;          // Address details
  property_id?: string;      // Geoscape property identifier
  confidence_score?: number; // 0.0 to 1.0
  error?: string;           // Error message if failed
}
```

**Error Codes:**
- `400`: Invalid request body
- `404`: Address not found
- `500`: Internal server error
- `503`: Service temporarily unavailable

### 4. Health Check

**Endpoint:** `GET /api/address/health`

**Description:** Returns the health status of address validation services.

**Example Response:**
```json
{
  "status": "healthy",
  "services": {
    "geoscape": {
      "configured": true,
      "base_url": "https://api.psma.com.au/v1"
    },
    "smarty_streets": {
      "configured": false,
      "base_url": "https://us-street.api.smartystreets.com/street-address"
    }
  },
  "timestamp": "2025-01-21T10:30:00Z"
}
```

## Data Models

### Address Components

```typescript
interface AddressComponents {
  streetNumber?: string;     // Street number (e.g., "4")
  streetName: string;        // Street name (e.g., "Milburn")
  streetType?: string;       // Street type (e.g., "Place", "Street")
  unitNumber?: string;       // Unit number (e.g., "2A")
  unitType?: string;         // Unit type (e.g., "Unit", "Apartment")
  suburb: string;           // Suburb/City (e.g., "St Ives Chase")
  state: string;            // State/Territory (e.g., "NSW")
  postcode: string;         // Postcode (e.g., "2075")
  country: string;          // Country (e.g., "Australia")
  latitude?: number;        // Latitude coordinate
  longitude?: number;       // Longitude coordinate
}
```

### Property Details

```typescript
interface PropertyDetails {
  property_id: string;      // Geoscape property identifier
  property_type?: string;   // Property type (e.g., "Residential")
  land_area?: number;       // Land area in square meters
  floor_area?: number;      // Floor area in square meters
  latitude?: number;        // Property latitude
  longitude?: number;       // Property longitude
  demographics?: object;    // Demographic data
  market_data?: object;     // Market information
  last_updated?: string;    // Last update timestamp
}
```

### Validation Metadata

```typescript
interface ValidationMetadata {
  propertyType?: string;    // Property type
  landArea?: number;        // Land area (sqm)
  floorArea?: number;       // Floor area (sqm)
  demographics?: {          // Demographic information
    population?: number;
    median_age?: number;
    median_income?: number;
  };
  validationDate: string;   // ISO timestamp
  validationSource: string; // Validation provider
}
```

## Error Codes

### HTTP Status Codes

| Code | Description | Example |
|------|-------------|---------|
| 200 | Success | Valid response data |
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Missing/invalid API key |
| 404 | Not Found | Address not found |
| 422 | Validation Error | Invalid address format |
| 429 | Rate Limited | Too many requests |
| 500 | Internal Error | Server error |
| 503 | Service Unavailable | API temporarily down |

### Error Types

```typescript
interface APIError {
  error: "validation_error" | "rate_limit" | "service_unavailable" | "invalid_request" | "internal_error";
  message: string;
  details?: {
    field?: string;
    value?: any;
    constraint?: string;
    retry_after?: number;
  };
}
```

### Common Error Messages

| Error Type | Message | Resolution |
|------------|---------|------------|
| `validation_error` | "Invalid address format" | Check address format |
| `rate_limit` | "Rate limit exceeded" | Wait and retry |
| `service_unavailable` | "Address validation service is temporarily unavailable" | Use manual entry |
| `invalid_request` | "Missing required parameter" | Check request body |
| `internal_error` | "Internal server error" | Contact support |

## Best Practices

### 1. Request Optimization

**Use Property IDs for Precision:**
```json
{
  "address": "4 Milburn Place, St Ives Chase NSW 2075",
  "property_id": "GNSW2075190"
}
```

**Implement Debouncing for Search:**
```typescript
const debouncedSearch = debounce(async (query: string) => {
  if (query.length >= 3) {
    return await searchAddresses(query);
  }
}, 300);
```

### 2. Error Handling

**Graceful Degradation:**
```typescript
try {
  const validation = await validateAddress(address);
  if (validation.validated) {
    // Use validated address
  } else {
    // Allow manual entry
  }
} catch (error) {
  // Fallback to manual entry
  console.warn('Address validation failed:', error);
}
```

**Retry Logic:**
```typescript
const validateWithRetry = async (address: string, retries = 3) => {
  for (let i = 0; i < retries; i++) {
    try {
      return await validateAddress(address);
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
};
```

### 3. Performance Optimization

**Cache Validation Results:**
```typescript
const validationCache = new Map();

const getCachedValidation = async (address: string) => {
  const cacheKey = address.toLowerCase().trim();
  
  if (validationCache.has(cacheKey)) {
    return validationCache.get(cacheKey);
  }
  
  const validation = await validateAddress(address);
  validationCache.set(cacheKey, validation);
  return validation;
};
```

**Batch Processing:**
```typescript
const validateAddressesBatch = async (addresses: string[]) => {
  const results = [];
  
  for (const address of addresses) {
    try {
      const validation = await validateAddress(address);
      results.push({ address, validation });
    } catch (error) {
      results.push({ address, error: error.message });
    }
    
    // Rate limiting delay
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  return results;
};
```

## SDK Integration

### JavaScript/TypeScript

**Installation:**
```bash
npm install @jobtracker/address-api
```

**Basic Usage:**
```typescript
import { AddressAPI } from '@jobtracker/address-api';

const addressAPI = new AddressAPI({
  baseURL: 'https://jobtrackerdb-backend-au.azurewebsites.net',
  apiKey: 'your-api-key'
});

// Search addresses
const suggestions = await addressAPI.search('4 Milburn');

// Validate address
const validation = await addressAPI.validate('4 Milburn Place, St Ives Chase NSW 2075');

// Get coordinates
const coordinates = await addressAPI.getCoordinates('4 Milburn Place, St Ives Chase NSW 2075');
```

### Python

**Installation:**
```bash
pip install jobtracker-address-api
```

**Basic Usage:**
```python
from jobtracker_address_api import AddressAPI

address_api = AddressAPI(
    base_url='https://jobtrackerdb-backend-au.azurewebsites.net',
    api_key='your-api-key'
)

# Search addresses
suggestions = await address_api.search('4 Milburn')

# Validate address
validation = await address_api.validate('4 Milburn Place, St Ives Chase NSW 2075')

# Get coordinates
coordinates = await address_api.get_coordinates('4 Milburn Place, St Ives Chase NSW 2075')
```

## Monitoring & Analytics

### Usage Tracking

Every API call is automatically logged with the following metrics:

```typescript
interface UsageMetrics {
  api_provider: string;     // 'geoscape', 'smarty_streets'
  endpoint: string;         // '/address/search', '/address/validate'
  request_type: string;     // 'autocomplete', 'validate', 'geocode'
  call_count: number;       // Number of API calls
  credit_cost: number;      // Cost in credits
  response_time: number;    // Response time in milliseconds
  response_status: string;  // 'success', 'error', 'timeout'
  billing_period: string;   // 'YYYY-MM' format
  is_billable: boolean;     // Whether call is billable
}
```

### Key Performance Indicators

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| Response Time | < 2s | > 5s |
| Success Rate | > 95% | < 90% |
| Error Rate | < 5% | > 10% |
| Availability | > 99.9% | < 99% |

### Monitoring Queries

**Recent API Usage:**
```sql
SELECT 
  APIProvider,
  APIEndpoint,
  COUNT(*) as call_count,
  AVG(ResponseTime) as avg_response_time,
  SUM(CreditCost) as total_cost
FROM APIUsageTracking 
WHERE CreatedAt >= DATEADD(day, -1, GETDATE())
GROUP BY APIProvider, APIEndpoint
ORDER BY call_count DESC;
```

**Error Analysis:**
```sql
SELECT 
  APIProvider,
  APIEndpoint,
  ResponseStatus,
  ErrorMessage,
  COUNT(*) as error_count
FROM APIUsageTracking 
WHERE ResponseStatus = 'error'
  AND CreatedAt >= DATEADD(day, -7, GETDATE())
GROUP BY APIProvider, APIEndpoint, ResponseStatus, ErrorMessage
ORDER BY error_count DESC;
```

## Support Information

### Documentation
- **API Documentation**: Available at `/docs` endpoint
- **Domain Documentation**: `project-knowledge/domains/geoscape/domain-doc.md`
- **Integration Guide**: `project-knowledge/domains/geoscape/integration-guide.md`

### Contact
- **Technical Support**: backend-team@jobtracker.com
- **API Issues**: api-support@jobtracker.com
- **Billing Questions**: billing@jobtracker.com

### Status Page
- **Service Status**: https://status.jobtracker.com
- **API Health**: `/api/address/health` endpoint
- **Incident History**: Available on status page

---

*Last Updated: 2025-01-21*
*API Version: 1.0*
*Documentation Version: 1.0*
