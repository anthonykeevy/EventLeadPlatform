"""
Unit Tests for Password Validator
Tests password strength validation logic
"""
import pytest
from common.password_validator import validate_password_strength, get_password_strength


@pytest.fixture
def password_policy_defaults(monkeypatch):
    """Use deterministic password policy defaults for validator unit tests."""
    class MockConfigurationService:
        def __init__(self, db):
            self.db = db

        def get_password_min_length(self):
            return 8

        def get_password_require_uppercase(self):
            return False

        def get_password_require_number(self):
            return True

    monkeypatch.setattr("common.password_validator.ConfigurationService", MockConfigurationService)


class TestPasswordValidator:
    """Test suite for password validation"""
    
    def test_strong_password_passes(self, test_db, password_policy_defaults):
        """Test that a strong password passes all validations"""
        password = "StrongP@ss123"
        errors = validate_password_strength(test_db, password)
        assert errors == [], f"Strong password should not have errors, got: {errors}"
    
    def test_minimum_length_validation(self, test_db, password_policy_defaults):
        """Test minimum length requirement (8 characters)"""
        short_password = "Pass1!"
        errors = validate_password_strength(test_db, short_password)
        assert any("at least 8 characters" in error for error in errors)
    
    def test_uppercase_not_required_by_default(self, test_db, password_policy_defaults):
        """Uppercase rule is currently configurable and disabled by default."""
        no_upper = "password123!"
        errors = validate_password_strength(test_db, no_upper)
        assert not any("uppercase" in error.lower() for error in errors)
    
    def test_lowercase_requirement(self, test_db, password_policy_defaults):
        """Test lowercase letter requirement"""
        no_lower = "PASSWORD123!"
        errors = validate_password_strength(test_db, no_lower)
        assert any("lowercase" in error.lower() for error in errors)
    
    def test_number_requirement(self, test_db, password_policy_defaults):
        """Test number requirement"""
        no_number = "Password!"
        errors = validate_password_strength(test_db, no_number)
        assert any("number" in error.lower() for error in errors)
    
    def test_special_character_not_required(self, test_db, password_policy_defaults):
        """Special character is currently optional in validator contract."""
        no_special = "Password123"
        errors = validate_password_strength(test_db, no_special)
        assert not any("special character" in error.lower() for error in errors)
    
    def test_multiple_validation_errors(self, test_db, password_policy_defaults):
        """Test that multiple errors are returned for very weak passwords"""
        weak_password = "weak"
        errors = validate_password_strength(test_db, weak_password)
        assert len(errors) >= 2, "Weak password should have multiple errors"
    
    def test_get_password_strength_weak(self, test_db, password_policy_defaults):
        """Test password strength scoring - weak password"""
        result = get_password_strength(test_db, "weak")
        assert result["is_valid"] is False
        assert result["strength"] == "weak"
        assert result["score"] <= 2
    
    def test_get_password_strength_medium(self, test_db, password_policy_defaults):
        """Test password strength scoring - medium password"""
        result = get_password_strength(test_db, "Password1!")
        assert result["is_valid"] is True
        assert result["strength"] in ["medium", "strong"]
        assert result["score"] >= 3
    
    def test_get_password_strength_strong(self, test_db, password_policy_defaults):
        """Test password strength scoring - strong password"""
        result = get_password_strength(test_db, "VeryStr0ng!Password123")
        assert result["is_valid"] is True
        assert result["strength"] == "strong"
        assert result["score"] >= 5
    
    def test_special_characters_variety(self, test_db, password_policy_defaults):
        """Test that various special characters are accepted"""
        special_chars = "!@#$%^&*(),.?\":{}|<>_-+=[]\\/'`~;"
        for char in special_chars:
            password = f"Password1{char}"
            errors = validate_password_strength(test_db, password)
            assert errors == [], f"Password with special char '{char}' should be valid"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


