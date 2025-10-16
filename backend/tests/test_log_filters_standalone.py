"""
Standalone Tests for Sensitive Data Filtering (No FastAPI dependencies)
Tests AC-0.2.9
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from common.log_filters import (
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
    print("[OK] Password fields correctly identified")


def test_is_sensitive_field_token():
    """Test AC-0.2.9: Token fields identified as sensitive"""
    assert is_sensitive_field("token") is True
    assert is_sensitive_field("access_token") is True
    assert is_sensitive_field("refresh_token") is True
    assert is_sensitive_field("authToken") is True
    print("[OK] Token fields correctly identified")


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
    print("[OK] Passwords correctly redacted from dictionaries")


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
    print("[OK] Authorization headers correctly redacted")


def test_sanitize_query_params_tokens():
    """Test AC-0.2.9: Tokens in query params removed"""
    params = "key=value&token=abc123&name=test"
    
    sanitized = sanitize_query_params(params)
    
    assert "key=value" in sanitized
    assert "token=[REDACTED]" in sanitized
    assert "name=test" in sanitized
    assert "abc123" not in sanitized
    print("[OK] Query params correctly sanitized")


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
    print("[OK] Stack traces correctly sanitized")


if __name__ == "__main__":
    print("Running standalone log filter tests...\n")
    test_is_sensitive_field_password()
    test_is_sensitive_field_token()
    test_sanitize_dict_passwords()
    test_sanitize_headers_authorization()
    test_sanitize_query_params_tokens()
    test_sanitize_stack_trace_jwt_tokens()
    print("\n[PASS] All log filter tests passed!")

