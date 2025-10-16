"""
Unit Tests for Request Logging Middleware
Tests AC-0.2.1, AC-0.2.2, AC-0.2.5, AC-0.2.6, AC-0.2.10
"""
import pytest
import uuid
from unittest.mock import Mock, patch, MagicMock
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.middleware.request_logger import RequestLoggingMiddleware, log_api_request
from backend.models.log.api_request import ApiRequest


# Test fixture: FastAPI app with middleware
@pytest.fixture
def app_with_middleware():
    """Create test FastAPI app with request logging middleware."""
    app = FastAPI()
    app.add_middleware(RequestLoggingMiddleware)
    
    @app.get("/test")
    async def test_endpoint():
        return {"message": "test"}
    
    @app.post("/test")
    async def test_post_endpoint(data: dict):
        return {"message": "created", "data": data}
    
    @app.get("/test/auth")
    async def test_auth_endpoint(request: Request):
        # Simulate JWT middleware setting user context
        request.state.user_id = 123
        request.state.company_id = 456
        return {"message": "authenticated"}
    
    return app


def test_request_logging_middleware_generates_request_id(app_with_middleware):
    """
    Test AC-0.2.5: Request ID generated for each request
    """
    client = TestClient(app_with_middleware)
    
    with patch('backend.middleware.request_logger.log_api_request'):
        response = client.get("/test")
        
        # Verify X-Request-ID header present
        assert "X-Request-ID" in response.headers
        
        # Verify it's a valid UUID
        request_id = response.headers["X-Request-ID"]
        uuid.UUID(request_id)  # Raises ValueError if invalid


def test_request_logging_middleware_logs_get_request(app_with_middleware):
    """
    Test AC-0.2.1, AC-0.2.2: Middleware logs GET requests
    """
    client = TestClient(app_with_middleware)
    
    with patch('backend.middleware.request_logger.log_api_request') as mock_log:
        response = client.get("/test?key=value")
        
        # Verify logging was called
        assert mock_log.called
        
        # Verify log data
        log_data = mock_log.call_args[0][0]
        assert log_data["method"] == "GET"
        assert log_data["path"] == "/test"
        assert log_data["status_code"] == 200
        assert log_data["duration_ms"] >= 0
        assert "request_id" in log_data


def test_request_logging_middleware_logs_post_request(app_with_middleware):
    """
    Test AC-0.2.1: Middleware logs POST requests
    """
    client = TestClient(app_with_middleware)
    
    with patch('backend.middleware.request_logger.log_api_request') as mock_log:
        response = client.post("/test", json={"name": "test"})
        
        # Verify logging was called
        assert mock_log.called
        
        # Verify log data
        log_data = mock_log.call_args[0][0]
        assert log_data["method"] == "POST"
        assert log_data["status_code"] == 200


def test_request_logging_middleware_captures_user_context(app_with_middleware):
    """
    Test AC-0.2.6: UserID and CompanyID extracted from JWT
    """
    client = TestClient(app_with_middleware)
    
    with patch('backend.middleware.request_logger.log_api_request') as mock_log:
        response = client.get("/test/auth")
        
        # Verify user context captured
        log_data = mock_log.call_args[0][0]
        assert log_data["user_id"] == 123
        assert log_data["company_id"] == 456


def test_request_logging_middleware_anonymous_request(app_with_middleware):
    """
    Test AC-0.2.6: Anonymous requests have NULL UserID/CompanyID
    """
    client = TestClient(app_with_middleware)
    
    with patch('backend.middleware.request_logger.log_api_request') as mock_log:
        response = client.get("/test")
        
        # Verify user context is None
        log_data = mock_log.call_args[0][0]
        assert log_data["user_id"] is None
        assert log_data["company_id"] is None


def test_request_logging_middleware_captures_ip_and_user_agent(app_with_middleware):
    """
    Test AC-0.2.2: IPAddress and UserAgent captured
    """
    client = TestClient(app_with_middleware)
    
    with patch('backend.middleware.request_logger.log_api_request') as mock_log:
        response = client.get("/test", headers={"User-Agent": "TestClient/1.0"})
        
        # Verify client info captured
        log_data = mock_log.call_args[0][0]
        assert log_data["ip_address"] is not None
        assert log_data["user_agent"] == "TestClient/1.0"


def test_request_logging_middleware_measures_duration(app_with_middleware):
    """
    Test AC-0.2.10: Duration measured accurately
    """
    client = TestClient(app_with_middleware)
    
    with patch('backend.middleware.request_logger.log_api_request') as mock_log:
        response = client.get("/test")
        
        # Verify duration is measured
        log_data = mock_log.call_args[0][0]
        assert log_data["duration_ms"] >= 0
        assert isinstance(log_data["duration_ms"], int)


def test_log_api_request_database_insert():
    """
    Test AC-0.2.2: Request logged to log.ApiRequest table
    """
    log_data = {
        "request_id": str(uuid.uuid4()),
        "method": "GET",
        "path": "/test",
        "query_params": "key=value",
        "status_code": 200,
        "duration_ms": 50,
        "user_id": 123,
        "company_id": 456,
        "ip_address": "127.0.0.1",
        "user_agent": "TestClient/1.0",
    }
    
    # Mock database session
    mock_db = MagicMock(spec=Session)
    
    with patch('backend.middleware.request_logger.SessionLocal', return_value=mock_db):
        log_api_request(log_data)
        
        # Verify database insert
        assert mock_db.add.called
        assert mock_db.commit.called
        assert mock_db.close.called
        
        # Verify ApiRequest object created
        api_request = mock_db.add.call_args[0][0]
        assert isinstance(api_request, ApiRequest)
        assert api_request.RequestID == log_data["request_id"]
        assert api_request.Method == "GET"
        assert api_request.StatusCode == 200


def test_request_logging_sanitizes_query_params(app_with_middleware):
    """
    Test AC-0.2.9: Sensitive query params are sanitized
    """
    client = TestClient(app_with_middleware)
    
    with patch('backend.middleware.request_logger.log_api_request') as mock_log:
        response = client.get("/test?key=value&token=secret123")
        
        # Verify query params sanitized
        log_data = mock_log.call_args[0][0]
        assert "[REDACTED]" in log_data["query_params"]
        assert "secret123" not in log_data["query_params"]


def test_request_logging_handles_database_error_gracefully():
    """
    Test: Database error doesn't fail the request
    """
    log_data = {
        "request_id": str(uuid.uuid4()),
        "method": "GET",
        "path": "/test",
        "query_params": None,
        "status_code": 200,
        "duration_ms": 50,
        "user_id": None,
        "company_id": None,
        "ip_address": "127.0.0.1",
        "user_agent": "TestClient/1.0",
    }
    
    # Mock database session that raises error
    mock_db = MagicMock(spec=Session)
    mock_db.commit.side_effect = Exception("Database error")
    
    with patch('backend.middleware.request_logger.SessionLocal', return_value=mock_db):
        # Should not raise exception
        log_api_request(log_data)
        
        # Verify rollback called
        assert mock_db.rollback.called
        assert mock_db.close.called

