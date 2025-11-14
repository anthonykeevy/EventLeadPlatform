"""
Smart Field Inference Service
Business logic for intelligent field pre-filling
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func, distinct
from typing import Optional, List, Dict, Any
from datetime import datetime

from models.ref.timezone import Timezone
from models.ref.country import Country
from models.user import User
from models.company import Company
from models.company_billing_details import CompanyBillingDetails
from models.event import Event
from common.logger import get_logger

logger = get_logger(__name__)

# Mapping of timezone identifier patterns to country codes
# This covers common IANA timezone patterns
TIMEZONE_TO_COUNTRY_MAP = {
    # Australia
    "Australia/Sydney": "AU",
    "Australia/Melbourne": "AU",
    "Australia/Brisbane": "AU",
    "Australia/Perth": "AU",
    "Australia/Adelaide": "AU",
    "Australia/Darwin": "AU",
    "Australia/Hobart": "AU",
    
    # United States
    "America/New_York": "US",
    "America/Chicago": "US",
    "America/Denver": "US",
    "America/Los_Angeles": "US",
    "America/Phoenix": "US",
    "America/Anchorage": "US",
    "America/Detroit": "US",
    
    # Canada
    "America/Toronto": "CA",
    "America/Vancouver": "CA",
    "America/Montreal": "CA",
    "America/Winnipeg": "CA",
    "America/Edmonton": "CA",
    "America/Halifax": "CA",
    
    # United Kingdom
    "Europe/London": "GB",
    
    # Europe
    "Europe/Paris": "FR",
    "Europe/Berlin": "DE",
    "Europe/Madrid": "ES",
    "Europe/Rome": "IT",
    "Europe/Amsterdam": "NL",
    "Europe/Brussels": "BE",
    "Europe/Vienna": "AT",
    "Europe/Zurich": "CH",
    
    # New Zealand
    "Pacific/Auckland": "NZ",
    "Pacific/Christchurch": "NZ",
    
    # Asia
    "Asia/Tokyo": "JP",
    "Asia/Shanghai": "CN",
    "Asia/Hong_Kong": "HK",
    "Asia/Singapore": "SG",
    "Asia/Dubai": "AE",
    "Asia/Kolkata": "IN",
    "Asia/Bangkok": "TH",
    "Asia/Seoul": "KR",
    
    # Middle East
    "Asia/Dubai": "AE",
    "Asia/Riyadh": "SA",
    "Asia/Jerusalem": "IL",
    
    # South America
    "America/Sao_Paulo": "BR",
    "America/Buenos_Aires": "AR",
    "America/Santiago": "CL",
    "America/Mexico_City": "MX",
}


def infer_country_code_from_timezone(timezone_identifier: str) -> Optional[str]:
    """
    Infer country code from IANA timezone identifier.
    
    Uses pattern matching and a mapping dictionary to determine country code.
    
    Args:
        timezone_identifier: IANA timezone identifier (e.g., 'Australia/Sydney')
        
    Returns:
        ISO 2-letter country code if found, None otherwise
    """
    # First check direct mapping
    if timezone_identifier in TIMEZONE_TO_COUNTRY_MAP:
        return TIMEZONE_TO_COUNTRY_MAP[timezone_identifier]
    
    # Try pattern matching: many IANA timezones follow "Country/City" format
    parts = timezone_identifier.split('/')
    if len(parts) >= 2:
        country_part = parts[0]
        
        # Direct country name matches (e.g., "Australia/Sydney" → "AU")
        country_name_to_code = {
            "Australia": "AU",
            "America": "US",  # Default for America/, but check specific cities
            "Europe": None,  # Too generic, need specific city
            "Asia": None,  # Too generic, need specific city
            "Africa": None,  # Too generic, need specific city
            "Pacific": None,  # Too generic, need specific city
            "Atlantic": None,  # Too generic, need specific city
        }
        
        if country_part in country_name_to_code:
            country_code = country_name_to_code[country_part]
            if country_code:
                return country_code
            
            # For "America/", check if it's US or Canada
            if country_part == "America":
                city = parts[1].lower()
                # Canadian cities
                if any(canadian_city in city for canadian_city in ['toronto', 'vancouver', 'montreal', 'winnipeg', 'edmonton', 'halifax', 'ottawa', 'calgary']):
                    return "CA"
                # Mexican cities
                elif any(mexican_city in city for mexican_city in ['mexico', 'tijuana', 'cancun', 'guadalajara']):
                    return "MX"
                # Brazilian cities
                elif any(brazilian_city in city for brazilian_city in ['sao_paulo', 'rio', 'brasilia', 'recife']):
                    return "BR"
                # Argentine cities
                elif any(argentine_city in city for argentine_city in ['buenos_aires', 'cordoba']):
                    return "AR"
                # Chilean cities
                elif any(chilean_city in city for chilean_city in ['santiago']):
                    return "CL"
                # Default to US for America/
                else:
                    return "US"
    
    return None


async def fetch_country_from_external_api(timezone_identifier: str) -> Optional[str]:
    """
    Fetch country code from external timezone API (fallback).
    
    Uses a free timezone API to get country information.
    
    Args:
        timezone_identifier: IANA timezone identifier
        
    Returns:
        ISO 2-letter country code if found, None otherwise
    """
    try:
        # Try using TimeZoneDB API (free tier available)
        # You can also use other APIs like WorldTimeAPI, etc.
        # For now, we'll use a simple approach with timezone identifier parsing
        
        # Note: External APIs may require API keys and have rate limits
        # This is a placeholder - implement with your preferred API
        logger.debug(f"External API lookup not implemented for timezone: {timezone_identifier}")
        return None
    except Exception as e:
        logger.warning(f"Error fetching from external API: {str(e)}")
        return None


async def get_country_from_timezone(
    db: Session,
    timezone_identifier: str
) -> Optional[Dict[str, Any]]:
    """
    Get country information from timezone identifier.
    
    Strategy:
    1. Check database first (fastest)
    2. If timezone exists but no CountryCode, infer and update database
    3. If timezone doesn't exist, infer country code and create/update timezone record
    4. Return country information
    
    Args:
        db: Database session
        timezone_identifier: IANA timezone identifier (e.g., 'Australia/Sydney')
        
    Returns:
        Dict with country_id and country_code if found, None otherwise
    """
    try:
        # Step 1: Try to infer country code from timezone identifier (works without database)
        country_code = infer_country_code_from_timezone(timezone_identifier)
        logger.info(f"[TIMEZONE-INFERENCE] Step 1: Inferred country code '{country_code}' from timezone '{timezone_identifier}'")
        
        # Step 2: If inference failed, try external API (optional)
        if not country_code:
            logger.debug(f"[TIMEZONE-INFERENCE] Step 2: Inference failed for '{timezone_identifier}', trying external API")
            country_code = await fetch_country_from_external_api(timezone_identifier)
        
        # Step 3: Try to check/update database if Timezone table exists (graceful fallback)
        timezone = None
        try:
            logger.debug(f"[TIMEZONE-INFERENCE] Step 3: Attempting to check Timezone table for '{timezone_identifier}'")
            timezone = db.execute(
                select(Timezone).where(Timezone.TimezoneIdentifier == timezone_identifier)
            ).scalar_one_or_none()
            
            # If timezone exists in DB and has CountryCode, prefer that (might be more accurate)
            if timezone and timezone.CountryCode:
                country_code = timezone.CountryCode
                logger.info(f"[TIMEZONE-INFERENCE] Using country code '{country_code}' from database for timezone '{timezone_identifier}'")
            elif country_code:
                # Update database with inferred country code if found
                logger.info(f"[TIMEZONE-INFERENCE] Updating database with country code '{country_code}' for timezone '{timezone_identifier}'")
                if timezone:
                    # Update existing timezone record
                    timezone.CountryCode = country_code
                    timezone.UpdatedDate = datetime.utcnow()
                    logger.info(f"[TIMEZONE-INFERENCE] Updated timezone {timezone_identifier} with country code {country_code}")
                else:
                    # Create new timezone record (basic info)
                    # Note: You may want to fetch more timezone details from an API
                    new_timezone = Timezone(
                        TimezoneIdentifier=timezone_identifier,
                        DisplayName=timezone_identifier.replace('_', ' ').replace('/', ' / '),
                        OffsetMinutes=0,  # Would need to fetch actual offset
                        CountryCode=country_code,
                        CreatedDate=datetime.utcnow()
                    )
                    db.add(new_timezone)
                    logger.info(f"[TIMEZONE-INFERENCE] Created new timezone {timezone_identifier} with country code {country_code}")
                
                # Commit the database changes
                try:
                    db.commit()
                    # Refresh to get updated timezone
                    if timezone:
                        db.refresh(timezone)
                    else:
                        timezone = db.execute(
                            select(Timezone).where(Timezone.TimezoneIdentifier == timezone_identifier)
                        ).scalar_one_or_none()
                except Exception as commit_error:
                    logger.warning(f"[TIMEZONE-INFERENCE] Error committing timezone update: {str(commit_error)} - continuing without database update")
                    db.rollback()
                    # Continue without database update - we still have the inferred country_code
        except Exception as db_error:
            # Timezone table doesn't exist or other DB error - that's fine, use inference only
            logger.info(f"[TIMEZONE-INFERENCE] Timezone table not available (expected if table doesn't exist), using inference only. Error: {str(db_error)[:200]}")
            timezone = None
        
        # Step 4: Get country by country code
        if not country_code:
            logger.warning(f"[TIMEZONE-INFERENCE] Step 4: Could not determine country code for timezone: {timezone_identifier}")
            return None
        
        logger.info(f"[TIMEZONE-INFERENCE] Step 4: Looking up country with code: '{country_code}' in Country table")
        try:
            country = db.execute(
                select(Country).where(Country.CountryCode == country_code)
            ).scalar_one_or_none()
        except Exception as country_lookup_error:
            logger.error(f"[TIMEZONE-INFERENCE] Error looking up country '{country_code}': {str(country_lookup_error)}", exc_info=True)
            return None
        
        if not country:
            logger.error(f"[TIMEZONE-INFERENCE] Country not found in database for code: '{country_code}' (timezone: {timezone_identifier})")
            logger.error(f"[TIMEZONE-INFERENCE] This means the Country table doesn't have a record with CountryCode='{country_code}'")
            return None
        
        logger.info(f"[TIMEZONE-INFERENCE] SUCCESS: Found country: {country.CountryName} ({country.CountryCode}) for timezone: {timezone_identifier}")
        
        return {
            "country_id": country.CountryID,
            "country_code": country.CountryCode,
            "country_name": country.CountryName,
            "timezone_identifier": timezone_identifier,
            "timezone_display_name": timezone.DisplayName if timezone else timezone_identifier.replace('_', ' ').replace('/', ' / ')
        }
    except Exception as e:
        # Log the full error for debugging
        logger.error(f"Error getting country from timezone: {str(e)}", exc_info=True)
        # Only rollback if we have an active transaction
        try:
            db.rollback()
        except:
            pass  # No active transaction to rollback
        return None


async def get_user_profile_with_location(
    db: Session,
    user_id: int
) -> Dict[str, Any]:
    """
    Get user profile with timezone and country information.
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        Dict with user profile including timezone and country
    """
    try:
        user = db.execute(
            select(User).options(
                joinedload(User.country)
            ).where(User.UserID == user_id)
        ).scalar_one_or_none()
        
        if not user:
            return None
        
        result = {
            "user_id": user.UserID,
            "timezone_identifier": user.TimezoneIdentifier,
            "country_id": user.CountryID,
            "country_code": user.country.CountryCode if user.country else None,
            "country_name": user.country.CountryName if user.country else None
        }
        
        # If country not set but timezone is, try to infer country from timezone
        if not result["country_id"] and user.TimezoneIdentifier:
            country_info = await get_country_from_timezone(db, user.TimezoneIdentifier)
            if country_info:
                result["country_id"] = country_info["country_id"]
                result["country_code"] = country_info["country_code"]
                result["country_name"] = country_info["country_name"]
        
        return result
    except Exception as e:
        logger.error(f"Error getting user profile with location: {str(e)}", exc_info=True)
        return None


async def get_company_profile_with_billing(
    db: Session,
    company_id: int
) -> Dict[str, Any]:
    """
    Get company profile with billing city information.
    
    Args:
        db: Database session
        company_id: Company ID
        
    Returns:
        Dict with company profile including billing city
    """
    try:
        company = db.execute(
            select(Company).options(
                joinedload(Company.billing_details)
            ).where(Company.CompanyID == company_id)
        ).scalar_one_or_none()
        
        if not company:
            return None
        
        billing_details = company.billing_details
        
        result = {
            "company_id": company.CompanyID,
            "company_name": company.CompanyName,
            "country_id": company.CountryID,
            "billing_city": billing_details.BillingCity if billing_details else None,
            "billing_state": billing_details.BillingState if billing_details else None,
            "billing_country_id": billing_details.BillingCountryID if billing_details else None
        }
        
        return result
    except Exception as e:
        logger.error(f"Error getting company profile with billing: {str(e)}", exc_info=True)
        return None


async def get_recent_event_cities(
    db: Session,
    user_id: int,
    limit: int = 5
) -> List[str]:
    """
    Get user's recently used cities from their events.
    
    Args:
        db: Database session
        user_id: User ID
        limit: Maximum number of cities to return
        
    Returns:
        List of unique city names, most recent first
    """
    try:
        # Get events created by this user (from their companies)
        # First, get user's companies
        from models.user_company import UserCompany
        from models.ref.user_company_status import UserCompanyStatus
        
        user_companies = db.execute(
            select(UserCompany.CompanyID).join(UserCompanyStatus).where(
                UserCompany.UserID == user_id,
                UserCompany.IsDeleted == False,
                UserCompanyStatus.StatusCode == "active"
            )
        ).scalars().all()
        
        if not user_companies:
            return []
        
        # Get distinct cities from events created by user's companies, ordered by most recent
        # SQL Server: Use a subquery with GROUP BY to get distinct cities with max date
        # Then use TOP to limit results
        from sqlalchemy import text
        
        # Build parameterized query for SQL Server
        # Use SQLAlchemy's select() instead of raw SQL for better parameter binding
        # This avoids SQL injection and parameter binding issues
        from sqlalchemy import select, func
        
        # Use SQLAlchemy ORM query instead of raw SQL for better compatibility
        cities_query = (
            select(
                Event.City.label('city'),
                func.max(Event.CreatedDate).label('last_used')
            )
            .where(
                Event.CompanyID.in_(user_companies),
                Event.City.isnot(None),
                Event.City != '',
                Event.IsDeleted == False
            )
            .group_by(Event.City)
            .order_by(func.max(Event.CreatedDate).desc())
            .limit(limit)
        )
        
        cities_result = db.execute(cities_query).all()
        
        # Extract city names from result tuples
        # Result format: (city, last_used) tuples
        city_list = [row[0] for row in cities_result if row[0]]
        
        logger.info(f"Found {len(city_list)} recent cities for user {user_id}")
        
        return city_list
    except Exception as e:
        logger.error(f"Error getting recent event cities: {str(e)}", exc_info=True)
        return []

