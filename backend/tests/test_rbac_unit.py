"""
Unit Tests for RBAC Functions
Tests role-based access control helper functions without requiring full app context
"""
import pytest
from modules.auth.models import CurrentUser
from common.rbac import has_role, is_company_admin, belongs_to_company, require_company_access
from fastapi import HTTPException


class TestRBACHelpers:
    """Test RBAC helper functions"""
    
    def test_has_role_returns_true_for_matching_role(self):
        """Test has_role returns True when roles match"""
        user = CurrentUser(
            user_id=1,
            email="admin@example.com",
            role="company_admin",
            company_id=100
        )
        
        assert has_role(user, "company_admin") is True
    
    def test_has_role_returns_false_for_different_role(self):
        """Test has_role returns False when roles don't match"""
        user = CurrentUser(
            user_id=1,
            email="user@example.com",
            role="company_user",
            company_id=100
        )
        
        assert has_role(user, "company_admin") is False
    
    def test_is_company_admin_returns_true_for_admin(self):
        """Test is_company_admin returns True for company_admin role"""
        admin = CurrentUser(
            user_id=1,
            email="admin@example.com",
            role="company_admin",
            company_id=100
        )
        
        assert is_company_admin(admin) is True
    
    def test_is_company_admin_returns_false_for_non_admin(self):
        """Test is_company_admin returns False for non-admin roles"""
        user = CurrentUser(
            user_id=2,
            email="user@example.com",
            role="company_user",
            company_id=100
        )
        
        assert is_company_admin(user) is False
    
    def test_belongs_to_company_returns_true_for_same_company(self):
        """Test belongs_to_company returns True when company IDs match"""
        user = CurrentUser(
            user_id=1,
            email="user@example.com",
            role="company_user",
            company_id=100
        )
        
        assert belongs_to_company(user, 100) is True
    
    def test_belongs_to_company_returns_false_for_different_company(self):
        """Test belongs_to_company returns False when company IDs don't match"""
        user = CurrentUser(
            user_id=1,
            email="user@example.com",
            role="company_user",
            company_id=100
        )
        
        assert belongs_to_company(user, 200) is False
    
    def test_require_company_access_allows_same_company(self):
        """Test require_company_access allows access to same company"""
        user = CurrentUser(
            user_id=1,
            email="user@example.com",
            role="company_user",
            company_id=100
        )
        
        # Should not raise exception
        require_company_access(user, 100)
    
    def test_require_company_access_raises_403_for_different_company(self):
        """Test require_company_access raises 403 for different company"""
        user = CurrentUser(
            user_id=1,
            email="user@example.com",
            role="company_user",
            company_id=100
        )
        
        with pytest.raises(HTTPException) as exc_info:
            require_company_access(user, 200)
        
        assert exc_info.value.status_code == 403
        assert "Access denied" in exc_info.value.detail


class TestCurrentUserModel:
    """Test CurrentUser model"""
    
    def test_current_user_creation_with_all_fields(self):
        """Test creating CurrentUser with all fields"""
        user = CurrentUser(
            user_id=123,
            email="test@example.com",
            role="company_admin",
            company_id=456
        )
        
        assert user.user_id == 123
        assert user.email == "test@example.com"
        assert user.role == "company_admin"
        assert user.company_id == 456
    
    def test_current_user_creation_with_minimal_fields(self):
        """Test creating CurrentUser with only required fields"""
        user = CurrentUser(
            user_id=123,
            email="test@example.com"
        )
        
        assert user.user_id == 123
        assert user.email == "test@example.com"
        assert user.role is None
        assert user.company_id is None
    
    def test_current_user_is_immutable(self):
        """Test that CurrentUser is immutable (frozen)"""
        user = CurrentUser(
            user_id=123,
            email="test@example.com",
            role="company_admin"
        )
        
        # Attempting to modify should raise an error
        with pytest.raises(Exception):  # Pydantic raises ValidationError for frozen models
            user.role = "company_user"

