"""
Password Strength Validation Module
Validates passwords meet security requirements for user signup
"""
import re
from typing import List, Dict, Any


def validate_password_strength(password: str) -> List[str]:
    """
    Validate password meets security requirements.
    
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    
    Args:
        password: The password string to validate
        
    Returns:
        List of error messages (empty list if password is valid)
        
    Example:
        >>> errors = validate_password_strength("weak")
        >>> if errors:
        ...     print(f"Invalid password: {', '.join(errors)}")
    """
    errors = []
    
    # Check minimum length
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    # Check for uppercase letter
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter")
    
    # Check for lowercase letter
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter")
    
    # Check for number
    if not re.search(r"\d", password):
        errors.append("Password must contain at least one number")
    
    # Check for special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\/'`~;]", password):
        errors.append("Password must contain at least one special character")
    
    return errors


def get_password_strength(password: str) -> Dict[str, Any]:
    """
    Get detailed password strength information.
    
    Args:
        password: The password string to analyze
        
    Returns:
        Dictionary with strength details:
        - is_valid: bool
        - score: int (0-5, based on criteria met)
        - errors: List[str]
        - strength: str ("weak", "medium", "strong")
    """
    errors = validate_password_strength(password)
    
    # Calculate score (each criteria met = 1 point)
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\/'`~;]", password):
        score += 1
    
    # Bonus point for length >= 12
    if len(password) >= 12:
        score += 1
    
    # Determine strength label
    if score <= 2:
        strength = "weak"
    elif score <= 4:
        strength = "medium"
    else:
        strength = "strong"
    
    return {
        "is_valid": len(errors) == 0,
        "score": score,
        "errors": errors,
        "strength": strength
    }

