"""
Security Tests for Sensitive Data Filtering
Tests AC-0.2.9
"""
import pytest
from backend.common.log_filters import (
    is_sensitive_field,
    sanitize_dict,
    sanitize_list,
    sanitize_headers,
    sanitize_query_params,
    sanitize_stack_trace,
)


def test_is_sensitive_field_password():
    """Test AC-0.2.9: Password fields identified as sensitive"""
    assert is_sensitive_field("password") is True
    assert is_sensitive_field("Password") is True
    assert is_sensitive_field("user_password") is True
    assert is_sensitive_field("passwordHash") is True


def test_is_sensitive_field_token():
    """Test AC-0.2.9: Token fields identified as sensitive"""
    assert is_sensitive_field("token") is True
    assert is_sensitive_field("access_token") is True
    assert is_sensitive_field("refresh_token") is True
    assert is_sensitive_field("authToken") is True


def test_is_sensitive_field_api_key():
    """Test AC-0.2.9: API key fields identified as sensitive"""
    assert is_sensitive_field("api_key") is True
    assert is_sensitive_field("apiKey") is True
    assert is_sensitive_field("api-key") is True


def test_is_sensitive_field_non_sensitive():
    """Test: Non-sensitive fields not flagged"""
    assert is_sensitive_field("email") is False
    assert is_sensitive_field("username") is False
    assert is_sensitive_field("name") is False


def test_sanitize_dict_passwords():
    """Test AC-0.2.9: Passwords removed from dictionaries"""
    data = {
        "username": "testuser",
        "password": "SecurePassword123!",
        "email": "test@example.com"
    }
    
    sanitized = sanitize_dict(data)
    
    assert sanitized["username"] == "testuser"
    assert sanitized["password"] == "[REDACTED]"
    assert sanitized["email"] == "test@example.com"


def test_sanitize_dict_tokens():
    """Test AC-0.2.9: Tokens removed from dictionaries"""
    data = {
        "user_id": 123,
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh_token": "abc123def456"
    }
    
    sanitized = sanitize_dict(data)
    
    assert sanitized["user_id"] == 123
    assert sanitized["access_token"] == "[REDACTED]"
    assert sanitized["refresh_token"] == "[REDACTED]"


def test_sanitize_dict_nested():
    """Test AC-0.2.9: Nested dictionaries sanitized"""
    data = {
        "user": {
            "name": "Test User",
            "credentials": {
                "password": "secret123",
                "api_key": "key123"
            }
        }
    }
    
    sanitized = sanitize_dict(data)
    
    assert sanitized["user"]["name"] == "Test User"
    assert sanitized["user"]["credentials"]["password"] == "[REDACTED]"
    assert sanitized["user"]["credentials"]["api_key"] == "[REDACTED]"


def test_sanitize_list_with_dicts():
    """Test AC-0.2.9: Lists containing dictionaries sanitized"""
    data = [
        {"name": "User 1", "password": "pass1"},
        {"name": "User 2", "token": "token123"}
    ]
    
    sanitized = sanitize_list(data)
    
    assert sanitized[0]["name"] == "User 1"
    assert sanitized[0]["password"] == "[REDACTED]"
    assert sanitized[1]["token"] == "[REDACTED]"


def test_sanitize_headers_authorization():
    """Test AC-0.2.9: Authorization header removed"""
    headers = {
        "User-Agent": "TestClient/1.0",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "Content-Type": "application/json"
    }
    
    sanitized = sanitize_headers(headers)
    
    assert sanitized["User-Agent"] == "TestClient/1.0"
    assert sanitized["Authorization"] == "[REDACTED]"
    assert sanitized["Content-Type"] == "application/json"


def test_sanitize_query_params_tokens():
    """Test AC-0.2.9: Tokens in query params removed"""
    params = "key=value&token=abc123&name=test"
    
    sanitized = sanitize_query_params(params)
    
    assert "key=value" in sanitized
    assert "token=[REDACTED]" in sanitized
    assert "name=test" in sanitized
    assert "abc123" not in sanitized


def test_sanitize_query_params_empty():
    """Test: Empty query params handled"""
    assert sanitize_query_params("") == ""
    assert sanitize_query_params(None) is None


def test_sanitize_stack_trace_jwt_tokens():
    """Test AC-0.2.9: JWT tokens removed from stack traces"""
    stack_trace = """
    Traceback (most recent call last):
      File "auth.py", line 10
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"}
    """
    
    sanitized = sanitize_stack_trace(stack_trace)
    
    assert "Bearer [REDACTED]" in sanitized
    assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in sanitized


def test_sanitize_stack_trace_api_keys():
    """Test AC-0.2.9: API keys removed from stack traces"""
    stack_trace = """
    Error: Failed to authenticate
    api_key = "sk_live_1234567890abcdef1234567890abcdef"
    """
    
    sanitized = sanitize_stack_trace(stack_trace)
    
    assert "api_key=[REDACTED]" in sanitized
    assert "sk_live_1234567890abcdef1234567890abcdef" not in sanitized


def test_sanitize_stack_trace_passwords():
    """Test AC-0.2.9: Passwords removed from stack traces"""
    stack_trace = """
    Connection failed:
    password="MySecretPassword123!"
    """
    
    sanitized = sanitize_stack_trace(stack_trace)
    
    assert "password=[REDACTED]" in sanitized
    assert "MySecretPassword123!" not in sanitized


def test_sanitize_dict_max_depth():
    """Test: Max depth prevents infinite recursion"""
    # Create deeply nested structure
    data = {"level": 1}
    current = data
    for i in range(20):
        current["nested"] = {"level": i + 2}
        current = current["nested"]
    
    # Should not raise RecursionError
    sanitized = sanitize_dict(data, max_depth=10)
    
    assert sanitized is not None

