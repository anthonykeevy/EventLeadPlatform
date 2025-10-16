"""
Unit Tests for Security Module
Tests password hashing and verification
"""
import pytest
from common.security import hash_password, verify_password


class TestPasswordHashing:
    """Test suite for password hashing and verification"""
    
    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string"""
        hashed = hash_password("TestPassword123!")
        assert isinstance(hashed, str)
        assert len(hashed) > 0
    
    def test_hash_password_is_bcrypt_format(self):
        """Test that hashed password follows bcrypt format"""
        hashed = hash_password("TestPassword123!")
        # Bcrypt hashes start with $2b$ (version identifier)
        assert hashed.startswith("$2b$")
        # Bcrypt hashes have cost factor (default 12)
        assert "$12$" in hashed
    
    def test_hash_password_unique_hashes(self):
        """Test that same password generates different hashes (due to salt)"""
        password = "TestPassword123!"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        # Hashes should be different due to different salts
        assert hash1 != hash2
    
    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "TestPassword123!"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "TestPassword123!"
        wrong_password = "WrongPassword123!"
        hashed = hash_password(password)
        assert verify_password(wrong_password, hashed) is False
    
    def test_verify_password_case_sensitive(self):
        """Test that password verification is case-sensitive"""
        password = "TestPassword123!"
        hashed = hash_password(password)
        assert verify_password("testpassword123!", hashed) is False
    
    def test_verify_password_invalid_hash(self):
        """Test password verification with invalid hash format"""
        password = "TestPassword123!"
        invalid_hash = "not_a_valid_hash"
        assert verify_password(password, invalid_hash) is False
    
    def test_hash_password_custom_rounds(self):
        """Test password hashing with custom cost factor"""
        password = "TestPassword123!"
        # Lower cost factor for testing (faster)
        hashed = hash_password(password, rounds=4)
        assert hashed.startswith("$2b$")
        assert "$04$" in hashed
        # Verify still works
        assert verify_password(password, hashed) is True
    
    def test_hash_password_unicode(self):
        """Test password hashing with Unicode characters"""
        password = "Tëst🔐Pässwörd123!"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
    
    def test_hash_password_long(self):
        """Test password hashing with very long password"""
        password = "A" * 100 + "1!aB"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
    
    def test_hash_password_empty_string(self):
        """Test password hashing with empty string"""
        password = ""
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
