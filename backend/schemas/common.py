"""
Common Field Validators
Reusable validation functions for common field types
"""
import re
from typing import Any


def validate_email(email: str) -> str:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        str: Validated email (lowercased)
        
    Raises:
        ValueError: If email format is invalid
        
    Example:
        >>> validate_email("User@Example.COM")
        'user@example.com'
        >>> validate_email("invalid")
        Traceback (most recent call last):
        ...
        ValueError: Invalid email format
    """
    email = email.strip().lower()
    
    # Basic email pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        raise ValueError("Invalid email format")
    
    # Additional checks
    if '..' in email:
        raise ValueError("Email cannot contain consecutive dots")
    
    if email.startswith('.') or email.endswith('.'):
        raise ValueError("Email cannot start or end with a dot")
    
    return email


def validate_australian_phone(phone: str) -> str:
    """
    Validate and format Australian phone number.
    
    Accepts formats:
    - Mobile: 04XX XXX XXX, 614XX XXX XXX, +61 4XX XXX XXX
    - Landline: (0X) XXXX XXXX, 61X XXXX XXXX, +61 X XXXX XXXX
    
    Args:
        phone: Phone number to validate
        
    Returns:
        str: Formatted phone number in E.164 format (+61XXXXXXXXX)
        
    Raises:
        ValueError: If phone format is invalid
        
    Example:
        >>> validate_australian_phone("0412 345 678")
        '+61412345678'
        >>> validate_australian_phone("+61 2 9999 8888")
        '+61299998888'
    """
    # Remove all non-digit characters except leading +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Remove leading + if present
    if cleaned.startswith('+'):
        cleaned = cleaned[1:]
    
    # Handle different formats
    if cleaned.startswith('61'):
        # Already in international format
        cleaned = cleaned[2:]
    elif cleaned.startswith('0'):
        # Remove leading 0
        cleaned = cleaned[1:]
    
    # Validate length (should be 9 digits after removing country code and leading 0)
    if len(cleaned) != 9:
        raise ValueError("Invalid Australian phone number length")
    
    # Validate mobile (starts with 4) or landline (starts with 2-8)
    if not cleaned[0].isdigit() or cleaned[0] == '0' or cleaned[0] == '9':
        raise ValueError("Invalid Australian phone number format")
    
    return f"+61{cleaned}"


def validate_abn(abn: str) -> str:
    """
    Validate Australian Business Number (ABN).
    
    Validates format (11 digits) and checksum algorithm.
    
    Args:
        abn: ABN to validate
        
    Returns:
        str: Validated ABN (digits only)
        
    Raises:
        ValueError: If ABN format or checksum is invalid
        
    Example:
        >>> validate_abn("51 824 753 556")
        '51824753556'
        >>> validate_abn("12345678901")
        Traceback (most recent call last):
        ...
        ValueError: Invalid ABN checksum
    """
    # Remove all non-digit characters
    cleaned = re.sub(r'\D', '', abn)
    
    if len(cleaned) != 11:
        raise ValueError("ABN must be 11 digits")
    
    # Validate checksum using ABN algorithm
    weights = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    
    # Subtract 1 from first digit
    digits = [int(cleaned[0]) - 1] + [int(d) for d in cleaned[1:]]
    
    # Calculate weighted sum
    total = sum(digit * weight for digit, weight in zip(digits, weights))
    
    if total % 89 != 0:
        raise ValueError("Invalid ABN checksum")
    
    return cleaned


def validate_acn(acn: str) -> str:
    """
    Validate Australian Company Number (ACN).
    
    Validates format (9 digits) and checksum algorithm.
    
    Args:
        acn: ACN to validate
        
    Returns:
        str: Validated ACN (digits only)
        
    Raises:
        ValueError: If ACN format or checksum is invalid
        
    Example:
        >>> validate_acn("123 456 782")
        '123456782'
        >>> validate_acn("123456789")
        Traceback (most recent call last):
        ...
        ValueError: Invalid ACN checksum
    """
    # Remove all non-digit characters
    cleaned = re.sub(r'\D', '', acn)
    
    if len(cleaned) != 9:
        raise ValueError("ACN must be 9 digits")
    
    # Validate checksum using ACN algorithm
    weights = [8, 7, 6, 5, 4, 3, 2, 1]
    
    # Calculate weighted sum for first 8 digits
    digits = [int(d) for d in cleaned[:8]]
    total = sum(digit * weight for digit, weight in zip(digits, weights))
    
    # Calculate check digit
    remainder = total % 10
    check_digit = (10 - remainder) % 10
    
    if int(cleaned[8]) != check_digit:
        raise ValueError("Invalid ACN checksum")
    
    return cleaned

