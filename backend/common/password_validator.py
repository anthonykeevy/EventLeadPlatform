"""
Password Strength Validation Module
Validates passwords meet security requirements for user signup

Updated for Story 1.13: Password rules now read from database (ConfigurationService)
"""
import re
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from common.config_service import ConfigurationService


def validate_password_strength(db: Session, password: str) -> List[str]:
    """
    Validate password meets security requirements.
    
    Story 1.13: Requirements read from database (config.AppSetting)
    - PASSWORD_MIN_LENGTH (default: 8)
    - PASSWORD_REQUIRE_UPPERCASE (default: False)
    - PASSWORD_REQUIRE_NUMBER (default: True)
    
    Args:
        db: Database session (for ConfigurationService)
        password: The password string to validate
        
    Returns:
        List of error messages (empty list if password is valid)
        
    Example:
        >>> errors = validate_password_strength(db, "weak")
        >>> if errors:
        ...     print(f"Invalid password: {', '.join(errors)}")
    """
    config = ConfigurationService(db)
    errors = []
    
    # Get configurable requirements from database
    min_length = config.get_password_min_length()
    require_uppercase = config.get_password_require_uppercase()
    require_number = config.get_password_require_number()
    
    # Check minimum length (configurable)
    if len(password) < min_length:
        errors.append(f"Password must be at least {min_length} characters long")
    
    # Check for uppercase letter (configurable)
    if require_uppercase and not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter")
    
    # Always require lowercase letter (not configurable in Epic 1)
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter")
    
    # Check for number (configurable)
    if require_number and not re.search(r"\d", password):
        errors.append("Password must contain at least one number")
    
    # Special character is optional in Epic 1 (not enforced)
    # Can be added to AppSetting in future epic if needed
    
    return errors


def get_password_strength(db: Session, password: str) -> Dict[str, Any]:
    """
    Get detailed password strength information.
    
    Story 1.13: Uses configurable password requirements from database
    
    Args:
        db: Database session (for ConfigurationService)
        password: The password string to analyze
        
    Returns:
        Dictionary with strength details:
        - is_valid: bool
        - score: int (0-5, based on criteria met)
        - errors: List[str]
        - strength: str ("weak", "medium", "strong")
    """
    config = ConfigurationService(db)
    errors = validate_password_strength(db, password)
    
    # Get configurable min length
    min_length = config.get_password_min_length()
    
    # Calculate score (each criteria met = 1 point)
    score = 0
    if len(password) >= min_length:
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

