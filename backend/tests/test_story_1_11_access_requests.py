"""
Tests for Story 1.11: Access Request Flow
Tests access request creation, approval, and rejection.
"""
import pytest
from sqlalchemy.orm import Session
from modules.companies.access_request_service import AccessRequestService
from models.company import Company
from models.user import User
from models.user_company import UserCompany
from models.company_switch_request import CompanySwitchRequest
from models.ref.user_company_role import UserCompanyRole
from models.ref.user_company_status import UserCompanyStatus
from models.ref.joined_via import JoinedVia
from models.ref.company_switch_request_type import CompanySwitchRequestType
from models.ref.company_switch_request_status import CompanySwitchRequestStatus


@pytest.fixture
def access_request_service(db_session: Session):
    return AccessRequestService(db_session)


@pytest.fixture
def requestor_and_target_company(db_session: Session, test_user: User):
    """Create a user and a company they don't belong to."""
    from models.ref.country import Country
    from models.ref.user_status import UserStatus
    
    # Get a valid CountryID (required field)
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
    
    # Create user's current company
    user_company = Company(
        CompanyName="User's Company",
        CountryID=country.CountryID,
        IsActive=True,
        CreatedBy=test_user.UserID,
        UpdatedBy=test_user.UserID
    )
    db_session.add(user_company)
    
    # Create target company (user doesn't belong to this)
    target_company = Company(
        CompanyName="Target Company",
        CountryID=country.CountryID,
        IsActive=True,
        CreatedBy=test_user.UserID,
        UpdatedBy=test_user.UserID
    )
    db_session.add(target_company)
    
    # Get active status for admin user
    active_status = db_session.query(UserStatus).filter_by(StatusCode='active').first()
    if not active_status:
        active_status = UserStatus(
            StatusCode='active',
            StatusName='Active',
            Description='User account is active',
            AllowLogin=True,
            IsActive=True,
            SortOrder=1
        )
        db_session.add(active_status)
        db_session.commit()
        db_session.refresh(active_status)
    
    # Create admin for target company (or reuse if exists)
    admin_user = db_session.query(User).filter_by(Email="admin@targetcompany.com").first()
    if not admin_user:
        admin_user = User(
            Email="admin@targetcompany.com",
            PasswordHash="dummy_hash",
            FirstName="Admin",
            LastName="User",
            StatusID=active_status.UserStatusID,
            IsEmailVerified=True,
            EmailVerifiedAt=None,
            CreatedBy=test_user.UserID,
            UpdatedBy=test_user.UserID
        )
        db_session.add(admin_user)
    
    db_session.commit()
    db_session.refresh(user_company)
    db_session.refresh(target_company)
    if admin_user.UserID is None:
        db_session.refresh(admin_user)
    
    # Give admin user membership in target company
    admin_role = db_session.query(UserCompanyRole).filter_by(RoleCode='company_admin').first()
    assert admin_role is not None, "company_admin role not found in database"
    active_status = db_session.query(UserCompanyStatus).filter_by(StatusCode='active').first()
    assert active_status is not None, "active status not found in database"
    
    # Get JoinedVia for signup
    joined_via = db_session.query(JoinedVia).filter_by(MethodCode='signup').first()
    if not joined_via:
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
    
    admin_uc = UserCompany(
        UserID=admin_user.UserID,
        CompanyID=target_company.CompanyID,
        UserCompanyRoleID=admin_role.UserCompanyRoleID,
        StatusID=active_status.UserCompanyStatusID,
        JoinedViaID=joined_via.JoinedViaID,
        IsPrimaryCompany=True,
        CreatedBy=test_user.UserID,
        UpdatedBy=test_user.UserID
    )
    db_session.add(admin_uc)
    db_session.commit()
    
    return {
        'requestor': test_user,
        'target_company': target_company,
        'admin_user': admin_user
    }


class TestAccessRequestCreation:
    """Test creating access requests."""

    def test_create_access_request(self, access_request_service, requestor_and_target_company):
        """Test creating a valid access request."""
        requestor = requestor_and_target_company['requestor']
        target_company = requestor_and_target_company['target_company']
        
        request = access_request_service.create_access_request(
            user_id=requestor.UserID,
            target_company_id=target_company.CompanyID,
            reason="I need access to collaborate on events."
        )
        
        assert request.UserID == requestor.UserID
        assert request.ToCompanyID == target_company.CompanyID
        assert request.Reason == "I need access to collaborate on events."
        assert request.RequestedBy == requestor.UserID

    def test_create_access_request_without_reason(self, access_request_service, requestor_and_target_company):
        """Test creating an access request without a reason (optional field)."""
        requestor = requestor_and_target_company['requestor']
        target_company = requestor_and_target_company['target_company']
        
        request = access_request_service.create_access_request(
            user_id=requestor.UserID,
            target_company_id=target_company.CompanyID,
            reason=None
        )
        
        assert request.UserID == requestor.UserID
        assert request.Reason is None

    def test_prevent_duplicate_pending_request(self, access_request_service, requestor_and_target_company):
        """Test that duplicate pending requests are prevented."""
        requestor = requestor_and_target_company['requestor']
        target_company = requestor_and_target_company['target_company']
        
        # Create first request
        access_request_service.create_access_request(
            user_id=requestor.UserID,
            target_company_id=target_company.CompanyID,
            reason="First request"
        )
        
        # Try to create duplicate
        with pytest.raises(ValueError, match="pending access request.*already exists"):
            access_request_service.create_access_request(
                user_id=requestor.UserID,
                target_company_id=target_company.CompanyID,
                reason="Second request"
            )


class TestAccessRequestApproval:
    """Test approving access requests."""

    def test_approve_access_request(self, access_request_service, requestor_and_target_company, db_session):
        """Test approving an access request creates UserCompany record."""
        requestor = requestor_and_target_company['requestor']
        target_company = requestor_and_target_company['target_company']
        admin = requestor_and_target_company['admin_user']
        
        # Create request
        request = access_request_service.create_access_request(
            user_id=requestor.UserID,
            target_company_id=target_company.CompanyID,
            reason="Need access"
        )
        
        # Approve it
        approved_request = access_request_service.approve_access_request(
            request_id=request.CompanySwitchRequestID,
            approved_by_user_id=admin.UserID
        )
        
        # Verify request status
        assert approved_request.ApprovedBy == admin.UserID
        assert approved_request.ApprovedAt is not None
        
        # Verify UserCompany record was created
        user_company = db_session.query(UserCompany).filter_by(
            UserID=requestor.UserID,
            CompanyID=target_company.CompanyID
        ).first()
        
        assert user_company is not None
        assert user_company.IsPrimaryCompany is False
        
        # Verify role is company_user
        role = db_session.get(UserCompanyRole, user_company.UserCompanyRoleID)
        assert role.RoleCode == 'company_user'

    def test_approve_sets_joined_via(self, access_request_service, requestor_and_target_company, db_session):
        """Test that approving sets JoinedVia to 'access_request'."""
        requestor = requestor_and_target_company['requestor']
        target_company = requestor_and_target_company['target_company']
        admin = requestor_and_target_company['admin_user']
        
        # Create and approve request
        request = access_request_service.create_access_request(
            user_id=requestor.UserID,
            target_company_id=target_company.CompanyID,
            reason="Need access"
        )
        
        access_request_service.approve_access_request(
            request_id=request.CompanySwitchRequestID,
            approved_by_user_id=admin.UserID
        )
        
        # Verify JoinedVia
        user_company = db_session.query(UserCompany).filter_by(
            UserID=requestor.UserID,
            CompanyID=target_company.CompanyID
        ).first()
        
        joined_via = db_session.get(JoinedVia, user_company.JoinedViaID)
        assert joined_via.MethodCode == 'access_request'

    def test_approve_non_pending_request_fails(self, access_request_service, requestor_and_target_company, db_session):
        """Test that approving a non-pending request fails."""
        requestor = requestor_and_target_company['requestor']
        target_company = requestor_and_target_company['target_company']
        admin = requestor_and_target_company['admin_user']
        
        # Create and approve request
        request = access_request_service.create_access_request(
            user_id=requestor.UserID,
            target_company_id=target_company.CompanyID,
            reason="Need access"
        )
        
        access_request_service.approve_access_request(
            request_id=request.CompanySwitchRequestID,
            approved_by_user_id=admin.UserID
        )
        
        # Try to approve again
        with pytest.raises(ValueError, match="not found or is not in a pending state"):
            access_request_service.approve_access_request(
                request_id=request.CompanySwitchRequestID,
                approved_by_user_id=admin.UserID
            )


class TestAccessRequestRejection:
    """Test rejecting access requests."""

    def test_reject_access_request(self, access_request_service, requestor_and_target_company):
        """Test rejecting an access request."""
        requestor = requestor_and_target_company['requestor']
        target_company = requestor_and_target_company['target_company']
        admin = requestor_and_target_company['admin_user']
        
        # Create request
        request = access_request_service.create_access_request(
            user_id=requestor.UserID,
            target_company_id=target_company.CompanyID,
            reason="Need access"
        )
        
        # Reject it
        rejected_request = access_request_service.reject_access_request(
            request_id=request.CompanySwitchRequestID,
            rejected_by_user_id=admin.UserID,
            reason="Insufficient justification"
        )
        
        assert rejected_request.RejectedBy == admin.UserID
        assert rejected_request.RejectedAt is not None
        assert rejected_request.RejectionReason == "Insufficient justification"

    def test_reject_does_not_create_user_company(self, access_request_service, requestor_and_target_company, db_session):
        """Test that rejecting a request does NOT create UserCompany record."""
        requestor = requestor_and_target_company['requestor']
        target_company = requestor_and_target_company['target_company']
        admin = requestor_and_target_company['admin_user']
        
        # Create and reject request
        request = access_request_service.create_access_request(
            user_id=requestor.UserID,
            target_company_id=target_company.CompanyID,
            reason="Need access"
        )
        
        access_request_service.reject_access_request(
            request_id=request.CompanySwitchRequestID,
            rejected_by_user_id=admin.UserID,
            reason="Not approved"
        )
        
        # Verify no UserCompany record exists
        user_company = db_session.query(UserCompany).filter_by(
            UserID=requestor.UserID,
            CompanyID=target_company.CompanyID
        ).first()
        
        assert user_company is None

    def test_reject_non_pending_request_fails(self, access_request_service, requestor_and_target_company):
        """Test that rejecting a non-pending request fails."""
        requestor = requestor_and_target_company['requestor']
        target_company = requestor_and_target_company['target_company']
        admin = requestor_and_target_company['admin_user']
        
        # Create and reject request
        request = access_request_service.create_access_request(
            user_id=requestor.UserID,
            target_company_id=target_company.CompanyID,
            reason="Need access"
        )
        
        access_request_service.reject_access_request(
            request_id=request.CompanySwitchRequestID,
            rejected_by_user_id=admin.UserID,
            reason="Not approved"
        )
        
        # Try to reject again
        with pytest.raises(ValueError, match="not found or is not in a pending state"):
            access_request_service.reject_access_request(
                request_id=request.CompanySwitchRequestID,
                rejected_by_user_id=admin.UserID,
                reason="Still not approved"
            )


class TestAccessRequestQueries:
    """Test querying access requests."""

    def test_get_pending_access_requests(self, access_request_service, requestor_and_target_company, db_session):
        """Test getting all pending requests for a company."""
        from models.ref.user_status import UserStatus
        
        requestor = requestor_and_target_company['requestor']
        target_company = requestor_and_target_company['target_company']
        
        # Get active status
        active_status = db_session.query(UserStatus).filter_by(StatusCode='active').first()
        
        # Create another user to make multiple requests (or reuse if exists)
        second_user = db_session.query(User).filter_by(Email="second@example.com").first()
        if not second_user:
            second_user = User(
                Email="second@example.com",
                PasswordHash="dummy_hash",
                FirstName="Second",
                LastName="User",
                StatusID=active_status.UserStatusID,
                IsEmailVerified=True,
                CreatedBy=requestor.UserID,
                UpdatedBy=requestor.UserID
            )
            db_session.add(second_user)
            db_session.commit()
            db_session.refresh(second_user)
        
        # Create multiple requests
        access_request_service.create_access_request(
            user_id=requestor.UserID,
            target_company_id=target_company.CompanyID,
            reason="First request"
        )
        
        access_request_service.create_access_request(
            user_id=second_user.UserID,
            target_company_id=target_company.CompanyID,
            reason="Second request"
        )
        
        # Get all pending requests
        pending_requests = access_request_service.get_pending_access_requests(target_company.CompanyID)
        
        assert len(pending_requests) == 2

    def test_pending_requests_exclude_approved(self, access_request_service, requestor_and_target_company):
        """Test that approved requests are not returned as pending."""
        requestor = requestor_and_target_company['requestor']
        target_company = requestor_and_target_company['target_company']
        admin = requestor_and_target_company['admin_user']
        
        # Create and approve request
        request = access_request_service.create_access_request(
            user_id=requestor.UserID,
            target_company_id=target_company.CompanyID,
            reason="Need access"
        )
        
        access_request_service.approve_access_request(
            request_id=request.CompanySwitchRequestID,
            approved_by_user_id=admin.UserID
        )
        
        # Get pending requests
        pending_requests = access_request_service.get_pending_access_requests(target_company.CompanyID)
        
        assert len(pending_requests) == 0

    def test_pending_requests_exclude_rejected(self, access_request_service, requestor_and_target_company):
        """Test that rejected requests are not returned as pending."""
        requestor = requestor_and_target_company['requestor']
        target_company = requestor_and_target_company['target_company']
        admin = requestor_and_target_company['admin_user']
        
        # Create and reject request
        request = access_request_service.create_access_request(
            user_id=requestor.UserID,
            target_company_id=target_company.CompanyID,
            reason="Need access"
        )
        
        access_request_service.reject_access_request(
            request_id=request.CompanySwitchRequestID,
            rejected_by_user_id=admin.UserID,
            reason="Not approved"
        )
        
        # Get pending requests
        pending_requests = access_request_service.get_pending_access_requests(target_company.CompanyID)
        
        assert len(pending_requests) == 0

