"""
Unit Tests for ABN/ACN Validators

Tests Story 1.5 AC-1.5.9: ABN/ACN validation with checksums
"""
import pytest
from common.validators import validate_abn, validate_acn, validate_australian_business_number


# ============================================================================
# ABN Validation Tests
# ============================================================================

def test_valid_abn_accepted():
    """Test that valid ABN passes checksum validation"""
    # Known valid ABN: 51 824 753 556
    is_valid, error = validate_abn("51824753556")
    assert is_valid is True
    assert error == ""


def test_valid_abn_with_spaces():
    """Test that valid ABN with spaces is normalized and accepted"""
    is_valid, error = validate_abn("51 824 753 556")
    assert is_valid is True
    assert error == ""


def test_invalid_abn_checksum():
    """Test that ABN with invalid checksum is rejected"""
    is_valid, error = validate_abn("12345678901")
    assert is_valid is False
    assert "checksum" in error.lower()


def test_abn_wrong_length():
    """Test that ABN with wrong length is rejected"""
    # Too short
    is_valid, error = validate_abn("1234567890")
    assert is_valid is False
    assert "11 digits" in error
    
    # Too long
    is_valid, error = validate_abn("123456789012")
    assert is_valid is False
    assert "11 digits" in error


def test_abn_non_numeric():
    """Test that ABN with non-numeric characters is rejected"""
    is_valid, error = validate_abn("5182475355A")
    assert is_valid is False
    assert "digits" in error.lower()


def test_abn_empty_string():
    """Test that empty ABN is accepted (optional field)"""
    is_valid, error = validate_abn("")
    assert is_valid is True
    assert error == ""


def test_abn_none():
    """Test that None ABN is accepted (optional field)"""
    is_valid, error = validate_abn(None)
    assert is_valid is True
    assert error == ""


def test_multiple_valid_abns():
    """Test multiple known valid ABNs"""
    valid_abns = [
        "51824753556",  # Standard test ABN
        "53 004 085 616",  # Another valid ABN with spaces
    ]
    
    for abn in valid_abns:
        is_valid, error = validate_abn(abn)
        assert is_valid is True, f"ABN {abn} should be valid"


# ============================================================================
# ACN Validation Tests
# ============================================================================

def test_valid_acn_accepted():
    """Test that valid ACN passes checksum validation"""
    # Known valid ACN: 123 456 782
    is_valid, error = validate_acn("123456782")
    assert is_valid is True
    assert error == ""


def test_valid_acn_with_spaces():
    """Test that valid ACN with spaces is normalized and accepted"""
    is_valid, error = validate_acn("123 456 782")
    assert is_valid is True
    assert error == ""


def test_invalid_acn_checksum():
    """Test that ACN with invalid checksum is rejected"""
    is_valid, error = validate_acn("123456789")
    assert is_valid is False
    assert "checksum" in error.lower()


def test_acn_wrong_length():
    """Test that ACN with wrong length is rejected"""
    # Too short
    is_valid, error = validate_acn("12345678")
    assert is_valid is False
    assert "9 digits" in error
    
    # Too long
    is_valid, error = validate_acn("1234567890")
    assert is_valid is False
    assert "9 digits" in error


def test_acn_non_numeric():
    """Test that ACN with non-numeric characters is rejected"""
    is_valid, error = validate_acn("12345678A")
    assert is_valid is False
    assert "digits" in error.lower()


def test_acn_empty_string():
    """Test that empty ACN is accepted (optional field)"""
    is_valid, error = validate_acn("")
    assert is_valid is True
    assert error == ""


def test_acn_none():
    """Test that None ACN is accepted (optional field)"""
    is_valid, error = validate_acn(None)
    assert is_valid is True
    assert error == ""


def test_multiple_valid_acns():
    """Test multiple known valid ACNs"""
    valid_acns = [
        "123456782",  # Standard test ACN
        "004 085 616",  # Another valid ACN with spaces
    ]
    
    for acn in valid_acns:
        is_valid, error = validate_acn(acn)
        assert is_valid is True, f"ACN {acn} should be valid"


# ============================================================================
# Combined ABN/ACN Validation Tests
# ============================================================================

def test_validate_both_abn_and_acn():
    """Test combined validation of both ABN and ACN"""
    is_valid, error = validate_australian_business_number(
        abn="51824753556",
        acn="123456782"
    )
    assert is_valid is True
    assert error == ""


def test_validate_only_abn():
    """Test validation with only ABN provided"""
    is_valid, error = validate_australian_business_number(abn="51824753556")
    assert is_valid is True
    assert error == ""


def test_validate_only_acn():
    """Test validation with only ACN provided"""
    is_valid, error = validate_australian_business_number(acn="123456782")
    assert is_valid is True
    assert error == ""


def test_validate_neither():
    """Test validation with neither ABN nor ACN provided"""
    is_valid, error = validate_australian_business_number()
    assert is_valid is True
    assert error == ""


def test_invalid_abn_in_combined():
    """Test that invalid ABN is caught in combined validation"""
    is_valid, error = validate_australian_business_number(
        abn="12345678901",
        acn="123456782"
    )
    assert is_valid is False
    assert "ABN" in error


def test_invalid_acn_in_combined():
    """Test that invalid ACN is caught in combined validation"""
    is_valid, error = validate_australian_business_number(
        abn="51824753556",
        acn="123456789"
    )
    assert is_valid is False
    assert "ACN" in error


# ============================================================================
# Edge Cases and Security
# ============================================================================

def test_abn_with_leading_zeros():
    """Test ABN with leading zeros is handled correctly"""
    # ABNs can have leading zeros
    is_valid, error = validate_abn("00000000000")
    # This will fail checksum, which is correct behavior
    assert is_valid is False


def test_sql_injection_attempt():
    """Test that SQL injection attempts in ABN/ACN are rejected"""
    malicious_inputs = [
        "51824753556'; DROP TABLE Company;--",
        "123456782' OR '1'='1",
    ]
    
    for malicious in malicious_inputs:
        is_valid, error = validate_abn(malicious)
        assert is_valid is False
        
        is_valid, error = validate_acn(malicious)
        assert is_valid is False


def test_unicode_and_special_characters():
    """Test that unicode and special characters are rejected"""
    invalid_inputs = [
        "518247535😀6",
        "51824753556\x00",
        "518247\n53556",
    ]
    
    for invalid in invalid_inputs:
        is_valid, error = validate_abn(invalid)
        assert is_valid is False

