"""
Unit Tests for Password Validator
Tests password strength validation logic
"""
import pytest
from common.password_validator import validate_password_strength, get_password_strength


class TestPasswordValidator:
    """Test suite for password validation"""
    
    def test_strong_password_passes(self):
        """Test that a strong password passes all validations"""
        password = "StrongP@ss123"
        errors = validate_password_strength(password)
        assert errors == [], f"Strong password should not have errors, got: {errors}"
    
    def test_minimum_length_validation(self):
        """Test minimum length requirement (8 characters)"""
        short_password = "Pass1!"
        errors = validate_password_strength(short_password)
        assert any("at least 8 characters" in error for error in errors)
    
    def test_uppercase_requirement(self):
        """Test uppercase letter requirement"""
        no_upper = "password123!"
        errors = validate_password_strength(no_upper)
        assert any("uppercase" in error.lower() for error in errors)
    
    def test_lowercase_requirement(self):
        """Test lowercase letter requirement"""
        no_lower = "PASSWORD123!"
        errors = validate_password_strength(no_lower)
        assert any("lowercase" in error.lower() for error in errors)
    
    def test_number_requirement(self):
        """Test number requirement"""
        no_number = "Password!"
        errors = validate_password_strength(no_number)
        assert any("number" in error.lower() for error in errors)
    
    def test_special_character_requirement(self):
        """Test special character requirement"""
        no_special = "Password123"
        errors = validate_password_strength(no_special)
        assert any("special character" in error.lower() for error in errors)
    
    def test_multiple_validation_errors(self):
        """Test that multiple errors are returned for very weak passwords"""
        weak_password = "weak"
        errors = validate_password_strength(weak_password)
        assert len(errors) >= 4, "Weak password should have multiple errors"
    
    def test_get_password_strength_weak(self):
        """Test password strength scoring - weak password"""
        result = get_password_strength("weak")
        assert result["is_valid"] is False
        assert result["strength"] == "weak"
        assert result["score"] <= 2
    
    def test_get_password_strength_medium(self):
        """Test password strength scoring - medium password"""
        result = get_password_strength("Password1!")
        assert result["is_valid"] is True
        assert result["strength"] in ["medium", "strong"]
        assert result["score"] >= 3
    
    def test_get_password_strength_strong(self):
        """Test password strength scoring - strong password"""
        result = get_password_strength("VeryStr0ng!Password123")
        assert result["is_valid"] is True
        assert result["strength"] == "strong"
        assert result["score"] >= 5
    
    def test_special_characters_variety(self):
        """Test that various special characters are accepted"""
        special_chars = "!@#$%^&*(),.?\":{}|<>_-+=[]\\/'`~;"
        for char in special_chars:
            password = f"Password1{char}"
            errors = validate_password_strength(password)
            assert errors == [], f"Password with special char '{char}' should be valid"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

