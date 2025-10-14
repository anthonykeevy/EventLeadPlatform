# Enhanced ABR Search Integration - Multiple Search Options

**Author:** Dimitri 🔍 (Data Domain Architect)  
**Date:** October 13, 2025  
**Purpose:** Enhanced company lookup with multiple search methods (ABN, ACN, Company Name)

---

## 🎯 **Problem Solved**

**Current Limitation:** Users must know their ABN to find their company (poor UX)
**Solution:** Multiple search options - ABN, ACN, and Company Name search
**Result:** Users can find their company using any identifier they know

---

## 🔍 **ABR API Search Capabilities**

The ABR Web Services provide multiple search endpoints:

### **Available Search Methods:**

1. **ABN Search** (Current Implementation)
   - **Endpoint:** `SearchByABNv202001`
   - **Input:** 11-digit ABN
   - **Use Case:** Users who know their ABN

2. **ACN Search** (Australian Company Number)
   - **Endpoint:** `SearchByACNv202001`
   - **Input:** 9-digit ACN
   - **Use Case:** Users who know their ACN (company registration number)

3. **Company Name Search** (NEW!)
   - **Endpoint:** `SearchByNamev202001`
   - **Input:** Company name (partial matches supported)
   - **Use Case:** Users who know company name but not ABN/ACN

---

## 🏗️ **Enhanced Implementation**

### **1. Updated ABR API Client**

```python
"""
Enhanced ABR API Client with Multiple Search Methods
"""
import httpx
import xml.etree.ElementTree as ET
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

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


class EnhancedABRClient:
    """
    Enhanced ABR API Client with Multiple Search Methods
    """
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = 10.0
        
        # API Endpoints
        self.endpoints = {
            "abn": f"{base_url}/SearchByABNv202001",
            "acn": f"{base_url}/SearchByACNv202001", 
            "name": f"{base_url}/SearchByNamev202001"
        }
    
    # ============================================================================
    # ABN Search (Existing - Enhanced)
    # ============================================================================
    
    async def search_by_abn(self, abn: str) -> Optional[ABRSearchResult]:
        """
        Search by Australian Business Number (ABN)
        
        Args:
            abn: 11-digit ABN
            
        Returns:
            ABRSearchResult or None if not found
        """
        if not self._validate_abn_format(abn):
            raise ValueError(f"Invalid ABN format: {abn}")
        
        params = {
            "authenticationGuid": self.api_key,
            "searchString": abn.replace(" ", ""),
            "includeHistoricalDetails": "N"
        }
        
        try:
            response = await self._make_request(self.endpoints["abn"], params)
            if response:
                return ABRSearchResult(response)
            return None
            
        except Exception as e:
            logger.error(f"ABN search failed for {abn}: {e}")
            raise
    
    # ============================================================================
    # ACN Search (NEW)
    # ============================================================================
    
    async def search_by_acn(self, acn: str) -> Optional[ABRSearchResult]:
        """
        Search by Australian Company Number (ACN)
        
        Args:
            acn: 9-digit ACN
            
        Returns:
            ABRSearchResult or None if not found
        """
        if not self._validate_acn_format(acn):
            raise ValueError(f"Invalid ACN format: {acn}")
        
        params = {
            "authenticationGuid": self.api_key,
            "searchString": acn.replace(" ", ""),
            "includeHistoricalDetails": "N"
        }
        
        try:
            response = await self._make_request(self.endpoints["acn"], params)
            if response:
                return ABRSearchResult(response)
            return None
            
        except Exception as e:
            logger.error(f"ACN search failed for {acn}: {e}")
            raise
    
    # ============================================================================
    # Company Name Search (NEW - KEY FEATURE)
    # ============================================================================
    
    async def search_by_name(
        self, 
        company_name: str, 
        max_results: int = 20
    ) -> List[ABRSearchResult]:
        """
        Search by Company Name (Partial matches supported)
        
        Args:
            company_name: Company name to search for
            max_results: Maximum results to return (default 20)
            
        Returns:
            List of ABRSearchResult objects (can be multiple matches)
        """
        if not company_name or len(company_name.strip()) < 2:
            raise ValueError("Company name must be at least 2 characters")
        
        params = {
            "authenticationGuid": self.api_key,
            "searchString": company_name.strip(),
            "includeHistoricalDetails": "N",
            "maxResults": str(max_results)
        }
        
        try:
            response = await self._make_request(self.endpoints["name"], params)
            if response and isinstance(response, list):
                return [ABRSearchResult(item) for item in response]
            elif response:
                return [ABRSearchResult(response)]
            return []
            
        except Exception as e:
            logger.error(f"Name search failed for '{company_name}': {e}")
            raise
    
    # ============================================================================
    # Smart Search (Combined Logic)
    # ============================================================================
    
    async def smart_search(self, query: str) -> Dict[str, Any]:
        """
        Smart search that tries multiple methods based on input format
        
        Args:
            query: ABN, ACN, or company name
            
        Returns:
            Dictionary with search results and method used
        """
        query_clean = query.strip().replace(" ", "")
        
        # Determine search method based on input format
        if len(query_clean) == 11 and query_clean.isdigit():
            # ABN search
            result = await self.search_by_abn(query)
            return {
                "method": "abn",
                "query": query,
                "results": [result] if result else [],
                "total": 1 if result else 0
            }
        
        elif len(query_clean) == 9 and query_clean.isdigit():
            # ACN search
            result = await self.search_by_acn(query)
            return {
                "method": "acn", 
                "query": query,
                "results": [result] if result else [],
                "total": 1 if result else 0
            }
        
        else:
            # Company name search
            results = await self.search_by_name(query)
            return {
                "method": "name",
                "query": query,
                "results": results,
                "total": len(results)
            }
    
    # ============================================================================
    # Helper Methods
    # ============================================================================
    
    async def _make_request(self, endpoint: str, params: Dict[str, str]) -> Any:
        """Make HTTP request to ABR API"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"Calling ABR API: {endpoint}")
                
                response = await client.get(endpoint, params=params)
                response.raise_for_status()
                
                return self._parse_response(response.text)
                
        except httpx.HTTPStatusError as e:
            logger.error(f"ABR API HTTP error: {e}")
            raise Exception(f"ABR API request failed: {e.response.status_code}")
        
        except httpx.RequestError as e:
            logger.error(f"ABR API connection error: {e}")
            raise Exception(f"Failed to connect to ABR API: {str(e)}")
    
    def _validate_abn_format(self, abn: str) -> bool:
        """Validate ABN format (11 digits)"""
        clean = abn.replace(" ", "")
        return len(clean) == 11 and clean.isdigit()
    
    def _validate_acn_format(self, acn: str) -> bool:
        """Validate ACN format (9 digits)"""
        clean = acn.replace(" ", "")
        return len(clean) == 9 and clean.isdigit()
    
    def _parse_response(self, xml_text: str) -> Any:
        """Parse ABR API XML response"""
        try:
            root = ET.fromstring(xml_text)
            
            # Check for exceptions
            exception = root.find(".//exception")
            if exception is not None:
                exception_desc = exception.find("exceptionDescription")
                if exception_desc is not None:
                    raise Exception(f"ABR API error: {exception_desc.text}")
            
            # Handle single result (ABN/ACN search)
            business_entity = root.find(".//businessEntity")
            if business_entity is not None:
                return self._parse_business_entity(business_entity)
            
            # Handle multiple results (name search)
            business_entities = root.findall(".//businessEntity")
            if business_entities:
                return [self._parse_business_entity(entity) for entity in business_entities]
            
            return None
            
        except ET.ParseError as e:
            logger.error(f"Failed to parse ABR API XML: {e}")
            raise Exception(f"Invalid XML response from ABR API: {str(e)}")
    
    def _parse_business_entity(self, entity) -> Dict[str, Any]:
        """Parse single business entity from XML"""
        # Extract ABN
        abn_element = entity.find("ABN")
        abn = abn_element.text if abn_element is not None else None
        abn_status = abn_element.get("status") if abn_element is not None else None
        
        # Extract entity type
        entity_type_element = entity.find(".//entityType/entityDescription")
        entity_type = entity_type_element.text if entity_type_element is not None else None
        
        # Extract main name (legal name)
        main_name_element = entity.find(".//mainName/organisationName")
        entity_name = main_name_element.text if main_name_element is not None else None
        
        # Extract business names
        business_names = []
        for name in entity.findall(".//businessName/organisationName"):
            if name.text and name.text not in business_names:
                business_names.append(name.text)
        
        # Extract trading names (legacy)
        trading_names = []
        for name in entity.findall(".//tradingName/organisationName"):
            if name.text and name.text not in trading_names:
                trading_names.append(name.text)
        
        # Extract GST registration
        gst_element = entity.find(".//goodsAndServicesTax")
        gst_registered = gst_element is not None
        
        # Extract address
        address = entity.find(".//mainBusinessPhysicalAddress")
        state = None
        postcode = None
        if address is not None:
            state_element = address.find("stateCode")
            state = state_element.text if state_element is not None else None
            postcode_element = address.find("postcode")
            postcode = postcode_element.text if postcode_element is not None else None
        
        return {
            "abn": abn,
            "abn_status": abn_status,
            "entity_type": entity_type,
            "entity_name": entity_name,
            "business_names": business_names,
            "trading_names": trading_names,
            "gst_registered": gst_registered,
            "state": state,
            "postcode": postcode,
            "retrieved_at": datetime.utcnow().isoformat()
        }
```

---

## 🎨 **Enhanced Frontend Components**

### **1. Smart Company Search Component**

```tsx
// src/components/CompanySearch/SmartCompanySearch.tsx
import React, { useState, useEffect } from 'react';
import { abrService } from '../../services/abrService';

interface CompanySearchResult {
  abn: string;
  entityName: string;
  entityType: string;
  abnStatus: string;
  gstRegistered: boolean;
  state: string | null;
  businessNames: string[];
  tradingNames: string[];
}

interface SmartCompanySearchProps {
  onCompanySelected: (company: CompanySearchResult) => void;
  placeholder?: string;
}

export const SmartCompanySearch: React.FC<SmartCompanySearchProps> = ({
  onCompanySelected,
  placeholder = "Enter ABN, ACN, or company name..."
}) => {
  const [query, setQuery] = useState('');
  const [searching, setSearching] = useState(false);
  const [results, setResults] = useState<CompanySearchResult[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [searchMethod, setSearchMethod] = useState<'abn' | 'acn' | 'name' | null>(null);

  // Debounced search
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (query.length >= 2) {
        handleSearch(query);
      } else {
        setResults([]);
        setSearchMethod(null);
      }
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [query]);

  const handleSearch = async (searchQuery: string) => {
    setSearching(true);
    setError(null);

    try {
      const response = await abrService.smartSearch(searchQuery);
      
      setResults(response.results);
      setSearchMethod(response.method);
      
      // Auto-select if single result
      if (response.results.length === 1) {
        onCompanySelected(response.results[0]);
      }
      
    } catch (err: any) {
      setError(err.message);
      setResults([]);
    } finally {
      setSearching(false);
    }
  };

  const handleCompanySelect = (company: CompanySearchResult) => {
    onCompanySelected(company);
    setResults([]);
    setQuery(company.entityName);
  };

  const getSearchHint = () => {
    switch (searchMethod) {
      case 'abn': return 'ABN search - exact match';
      case 'acn': return 'ACN search - exact match';
      case 'name': return `Name search - ${results.length} results found`;
      default: return 'Enter ABN (11 digits), ACN (9 digits), or company name';
    }
  };

  return (
    <div className="smart-company-search">
      <div className="search-input-group">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          className="search-input"
          autoComplete="off"
        />
        {searching && <div className="search-spinner">🔍</div>}
      </div>

      <div className="search-hint">
        {getSearchHint()}
      </div>

      {error && (
        <div className="search-error">
          ⚠️ {error}
        </div>
      )}

      {results.length > 0 && (
        <div className="search-results">
          {results.map((company, index) => (
            <div
              key={`${company.abn}-${index}`}
              className="search-result-item"
              onClick={() => handleCompanySelect(company)}
            >
              <div className="result-header">
                <h4>{company.entityName}</h4>
                <span className="abn-badge">ABN: {company.abn}</span>
              </div>
              
              <div className="result-details">
                <div className="detail-row">
                  <span className="label">Type:</span>
                  <span>{company.entityType}</span>
                </div>
                
                {company.businessNames.length > 0 && (
                  <div className="detail-row">
                    <span className="label">Business Names:</span>
                    <span>{company.businessNames.join(', ')}</span>
                  </div>
                )}
                
                <div className="detail-row">
                  <span className="label">GST:</span>
                  <span className={company.gstRegistered ? 'gst-registered' : 'gst-not-registered'}>
                    {company.gstRegistered ? '✓ Registered' : '✗ Not Registered'}
                  </span>
                </div>
                
                {company.state && (
                  <div className="detail-row">
                    <span className="label">State:</span>
                    <span>{company.state}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
```

### **2. Enhanced ABR Service**

```typescript
// src/services/abrService.ts
import { api } from './api';

export interface CompanySearchResult {
  abn: string;
  entityName: string;
  entityType: string;
  abnStatus: string;
  gstRegistered: boolean;
  state: string | null;
  postcode: string | null;
  businessNames: string[];
  tradingNames: string[];
  retrievedAt: string;
}

export interface SmartSearchResponse {
  method: 'abn' | 'acn' | 'name';
  query: string;
  results: CompanySearchResult[];
  total: number;
}

export class ABRService {
  /**
   * Smart search that automatically detects search type
   */
  async smartSearch(query: string): Promise<SmartSearchResponse> {
    try {
      const response = await api.post<SmartSearchResponse>('/companies/smart-search', {
        query: query.trim()
      });
      return response.data;
    } catch (error: any) {
      if (error.response?.status === 400) {
        throw new Error(error.response.data.detail.message);
      }
      throw new Error('Search failed. Please try again.');
    }
  }

  /**
   * Search by ABN (exact match)
   */
  async searchByABN(abn: string): Promise<CompanySearchResult | null> {
    try {
      const response = await api.post<CompanySearchResult | null>('/companies/search-by-abn', {
        abn: abn.replace(/\s/g, '')
      });
      return response.data;
    } catch (error: any) {
      if (error.response?.status === 404) {
        return null; // ABN not found
      }
      throw new Error('ABN search failed. Please try again.');
    }
  }

  /**
   * Search by ACN (exact match)
   */
  async searchByACN(acn: string): Promise<CompanySearchResult | null> {
    try {
      const response = await api.post<CompanySearchResult | null>('/companies/search-by-acn', {
        acn: acn.replace(/\s/g, '')
      });
      return response.data;
    } catch (error: any) {
      if (error.response?.status === 404) {
        return null; // ACN not found
      }
      throw new Error('ACN search failed. Please try again.');
    }
  }

  /**
   * Search by company name (partial matches)
   */
  async searchByName(companyName: string, maxResults: number = 20): Promise<CompanySearchResult[]> {
    try {
      const response = await api.post<CompanySearchResult[]>('/companies/search-by-name', {
        companyName: companyName.trim(),
        maxResults
      });
      return response.data;
    } catch (error: any) {
      throw new Error('Name search failed. Please try again.');
    }
  }

  /**
   * Format ABN with spaces for display
   */
  formatABN(abn: string): string {
    const clean = abn.replace(/\s/g, '');
    if (clean.length !== 11) return abn;
    return `${clean.slice(0, 2)} ${clean.slice(2, 5)} ${clean.slice(5, 8)} ${clean.slice(8)}`;
  }

  /**
   * Format ACN with spaces for display
   */
  formatACN(acn: string): string {
    const clean = acn.replace(/\s/g, '');
    if (clean.length !== 9) return acn;
    return `${clean.slice(0, 3)} ${clean.slice(3, 6)} ${clean.slice(6)}`;
  }
}

export const abrService = new ABRService();
```

---

## 🔧 **Enhanced Backend Routes**

```python
# backend/modules/companies/routes.py

@router.post("/smart-search", response_model=SmartSearchResponse)
async def smart_search(
    request: SmartSearchRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    settings = Depends(get_settings)
):
    """
    Smart company search - automatically detects search type
    
    **Input Examples:**
    - "53004085616" → ABN search
    - "123456789" → ACN search  
    - "ICC Sydney" → Name search
    - "International Convention" → Name search (partial)
    
    **Features:**
    - Auto-detects search method based on input format
    - Debounced frontend search (300ms delay)
    - Caching for performance
    - Partial name matching
    """
    abr_client = get_abr_client(settings)
    cache_service = ABRCacheService(db, settings.abr_cache_ttl_seconds)
    service = CompanyService(db, abr_client, cache_service)
    
    result = await service.smart_search(request.query)
    return SmartSearchResponse(**result)


@router.post("/search-by-name", response_model=List[CompanySearchResult])
async def search_by_name(
    request: NameSearchRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    settings = Depends(get_settings)
):
    """
    Search companies by name (partial matches supported)
    
    **Features:**
    - Partial name matching
    - Multiple results returned
    - Sorted by relevance
    - Configurable result limit
    """
    abr_client = get_abr_client(settings)
    cache_service = ABRCacheService(db, settings.abr_cache_ttl_seconds)
    service = CompanyService(db, abr_client, cache_service)
    
    results = await service.search_by_name(
        request.companyName, 
        request.maxResults
    )
    return [CompanySearchResult(**result) for result in results]


@router.post("/search-by-acn", response_model=Optional[CompanySearchResult])
async def search_by_acn(
    request: ACNSearchRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    settings = Depends(get_settings)
):
    """
    Search company by Australian Company Number (ACN)
    
    **Features:**
    - Exact match only
    - Single result returned
    - 9-digit validation
    """
    abr_client = get_abr_client(settings)
    cache_service = ABRCacheService(db, settings.abr_cache_ttl_seconds)
    service = CompanyService(db, abr_client, cache_service)
    
    result = await service.search_by_acn(request.acn)
    if result:
        return CompanySearchResult(**result)
    return None
```

---

## 🎯 **User Experience Benefits**

### **Before (ABN Only):**
```
User: "I need to find my company"
System: "Enter your 11-digit ABN"
User: "I don't know my ABN..."
System: "You need to look it up first"
```

### **After (Multiple Search Options):**
```
User: "I need to find my company"
System: "Enter ABN, ACN, or company name..."
User: "ICC Sydney"
System: "Found 3 matches: ICC Sydney, ICC Sydney Events, etc."
User: "That's the first one!"
System: "✓ Company found - ABN: 53 004 085 616"
```

---

## 📊 **Implementation Priority**

### **Phase 1: Enhanced Backend (Week 1)**
- [ ] Add ACN search endpoint
- [ ] Add company name search endpoint
- [ ] Implement smart search logic
- [ ] Add caching for all search methods

### **Phase 2: Enhanced Frontend (Week 2)**
- [ ] Smart search component
- [ ] Auto-detection of search type
- [ ] Debounced search (300ms)
- [ ] Results dropdown with company details

### **Phase 3: UX Polish (Week 3)**
- [ ] Search suggestions
- [ ] Recent searches
- [ ] Favorite companies
- [ ] Search analytics

---

## 💰 **Cost Impact**

### **API Usage Increase:**
- **Name searches:** More API calls (multiple results per search)
- **Cache efficiency:** Name searches cached individually
- **Smart caching:** Results cached by search method + query

### **Estimated Usage:**
- **ABN searches:** 20% (users who know ABN)
- **ACN searches:** 10% (users who know ACN)  
- **Name searches:** 70% (users who know company name)

**Cost increase:** ~30% more API calls, but better UX = higher conversion

---

**This enhanced search capability will significantly improve user onboarding experience while maintaining Australian compliance!** 🇦🇺

---

*Dimitri - Data Domain Architect* 🔍  
*"Multiple search paths lead to better user adoption!"*


