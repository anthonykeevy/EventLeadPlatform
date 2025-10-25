"""
Company Ownership Verification Utilities
Story 1.19: Email domain verification to prevent squatter attacks

Verifies if a user likely works for a company based on email domain matching.
"""
import re
from typing import Tuple
from common.logger import get_logger

logger = get_logger(__name__)


def normalize_company_name(company_name: str) -> str:
    """
    Extract base company name for domain matching
    
    Examples:
    - "Atlassian Pty Ltd" → "atlassian"
    - "REA Group Limited" → "reagroup"  
    - "Inchcape Australia Limited" → "inchcape"
    - "Canva Pty. Ltd." → "canva"
    
    Args:
        company_name: Full legal company name
        
    Returns:
        Normalized base name (lowercase, alphanumeric only)
    """
    # Convert to lowercase
    normalized = company_name.lower()
    
    # Remove common legal suffixes (order matters - remove longer patterns first)
    legal_suffixes = [
        r'\s+pty\s*limited',
        r'\s+pty\s*ltd',
        r'\s+proprietary\s+limited',
        r'\s+limited',
        r'\s+ltd',
        r'\s+incorporated',
        r'\s+inc',
        r'\s+corporation',
        r'\s+corp',
        # Keep geographic and business type modifiers (Group, Australia)
        # These are part of the company brand, not legal suffixes
    ]
    
    for suffix in legal_suffixes:
        normalized = re.sub(suffix + r'\.?$', '', normalized)
    
    # Remove all non-alphanumeric characters
    normalized = re.sub(r'[^a-z0-9]', '', normalized)
    
    return normalized.strip()


def extract_email_domain(email: str) -> str:
    """
    Extract domain from email address
    
    Examples:
    - "alice@atlassian.com" → "atlassian.com"
    - "bob@mail.canva.com.au" → "mail.canva.com.au"
    
    Args:
        email: User email address
        
    Returns:
        Email domain (everything after @)
    """
    return email.split('@')[1].lower() if '@' in email else ''


def normalize_domain_for_matching(domain: str) -> str:
    """
    Normalize domain for company name matching
    
    Examples:
    - "atlassian.com" → "atlassian"
    - "atlassian.com.au" → "atlassian"
    - "mail.canva.com" → "canva" (removes subdomain)
    
    Args:
        domain: Email domain
        
    Returns:
        Normalized domain name for matching
    """
    # Remove common TLDs
    domain = domain.replace('.com.au', '')
    domain = domain.replace('.com', '')
    domain = domain.replace('.net.au', '')
    domain = domain.replace('.net', '')
    domain = domain.replace('.org.au', '')
    domain = domain.replace('.org', '')
    domain = domain.replace('.edu.au', '')
    domain = domain.replace('.gov.au', '')
    
    # Remove common subdomains
    domain = domain.replace('mail.', '')
    domain = domain.replace('email.', '')
    domain = domain.replace('smtp.', '')
    
    # Remove dots and special characters
    domain = re.sub(r'[^a-z0-9]', '', domain)
    
    return domain.strip()


def verify_email_domain_ownership(user_email: str, company_name: str) -> Tuple[bool, str]:
    """
    Verify if user's email domain indicates they likely work for the company
    
    Story 1.19: Prevent squatter attacks while allowing legitimate users
    
    Examples:
    - alice@atlassian.com + "Atlassian Pty Ltd" → TRUE (domain matches)
    - bob@gmail.com + "Atlassian Pty Ltd" → FALSE (generic email)
    - competitor@evil.com + "Atlassian Pty Ltd" → FALSE (different company)
    
    Args:
        user_email: User's email address
        company_name: Company legal name from ABR
        
    Returns:
        Tuple of (is_verified: bool, reason: str)
        
    Examples:
        (True, "Email domain 'atlassian.com' matches company name")
        (False, "Email domain 'gmail.com' is a generic provider")
        (False, "Email domain 'competitor.com' doesn't match company name")
    """
    email_domain = extract_email_domain(user_email)
    
    if not email_domain:
        return False, "Invalid email format"
    
    # Check for generic email providers (never verify)
    generic_providers = [
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
        'live.com', 'msn.com', 'icloud.com', 'me.com',
        'mail.com', 'aol.com', 'protonmail.com', 'yandex.com'
    ]
    
    for provider in generic_providers:
        if email_domain.endswith(provider):
            return False, f"Email domain '{email_domain}' is a generic email provider"
    
    # Normalize both for comparison
    normalized_company = normalize_company_name(company_name)
    normalized_domain = normalize_domain_for_matching(email_domain)
    
    # Check if company name appears in domain (primary match)
    if normalized_company in normalized_domain:
        logger.info(
            f"Email domain verification SUCCESS: '{email_domain}' matches company '{company_name}' "
            f"(normalized: '{normalized_domain}' contains '{normalized_company}')"
        )
        return True, f"Email domain '{email_domain}' matches company name"
    
    # Check if domain appears in company name (reverse match)
    # IMPORTANT: Only match if domain is substantial (>=4 chars) to avoid false positives
    # Example: "atlas" (5 chars) should NOT match "atlassian"
    if len(normalized_domain) >= 4 and normalized_domain in normalized_company:
        # Additional check: Domain should be at least 70% of company name length
        # Prevents: "atlas.com" (5) matching "atlassian" (9) - only 55% match
        match_percentage = len(normalized_domain) / len(normalized_company)
        
        if match_percentage >= 0.7:
            logger.info(
                f"Email domain verification SUCCESS (reverse match): '{normalized_company}' contains '{normalized_domain}' "
                f"(match percentage: {match_percentage:.0%})"
            )
            return True, f"Company name contains email domain '{email_domain}'"
        else:
            logger.info(
                f"Email domain verification FAILED (insufficient match): '{normalized_domain}' in '{normalized_company}' "
                f"but only {match_percentage:.0%} match (need >=70%)"
            )
            return False, f"Email domain '{email_domain}' is only partial match ({match_percentage:.0%})"
    
    # No match
    logger.info(
        f"Email domain verification FAILED: '{email_domain}' doesn't match company '{company_name}' "
        f"(normalized domain: '{normalized_domain}', normalized company: '{normalized_company}')"
    )
    return False, f"Email domain '{email_domain}' doesn't match company name"


def should_auto_join_company(user_email: str, company_name: str) -> bool:
    """
    Simplified check: Should user auto-join existing company?
    
    Returns True if email domain matches company name
    """
    is_verified, _ = verify_email_domain_ownership(user_email, company_name)
    return is_verified

