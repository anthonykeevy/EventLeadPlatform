"""
Integration Tests for Story 1.11: Multi-Company Scenarios
Tests end-to-end flows for cross-company invitations, company switching, and access requests.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
from models.user import User
from models.company import Company
from models.user_company import UserCompany
from models.ref.user_company_role import UserCompanyRole
from models.ref.user_company_status import UserCompanyStatus
from models.ref.joined_via import JoinedVia
from models.ref.user_status import UserStatus
from models.ref.country import Country
from modules.auth.models import CurrentUser
from modules.auth.dependencies import get_current_user
from modules.auth.jwt_service import decode_token
from fastapi import HTTPException, status, Request


@pytest.fixture
def auth_client(db_session: Session):
    """
    Create a test client with proper auth handling.
    Overrides get_current_user to decode JWT from Authorization header.
    """
    from common.database import get_db
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    def override_get_current_user(request: Request) -> CurrentUser:
        """Extract and decode JWT from Authorization header."""
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        
        token = auth_header.replace("Bearer ", "")
        try:
            payload = decode_token(token)
            return CurrentUser(
                user_id=int(payload["sub"]),
                email=payload["email"],
                role=payload.get("role"),
                company_id=payload.get("company_id")
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}"
            )
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()



@pytest.fixture
def authenticated_user_two_companies(db_session: Session):
    """Create an authenticated user belonging to two companies."""
    # Get/create active user status
    active_user_status = db_session.query(UserStatus).filter_by(StatusCode='active').first()
    if not active_user_status:
        active_user_status = UserStatus(
            StatusCode='active',
            StatusName='Active',
            Description='User account is active',
            AllowLogin=True,
            IsActive=True,
            SortOrder=1
        )
        db_session.add(active_user_status)
        db_session.commit()
        db_session.refresh(active_user_status)
    
    # Get/create country
    country = db_session.query(Country).first()
    if not country:
        country = Country(
            CountryName='Australia',
            CountryCode='AU',
            IsActive=True
        )
        db_session.add(country)
        db_session.commit()
        db_session.refresh(country)
    
    # Create or reuse user
    user = db_session.query(User).filter_by(Email="multicompany@example.com").first()
    if not user:
        user = User(
            Email="multicompany@example.com",
            PasswordHash="$2b$12$dummyhash",
            FirstName="Multi",
            LastName="Company",
            StatusID=active_user_status.UserStatusID,
            IsEmailVerified=True
        )
        db_session.add(user)
        db_session.flush()
    
    # Get reference data
    admin_role = db_session.query(UserCompanyRole).filter_by(RoleCode='company_admin').first()
    assert admin_role is not None, "company_admin role not found in database"
    user_role = db_session.query(UserCompanyRole).filter_by(RoleCode='company_user').first()
    assert user_role is not None, "company_user role not found in database"
    active_status = db_session.query(UserCompanyStatus).filter_by(StatusCode='active').first()
    assert active_status is not None, "active status not found in database"
    onboarding_via = db_session.query(JoinedVia).filter_by(MethodCode='signup').first()
    if not onboarding_via:
        onboarding_via = JoinedVia(
            MethodCode='signup',
            MethodName='Sign Up',
            Description='User signed up',
            IsActive=True,
            SortOrder=1
        )
        db_session.add(onboarding_via)
        db_session.commit()
        db_session.refresh(onboarding_via)
    
    # Clean up any existing user companies for this user
    db_session.query(UserCompany).filter_by(UserID=user.UserID).delete()
    db_session.commit()
    
    # Create two companies
    company1 = Company(
        CompanyName="Company One",
        CountryID=country.CountryID,
        IsActive=True,
        CreatedBy=user.UserID,
        UpdatedBy=user.UserID
    )
    company2 = Company(
        CompanyName="Company Two",
        CountryID=country.CountryID,
        IsActive=True,
        CreatedBy=user.UserID,
        UpdatedBy=user.UserID
    )
    db_session.add_all([company1, company2])
    db_session.flush()
    
    # Add user to both companies
    uc1 = UserCompany(
        UserID=user.UserID,
        CompanyID=company1.CompanyID,
        UserCompanyRoleID=admin_role.UserCompanyRoleID,
        StatusID=active_status.UserCompanyStatusID,
        IsPrimaryCompany=True,
        JoinedViaID=onboarding_via.JoinedViaID,
        CreatedBy=user.UserID,
        UpdatedBy=user.UserID
    )
    uc2 = UserCompany(
        UserID=user.UserID,
        CompanyID=company2.CompanyID,
        UserCompanyRoleID=user_role.UserCompanyRoleID,
        StatusID=active_status.UserCompanyStatusID,
        IsPrimaryCompany=False,
        JoinedViaID=onboarding_via.JoinedViaID,
        CreatedBy=user.UserID,
        UpdatedBy=user.UserID
    )
    db_session.add_all([uc1, uc2])
    db_session.commit()
    
    # Generate auth token
    from modules.auth.jwt_service import create_access_token
    token = create_access_token(
        db=db_session,
        user_id=user.UserID,  # type: ignore
        email=user.Email,  # type: ignore
        role='company_admin',
        company_id=company1.CompanyID  # type: ignore
    )
    
    return {
        'user': user,
        'company1': company1,
        'company2': company2,
        'token': token
    }


@pytest.fixture
def test_helpers(db_session: Session):
    """Helper functions for creating test data consistently."""
    # Cache reference data
    active_user_status = db_session.query(UserStatus).filter_by(StatusCode='active').first()
    if not active_user_status:
        active_user_status = UserStatus(
            StatusCode='active',
            StatusName='Active',
            Description='User account is active',
            AllowLogin=True,
            IsActive=True,
            SortOrder=1
        )
        db_session.add(active_user_status)
        db_session.commit()
        db_session.refresh(active_user_status)
    
    country = db_session.query(Country).first()
    if not country:
        country = Country(
            CountryName='Australia',
            CountryCode='AU',
            IsActive=True
        )
        db_session.add(country)
        db_session.commit()
        db_session.refresh(country)
    
    signup_via = db_session.query(JoinedVia).filter_by(MethodCode='signup').first()
    if not signup_via:
        signup_via = JoinedVia(
            MethodCode='signup',
            MethodName='Sign Up',
            Description='User signed up',
            IsActive=True,
            SortOrder=1
        )
        db_session.add(signup_via)
        db_session.commit()
        db_session.refresh(signup_via)
    
    def create_user(email, first_name, last_name):
        # Check if user already exists
        user = db_session.query(User).filter_by(Email=email).first()
        if user:
            return user
        user = User(
            Email=email,
            PasswordHash="$2b$12$dummyhash",
            FirstName=first_name,
            LastName=last_name,
            StatusID=active_user_status.UserStatusID,
            IsEmailVerified=True
        )
        db_session.add(user)
        db_session.flush()
        return user
    
    def create_company(name, created_by_user_id):
        company = Company(
            CompanyName=name,
            CountryID=country.CountryID,
            IsActive=True,
            CreatedBy=created_by_user_id,
            UpdatedBy=created_by_user_id
        )
        db_session.add(company)
        db_session.flush()
        return company
    
    return {
        'create_user': create_user,
        'create_company': create_company,
        'signup_via': signup_via,
        'country': country,
        'active_user_status': active_user_status
    }


class TestCrossCompanyInvitationFlow:
    """Integration tests for inviting existing users to new companies."""

    def test_invite_existing_user_to_second_company(self, auth_client: TestClient, db_session: Session, test_helpers):
        """Test inviting a user who already has an account to join a new company."""
        # Create existing user with company
        existing_user = test_helpers["create_user"]("existing@example.com", "Existing", "User")
        
        # Clean up any previous user companies from prior test runs
        db_session.query(UserCompany).filter_by(UserID=existing_user.UserID).delete()
        db_session.commit()
        
        admin_role = db_session.query(UserCompanyRole).filter_by(RoleCode='company_admin').first()
        assert admin_role is not None, "company_admin role not found"
        active_status = db_session.query(UserCompanyStatus).filter_by(StatusCode='active').first()
        assert active_status is not None, "active status not found"
        onboarding_via = db_session.query(JoinedVia).filter_by(MethodCode='signup').first()
        if not onboarding_via:
            onboarding_via = test_helpers["signup_via"]
        assert onboarding_via is not None, "signup via not found"
        
        # Existing user's company
        existing_company = test_helpers["create_company"]("Existing Company", existing_user.UserID)
        
        uc_existing = UserCompany(
            UserID=existing_user.UserID,
            CompanyID=existing_company.CompanyID,
            UserCompanyRoleID=admin_role.UserCompanyRoleID,
            StatusID=active_status.UserCompanyStatusID,
            IsPrimaryCompany=True,
            JoinedViaID=onboarding_via.JoinedViaID,
            CreatedBy=existing_user.UserID,
            UpdatedBy=existing_user.UserID
        )
        db_session.add(uc_existing)
        
        # Create inviting company and admin
        inviting_company = test_helpers["create_company"]("Inviting Company", existing_user.UserID)
        
        inviting_admin = test_helpers["create_user"]("admin@inviting.com", "Admin", "User")
        
        uc_admin = UserCompany(
            UserID=inviting_admin.UserID,
            CompanyID=inviting_company.CompanyID,
            UserCompanyRoleID=admin_role.UserCompanyRoleID,
            StatusID=active_status.UserCompanyStatusID,
            IsPrimaryCompany=True,
            JoinedViaID=onboarding_via.JoinedViaID,
            CreatedBy=inviting_admin.UserID,
            UpdatedBy=inviting_admin.UserID
        )
        db_session.add(uc_admin)
        db_session.commit()
        
        # Get admin's token
        from modules.auth.jwt_service import create_access_token
        admin_token = create_access_token(
            db=db_session,
            user_id=inviting_admin.UserID,
            email=inviting_admin.Email,
            role='company_admin',
            company_id=inviting_company.CompanyID
        )
        
        # Invite existing user to new company (using invitation endpoint)
        response = auth_client.post(
            f"/api/companies/{inviting_company.CompanyID}/invite",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "email": "existing@example.com",
                "first_name": "Existing",
                "last_name": "User",
                "role": "company_user"
            }
        )
        
        # Debug output
        if response.status_code not in [200, 201]:
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.json()}")
        
        # Should succeed
        assert response.status_code in [200, 201]
        
        # Verify existing user now belongs to both companies
        user_companies = db_session.query(UserCompany).filter_by(
            UserID=existing_user.UserID
        ).all()
        
        assert len(user_companies) == 2
        company_ids = [uc.CompanyID for uc in user_companies]
        assert existing_company.CompanyID in company_ids
        assert inviting_company.CompanyID in company_ids


class TestCompanySwitchingIntegration:
    """Integration tests for company switching API."""

    def test_switch_company_api_endpoint(self, auth_client: TestClient, authenticated_user_two_companies):
        """Test the POST /api/users/me/switch-company endpoint."""
        user_data = authenticated_user_two_companies
        token = user_data['token']
        company2 = user_data['company2']
        
        response = auth_client.post(
            "/api/users/me/switch-company",
            headers={"Authorization": f"Bearer {token}"},
            json={"company_id": company2.CompanyID}
        )
        
        # Debug output
        if response.status_code != 200:
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.json()}")
            print(f"Token: {token[:50]}...")
            
            # Try decoding the token manually
            import jwt
            from config.jwt import get_secret_key, get_algorithm
            try:
                decoded = jwt.decode(token, get_secret_key(), algorithms=[get_algorithm()])
                print(f"Decoded token: {decoded}")
            except Exception as e:
                print(f"Token decode error: {e}")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert 'company' in data
        assert data['company']['company_id'] == company2.CompanyID
        assert data['company']['company_name'] == "Company Two"

    def test_switch_company_updates_jwt(self, auth_client: TestClient, authenticated_user_two_companies):
        """Test that company switching returns a JWT with updated company_id."""
        import jwt
        from config.jwt import get_secret_key, get_algorithm
        
        user_data = authenticated_user_two_companies
        token = user_data['token']
        company2 = user_data['company2']
        
        response = auth_client.post(
            "/api/users/me/switch-company",
            headers={"Authorization": f"Bearer {token}"},
            json={"company_id": company2.CompanyID}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Decode new token
        decoded = jwt.decode(data['access_token'], get_secret_key(), algorithms=[get_algorithm()])
        
        assert decoded['company_id'] == company2.CompanyID
        assert decoded['role'] == 'company_user'  # User is company_user in company2

    def test_switch_to_unauthorized_company_fails(self, auth_client: TestClient, authenticated_user_two_companies, db_session: Session, test_helpers):
        """Test that switching to a company the user doesn't belong to fails."""
        user_data = authenticated_user_two_companies
        token = user_data['token']
        user = user_data['user']
        
        # Create a third company that user doesn't belong to
        other_company = test_helpers["create_company"]("Unauthorized Company", user.UserID)
        db_session.add(other_company)
        db_session.commit()
        db_session.refresh(other_company)
        
        response = auth_client.post(
            "/api/users/me/switch-company",
            headers={"Authorization": f"Bearer {token}"},
            json={"company_id": other_company.CompanyID}
        )
        
        assert response.status_code in [400, 403, 404]

    def test_get_user_companies_endpoint(self, auth_client: TestClient, authenticated_user_two_companies):
        """Test GET /api/users/me/companies endpoint."""
        user_data = authenticated_user_two_companies
        token = user_data['token']
        company1 = user_data['company1']
        company2 = user_data['company2']
        
        response = auth_client.get(
            "/api/users/me/companies",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return both companies
        assert len(data) >= 2
        company_ids = [c['company_id'] for c in data]
        assert company1.CompanyID in company_ids
        assert company2.CompanyID in company_ids


class TestAccessRequestIntegration:
    """Integration tests for access request flow."""

    def test_create_access_request_api(self, auth_client: TestClient, authenticated_user_two_companies, db_session: Session, test_helpers):
        """Test POST /api/companies/{company_id}/access-requests endpoint."""
        user_data = authenticated_user_two_companies
        token = user_data['token']
        user = user_data['user']
        
        # Create a company the user doesn't belong to
        target_company = test_helpers["create_company"]("Target Company", user.UserID)
        db_session.add(target_company)
        db_session.commit()
        db_session.refresh(target_company)
        
        response = auth_client.post(
            f"/api/companies/{target_company.CompanyID}/access-requests",
            headers={"Authorization": f"Bearer {token}"},
            json={"reason": "I need access to collaborate."}
        )
        
        # Debug output
        if response.status_code not in [200, 201]:
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
        
        assert response.status_code in [200, 201]
        data = response.json()
        
        # Response structure: {'success': True, 'message': '...', 'request': {...}}
        assert 'success' in data
        assert data['success'] is True
        assert 'request' in data
        assert 'CompanySwitchRequestID' in data['request'] or 'request_id' in data['request']

    def test_approve_access_request_api(self, auth_client: TestClient, authenticated_user_two_companies, db_session: Session, test_helpers):
        """Test approving an access request through API."""
        user_data = authenticated_user_two_companies
        user = user_data['user']
        company1 = user_data['company1']
        
        # Create a requestor
        requestor = test_helpers["create_user"]("requestor@example.com", "Requestor", "User")
        db_session.add(requestor)
        db_session.commit()
        db_session.refresh(requestor)
        
        # Requestor creates access request
        from modules.companies.access_request_service import AccessRequestService
        access_service = AccessRequestService(db_session)
        request = access_service.create_access_request(
            user_id=requestor.UserID,
            target_company_id=company1.CompanyID,
            reason="Need access"
        )
        
        # Admin approves request
        from modules.auth.jwt_service import create_access_token
        admin_token = create_access_token(
            db=db_session,
            user_id=user.UserID,
            email=user.Email,
            role='company_admin',
            company_id=company1.CompanyID
        )
        
        response = auth_client.post(
            f"/api/companies/{company1.CompanyID}/access-requests/{request.CompanySwitchRequestID}/approve",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        
        # Verify requestor now belongs to company
        user_company = db_session.query(UserCompany).filter_by(
            UserID=requestor.UserID,
            CompanyID=company1.CompanyID
        ).first()
        
        assert user_company is not None

    def test_get_pending_access_requests_api(self, auth_client: TestClient, authenticated_user_two_companies, db_session: Session, test_helpers):
        """Test GET /api/companies/{company_id}/access-requests endpoint."""
        user_data = authenticated_user_two_companies
        user = user_data['user']
        company1 = user_data['company1']
        
        # Create a requestor
        requestor = test_helpers["create_user"]("requestor2@example.com", "Requestor", "Two")
        db_session.add(requestor)
        db_session.commit()
        db_session.refresh(requestor)
        
        # Create access request
        from modules.companies.access_request_service import AccessRequestService
        access_service = AccessRequestService(db_session)
        access_service.create_access_request(
            user_id=requestor.UserID,
            target_company_id=company1.CompanyID,
            reason="Need access"
        )
        
        # Admin gets pending requests
        from modules.auth.jwt_service import create_access_token
        admin_token = create_access_token(
            db=db_session,
            user_id=user.UserID,
            email=user.Email,
            role='company_admin',
            company_id=company1.CompanyID
        )
        
        response = auth_client.get(
            f"/api/companies/{company1.CompanyID}/access-requests",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have at least one pending request
        assert len(data) >= 1


class TestEndToEndMultiCompanyScenario:
    """End-to-end test of the multi-company user journey."""

    def test_multi_company_user_journey(self, auth_client: TestClient, db_session: Session, test_helpers):
        """
        Test complete multi-company flow:
        1. User creates account and company
        2. User receives invitation to second company
        3. User accepts invitation
        4. User can switch between companies
        5. Data isolation is maintained
        """
        # Step 1: Create user and first company
        user = test_helpers["create_user"]("journey@example.com", "Journey", "User")
        db_session.add(user)
        db_session.flush()
        
        admin_role = db_session.query(UserCompanyRole).filter_by(RoleCode='company_admin').first()
        assert admin_role is not None
        user_role = db_session.query(UserCompanyRole).filter_by(RoleCode='company_user').first()
        assert user_role is not None
        active_status = db_session.query(UserCompanyStatus).filter_by(StatusCode='active').first()
        assert active_status is not None
        onboarding_via = db_session.query(JoinedVia).filter_by(MethodCode='signup').first()
        if not onboarding_via:
            onboarding_via = test_helpers["signup_via"]
        assert onboarding_via is not None
        
        company_a = test_helpers["create_company"]("Company A", user.UserID)
        db_session.add(company_a)
        db_session.flush()
        
        uc_a = UserCompany(
            UserID=user.UserID,
            CompanyID=company_a.CompanyID,
            UserCompanyRoleID=admin_role.UserCompanyRoleID,
            StatusID=active_status.UserCompanyStatusID,
            IsPrimaryCompany=True,
            JoinedViaID=onboarding_via.JoinedViaID,
            CreatedBy=user.UserID,
            UpdatedBy=user.UserID
        )
        db_session.add(uc_a)
        db_session.commit()
        
        # Step 2 & 3: User receives invitation to second company and accepts
        company_b = test_helpers["create_company"]("Company B", user.UserID)
        db_session.add(company_b)
        db_session.flush()
        
        invitation_via = db_session.query(JoinedVia).filter_by(MethodCode='invitation').first()
        assert invitation_via is not None
        
        uc_b = UserCompany(
            UserID=user.UserID,
            CompanyID=company_b.CompanyID,
            UserCompanyRoleID=user_role.UserCompanyRoleID,
            StatusID=active_status.UserCompanyStatusID,
            IsPrimaryCompany=False,
            JoinedViaID=invitation_via.JoinedViaID,
            CreatedBy=user.UserID,
            UpdatedBy=user.UserID
        )
        db_session.add(uc_b)
        db_session.commit()
        
        # Step 4: User switches between companies
        from modules.users.switch_service import CompanySwitchService
        switch_service = CompanySwitchService(db_session)
        
        # Switch to Company B
        result = switch_service.switch_company(user.UserID, company_b.CompanyID)
        assert result['company']['company_id'] == company_b.CompanyID
        
        # Verify Company B is now primary
        db_session.expire_all()
        uc_b_updated = db_session.query(UserCompany).filter_by(
            UserID=user.UserID,
            CompanyID=company_b.CompanyID
        ).first()
        assert uc_b_updated is not None, "UserCompany record not found"
        assert uc_b_updated.IsPrimaryCompany is True
        
        # Switch back to Company A
        result = switch_service.switch_company(user.UserID, company_a.CompanyID)
        assert result['company']['company_id'] == company_a.CompanyID
        
        # Step 5: Verify user belongs to both companies
        user_companies = db_session.query(UserCompany).filter_by(
            UserID=user.UserID
        ).all()
        
        assert len(user_companies) == 2
        company_ids = [uc.CompanyID for uc in user_companies]
        assert company_a.CompanyID in company_ids
        assert company_b.CompanyID in company_ids

