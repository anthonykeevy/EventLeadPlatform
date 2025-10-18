"""
Tests for Story 1.11: Company Switching
Tests company switching logic, JWT generation, and default company updates.
"""
import pytest
from sqlalchemy.orm import Session
from modules.users.switch_service import CompanySwitchService
from models.company import Company
from models.user import User
from models.user_company import UserCompany
from models.ref.user_company_role import UserCompanyRole
from models.ref.user_company_status import UserCompanyStatus


@pytest.fixture
def switch_service(db_session: Session):
    return CompanySwitchService(db_session)


@pytest.fixture
def multi_company_user(db_session: Session, test_user: User):
    """Create a user belonging to multiple companies."""
    # Get reference data
    admin_role = db_session.query(UserCompanyRole).filter_by(RoleCode='company_admin').first()
    assert admin_role is not None, "company_admin role not found in database"
    user_role = db_session.query(UserCompanyRole).filter_by(RoleCode='company_user').first()
    assert user_role is not None, "company_user role not found in database"
    active_status = db_session.query(UserCompanyStatus).filter_by(StatusCode='active').first()
    assert active_status is not None, "active status not found in database"
    
    # Get a valid CountryID (required field)
    from models.ref.country import Country
    from models.ref.joined_via import JoinedVia
    country = db_session.query(Country).first()
    if not country:
        # Create a test country if none exists
        country = Country(
            CountryName='Australia',
            CountryCode='AU',
            IsActive=True
        )
        db_session.add(country)
        db_session.commit()
        db_session.refresh(country)
    
    # Get a valid JoinedViaID (required field)
    joined_via = db_session.query(JoinedVia).filter_by(MethodCode='signup').first()
    if not joined_via:
        # Create signup method if none exists
        joined_via = JoinedVia(
            MethodCode='signup',
            MethodName='Sign Up',
            Description='User signed up and created the company',
            IsActive=True,
            SortOrder=1
        )
        db_session.add(joined_via)
        db_session.commit()
        db_session.refresh(joined_via)
    
    # Create multiple companies
    companies = []
    for i in range(3):
        company = Company(
            CompanyName=f"Test Company {i}",
            CountryID=country.CountryID,
            IsActive=True,
            CreatedBy=test_user.UserID,
            UpdatedBy=test_user.UserID
        )
        db_session.add(company)
        companies.append(company)
    
    db_session.commit()
    for company in companies:
        db_session.refresh(company)
    
    # Create UserCompany records
    user_companies = []
    for idx, company in enumerate(companies):
        uc = UserCompany(
            UserID=test_user.UserID,
            CompanyID=company.CompanyID,
            UserCompanyRoleID=admin_role.UserCompanyRoleID if idx == 0 else user_role.UserCompanyRoleID,
            StatusID=active_status.UserCompanyStatusID,
            JoinedViaID=joined_via.JoinedViaID,
            IsPrimaryCompany=(idx == 0),  # First company is primary
            CreatedBy=test_user.UserID,
            UpdatedBy=test_user.UserID
        )
        db_session.add(uc)
        user_companies.append(uc)
    
    db_session.commit()
    
    return {
        'user': test_user,
        'companies': companies,
        'user_companies': user_companies
    }


class TestCompanySwitching:
    """Test basic company switching functionality."""

    def test_switch_to_valid_company(self, switch_service, multi_company_user):
        """Test switching to a company the user belongs to."""
        user = multi_company_user['user']
        target_company = multi_company_user['companies'][1]  # Switch to second company
        
        result = switch_service.switch_company(user.UserID, target_company.CompanyID)
        
        # Verify response structure
        assert 'access_token' in result
        assert 'refresh_token' in result
        assert 'company' in result
        assert result['company']['company_id'] == target_company.CompanyID
        assert result['company']['company_name'] == target_company.CompanyName

    def test_switch_updates_primary_company(self, switch_service, multi_company_user, db_session):
        """Test that switching updates IsPrimaryCompany correctly."""
        user = multi_company_user['user']
        companies = multi_company_user['companies']
        
        # Initially, first company is primary
        initial_primary = db_session.query(UserCompany).filter_by(
            UserID=user.UserID,
            CompanyID=companies[0].CompanyID
        ).first()
        assert initial_primary.IsPrimaryCompany is True
        
        # Switch to second company
        switch_service.switch_company(user.UserID, companies[1].CompanyID)
        
        # Verify first company is no longer primary
        db_session.expire_all()
        old_primary = db_session.query(UserCompany).filter_by(
            UserID=user.UserID,
            CompanyID=companies[0].CompanyID
        ).first()
        assert old_primary.IsPrimaryCompany is False
        
        # Verify second company is now primary
        new_primary = db_session.query(UserCompany).filter_by(
            UserID=user.UserID,
            CompanyID=companies[1].CompanyID
        ).first()
        assert new_primary.IsPrimaryCompany is True

    def test_all_other_companies_set_to_non_primary(self, switch_service, multi_company_user, db_session):
        """Test that switching sets ALL other companies to non-primary."""
        user = multi_company_user['user']
        companies = multi_company_user['companies']
        
        # Switch to third company
        switch_service.switch_company(user.UserID, companies[2].CompanyID)
        
        # Verify only third company is primary
        db_session.expire_all()
        all_user_companies = db_session.query(UserCompany).filter_by(
            UserID=user.UserID
        ).all()
        
        primary_count = sum(1 for uc in all_user_companies if uc.IsPrimaryCompany)
        assert primary_count == 1
        
        primary_company = next(uc for uc in all_user_companies if uc.IsPrimaryCompany)
        assert primary_company.CompanyID == companies[2].CompanyID


class TestSwitchingValidations:
    """Test validation rules for company switching."""

    def test_switch_to_non_member_company(self, switch_service, multi_company_user, db_session, test_user):
        """Test that switching to a company the user doesn't belong to fails."""
        from models.ref.country import Country
        user = multi_company_user['user']
        
        # Get a valid CountryID
        country = db_session.query(Country).first()
        
        # Create a company the user doesn't belong to
        other_company = Company(
            CompanyName="Other Company",
            CountryID=country.CountryID,
            IsActive=True,
            CreatedBy=test_user.UserID,
            UpdatedBy=test_user.UserID
        )
        db_session.add(other_company)
        db_session.commit()
        db_session.refresh(other_company)
        
        # Try to switch
        with pytest.raises(ValueError, match="does not have access"):
            switch_service.switch_company(user.UserID, other_company.CompanyID)

    def test_switch_to_inactive_membership(self, switch_service, multi_company_user, db_session):
        """Test that switching to a company with inactive membership fails."""
        user = multi_company_user['user']
        target_company = multi_company_user['companies'][1]
        
        # Get inactive status
        inactive_status = db_session.query(UserCompanyStatus).filter_by(StatusCode='inactive').first()
        if not inactive_status:
            # Create inactive status if it doesn't exist
            inactive_status = UserCompanyStatus(
                StatusName='Inactive',
                StatusCode='inactive',
                Description='User is inactive in this company',
                IsActive=True
            )
            db_session.add(inactive_status)
            db_session.commit()
            db_session.refresh(inactive_status)
        
        # Set membership to inactive
        user_company = db_session.query(UserCompany).filter_by(
            UserID=user.UserID,
            CompanyID=target_company.CompanyID
        ).first()
        user_company.StatusID = inactive_status.UserCompanyStatusID
        db_session.commit()
        
        # Try to switch
        with pytest.raises(ValueError, match="not active in the target company"):
            switch_service.switch_company(user.UserID, target_company.CompanyID)


class TestJWTGeneration:
    """Test that JWT tokens are generated correctly after switching."""

    def test_jwt_contains_correct_company_id(self, switch_service, multi_company_user):
        """Test that the JWT contains the correct company_id after switching."""
        import jwt
        from config.jwt import get_secret_key, get_algorithm
        
        user = multi_company_user['user']
        target_company = multi_company_user['companies'][1]
        
        result = switch_service.switch_company(user.UserID, target_company.CompanyID)
        
        # Decode the access token
        decoded = jwt.decode(result['access_token'], get_secret_key(), algorithms=[get_algorithm()])
        
        assert decoded['company_id'] == target_company.CompanyID
        assert decoded['sub'] == str(user.UserID)  # JWT standard uses 'sub' for user_id

    def test_jwt_contains_correct_role(self, switch_service, multi_company_user):
        """Test that the JWT contains the correct role for the target company."""
        import jwt
        from config.jwt import get_secret_key, get_algorithm
        
        user = multi_company_user['user']
        target_company = multi_company_user['companies'][1]  # User is 'company_user' in this company
        
        result = switch_service.switch_company(user.UserID, target_company.CompanyID)
        
        # Decode the access token
        decoded = jwt.decode(result['access_token'], get_secret_key(), algorithms=[get_algorithm()])
        
        assert decoded['role'] == 'company_user'

    def test_switch_multiple_times(self, switch_service, multi_company_user):
        """Test switching between companies multiple times."""
        user = multi_company_user['user']
        companies = multi_company_user['companies']
        
        # Switch to company 1
        result1 = switch_service.switch_company(user.UserID, companies[1].CompanyID)
        assert result1['company']['company_id'] == companies[1].CompanyID
        
        # Switch to company 2
        result2 = switch_service.switch_company(user.UserID, companies[2].CompanyID)
        assert result2['company']['company_id'] == companies[2].CompanyID
        
        # Switch back to company 0
        result3 = switch_service.switch_company(user.UserID, companies[0].CompanyID)
        assert result3['company']['company_id'] == companies[0].CompanyID


class TestSwitchingEdgeCases:
    """Test edge cases in company switching."""

    def test_switch_to_same_company(self, switch_service, multi_company_user):
        """Test switching to the company the user is already in."""
        user = multi_company_user['user']
        current_company = multi_company_user['companies'][0]  # Already primary
        
        # Should succeed (idempotent operation)
        result = switch_service.switch_company(user.UserID, current_company.CompanyID)
        assert result['company']['company_id'] == current_company.CompanyID

    def test_refresh_token_generated(self, switch_service, multi_company_user):
        """Test that a refresh token is generated on company switch."""
        user = multi_company_user['user']
        target_company = multi_company_user['companies'][1]
        
        result = switch_service.switch_company(user.UserID, target_company.CompanyID)
        
        assert 'refresh_token' in result
        assert result['refresh_token'] is not None
        assert len(result['refresh_token']) > 0

