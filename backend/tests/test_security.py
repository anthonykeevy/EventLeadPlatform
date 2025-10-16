"""
Test Security Utilities (AC-0.1.4)
Validates password hashing (bcrypt) and token generation
"""
import pytest
import re
from backend.common.security import hash_password, verify_password, generate_secure_token


def test_hash_password_produces_bcrypt_format():
    """Test that password hashing produces bcrypt format $2b$12$..."""
    password = "MySecurePassword123!"
    hashed = hash_password(password)
    
    # Verify bcrypt format
    assert hashed.startswith("$2b$12$"), f"Expected bcrypt format $2b$12$..., got {hashed[:10]}"
    assert len(hashed) == 60, f"Expected 60 character bcrypt hash, got {len(hashed)}"


def test_hash_password_different_hashes():
    """Test that same password produces different hashes (due to salt)."""
    password = "MySecurePassword123!"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    assert hash1 != hash2, "Same password should produce different hashes due to salt"


def test_verify_password_correct():
    """Test password verification with correct password."""
    password = "MySecurePassword123!"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Test password verification with incorrect password."""
    password = "MySecurePassword123!"
    hashed = hash_password(password)
    
    assert verify_password("WrongPassword", hashed) is False
    assert verify_password("MySecurePassword123", hashed) is False  # Missing !
    assert verify_password("mySecurePassword123!", hashed) is False  # Wrong case


def test_verify_password_timing_attack_resistant():
    """Test that password verification is timing-attack resistant."""
    import time
    
    password = "MySecurePassword123!"
    hashed = hash_password(password)
    
    # Measure time for correct password
    start = time.time()
    verify_password(password, hashed)
    correct_time = time.time() - start
    
    # Measure time for incorrect password
    start = time.time()
    verify_password("WrongPassword", hashed)
    incorrect_time = time.time() - start
    
    # Times should be similar (within 10ms) - bcrypt is constant-time
    time_diff = abs(correct_time - incorrect_time)
    assert time_diff < 0.01, f"Timing difference too large: {time_diff}s (potential timing attack vulnerability)"


def test_verify_password_invalid_hash():
    """Test password verification with invalid hash."""
    result = verify_password("password", "invalid_hash")
    assert result is False


def test_generate_secure_token_default_length():
    """Test token generation with default length (32 bytes)."""
    token = generate_secure_token()
    
    # URL-safe base64 encoding of 32 bytes produces ~43 characters
    assert len(token) >= 40, f"Expected token length >= 40 chars, got {len(token)}"
    assert len(token) <= 50, f"Expected token length <= 50 chars, got {len(token)}"
    
    # Verify URL-safe characters only
    assert re.match(r'^[A-Za-z0-9_-]+$', token), "Token should only contain URL-safe characters"


def test_generate_secure_token_custom_length():
    """Test token generation with custom length."""
    token_16 = generate_secure_token(16)
    token_64 = generate_secure_token(64)
    
    # 16 bytes ~= 22 chars, 64 bytes ~= 86 chars
    assert 20 <= len(token_16) <= 25
    assert 85 <= len(token_64) <= 90


def test_generate_secure_token_uniqueness():
    """Test that generated tokens are unique."""
    tokens = set()
    for _ in range(100):
        token = generate_secure_token()
        tokens.add(token)
    
    # All 100 tokens should be unique
    assert len(tokens) == 100, "Generated tokens should be unique"


def test_generate_secure_token_entropy():
    """Test that generated tokens have high entropy (cryptographically secure)."""
    token = generate_secure_token(32)
    
    # Check character distribution (should have good variety)
    char_types = {
        'uppercase': any(c.isupper() for c in token),
        'lowercase': any(c.islower() for c in token),
        'digits': any(c.isdigit() for c in token),
        'special': any(c in '_-' for c in token)
    }
    
    # Should have at least 2 different character types
    assert sum(char_types.values()) >= 2, "Token should have good character variety"


def test_password_hashing_cost_factor():
    """Test that bcrypt uses cost factor 12 (balance security/performance)."""
    import time
    
    password = "MySecurePassword123!"
    
    # Measure hashing time
    start = time.time()
    hash_password(password)
    duration = time.time() - start
    
    # Cost factor 12 should take ~0.1-0.5 seconds
    # This is a rough check - actual time varies by hardware
    assert 0.05 < duration < 2.0, f"Hashing time {duration}s seems wrong for cost factor 12"


def test_password_max_length():
    """Test password hashing with very long passwords."""
    # Bcrypt has a 72 byte limit, but we should handle longer passwords gracefully
    long_password = "A" * 200
    hashed = hash_password(long_password)
    
    assert verify_password(long_password, hashed) is True


def test_password_special_characters():
    """Test password hashing with special characters."""
    passwords = [
        "P@ssw0rd!",
        "Test#123$",
        "Spëcïål€haracters",
        "密码123",  # Unicode characters
        "Pass\nWord",  # Newline
        "Pass\tWord",  # Tab
    ]
    
    for password in passwords:
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True, f"Failed for password: {password}"

