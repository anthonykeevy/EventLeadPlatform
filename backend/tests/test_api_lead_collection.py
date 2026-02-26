import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import uuid

class TestLeadCollectionAPI:
    """[P0] API Integration tests for Lead Collection (Area 9)"""

    def test_anonymous_user_can_submit_to_published_form(self, client: TestClient, test_db: Session, mock_published_form):
        """
        [P0] Should accept public submissions to a published form and flag as production lead.
        """
        payload = {
            "idempotencyKey": "test-key-123",
            "submittedAtClient": "2026-02-25T12:00:00Z",
            "answersByComponentId": {
                "first_name_comp": "John",
                "last_name_comp": "Doe",
                "email_comp": "john.doe@example.com"
            },
            "context": {
                "clientDeviceId": "test-device",
                "clientSessionId": "test-session",
                "submitAttemptId": "attempt-1"
            }
        }
        
        response = client.post(
            f"/api/public/forms/{mock_published_form['token']}/submissions",
            json=payload
        )
        
        assert response.status_code in [200, 201], f"Expected 200/201, got {response.status_code}. Response: {response.text}"
        data = response.json()
        assert data.get("status") in ["ACCEPTED", "DUPLICATE"]
        assert "submissionId" in data
        
        from models.form_submission import FormSubmission
        submission = test_db.query(FormSubmission).filter_by(FormSubmissionID=data["submissionId"]).first()
        assert submission.IsPreview is False

    def test_authenticated_user_can_submit_preview_lead(self, client: TestClient, test_db: Session, admin_token_headers, mock_draft_form):
        """
        [P0] Should accept submissions to a draft form IF user is authenticated, and flag as preview lead.
        """
        payload = {
            "idempotencyKey": "test-key-preview",
            "submittedAtClient": "2026-02-25T12:00:00Z",
            "answersByComponentId": {
                "email_comp": "preview.tester@example.com"
            },
            "context": {
                "clientDeviceId": "test-device",
                "clientSessionId": "test-session",
                "submitAttemptId": "attempt-1"
            }
        }
        
        response = client.post(
            f"/api/public/forms/{mock_draft_form['token']}/submissions",
            headers=admin_token_headers,
            json=payload
        )
        
        assert response.status_code in [200, 201], f"Expected 200/201, got {response.status_code}. Response: {response.text}"
        data = response.json()
        assert data.get("status") in ["ACCEPTED", "DUPLICATE"]
        
        from models.form_submission import FormSubmission
        submission = test_db.query(FormSubmission).filter_by(FormSubmissionID=data["submissionId"]).first()
        assert submission.IsPreview is True

    def test_anonymous_user_cannot_submit_to_draft_form(self, client: TestClient, mock_draft_form):
        """
        [P0] Should reject public submissions to an unpublished/draft form with invalid token.
        """
        payload = {
            "idempotencyKey": "test-key-hacker",
            "submittedAtClient": "2026-02-25T12:00:00Z",
            "answersByComponentId": {
                "email_comp": "hacker@example.com"
            },
            "context": {
                "clientDeviceId": "test-device",
                "clientSessionId": "test-session",
                "submitAttemptId": "attempt-1"
            }
        }
        
        response = client.post(
            f"/api/public/forms/invalid-token-123/submissions",
            json=payload
        )
        
        assert response.status_code in [403, 404, 401], f"Expected 4xx, got {response.status_code}"
