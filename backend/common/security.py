"""
Security Utilities - Epic 1
Password hashing (bcrypt), token generation, validation, and security utilities
"""
import re
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
from passlib.context import CryptContext  # type: ignore

logger = logging.getLogger(__name__)

# Password hashing context with bcrypt (cost factor 12 per Solomon standards)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__default_rounds=12)


# ============================================================================
# CORE PASSWORD HASHING FUNCTIONS (AC-0.1.4)
# ============================================================================

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with cost factor 12.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        str: Bcrypt hashed password in format $2b$12$...
        
    Example:
        >>> hashed = hash_password("MySecurePass123!")
        >>> hashed.startswith("$2b$12$")
        True
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a bcrypt hash.
    Timing-attack resistant comparison.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hash to verify against
        
    Returns:
        bool: True if password matches hash, False otherwise
        
    Example:
        >>> hashed = hash_password("MySecurePass123!")
        >>> verify_password("MySecurePass123!", hashed)
        True
        >>> verify_password("WrongPassword", hashed)
        False
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification failed: {str(e)}")
        return False


def generate_secure_token(length: int = 32) -> str:
    """
    Generate cryptographically secure random token.
    Uses secrets.token_urlsafe for 256-bit security.
    
    Args:
        length: Token length in bytes (default 32 = 256 bits)
        
    Returns:
        str: URL-safe base64 encoded token
        
    Example:
        >>> token = generate_secure_token(32)
        >>> len(token) >= 40  # Base64 encoding makes it longer
        True
    """
    return secrets.token_urlsafe(length)


class SecurityUtils:
    """Security utilities for Epic 1"""
    
    # Password requirements
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 128
    REQUIRED_PASSWORD_CHARS = {
        'lowercase': r'[a-z]',
        'uppercase': r'[A-Z]',
        'digits': r'[0-9]',
        'special': r'[!@#$%^&*(),.?":{}|<>]'
    }
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """
        Validate password strength according to security requirements
        
        Args:
            password: Password to validate
            
        Returns:
            Dict with validation results
        """
        errors = []
        warnings = []
        
        # Check length
        if len(password) < SecurityUtils.MIN_PASSWORD_LENGTH:
            errors.append(f"Password must be at least {SecurityUtils.MIN_PASSWORD_LENGTH} characters long")
        
        if len(password) > SecurityUtils.MAX_PASSWORD_LENGTH:
            errors.append(f"Password must be no more than {SecurityUtils.MAX_PASSWORD_LENGTH} characters long")
        
        # Check character requirements
        for char_type, pattern in SecurityUtils.REQUIRED_PASSWORD_CHARS.items():
            if not re.search(pattern, password):
                if char_type == 'lowercase':
                    errors.append("Password must contain at least one lowercase letter")
                elif char_type == 'uppercase':
                    errors.append("Password must contain at least one uppercase letter")
                elif char_type == 'digits':
                    errors.append("Password must contain at least one number")
                elif char_type == 'special':
                    warnings.append("Consider adding special characters for better security")
        
        # Check for common weak patterns
        if re.search(r'(.)\1{2,}', password):
            warnings.append("Avoid repeating characters")
        
        if re.search(r'(123|abc|qwe|password|admin)', password.lower()):
            warnings.append("Avoid common patterns or words")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'strength_score': SecurityUtils._calculate_password_strength(password)
        }
    
    @staticmethod
    def _calculate_password_strength(password: str) -> int:
        """
        Calculate password strength score (0-100)
        
        Args:
            password: Password to score
            
        Returns:
            int: Strength score from 0-100
        """
        score = 0
        
        # Length score (0-40 points)
        if len(password) >= 8:
            score += 20
        if len(password) >= 12:
            score += 20
        
        # Character variety score (0-40 points)
        char_types = 0
        for pattern in SecurityUtils.REQUIRED_PASSWORD_CHARS.values():
            if re.search(pattern, password):
                char_types += 1
        
        score += char_types * 10
        
        # Complexity score (0-20 points)
        if len(set(password)) > len(password) * 0.7:  # 70% unique characters
            score += 10
        if not re.search(r'(.)\1{2,}', password):  # No repeated characters
            score += 10
        
        return min(score, 100)
    
    @staticmethod
    def validate_email_format(email: str) -> bool:
        """
        Validate email format using regex
        
        Args:
            email: Email address to validate
            
        Returns:
            bool: True if valid email format
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """
        Generate cryptographically secure random token (DEPRECATED - use module-level function)
        
        Args:
            length: Token length in bytes
            
        Returns:
            str: URL-safe base64 encoded token
        """
        return generate_secure_token(length)
    
    @staticmethod
    def generate_api_key() -> str:
        """
        Generate secure API key
        
        Returns:
            str: Secure API key
        """
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_sensitive_data(data: str, salt: Optional[str] = None) -> str:
        """
        Hash sensitive data with optional salt
        
        Args:
            data: Data to hash
            salt: Optional salt (generates random if not provided)
            
        Returns:
            str: Hashed data with salt
        """
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Combine data and salt
        combined = f"{data}{salt}"
        
        # Hash using SHA-256
        hash_obj = hashlib.sha256(combined.encode())
        hash_hex = hash_obj.hexdigest()
        
        # Return salt and hash combined
        return f"{salt}:{hash_hex}"
    
    @staticmethod
    def verify_hashed_data(data: str, hashed_data: str) -> bool:
        """
        Verify data against hashed version
        
        Args:
            data: Original data
            hashed_data: Salted hash to verify against
            
        Returns:
            bool: True if data matches hash
        """
        try:
            salt, hash_hex = hashed_data.split(':', 1)
            expected_hash = SecurityUtils.hash_sensitive_data(data, salt)
            return expected_hash == hashed_data
        except (ValueError, IndexError):
            return False
    
    @staticmethod
    def sanitize_input(input_str: str, max_length: int = 1000) -> str:
        """
        Sanitize user input to prevent injection attacks
        
        Args:
            input_str: Input string to sanitize
            max_length: Maximum allowed length
            
        Returns:
            str: Sanitized input
        """
        if not input_str:
            return ""
        
        # Truncate to max length
        sanitized = input_str[:max_length]
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`', '$']
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        # Remove multiple spaces
        sanitized = re.sub(r'\s+', ' ', sanitized)
        
        return sanitized.strip()
    
    @staticmethod
    def get_security_headers() -> Dict[str, str]:
        """
        Get security headers for HTTP responses
        
        Returns:
            Dict[str, str]: Security headers
        """
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
            'Referrer-Policy': 'strict-origin-when-cross-origin'
        }
    
    @staticmethod
    def is_rate_limit_exceeded(identifier: str, max_attempts: int = 5, window_minutes: int = 15) -> bool:
        """
        Check if rate limit is exceeded for an identifier
        
        Args:
            identifier: Unique identifier (IP, user ID, etc.)
            max_attempts: Maximum attempts allowed
            window_minutes: Time window in minutes
            
        Returns:
            bool: True if rate limit exceeded
        """
        # TODO: Implement actual rate limiting with Redis or database
        # For now, return False (no rate limiting)
        logger.warning(f"Rate limiting not implemented - identifier: {identifier}")
        return False
    
    @staticmethod
    def log_security_event(event_type: str, details: Dict[str, Any], severity: str = "INFO"):
        """
        Log security-related events
        
        Args:
            event_type: Type of security event
            details: Event details
            severity: Log severity level
        """
        log_message = f"SECURITY_EVENT: {event_type} - {details}"
        
        if severity == "ERROR":
            logger.error(log_message)
        elif severity == "WARNING":
            logger.warning(log_message)
        else:
            logger.info(log_message)

# Global security utils instance
security_utils = SecurityUtils()
