"""
Unit Tests for JWT Service
Tests JWT token creation, decoding, and validation
"""
import pytest
from datetime import datetime, timedelta
from jose import jwt, JWTError

from modules.auth.jwt_service import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token_type,
    extract_user_id,
    is_token_expired
)
from config.jwt import get_secret_key, get_algorithm


class TestJWTService:
    """Test suite for JWT service"""
    
    def test_create_access_token_minimal(self):
        """Test creating access token with minimal claims"""
        token = create_access_token(
            user_id=123,
            email="test@example.com"
        )
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Decode and verify
        payload = decode_token(token)
        assert payload["sub"] == 123
        assert payload["email"] == "test@example.com"
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload
    
    def test_create_access_token_with_role_and_company(self):
        """Test creating access token with role and company claims"""
        token = create_access_token(
            user_id=123,
            email="test@example.com",
            role="admin",
            company_id=456
        )
        
        payload = decode_token(token)
        assert payload["sub"] == 123
        assert payload["email"] == "test@example.com"
        assert payload["role"] == "admin"
        assert payload["company_id"] == 456
        assert payload["type"] == "access"
    
    def test_access_token_expiry(self):
        """Test access token has correct expiry (1 hour)"""
        token = create_access_token(123, "test@example.com")
        payload = decode_token(token)
        
        exp = datetime.fromtimestamp(payload["exp"])
        iat = datetime.fromtimestamp(payload["iat"])
        
        # Should be approximately 1 hour (3600 seconds)
        time_diff = (exp - iat).total_seconds()
        assert 3550 <= time_diff <= 3650  # Allow 50 second tolerance
    
    def test_create_refresh_token(self):
        """Test creating refresh token"""
        token = create_refresh_token(user_id=123)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Decode and verify
        payload = decode_token(token)
        assert payload["sub"] == 123
        assert payload["type"] == "refresh"
        assert "exp" in payload
        assert "iat" in payload
        # Refresh tokens should not have email, role, or company_id
        assert "email" not in payload
        assert "role" not in payload
        assert "company_id" not in payload
    
    def test_refresh_token_expiry(self):
        """Test refresh token has correct expiry (7 days)"""
        token = create_refresh_token(123)
        payload = decode_token(token)
        
        exp = datetime.fromtimestamp(payload["exp"])
        iat = datetime.fromtimestamp(payload["iat"])
        
        # Should be approximately 7 days
        time_diff = (exp - iat).total_seconds()
        expected = 7 * 24 * 3600  # 7 days in seconds
        assert expected - 100 <= time_diff <= expected + 100  # Allow tolerance
    
    def test_decode_valid_token(self):
        """Test decoding a valid token"""
        token = create_access_token(123, "test@example.com")
        payload = decode_token(token)
        
        assert payload["sub"] == 123
        assert payload["email"] == "test@example.com"
    
    def test_decode_invalid_token(self):
        """Test decoding an invalid token raises error"""
        invalid_token = "invalid.jwt.token"
        
        with pytest.raises(JWTError):
            decode_token(invalid_token)
    
    def test_decode_tampered_token(self):
        """Test decoding a tampered token raises error"""
        token = create_access_token(123, "test@example.com")
        # Tamper with the token
        parts = token.split('.')
        tampered_token = parts[0] + ".tampered." + parts[2]
        
        with pytest.raises(JWTError):
            decode_token(tampered_token)
    
    def test_verify_token_type_access(self):
        """Test verifying access token type"""
        token = create_access_token(123, "test@example.com")
        payload = decode_token(token)
        
        assert verify_token_type(payload, "access") is True
        assert verify_token_type(payload, "refresh") is False
    
    def test_verify_token_type_refresh(self):
        """Test verifying refresh token type"""
        token = create_refresh_token(123)
        payload = decode_token(token)
        
        assert verify_token_type(payload, "refresh") is True
        assert verify_token_type(payload, "access") is False
    
    def test_extract_user_id(self):
        """Test extracting user ID from token payload"""
        token = create_access_token(123, "test@example.com")
        payload = decode_token(token)
        
        user_id = extract_user_id(payload)
        assert user_id == 123
    
    def test_extract_user_id_from_refresh_token(self):
        """Test extracting user ID from refresh token"""
        token = create_refresh_token(456)
        payload = decode_token(token)
        
        user_id = extract_user_id(payload)
        assert user_id == 456
    
    def test_is_token_expired_not_expired(self):
        """Test checking if non-expired token is valid"""
        token = create_access_token(123, "test@example.com")
        payload = decode_token(token)
        
        assert is_token_expired(payload) is False
    
    def test_token_uniqueness(self):
        """Test that tokens are unique (different even for same user)"""
        token1 = create_access_token(123, "test@example.com")
        token2 = create_access_token(123, "test@example.com")
        
        # Tokens should be different due to different iat timestamps
        assert token1 != token2
    
    def test_optional_claims_omitted(self):
        """Test that optional claims are omitted when not provided"""
        token = create_access_token(123, "test@example.com")
        payload = decode_token(token)
        
        assert "role" not in payload
        assert "company_id" not in payload


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

