"""
ABR (Australian Business Register) API Client

Provides search functionality for Australian businesses via ABR Web Services.
Supports search by ABN, ACN, and compAny name with automatic XML parsing
and error handling.

Story 1.10: Enhanced ABR Search Implementation
AC-1.10.2: ABN Search Implementation
AC-1.10.3: ACN Search Implementation  
AC-1.10.4: CompAny Name Search Implementation
"""
import asyncio
import os
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Union, Any
from datetime import datetime, timedelta
import re

import httpx
from common.logger import get_logger

logger = get_logger(__name__)


class ABRClientError(Exception):
    """Base exception for ABR client errors"""
    pass


class ABRTimeoutError(ABRClientError):
    """Raised when ABR API request times out"""
    pass


class ABRAuthenticationError(ABRClientError):
    """Raised when ABR API authentication fails"""
    pass


class ABRValidationError(ABRClientError):
    """Raised when search parameters are invalid"""
    pass


class ABRClient:
    """
    Australian Business Register API Client
    
    Provides async methods to search for businesses by ABN, ACN, or compAny name.
    Handles XML response parsing, error handling, timeouts, and retry logic.
    
    Environment Variables:
        ABR_API_KEY: GUID from ABR website (required)
        ABR_API_TIMEOUT: Request timeout in seconds (default: 5)
    """
    
    BASE_URL = "https://abr.business.gov.au/abrxmlsearch/AbrXmlSearch.asmx"
    
    def __init__(self):
        """Initialize ABR client with configuration"""
        self.api_key = os.getenv("ABR_API_KEY")
        self.timeout = float(os.getenv("ABR_API_TIMEOUT", "5"))
        
        if not self.api_key or self.api_key == "your-abr-guid-here":
            raise ABRAuthenticationError(
                "ABR_API_KEY not configured. Get your free GUID from "
                "https://abr.business.gov.au/AbrXmlSearch/"
            )
        
        # Validate GUID format
        if not self._is_valid_guid(self.api_key):
            raise ABRAuthenticationError("ABR_API_KEY must be a valid GUID format")
    
    def _is_valid_guid(self, guid: str) -> bool:
        """Validate GUID format"""
        pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        return bool(re.match(pattern, guid.lower()))
    
    def _normalize_abn(self, abn: str) -> str:
        """
        Normalize ABN by removing spaces and validating format
        
        Args:
            abn: ABN string (with or without spaces)
            
        Returns:
            Normalized 11-digit ABN string
            
        Raises:
            ABRValidationError: If ABN format is invalid
        """
        normalized = re.sub(r'\s+', '', abn.strip())
        
        if not normalized.isdigit() or len(normalized) != 11:
            raise ABRValidationError(
                f"ABN must be 11 digits. Got: '{abn}' (normalized: '{normalized}')"
            )
        
        return normalized
    
    def _normalize_acn(self, acn: str) -> str:
        """
        Normalize ACN by removing spaces and validating format
        
        Args:
            acn: ACN string (with or without spaces)
            
        Returns:
            Normalized 9-digit ACN string
            
        Raises:
            ABRValidationError: If ACN format is invalid
        """
        normalized = re.sub(r'\s+', '', acn.strip())
        
        if not normalized.isdigit() or len(normalized) != 9:
            raise ABRValidationError(
                f"ACN must be 9 digits. Got: '{acn}' (normalized: '{normalized}')"
            )
        
        return normalized
    
    def _normalize_name(self, name: str) -> str:
        """
        Normalize compAny name for search
        
        Args:
            name: CompAny name string
            
        Returns:
            Normalized compAny name
            
        Raises:
            ABRValidationError: If name is empty or too short
        """
        normalized = name.strip()
        
        if len(normalized) < 2:
            raise ABRValidationError(
                f"CompAny name must be at least 2 characters. Got: '{name}'"
            )
        
        return normalized
    
    async def _make_request(
        self, 
        endpoint: str, 
        params: Dict[str, str],
        retries: int = 3
    ) -> str:
        """
        Make HTTP request to ABR API with retry logic
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            retries: Number of retry attempts
            
        Returns:
            XML response string
            
        Raises:
            ABRTimeoutError: If request times out
            ABRClientError: For other API errors
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        # Add authentication
        params["authenticationGuid"] = self.api_key
        
        for attempt in range(retries + 1):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        url,
                        params=params,
                        timeout=self.timeout
                    )
                    
                    # Log successful request
                    logger.info(
                        f"ABR API request successful: {endpoint} "
                        f"(attempt {attempt + 1}, status {response.status_code})"
                    )
                    
                    response.raise_for_status()
                    return response.text
                    
            except httpx.TimeoutException as e:
                if attempt == retries:
                    logger.error(f"ABR API timeout after {retries + 1} attempts: {e}")
                    raise ABRTimeoutError(
                        "Search is taking longer than expected. Try again or enter details manually."
                    )
                
                # Exponential backoff
                wait_time = 2 ** attempt
                logger.warning(f"ABR API timeout on attempt {attempt + 1}, retrying in {wait_time}s")
                await asyncio.sleep(wait_time)
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    raise ABRAuthenticationError("Invalid ABR API key")
                elif e.response.status_code == 403:
                    raise ABRAuthenticationError("ABR API access denied")
                else:
                    logger.error(f"ABR API HTTP error: {e.response.status_code} - {e.response.text}")
                    if attempt == retries:
                        raise ABRClientError(f"ABR API error: {e.response.status_code}")
                    await asyncio.sleep(2 ** attempt)
                    
            except Exception as e:
                logger.error(f"ABR API unexpected error on attempt {attempt + 1}: {e}")
                if attempt == retries:
                    raise ABRClientError(f"Unable to search ABR: {str(e)}")
                await asyncio.sleep(2 ** attempt)
        
        # This should never be reached due to raise statements above
        raise ABRClientError("Maximum retry attempts exceeded")
    
    def _parse_search_result(self, xml_content: str, search_type: str) -> List[Dict[str, Any]]:
        """
        Parse XML response into standardized result format
        
        Args:
            xml_content: XML response from ABR API
            search_type: Type of search ('ABN', 'ACN', 'Name')
            
        Returns:
            List of compAny details dictionaries
        """
        try:
            root = ET.fromstring(xml_content)
            
            # Handle different response structures based on search type
            if search_type in ['ABN', 'ACN']:
                return self._parse_single_entity_response(root)
            else:  # Name search
                return self._parse_name_search_response(root)
                
        except ET.ParseError as e:
            logger.error(f"Failed to parse ABR XML response: {e}")
            raise ABRClientError("Invalid response from ABR API")
    
    def _parse_single_entity_response(self, root: ET.Element) -> List[Dict[str, Any]]:
        """Parse single entity response (ABN/ACN search)"""
        results = []
        
        # Look for business entity in XML
        business_entity = root.find(".//businessEntity")
        if business_entity is not None:
            result = self._extract_entity_details(business_entity)
            if result:
                results.append(result)
        
        return results
    
    def _parse_name_search_response(self, root: ET.Element) -> List[Dict[str, Any]]:
        """Parse multiple entity response (name search)"""
        results = []
        
        # Look for multiple business entities
        business_entities = root.findall(".//searchResultsList/searchResultsRecord")
        
        for entity in business_entities[:10]:  # Limit to top 10 results
            result = self._extract_entity_details(entity)
            if result:
                results.append(result)
        
        return results
    
    def _extract_entity_details(self, entity_element: ET.Element) -> Optional[Dict[str, Any]]:
        """Extract compAny details from XML entity element"""
        try:
            # Extract basic fields with safe XML parsing
            abn = self._get_xml_text(entity_element, ".//ABN/identifierValue")
            legal_name = self._get_xml_text(entity_element, ".//legalName/fullName")
            entity_type = self._get_xml_text(entity_element, ".//entityType/entityTypeText")
            abn_status = self._get_xml_text(entity_element, ".//ABN/entityStatus/entityStatusCode")
            
            # GST registration
            gst_element = entity_element.find(".//goodsAndServicesTax")
            gst_registered = False
            if gst_element is not None:
                gst_status = self._get_xml_text(gst_element, "./entityStatus/entityStatusCode")
                gst_registered = gst_status == "Active"
            
            # Business address
            address_element = entity_element.find(".//mainBusinessPhysicalAddress")
            business_address = self._format_address(address_element) if address_element is not None else None
            
            # Only return result if we have essential data
            if not abn or not legal_name:
                return None
            
            return {
                "compAny_name": legal_name,
                "abn": abn,
                "abn_formatted": self._format_abn(abn) if abn else None,
                "gst_registered": gst_registered,
                "entity_type": entity_type or "Unknown",
                "business_address": business_address,
                "status": "Active" if abn_status == "Active" else abn_status or "Unknown"
            }
            
        except Exception as e:
            logger.warning(f"Failed to extract entity details: {e}")
            return None
    
    def _get_xml_text(self, element: ET.Element, xpath: str) -> Optional[str]:
        """Safely get text content from XML element"""
        found = element.find(xpath)
        return found.text.strip() if found is not None and found.text else None
    
    def _format_abn(self, abn: str) -> str:
        """Format ABN with spaces (12 345 678 901)"""
        if len(abn) == 11:
            return f"{abn[:2]} {abn[2:5]} {abn[5:8]} {abn[8:11]}"
        return abn
    
    def _format_address(self, address_element: ET.Element) -> Optional[str]:
        """Format business address from XML element"""
        try:
            parts = []
            
            # Street address
            street = self._get_xml_text(address_element, ".//addressLine")
            if street:
                parts.append(street)
            
            # Locality (suburb)
            locality = self._get_xml_text(address_element, ".//localityName")
            if locality:
                parts.append(locality)
            
            # State
            state = self._get_xml_text(address_element, ".//stateCode")
            if state:
                parts.append(state)
            
            # Postcode
            postcode = self._get_xml_text(address_element, ".//postcode")
            if postcode:
                parts.append(postcode)
            
            return ", ".join(parts) if parts else None
            
        except Exception:
            return None
    
    async def search_by_abn(self, abn: str) -> Optional[Dict[str, Any]]:
        """
        Search for compAny by ABN
        
        Args:
            abn: Australian Business Number (11 digits, with or without spaces)
            
        Returns:
            CompAny details dictionary or None if not found
            
        Raises:
            ABRValidationError: If ABN format is invalid
            ABRTimeoutError: If request times out
            ABRClientError: For other API errors
        """
        normalized_abn = self._normalize_abn(abn)
        
        logger.info(f"Searching ABR by ABN: {normalized_abn}")
        
        params = {
            "searchString": normalized_abn,
            "includeHistoricalDetails": "N",
            "authenticationGuid": self.api_key
        }
        
        xml_response = await self._make_request("SearchByABNv202001", params)
        results = self._parse_search_result(xml_response, "ABN")
        
        return results[0] if results else None
    
    async def search_by_acn(self, acn: str) -> Optional[Dict[str, Any]]:
        """
        Search for compAny by ACN
        
        Args:
            acn: Australian CompAny Number (9 digits, with or without spaces)
            
        Returns:
            CompAny details dictionary or None if not found
            
        Raises:
            ABRValidationError: If ACN format is invalid
            ABRTimeoutError: If request times out
            ABRClientError: For other API errors
        """
        normalized_acn = self._normalize_acn(acn)
        
        logger.info(f"Searching ABR by ACN: {normalized_acn}")
        
        params = {
            "searchString": normalized_acn,
            "includeHistoricalDetails": "N",
            "authenticationGuid": self.api_key
        }
        
        xml_response = await self._make_request("SearchByASICv202001", params)
        results = self._parse_search_result(xml_response, "ACN")
        
        return results[0] if results else None
    
    async def search_by_name(self, name: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for companies by name (fuzzy matching)
        
        Args:
            name: CompAny name (full or partial)
            max_results: Maximum number of results to return
            
        Returns:
            List of compAny details dictionaries (up to max_results)
            
        Raises:
            ABRValidationError: If name is invalid
            ABRTimeoutError: If request times out
            ABRClientError: For other API errors
        """
        normalized_name = self._normalize_name(name)
        
        logger.info(f"Searching ABR by name: '{normalized_name}'")
        
        params = {
            "name": normalized_name,
            "maxSearchResults": str(min(max_results, 200)),  # ABR API limit
            "authenticationGuid": self.api_key
        }
        
        xml_response = await self._make_request("ABRSearchByName", params)
        results = self._parse_search_result(xml_response, "Name")
        
        # Return up to max_results, sorted by relevance (exact matches first)
        sorted_results = self._sort_name_results(results, normalized_name)
        return sorted_results[:max_results]
    
    def _sort_name_results(self, results: List[Dict[str, Any]], search_name: str) -> List[Dict[str, Any]]:
        """Sort name search results by relevance"""
        def relevance_score(result: Dict[str, Any]) -> int:
            compAny_name = result.get("compAny_name", "").lower()
            search_lower = search_name.lower()
            
            # Exact match = highest score
            if compAny_name == search_lower:
                return 100
            
            # Starts with search term = high score
            if compAny_name.startswith(search_lower):
                return 80
            
            # Contains search term = medium score
            if search_lower in compAny_name:
                return 60
            
            # Default score
            return 0
        
        return sorted(results, key=relevance_score, reverse=True)


# Module-level client instance (singleton pattern)
_abr_client: Optional[ABRClient] = None


def get_abr_client() -> ABRClient:
    """
    Get ABR client instance (singleton)
    
    Returns:
        ABRClient instance
        
    Raises:
        ABRAuthenticationError: If API key not configured
    """
    global _abr_client
    
    if _abr_client is None:
        _abr_client = ABRClient()
    
    return _abr_client
