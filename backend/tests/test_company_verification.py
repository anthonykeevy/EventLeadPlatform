"""
Tests for Company Ownership Verification
Story 1.19: Email domain verification to prevent squatter attacks
"""
import pytest
from common.company_verification import (
    normalize_company_name,
    extract_email_domain,
    normalize_domain_for_matching,
    verify_email_domain_ownership,
    should_auto_join_company
)


class TestNormalizeCompanyName:
    """Test company name normalization"""
    
    def test_removes_pty_ltd(self):
        assert normalize_company_name("Atlassian Pty Ltd") == "atlassian"
    
    def test_removes_limited(self):
        # "Group" is kept as it's part of the brand name
        assert normalize_company_name("REA Group Limited") == "reagroup"
    
    def test_removes_inc(self):
        assert normalize_company_name("Canva Inc.") == "canva"
    
    def test_removes_australia_suffix(self):
        # "Australia" is kept as it's part of the brand name
        assert normalize_company_name("Inchcape Australia Limited") == "inchcapeaustralia"
    
    def test_removes_special_characters(self):
        # "Australia" is kept, only &special chars removed
        assert normalize_company_name("AT&T Australia Pty Ltd") == "attaustralia"
    
    def test_handles_lowercase(self):
        assert normalize_company_name("ATLASSIAN PTY LTD") == "atlassian"


class TestExtractEmailDomain:
    """Test email domain extraction"""
    
    def test_extracts_simple_domain(self):
        assert extract_email_domain("alice@atlassian.com") == "atlassian.com"
    
    def test_extracts_au_domain(self):
        assert extract_email_domain("bob@canva.com.au") == "canva.com.au"
    
    def test_extracts_subdomain(self):
        assert extract_email_domain("user@mail.example.com") == "mail.example.com"
    
    def test_handles_uppercase(self):
        assert extract_email_domain("Alice@ATLASSIAN.COM") == "atlassian.com"


class TestNormalizeDomainForMatching:
    """Test domain normalization for matching"""
    
    def test_removes_com(self):
        assert normalize_domain_for_matching("atlassian.com") == "atlassian"
    
    def test_removes_com_au(self):
        assert normalize_domain_for_matching("canva.com.au") == "canva"
    
    def test_removes_mail_subdomain(self):
        assert normalize_domain_for_matching("mail.atlassian.com") == "atlassian"


class TestVerifyEmailDomainOwnership:
    """Test email domain ownership verification"""
    
    # ============================================================================
    # SUCCESS Cases (Domain Matches)
    # ============================================================================
    
    def test_perfect_match(self):
        is_verified, reason = verify_email_domain_ownership(
            "alice@atlassian.com",
            "Atlassian Pty Ltd"
        )
        assert is_verified is True
        assert "matches" in reason.lower()
    
    def test_match_with_com_au(self):
        is_verified, reason = verify_email_domain_ownership(
            "alice@canva.com.au",
            "Canva Pty Ltd"
        )
        assert is_verified is True
    
    def test_match_with_subdomain(self):
        is_verified, reason = verify_email_domain_ownership(
            "alice@mail.atlassian.com",
            "Atlassian Pty Ltd"
        )
        assert is_verified is True
    
    def test_match_complex_company_name(self):
        is_verified, reason = verify_email_domain_ownership(
            "user@reagroup.com.au",
            "REA Group Limited"
        )
        assert is_verified is True
    
    def test_match_with_hyphens(self):
        is_verified, reason = verify_email_domain_ownership(
            "user@seek.com.au",
            "SEEK Limited"
        )
        assert is_verified is True
    
    # ============================================================================
    # FAILURE Cases (Generic Email Providers)
    # ============================================================================
    
    def test_rejects_gmail(self):
        is_verified, reason = verify_email_domain_ownership(
            "alice@gmail.com",
            "Atlassian Pty Ltd"
        )
        assert is_verified is False
        assert "generic" in reason.lower()
    
    def test_rejects_yahoo(self):
        is_verified, reason = verify_email_domain_ownership(
            "bob@yahoo.com",
            "Canva Pty Ltd"
        )
        assert is_verified is False
    
    def test_rejects_hotmail(self):
        is_verified, reason = verify_email_domain_ownership(
            "user@hotmail.com",
            "REA Group Limited"
        )
        assert is_verified is False
    
    def test_rejects_outlook(self):
        is_verified, reason = verify_email_domain_ownership(
            "user@outlook.com",
            "SEEK Limited"
        )
        assert is_verified is False
    
    # ============================================================================
    # FAILURE Cases (Domain Doesn't Match)
    # ============================================================================
    
    def test_rejects_different_company_domain(self):
        is_verified, reason = verify_email_domain_ownership(
            "competitor@evilcorp.com",
            "Atlassian Pty Ltd"
        )
        assert is_verified is False
        assert "doesn't match" in reason.lower()
    
    def test_rejects_partial_match(self):
        # "atlas" in domain but company is "atlassian"
        is_verified, reason = verify_email_domain_ownership(
            "user@atlas.com",
            "Atlassian Pty Ltd"
        )
        assert is_verified is False
    
    # ============================================================================
    # EDGE Cases
    # ============================================================================
    
    def test_handles_uppercase_email(self):
        is_verified, reason = verify_email_domain_ownership(
            "ALICE@ATLASSIAN.COM",
            "Atlassian Pty Ltd"
        )
        assert is_verified is True
    
    def test_handles_uppercase_company_name(self):
        is_verified, reason = verify_email_domain_ownership(
            "alice@atlassian.com",
            "ATLASSIAN PTY LTD"
        )
        assert is_verified is True
    
    def test_handles_punctuation_in_company_name(self):
        is_verified, reason = verify_email_domain_ownership(
            "user@reagroup.com.au",
            "R.E.A. Group Limited"
        )
        assert is_verified is True


class TestShouldAutoJoinCompany:
    """Test simplified auto-join helper"""
    
    def test_returns_true_for_matching_domain(self):
        assert should_auto_join_company(
            "alice@atlassian.com",
            "Atlassian Pty Ltd"
        ) is True
    
    def test_returns_false_for_generic_email(self):
        assert should_auto_join_company(
            "alice@gmail.com",
            "Atlassian Pty Ltd"
        ) is False
    
    def test_returns_false_for_different_domain(self):
        assert should_auto_join_company(
            "user@competitor.com",
            "Atlassian Pty Ltd"
        ) is False

