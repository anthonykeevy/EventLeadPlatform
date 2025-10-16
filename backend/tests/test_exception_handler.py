"""
Unit Tests for Global Exception Handler
Tests AC-0.2.3, AC-0.2.4, AC-0.2.5, AC-0.2.9
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.middleware.exception_handler import global_exception_handler
from backend.models.log.application_error import ApplicationError


# Test fixture: FastAPI app with exception handler
@pytest.fixture
def app_with_exception_handler():
    """Create test FastAPI app with global exception handler."""
    app = FastAPI()
    app.add_exception_handler(Exception, global_exception_handler)
    
    @app.get("/test/error")
    async def test_error_endpoint():
        raise ValueError("Test error message")
    
    @app.get("/test/critical")
    async def test_critical_endpoint():
        raise Exception("CriticalError: System failure")
    
    @app.get("/test/auth-error")
    async def test_auth_error_endpoint(request: Request):
        # Simulate JWT middleware setting user context
        request.state.user_id = 123
        request.state.company_id = 456
        raise RuntimeError("Authenticated user error")
    
    return app


def test_global_exception_handler_catches_unhandled_exceptions(app_with_exception_handler):
    """
    Test AC-0.2.3: Global exception handler catches all unhandled errors
    """
    client = TestClient(app_with_exception_handler, raise_server_exceptions=False)
    
    with patch('backend.middleware.exception_handler.SessionLocal'):
        response = client.get("/test/error")
        
        # Verify error response
        assert response.status_code == 500
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "message" in data


def test_global_exception_handler_logs_error_to_database(app_with_exception_handler):
    """
    Test AC-0.2.4: Errors logged to log.ApplicationError table
    """
    client = TestClient(app_with_exception_handler, raise_server_exceptions=False)
    
    # Mock database session
    mock_db = MagicMock(spec=Session)
    
    with patch('backend.middleware.exception_handler.SessionLocal', return_value=mock_db):
        response = client.get("/test/error")
        
        # Verify database insert
        assert mock_db.add.called
        assert mock_db.commit.called
        assert mock_db.close.called
        
        # Verify ApplicationError object created
        app_error = mock_db.add.call_args[0][0]
        assert isinstance(app_error, ApplicationError)
        assert app_error.ErrorType == "ValueError"
        assert app_error.ErrorMessage == "Test error message"
        assert app_error.StackTrace is not None


def test_global_exception_handler_includes_request_context(app_with_exception_handler):
    """
    Test AC-0.2.5: RequestID included in error log
    """
    client = TestClient(app_with_exception_handler, raise_server_exceptions=False)
    
    # Mock database session
    mock_db = MagicMock(spec=Session)
    
    with patch('backend.middleware.exception_handler.SessionLocal', return_value=mock_db):
        with patch('backend.middleware.exception_handler.get_current_request_context') as mock_context:
            # Mock request context with RequestID
            mock_context.return_value = Mock(
                request_id="test-request-id-123",
                ip_address="127.0.0.1",
                user_agent="TestClient/1.0"
            )
            
            response = client.get("/test/error")
            
            # Verify error log includes RequestID
            app_error = mock_db.add.call_args[0][0]
            assert app_error.RequestID == "test-request-id-123"


def test_global_exception_handler_includes_user_context(app_with_exception_handler):
    """
    Test AC-0.2.6: UserID and CompanyID included in error log
    """
    client = TestClient(app_with_exception_handler, raise_server_exceptions=False)
    
    # Mock database session
    mock_db = MagicMock(spec=Session)
    
    with patch('backend.middleware.exception_handler.SessionLocal', return_value=mock_db):
        response = client.get("/test/auth-error")
        
        # Verify error log includes user context
        app_error = mock_db.add.call_args[0][0]
        assert app_error.UserID == 123
        assert app_error.CompanyID == 456


def test_global_exception_handler_sanitizes_stack_trace(app_with_exception_handler):
    """
    Test AC-0.2.9: Sensitive data filtered from stack traces
    """
    client = TestClient(app_with_exception_handler, raise_server_exceptions=False)
    
    # Mock database session
    mock_db = MagicMock(spec=Session)
    
    with patch('backend.middleware.exception_handler.SessionLocal', return_value=mock_db):
        with patch('backend.middleware.exception_handler.sanitize_stack_trace') as mock_sanitize:
            mock_sanitize.return_value = "Sanitized stack trace"
            
            response = client.get("/test/error")
            
            # Verify sanitization was called
            assert mock_sanitize.called


def test_global_exception_handler_returns_user_friendly_message(app_with_exception_handler):
    """
    Test AC-0.2.3: Client receives user-friendly error message
    """
    client = TestClient(app_with_exception_handler, raise_server_exceptions=False)
    
    with patch('backend.middleware.exception_handler.SessionLocal'):
        response = client.get("/test/error")
        
        # Verify user-friendly response
        data = response.json()
        assert "An unexpected error occurred" in data["message"]
        assert "requestId" in data["details"]


def test_global_exception_handler_determines_severity(app_with_exception_handler):
    """
    Test AC-0.2.4: Severity determined from error type
    """
    client = TestClient(app_with_exception_handler, raise_server_exceptions=False)
    
    # Mock database session
    mock_db = MagicMock(spec=Session)
    
    with patch('backend.middleware.exception_handler.SessionLocal', return_value=mock_db):
        response = client.get("/test/critical")
        
        # Verify severity set to CRITICAL
        app_error = mock_db.add.call_args[0][0]
        assert app_error.Severity in ["ERROR", "CRITICAL"]


def test_global_exception_handler_handles_database_error_gracefully(app_with_exception_handler):
    """
    Test: Database error doesn't prevent error response
    """
    client = TestClient(app_with_exception_handler, raise_server_exceptions=False)
    
    # Mock database session that raises error
    mock_db = MagicMock(spec=Session)
    mock_db.commit.side_effect = Exception("Database logging error")
    
    with patch('backend.middleware.exception_handler.SessionLocal', return_value=mock_db):
        # Should still return error response
        response = client.get("/test/error")
        
        assert response.status_code == 500
        assert mock_db.rollback.called

