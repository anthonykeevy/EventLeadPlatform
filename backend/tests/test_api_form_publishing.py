import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import uuid

# Assuming standard fixtures from backend/tests/conftest.py are available
# client, test_db, auth_headers

class TestFormPublishingAPI:
    """[P0] API Integration tests for Form Publishing (Area 8)"""

    def test_admin_can_publish_valid_draft_form(self, client: TestClient, admin_token_headers, mock_draft_form):
        """
        [P0] Should successfully publish a draft form and return a public URL when called by a Company Admin.
        """
        response = client.post(
            f"/api/forms/{mock_draft_form['form_id']}/publish", 
            headers=admin_token_headers
        )
        
        # Exact assertions depend on final implementation details. We assert the expected contract.
        assert response.status_code in [200, 201], response.text
        data = response.json()
        
        # Assertions (Test Quality: explicit, visible in test)
        assert data["status"] == "approved"
        assert "formId" in data

    def test_user_cannot_publish_if_approval_required(self, client: TestClient, test_db: Session, test_company, user_token_headers, mock_draft_form):
        """
        [P0] Should reject direct publish attempts from Company Users if the company requires admin approval.
        """
        from models.company_form_test_config import CompanyFormTestConfig
        
        # Set RequirePublishApproval=True for the company
        config = test_db.query(CompanyFormTestConfig).filter_by(CompanyID=test_company.CompanyID).first()
        if not config:
            config = CompanyFormTestConfig(
                CompanyID=test_company.CompanyID,
                TestThresholdEnabled=False,
                TestThresholdValue=3,
                RequirePublishApproval=True
            )
            test_db.add(config)
        else:
            config.RequirePublishApproval = True
        test_db.commit()

        # user_token_headers represents a token for a 'company_user' role
        response = client.post(
            f"/api/forms/{mock_draft_form['form_id']}/publish", 
            headers=user_token_headers
        )
        
        assert response.status_code in [403, 401] # Forbidden/Unauthorized
        
    def test_publish_fails_if_testing_threshold_unmet(self, client: TestClient, test_db: Session, test_company, admin_token_headers, mock_draft_form):
        """
        [P1] Should reject publish attempt if preview testing is enabled and threshold is not met.
        """
        from models.company_form_test_config import CompanyFormTestConfig
        
        # Set TestThresholdEnabled=True for the company
        config = test_db.query(CompanyFormTestConfig).filter_by(CompanyID=test_company.CompanyID).first()
        if not config:
            config = CompanyFormTestConfig(
                CompanyID=test_company.CompanyID,
                TestThresholdEnabled=True,
                TestThresholdValue=3,
                RequirePublishApproval=False
            )
            test_db.add(config)
        else:
            config.TestThresholdEnabled = True
            config.TestThresholdValue = 3
        test_db.commit()

        # Assuming mock_draft_form has 0 test submissions
        response = client.post(
            f"/api/forms/{mock_draft_form['form_id']}/publish", 
            headers=admin_token_headers
        )
        
        # Usually a 400 Bad Request or 422 Unprocessable Entity for business rule violations
        assert response.status_code in [400, 422]
        assert "threshold" in response.json().get("detail", "").lower() or "test" in response.text.lower()
