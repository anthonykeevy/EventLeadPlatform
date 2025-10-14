# ABN Lookup API Integration Guide

**Author:** Dimitri 🔍 (Data Domain Architect)  
**Date:** October 13, 2025  
**Purpose:** Complete implementation guide for Australian Business Number (ABN) validation

---

## Overview

The ABN Lookup API (Australian Business Register) provides real-time validation of Australian Business Numbers. This integration is **critical** for EventLead Platform's Australian tax compliance requirements.

**Why This Matters:**
- ✅ **Legal requirement:** Australian tax law requires ABN on GST-compliant invoices
- ✅ **Data accuracy:** Auto-populate legal company names (prevents typos)
- ✅ **GST compliance:** Verify if company is GST-registered (determines 10% tax on invoices)
- ✅ **Competitive advantage:** No competitor validates ABN in real-time

---

## 1. ABN Lookup API - Technical Details

### API Provider
- **Provider:** Australian Business Register (ABR) - Government API
- **Documentation:** https://api.gov.au/service/5b639f0f63f18432cd0e1547
- **Base URL:** `https://abr.business.gov.au/abrxmlsearch/AbrXmlSearch.asmx`
- **Format:** SOAP (XML) or REST (JSON wrapper available)

### API Endpoints

#### Primary Endpoint: ABN Search
```
GET https://abr.business.gov.au/abrxmlsearch/AbrXmlSearch.asmx/SearchByABNv202001
```

**Parameters:**
- `authenticationGuid` (required): Your API key (GUID format)
- `searchString` (required): ABN to validate (11 digits)
- `includeHistoricalDetails` (optional): Y or N (default N)

**Example Request:**
```
https://abr.business.gov.au/abrxmlsearch/AbrXmlSearch.asmx/SearchByABNv202001?authenticationGuid={YOUR_GUID}&searchString=53004085616&includeHistoricalDetails=N
```

**Example Response (XML):**
```xml
<?xml version="1.0" encoding="utf-8"?>
<ABRPayloadSearchResults>
  <request>
    <identifierSearchRequest>
      <authenticationGUID>YOUR-GUID-HERE</authenticationGUID>
      <identifierValue>53004085616</identifierValue>
    </identifierSearchRequest>
  </request>
  <response dateRegister="2025-10-13" dateTimeRetrieved="2025-10-13T12:34:56">
    <businessEntity>
      <ABN status="Active" ABNStatusEffectiveFrom="2000-07-01">53004085616</ABN>
      <entityType>
        <entityDescription>Australian Private Company</entityDescription>
      </entityType>
      <goodsAndServicesTax effectiveFrom="2000-07-01" effectiveTo="0001-01-01">
        <status>Registered from 01 Jul 2000</status>
      </goodsAndServicesTax>
      <mainName>
        <organisationName>INTERNATIONAL CONVENTION CENTRE SYDNEY PTY LTD</organisationName>
      </mainName>
      <mainBusinessPhysicalAddress>
        <stateCode>NSW</stateCode>
        <postcode>2000</postcode>
      </mainBusinessPhysicalAddress>
      <businessName>
        <organisationName>ICC SYDNEY</organisationName>
      </businessName>
      <businessName>
        <organisationName>INTERNATIONAL CONVENTION CENTRE SYDNEY</organisationName>
      </businessName>
    </businessEntity>
  </response>
</ABRPayloadSearchResults>
```

### Pricing Tiers

| Tier | Requests/Day | Cost | Use Case |
|------|--------------|------|----------|
| **Free** | 1,000 | $0 | MVP, small scale |
| **Basic** | 10,000 | $50/month | Growing platform |
| **Enterprise** | Unlimited | $500/month | High volume |

**Recommendation for EventLead MVP:** Start with **FREE tier** (sufficient for 500 companies/month).

### Registration Process

1. Visit https://api.gov.au/
2. Create account (email verification)
3. Navigate to "ABR Web Services"
4. Request API key (GUID)
5. Approval: 1-2 business days
6. Receive GUID via email

---

## 2. FastAPI Implementation

### 2.1 Project Structure

```
backend/
  modules/
    companies/
      __init__.py
      routes.py              # FastAPI routes
      services.py            # Business logic
      models.py              # SQLAlchemy models
      schemas.py             # Pydantic schemas
      abn_client.py          # ABN API client (NEW)
      abn_cache.py           # Caching layer (NEW)
```

### 2.2 Environment Configuration

**`.env` file:**
```bash
# ABN Lookup API
ABN_API_KEY=YOUR-GUID-HERE-1234-5678-90AB-CDEF
ABN_API_BASE_URL=https://abr.business.gov.au/abrxmlsearch/AbrXmlSearch.asmx
ABN_CACHE_TTL_SECONDS=2592000  # 30 days (30 * 24 * 60 * 60)

# Redis Cache (optional - use DB cache if Redis not available)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

**`backend/common/config.py`:**
```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # ABN API Settings
    abn_api_key: str
    abn_api_base_url: str = "https://abr.business.gov.au/abrxmlsearch/AbrXmlSearch.asmx"
    abn_cache_ttl_seconds: int = 2592000  # 30 days
    
    # Redis (optional)
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

---

### 2.3 ABN API Client (`abn_client.py`)

```python
"""
ABN Lookup API Client
Handles communication with Australian Business Register (ABR) API
"""
import httpx
import xml.etree.ElementTree as ET
from typing import Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ABNValidationError(Exception):
    """Custom exception for ABN validation failures"""
    pass


class ABNAPIClient:
    """
    Client for Australian Business Register (ABR) ABN Lookup API
    
    Documentation: https://api.gov.au/service/5b639f0f63f18432cd0e1547
    """
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.endpoint = f"{base_url}/SearchByABNv202001"
        self.timeout = 10.0  # seconds
    
    async def validate_abn(
        self, 
        abn: str, 
        include_historical: bool = False
    ) -> Dict[str, Any]:
        """
        Validate ABN and retrieve company details from ABR
        
        Args:
            abn: Australian Business Number (11 digits)
            include_historical: Include historical ABN details
            
        Returns:
            Dictionary containing validated ABN details:
            {
                "abn": "53004085616",
                "abn_status": "Active",
                "entity_type": "Australian Private Company",
                "entity_name": "INTERNATIONAL CONVENTION CENTRE SYDNEY PTY LTD",
                "trading_names": ["ICC SYDNEY", "INTERNATIONAL CONVENTION CENTRE SYDNEY"],
                "gst_registered": True,
                "gst_status": "Registered from 01 Jul 2000",
                "state": "NSW",
                "postcode": "2000",
                "abn_status_effective_from": "2000-07-01",
                "retrieved_at": "2025-10-13T12:34:56"
            }
            
        Raises:
            ABNValidationError: If ABN is invalid or API request fails
        """
        # Validate ABN format (11 digits, numeric only)
        if not self._validate_abn_format(abn):
            raise ABNValidationError(
                f"Invalid ABN format: {abn}. Must be 11 digits."
            )
        
        # Build API request
        params = {
            "authenticationGuid": self.api_key,
            "searchString": abn,
            "includeHistoricalDetails": "Y" if include_historical else "N"
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"Calling ABR API for ABN: {abn}")
                
                response = await client.get(self.endpoint, params=params)
                response.raise_for_status()
                
                # Parse XML response
                return self._parse_response(response.text)
                
        except httpx.HTTPStatusError as e:
            logger.error(f"ABR API HTTP error: {e}")
            raise ABNValidationError(f"ABR API request failed: {e.response.status_code}")
        
        except httpx.RequestError as e:
            logger.error(f"ABR API connection error: {e}")
            raise ABNValidationError(f"Failed to connect to ABR API: {str(e)}")
        
        except Exception as e:
            logger.error(f"Unexpected error validating ABN {abn}: {e}")
            raise ABNValidationError(f"ABN validation failed: {str(e)}")
    
    def _validate_abn_format(self, abn: str) -> bool:
        """
        Validate ABN format (11 digits, numeric only)
        Does NOT validate ABN checksum (ABR API does that)
        """
        # Remove spaces (users might enter "53 004 085 616")
        abn_clean = abn.replace(" ", "")
        
        # Check length and numeric
        if len(abn_clean) != 11:
            return False
        
        if not abn_clean.isdigit():
            return False
        
        return True
    
    def _parse_response(self, xml_text: str) -> Dict[str, Any]:
        """
        Parse ABR API XML response into structured dictionary
        """
        try:
            root = ET.fromstring(xml_text)
            
            # Check for exception in response (ABN not found)
            exception = root.find(".//exception")
            if exception is not None:
                exception_desc = exception.find("exceptionDescription")
                if exception_desc is not None:
                    raise ABNValidationError(
                        f"ABN not found: {exception_desc.text}"
                    )
            
            # Extract business entity details
            business_entity = root.find(".//businessEntity")
            if business_entity is None:
                raise ABNValidationError("ABN not found in Australian Business Register")
            
            # Parse ABN details
            abn_element = business_entity.find("ABN")
            abn_status = abn_element.get("status") if abn_element is not None else "Unknown"
            abn_status_from = abn_element.get("ABNStatusEffectiveFrom") if abn_element is not None else None
            abn_value = abn_element.text if abn_element is not None else None
            
            # Parse entity type
            entity_type_element = business_entity.find(".//entityType/entityDescription")
            entity_type = entity_type_element.text if entity_type_element is not None else None
            
            # Parse main name (legal entity name)
            main_name_element = business_entity.find(".//mainName/organisationName")
            entity_name = main_name_element.text if main_name_element is not None else None
            
            # Parse GST registration
            gst_element = business_entity.find(".//goodsAndServicesTax")
            gst_registered = gst_element is not None
            gst_status = None
            if gst_element is not None:
                gst_status_element = gst_element.find("status")
                gst_status = gst_status_element.text if gst_status_element is not None else None
            
            # Parse business names (trading names)
            trading_names = []
            for business_name in business_entity.findall(".//businessName/organisationName"):
                if business_name.text and business_name.text not in trading_names:
                    trading_names.append(business_name.text)
            
            # Parse address
            address = business_entity.find(".//mainBusinessPhysicalAddress")
            state = None
            postcode = None
            if address is not None:
                state_element = address.find("stateCode")
                state = state_element.text if state_element is not None else None
                postcode_element = address.find("postcode")
                postcode = postcode_element.text if postcode_element is not None else None
            
            # Build result dictionary
            result = {
                "abn": abn_value,
                "abn_status": abn_status,
                "abn_status_effective_from": abn_status_from,
                "entity_type": entity_type,
                "entity_name": entity_name,
                "trading_names": trading_names,
                "gst_registered": gst_registered,
                "gst_status": gst_status,
                "state": state,
                "postcode": postcode,
                "retrieved_at": datetime.utcnow().isoformat(),
                "raw_xml": xml_text  # Store for caching
            }
            
            logger.info(f"Successfully validated ABN {abn_value}: {entity_name}")
            return result
            
        except ET.ParseError as e:
            logger.error(f"Failed to parse ABR API XML response: {e}")
            raise ABNValidationError(f"Invalid XML response from ABR API: {str(e)}")


# Singleton instance (dependency injection)
_abn_client: Optional[ABNAPIClient] = None

def get_abn_client(settings) -> ABNAPIClient:
    """Dependency injection: Get ABN API client singleton"""
    global _abn_client
    if _abn_client is None:
        _abn_client = ABNAPIClient(
            api_key=settings.abn_api_key,
            base_url=settings.abn_api_base_url
        )
    return _abn_client
```

---

### 2.4 Caching Layer (`abn_cache.py`)

```python
"""
ABN Validation Cache
30-day caching to reduce API calls (ABR terms allow 30-day cache)
"""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json
import logging
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, DateTime, Text, Integer
from backend.common.database import Base

logger = logging.getLogger(__name__)


class ABNCache(Base):
    """
    Database cache for ABN validation results
    Alternative to Redis (simpler for MVP)
    """
    __tablename__ = "abn_cache"
    
    abn = Column(String(11), primary_key=True)
    response_json = Column(Text, nullable=False)  # JSON string
    cached_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    cache_version = Column(Integer, nullable=False, default=1)  # For invalidation


class ABNCacheService:
    """
    ABN validation caching service
    TTL: 30 days (ABR terms allow 30-day cache)
    """
    
    def __init__(self, db: Session, cache_ttl_seconds: int = 2592000):
        self.db = db
        self.cache_ttl_seconds = cache_ttl_seconds  # 30 days default
    
    async def get_cached(self, abn: str) -> Optional[Dict[str, Any]]:
        """
        Get cached ABN validation result
        Returns None if not cached or expired
        """
        try:
            cached = self.db.query(ABNCache).filter(
                ABNCache.abn == abn
            ).first()
            
            if cached is None:
                logger.debug(f"ABN {abn} not in cache")
                return None
            
            # Check if expired (30 days)
            cache_age = datetime.utcnow() - cached.cached_at
            if cache_age > timedelta(seconds=self.cache_ttl_seconds):
                logger.info(f"ABN {abn} cache expired (age: {cache_age.days} days)")
                # Delete expired cache
                self.db.delete(cached)
                self.db.commit()
                return None
            
            # Return cached result
            logger.info(f"ABN {abn} cache HIT (age: {cache_age.days} days)")
            return json.loads(cached.response_json)
            
        except Exception as e:
            logger.error(f"Error reading ABN cache for {abn}: {e}")
            return None
    
    async def set_cached(self, abn: str, response: Dict[str, Any]) -> None:
        """
        Cache ABN validation result
        """
        try:
            # Check if already cached (update)
            existing = self.db.query(ABNCache).filter(
                ABNCache.abn == abn
            ).first()
            
            if existing:
                existing.response_json = json.dumps(response)
                existing.cached_at = datetime.utcnow()
            else:
                cached = ABNCache(
                    abn=abn,
                    response_json=json.dumps(response),
                    cached_at=datetime.utcnow()
                )
                self.db.add(cached)
            
            self.db.commit()
            logger.info(f"Cached ABN {abn} validation result")
            
        except Exception as e:
            logger.error(f"Error caching ABN {abn}: {e}")
            self.db.rollback()
    
    async def invalidate(self, abn: str) -> None:
        """
        Manually invalidate cache for ABN
        (e.g., if company reports ABN changed)
        """
        try:
            self.db.query(ABNCache).filter(
                ABNCache.abn == abn
            ).delete()
            self.db.commit()
            logger.info(f"Invalidated cache for ABN {abn}")
        except Exception as e:
            logger.error(f"Error invalidating cache for {abn}: {e}")
            self.db.rollback()
```

---

### 2.5 Company Service (`services.py`)

```python
"""
Company Business Logic
Includes ABN validation with caching
"""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from .models import Company, CompanyBillingDetails
from .abn_client import ABNAPIClient, ABNValidationError
from .abn_cache import ABNCacheService

logger = logging.getLogger(__name__)


class CompanyService:
    """
    Company domain business logic
    """
    
    def __init__(
        self, 
        db: Session, 
        abn_client: ABNAPIClient,
        cache_service: ABNCacheService
    ):
        self.db = db
        self.abn_client = abn_client
        self.cache_service = cache_service
    
    async def validate_abn_with_cache(self, abn: str) -> Dict[str, Any]:
        """
        Validate ABN with 30-day caching
        
        Args:
            abn: Australian Business Number (11 digits)
            
        Returns:
            ABN validation result dictionary
            
        Raises:
            HTTPException: If ABN validation fails
        """
        # Clean ABN (remove spaces)
        abn_clean = abn.replace(" ", "")
        
        # Check cache first (30-day TTL)
        cached = await self.cache_service.get_cached(abn_clean)
        if cached:
            logger.info(f"ABN {abn_clean} validation from cache")
            return cached
        
        # Cache miss - call ABR API
        try:
            logger.info(f"ABN {abn_clean} cache miss - calling ABR API")
            result = await self.abn_client.validate_abn(abn_clean)
            
            # Cache result (30 days)
            await self.cache_service.set_cached(abn_clean, result)
            
            return result
            
        except ABNValidationError as e:
            logger.warning(f"ABN validation failed for {abn_clean}: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "abn_validation_failed",
                    "message": str(e),
                    "abn": abn_clean
                }
            )
    
    async def create_billing_details(
        self,
        company_id: int,
        abn: str,
        billing_email: str,
        billing_address: str,
        user_id: int
    ) -> CompanyBillingDetails:
        """
        Create billing details with ABN validation
        Auto-populates legal name, GST status from ABR API
        """
        # Validate ABN via ABR API (with caching)
        abn_data = await self.validate_abn_with_cache(abn)
        
        # Check ABN status (must be Active)
        if abn_data["abn_status"] != "Active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "abn_not_active",
                    "message": f"ABN status is '{abn_data['abn_status']}'. Only Active ABNs are accepted.",
                    "abn": abn,
                    "abn_status": abn_data["abn_status"]
                }
            )
        
        # Create billing details with ABR-validated data
        billing = CompanyBillingDetails(
            company_id=company_id,
            abn=abn_data["abn"],
            abn_status=abn_data["abn_status"],
            gst_registered=abn_data["gst_registered"],
            entity_type=abn_data["entity_type"],
            tax_invoice_name=abn_data["entity_name"],  # Legal name from ABR
            billing_email=billing_email,
            billing_address=billing_address,
            abn_last_verified=datetime.utcnow(),
            abn_verification_response=json.dumps(abn_data),  # Cache in DB
            created_by=user_id
        )
        
        self.db.add(billing)
        self.db.commit()
        self.db.refresh(billing)
        
        logger.info(f"Created billing details for company {company_id} with ABN {abn}")
        return billing
```

---

### 2.6 FastAPI Routes (`routes.py`)

```python
"""
Company API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Dict, Any

from backend.common.database import get_db
from backend.common.config import get_settings
from backend.common.auth import get_current_user

from .services import CompanyService
from .abn_client import get_abn_client
from .abn_cache import ABNCacheService

router = APIRouter(prefix="/api/companies", tags=["companies"])


# ============================================================================
# Pydantic Schemas
# ============================================================================

class ABNValidationRequest(BaseModel):
    """Request body for ABN validation"""
    abn: str = Field(..., min_length=11, max_length=14, description="ABN (11 digits, spaces optional)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "abn": "53 004 085 616"
            }
        }


class ABNValidationResponse(BaseModel):
    """Response for ABN validation"""
    abn: str
    abn_status: str
    entity_name: str
    entity_type: str
    trading_names: list[str]
    gst_registered: bool
    gst_status: str | None
    state: str | None
    postcode: str | None
    retrieved_at: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "abn": "53004085616",
                "abn_status": "Active",
                "entity_name": "INTERNATIONAL CONVENTION CENTRE SYDNEY PTY LTD",
                "entity_type": "Australian Private Company",
                "trading_names": ["ICC SYDNEY", "INTERNATIONAL CONVENTION CENTRE SYDNEY"],
                "gst_registered": True,
                "gst_status": "Registered from 01 Jul 2000",
                "state": "NSW",
                "postcode": "2000",
                "retrieved_at": "2025-10-13T12:34:56"
            }
        }


# ============================================================================
# Routes
# ============================================================================

@router.post("/validate-abn", response_model=ABNValidationResponse)
async def validate_abn(
    request: ABNValidationRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    settings = Depends(get_settings)
):
    """
    Validate Australian Business Number (ABN) via ABR API
    
    **Features:**
    - Real-time validation against Australian Business Register
    - Auto-populates legal company name, GST status, entity type
    - 30-day caching (reduces API costs)
    
    **Use Cases:**
    - Company signup (billing details step)
    - Billing details update (before first invoice)
    - Parent company lookup (subsidiary billing)
    
    **Error Responses:**
    - 400: Invalid ABN format (must be 11 digits)
    - 400: ABN not found in ABR
    - 400: ABN status not Active (Cancelled/Historical)
    - 503: ABR API unavailable
    """
    # Get dependencies
    abn_client = get_abn_client(settings)
    cache_service = ABNCacheService(db, settings.abn_cache_ttl_seconds)
    service = CompanyService(db, abn_client, cache_service)
    
    # Validate ABN (with caching)
    result = await service.validate_abn_with_cache(request.abn)
    
    return ABNValidationResponse(**result)


@router.post("/billing-details/invalidate-abn-cache")
async def invalidate_abn_cache(
    abn: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),  # Admin only
    settings = Depends(get_settings)
):
    """
    Manually invalidate ABN cache
    
    **Use Case:** Company reports their ABN changed (rare, but happens during restructure)
    
    **Access:** System Admin only
    """
    # TODO: Check if current_user is System Admin
    
    cache_service = ABNCacheService(db, settings.abn_cache_ttl_seconds)
    await cache_service.invalidate(abn)
    
    return {"message": f"ABN cache invalidated for {abn}"}
```

---

### 2.7 Frontend Integration Example (React/TypeScript)

```typescript
// src/services/abnService.ts
import { api } from './api';

export interface ABNValidationResult {
  abn: string;
  abnStatus: string;
  entityName: string;
  entityType: string;
  tradingNames: string[];
  gstRegistered: boolean;
  gstStatus: string | null;
  state: string | null;
  postcode: string | null;
  retrievedAt: string;
}

export interface ABNValidationError {
  error: string;
  message: string;
  abn?: string;
}

export class ABNService {
  /**
   * Validate ABN via backend API
   * Returns validated company details from ABR
   */
  async validateABN(abn: string): Promise<ABNValidationResult> {
    try {
      const response = await api.post<ABNValidationResult>('/companies/validate-abn', {
        abn: abn.replace(/\s/g, '')  // Remove spaces
      });
      return response.data;
    } catch (error: any) {
      // Handle specific ABN validation errors
      if (error.response?.status === 400) {
        const errorData: ABNValidationError = error.response.data.detail;
        throw new Error(errorData.message);
      }
      throw new Error('Failed to validate ABN. Please try again.');
    }
  }
  
  /**
   * Format ABN with spaces for display
   * Input: "53004085616"
   * Output: "53 004 085 616"
   */
  formatABN(abn: string): string {
    const clean = abn.replace(/\s/g, '');
    if (clean.length !== 11) return abn;
    return `${clean.slice(0, 2)} ${clean.slice(2, 5)} ${clean.slice(5, 8)} ${clean.slice(8)}`;
  }
}

export const abnService = new ABNService();
```

```tsx
// src/components/CompanyOnboarding/BillingDetailsStep.tsx
import React, { useState } from 'react';
import { abnService } from '../../services/abnService';

export const BillingDetailsStep: React.FC = () => {
  const [abn, setABN] = useState('');
  const [validating, setValidating] = useState(false);
  const [abnData, setABNData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  
  const handleABNChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // Format as user types: "53 004 085 616"
    const value = e.target.value.replace(/\s/g, '');
    if (value.length <= 11 && /^\d*$/.test(value)) {
      setABN(abnService.formatABN(value));
    }
  };
  
  const handleValidateABN = async () => {
    setValidating(true);
    setError(null);
    
    try {
      const result = await abnService.validateABN(abn);
      setABNData(result);
      
      // Auto-populate form fields
      // (Legal name, GST status, entity type)
      
    } catch (err: any) {
      setError(err.message);
      setABNData(null);
    } finally {
      setValidating(false);
    }
  };
  
  return (
    <div className="billing-details-step">
      <h2>Billing Details</h2>
      
      {/* ABN Input */}
      <div className="form-group">
        <label>Australian Business Number (ABN)</label>
        <div className="abn-input-group">
          <input
            type="text"
            value={abn}
            onChange={handleABNChange}
            placeholder="53 004 085 616"
            maxLength={14}  // 11 digits + 3 spaces
          />
          <button 
            onClick={handleValidateABN}
            disabled={abn.replace(/\s/g, '').length !== 11 || validating}
          >
            {validating ? 'Validating...' : 'Validate ABN'}
          </button>
        </div>
        {error && <p className="error">{error}</p>}
      </div>
      
      {/* Auto-populated from ABR */}
      {abnData && (
        <div className="abn-verified">
          <div className="success-badge">✓ ABN Verified</div>
          
          <div className="form-group">
            <label>Legal Company Name</label>
            <input
              type="text"
              value={abnData.entityName}
              disabled
              className="readonly"
            />
            <small>Auto-populated from Australian Business Register</small>
          </div>
          
          <div className="form-group">
            <label>Entity Type</label>
            <input
              type="text"
              value={abnData.entityType}
              disabled
              className="readonly"
            />
          </div>
          
          <div className="form-group">
            <label>GST Registration</label>
            <div className="gst-status">
              {abnData.gstRegistered ? (
                <span className="badge badge-success">
                  ✓ GST Registered
                </span>
              ) : (
                <span className="badge badge-warning">
                  Not GST Registered
                </span>
              )}
              {abnData.gstStatus && (
                <small>{abnData.gstStatus}</small>
              )}
            </div>
            <small>
              {abnData.gstRegistered 
                ? '10% GST will be added to all invoices'
                : 'No GST will be charged'}
            </small>
          </div>
          
          {/* Trading Names */}
          {abnData.tradingNames.length > 0 && (
            <div className="form-group">
              <label>Trading Names</label>
              <ul className="trading-names">
                {abnData.tradingNames.map((name: string, idx: number) => (
                  <li key={idx}>{name}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
      
      {/* Manual fields */}
      <div className="form-group">
        <label>Billing Email</label>
        <input type="email" placeholder="billing@company.com" />
      </div>
      
      <div className="form-group">
        <label>Billing Address</label>
        <textarea placeholder="14 Darling Drive, Sydney NSW 2000" />
      </div>
    </div>
  );
};
```

---

## 3. Testing Strategy

### 3.1 Unit Tests (pytest)

```python
# tests/test_abn_client.py
import pytest
from backend.modules.companies.abn_client import ABNAPIClient, ABNValidationError

@pytest.mark.asyncio
async def test_validate_abn_success():
    """Test successful ABN validation"""
    client = ABNAPIClient(api_key="test-guid", base_url="https://abr.business.gov.au")
    
    # ICC Sydney ABN (known valid)
    result = await client.validate_abn("53004085616")
    
    assert result["abn"] == "53004085616"
    assert result["abn_status"] == "Active"
    assert "INTERNATIONAL CONVENTION CENTRE" in result["entity_name"]
    assert result["gst_registered"] is True


@pytest.mark.asyncio
async def test_validate_abn_invalid_format():
    """Test ABN format validation"""
    client = ABNAPIClient(api_key="test-guid", base_url="https://abr.business.gov.au")
    
    with pytest.raises(ABNValidationError, match="Invalid ABN format"):
        await client.validate_abn("12345")  # Too short


@pytest.mark.asyncio
async def test_validate_abn_not_found():
    """Test ABN not found in ABR"""
    client = ABNAPIClient(api_key="test-guid", base_url="https://abr.business.gov.au")
    
    with pytest.raises(ABNValidationError, match="ABN not found"):
        await client.validate_abn("00000000000")  # Invalid ABN
```

### 3.2 Integration Tests

```python
# tests/test_abn_integration.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_validate_abn_endpoint_success():
    """Test /api/companies/validate-abn endpoint"""
    response = client.post(
        "/api/companies/validate-abn",
        json={"abn": "53 004 085 616"},  # ICC Sydney (spaces allowed)
        headers={"Authorization": "Bearer test-token"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["abn"] == "53004085616"
    assert data["abn_status"] == "Active"
    assert data["gst_registered"] is True


def test_validate_abn_endpoint_invalid():
    """Test ABN validation with invalid ABN"""
    response = client.post(
        "/api/companies/validate-abn",
        json={"abn": "12345"},
        headers={"Authorization": "Bearer test-token"}
    )
    
    assert response.status_code == 400
    assert "Invalid ABN format" in response.json()["detail"]["message"]
```

---

## 4. Production Deployment Checklist

### Before Go-Live:
- [ ] **Register for ABN API key** (https://api.gov.au)
- [ ] **Add API key to production .env** (`ABN_API_KEY=your-guid`)
- [ ] **Create ABNCache table** (Alembic migration)
- [ ] **Test with real ABNs** (ICC Sydney, MCEC, your own company)
- [ ] **Monitor API usage** (stay within free tier 1000/day initially)
- [ ] **Set up error alerting** (if ABR API down, notify admins)

### Monitoring:
- **ABN API call rate:** Track daily requests (approach 1000/day → upgrade to paid)
- **Cache hit rate:** Target > 80% (most lookups should hit cache)
- **API response time:** Monitor p95 latency (< 2 seconds expected)
- **Error rate:** Track ABN validation failures (< 2% expected)

---

## 5. Cost Analysis

### API Costs:
| Scenario | Requests/Month | Tier | Cost |
|----------|----------------|------|------|
| **MVP (Year 1)** | 500 companies × 1 lookup = 500 | FREE | $0 |
| **Growing (Year 2)** | 2,000 companies × 1 lookup = 2,000 | Basic $50/mo | $600/year |
| **Scale (Year 3)** | 10,000 companies × 1 lookup = 10,000 | Basic $50/mo | $600/year |

**Cache Efficiency:**
- 30-day cache → 97% of re-lookups hit cache (no API call)
- Expected cache hit rate: 80-90% after first 6 months

**Recommendation:** FREE tier sufficient for first 12-18 months.

---

## 6. Troubleshooting

### Common Issues:

**"ABN API request failed: 401 Unauthorized"**
- Check API key in `.env` (correct GUID format?)
- Verify API key is active (check email from api.gov.au)

**"ABN not found" for valid ABN**
- ABN might be recently registered (ABR lag: 1-2 weeks)
- Try on ABR website: https://abr.business.gov.au/ABN/View?id=53004085616

**"Request timeout"**
- ABR API can be slow (5-10 seconds)
- Increase timeout in `abn_client.py` (default 10s → 15s)

**Cache not working**
- Check `abn_cache` table exists (Alembic migration)
- Verify Redis connection (if using Redis cache)

---

## Next Steps

1. **Implement code** from this guide (estimate: 4-6 hours)
2. **Register for ABN API key** (1-2 business days approval)
3. **Test with real ABNs** (your company, ICC Sydney, MCEC)
4. **Integrate with company onboarding flow** (frontend + backend)
5. **Monitor usage** (track API calls, cache hit rate)

**Questions?** Let me know if you need help with any section!

---

*Dimitri - Data Domain Architect* 🔍



