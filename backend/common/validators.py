"""
Common Validators Module
Business validation logic for various data types
"""
import re
from typing import Tuple, Optional


def validate_abn(abn: str) -> Tuple[bool, str]:
    """
    Validate Australian Business Number (ABN) format and checksum.
    
    ABN Format:
    - 11 digits
    - Weighted checksum algorithm
    - Weights: [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    - Subtract 1 from first digit before applying weight
    - Sum of weighted digits must be divisible by 89
    
    Args:
        abn: ABN string (may contain spaces)
        
    Returns:
        Tuple of (is_valid, error_message)
        
    Examples:
        >>> validate_abn("51 824 753 556")
        (True, "")
        >>> validate_abn("12 345 678 901")
        (False, "Invalid ABN checksum")
    """
    if not abn:
        return True, ""  # Optional field
    
    # Remove spaces and non-digits
    abn_digits = re.sub(r'[^\d]', '', abn)
    
    # Check length
    if len(abn_digits) != 11:
        return False, "ABN must be 11 digits"
    
    # Check all numeric
    if not abn_digits.isdigit():
        return False, "ABN must contain only digits"
    
    # Validate checksum
    weights = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    digits = [int(d) for d in abn_digits]
    
    # Subtract 1 from first digit
    digits[0] -= 1
    
    # Calculate weighted sum
    weighted_sum = sum(d * w for d, w in zip(digits, weights))
    
    # Check divisibility by 89
    if weighted_sum % 89 != 0:
        return False, "Invalid ABN checksum"
    
    return True, ""


def validate_acn(acn: str) -> Tuple[bool, str]:
    """
    Validate Australian Company Number (ACN) format and checksum.
    
    ACN Format:
    - 9 digits
    - Weighted checksum algorithm
    - Weights: [8, 7, 6, 5, 4, 3, 2, 1] for first 8 digits
    - Last digit is check digit
    - (10 - (sum mod 10)) mod 10 = check digit
    
    Args:
        acn: ACN string (may contain spaces)
        
    Returns:
        Tuple of (is_valid, error_message)
        
    Examples:
        >>> validate_acn("123 456 782")
        (True, "")
        >>> validate_acn("123 456 789")
        (False, "Invalid ACN checksum")
    """
    if not acn:
        return True, ""  # Optional field
    
    # Remove spaces and non-digits
    acn_digits = re.sub(r'[^\d]', '', acn)
    
    # Check length
    if len(acn_digits) != 9:
        return False, "ACN must be 9 digits"
    
    # Check all numeric
    if not acn_digits.isdigit():
        return False, "ACN must contain only digits"
    
    # Validate checksum
    weights = [8, 7, 6, 5, 4, 3, 2, 1]
    digits = [int(d) for d in acn_digits]
    
    # Calculate weighted sum for first 8 digits
    weighted_sum = sum(d * w for d, w in zip(digits[:8], weights))
    
    # Calculate expected check digit
    remainder = weighted_sum % 10
    expected_check = (10 - remainder) % 10
    
    # Compare with actual check digit
    if digits[8] != expected_check:
        return False, "Invalid ACN checksum"
    
    return True, ""


def validate_australian_business_number(abn: Optional[str] = None, acn: Optional[str] = None) -> Tuple[bool, str]:
    """
    Validate ABN and/or ACN.
    
    Both are optional, but if provided must be valid.
    
    Args:
        abn: ABN string (optional)
        acn: ACN string (optional)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if abn:
        is_valid, error = validate_abn(abn)
        if not is_valid:
            return False, f"ABN: {error}"
    
    if acn:
        is_valid, error = validate_acn(acn)
        if not is_valid:
            return False, f"ACN: {error}"
    
    return True, ""

