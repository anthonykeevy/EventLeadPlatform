"""
Security Utilities Module
Password hashing and verification using bcrypt
"""
import bcrypt


def hash_password(password: str, rounds: int = 12) -> str:
    """
    Hash a password using bcrypt with configurable cost factor.
    
    Args:
        password: Plain text password to hash
        rounds: Bcrypt cost factor (default 12, range 4-31)
                Higher values = more secure but slower
                
    Returns:
        Bcrypt hash string (UTF-8 decoded)
        
    Security Notes:
        - Cost factor 12 = ~300ms on modern hardware
        - Automatically includes salt generation
        - Hash format: $2b$12$<22-char-salt><31-char-hash>
        
    Example:
        >>> hashed = hash_password("MySecureP@ss123")
        >>> print(hashed[:7])  # Shows algorithm and cost
        $2b$12$
    """
    # Generate salt and hash password
    salt = bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # Return as UTF-8 string for database storage
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its bcrypt hash.
    
    Args:
        password: Plain text password to verify
        hashed_password: Bcrypt hash string from database
        
    Returns:
        True if password matches hash, False otherwise
        
    Example:
        >>> hashed = hash_password("MySecureP@ss123")
        >>> verify_password("MySecureP@ss123", hashed)
        True
        >>> verify_password("wrong_password", hashed)
        False
    """
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        # Handle invalid hash format or other errors
        return False
