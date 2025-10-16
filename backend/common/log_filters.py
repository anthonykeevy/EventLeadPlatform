"""
Sensitive Data Filtering for Logs
Ensures passwords, tokens, and secrets are never logged
"""
import re
from typing import Any, Dict, List


# Patterns for sensitive field names (case-insensitive)
SENSITIVE_FIELD_PATTERNS = [
    r"password",
    r"passwd",
    r"pwd",
    r"token",
    r"secret",
    r"api[_-]?key",
    r"apikey",
    r"auth",
    r"authorization",
    r"credential",
    r"private[_-]?key",
    r"access[_-]?token",
    r"refresh[_-]?token",
    r"session[_-]?id",
    r"csrf",
    r"xsrf",
]


def is_sensitive_field(field_name: str) -> bool:
    """
    Check if a field name matches sensitive patterns.
    
    Args:
        field_name: Field name to check
        
    Returns:
        True if field is sensitive, False otherwise
    """
    for pattern in SENSITIVE_FIELD_PATTERNS:
        if re.search(pattern, field_name, re.IGNORECASE):
            return True
    return False


def sanitize_dict(data: Dict[str, Any], max_depth: int = 10) -> Dict[str, Any]:
    """
    Recursively sanitize dictionary, replacing sensitive values with [REDACTED].
    
    Args:
        data: Dictionary to sanitize
        max_depth: Maximum recursion depth (prevents infinite loops)
        
    Returns:
        Sanitized dictionary with sensitive values removed
    """
    if max_depth <= 0:
        return {"_truncated": "Max depth reached"}
    
    sanitized: Dict[str, Any] = {}
    for key, value in data.items():
        # Check if key matches sensitive patterns
        if is_sensitive_field(key):
            sanitized[key] = "[REDACTED]"
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, max_depth - 1)
        elif isinstance(value, list):
            sanitized[key] = sanitize_list(value, max_depth - 1)
        else:
            sanitized[key] = value
    
    return sanitized


def sanitize_list(data: List[Any], max_depth: int = 10) -> List[Any]:
    """
    Recursively sanitize list items.
    
    Args:
        data: List to sanitize
        max_depth: Maximum recursion depth
        
    Returns:
        Sanitized list with sensitive values removed
    """
    if max_depth <= 0:
        return ["_truncated"]
    
    sanitized: List[Any] = []
    for item in data:
        if isinstance(item, dict):
            sanitized.append(sanitize_dict(item, max_depth - 1))
        elif isinstance(item, list):
            sanitized.append(sanitize_list(item, max_depth - 1))
        else:
            sanitized.append(item)
    
    return sanitized


def sanitize_headers(headers: Dict[str, str]) -> Dict[str, str]:
    """
    Sanitize HTTP headers, removing Authorization and other sensitive headers.
    
    Args:
        headers: HTTP headers dictionary
        
    Returns:
        Sanitized headers
    """
    sanitized: Dict[str, str] = {}
    for key, value in headers.items():
        if is_sensitive_field(key):
            sanitized[key] = "[REDACTED]"
        else:
            sanitized[key] = value
    
    return sanitized


def sanitize_query_params(params: str) -> str:
    """
    Sanitize query parameters string, removing sensitive values.
    
    Args:
        params: Query string (e.g., "key=value&token=abc123")
        
    Returns:
        Sanitized query string
    """
    if not params:
        return params
    
    # Split into key=value pairs
    pairs = params.split("&")
    sanitized_pairs = []
    
    for pair in pairs:
        if "=" in pair:
            key, value = pair.split("=", 1)
            if is_sensitive_field(key):
                sanitized_pairs.append(f"{key}=[REDACTED]")
            else:
                sanitized_pairs.append(pair)
        else:
            sanitized_pairs.append(pair)
    
    return "&".join(sanitized_pairs)


def sanitize_stack_trace(stack_trace: str) -> str:
    """
    Sanitize stack trace, removing potential sensitive data from error messages.
    
    This is a basic implementation - for production, consider more sophisticated filtering.
    
    Args:
        stack_trace: Stack trace string
        
    Returns:
        Sanitized stack trace
    """
    if not stack_trace:
        return stack_trace
    
    # Replace common patterns that might leak secrets
    sanitized = stack_trace
    
    # Replace JWT tokens (Bearer xxx...)
    sanitized = re.sub(
        r"Bearer\s+[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+",
        "Bearer [REDACTED]",
        sanitized,
        flags=re.IGNORECASE
    )
    
    # Replace API keys (common patterns)
    sanitized = re.sub(
        r"(api[_-]?key|apikey|token|secret)['\"]?\s*[:=]\s*['\"]?[A-Za-z0-9\-_]{16,}['\"]?",
        r"\1=[REDACTED]",
        sanitized,
        flags=re.IGNORECASE
    )
    
    # Replace passwords in connection strings
    sanitized = re.sub(
        r"(password|pwd)['\"]?\s*[:=]\s*['\"]?[^;'\"\s]+['\"]?",
        r"\1=[REDACTED]",
        sanitized,
        flags=re.IGNORECASE
    )
    
    return sanitized

