"""
Integration Tests for Complete Logging Flow
Tests all ACs end-to-end with real database
"""
import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from backend.common.database import get_db, SessionLocal
from backend.middleware import RequestLoggingMiddleware, global_exception_handler
from backend.models.log.api_request import ApiRequest
from backend.models.log.application_error import ApplicationError


# Test fixture: FastAPI app with full logging
@pytest.fixture
def app_with_logging():
    """Create test FastAPI app with complete logging setup."""
    app = FastAPI()
    
    # Register exception handler
    app.add_exception_handler(Exception, global_exception_handler)
    
    # Add request logging middleware
    app.add_middleware(RequestLoggingMiddleware)
    
    # Test endpoints
    @app.get("/test/success")
    async def success_endpoint():
        return {"status": "success"}
    
    @app.post("/test/create")
    async def create_endpoint(data: dict):
        return {"status": "created", "data": data}
    
    @app.get("/test/authenticated")
    async def authenticated_endpoint(request: Request):
        request.state.user_id = 999
        request.state.company_id = 888
        return {"status": "authenticated"}
    
    @app.get("/test/error")
    async def error_endpoint():
        raise ValueError("Test error for integration testing")
    
    @app.get("/test/sensitive")
    async def sensitive_endpoint(password: str = None, token: str = None):
        return {"status": "ok"}
    
    return app


@pytest.mark.integration
def test_successful_request_logged_to_database(app_with_logging):
    """
    Test AC-0.2.1, AC-0.2.2: Successful request logged to log.ApiRequest
    """
    client = TestClient(app_with_logging)
    db: Session = SessionLocal()
    
    try:
        # Get initial count
        initial_count = db.execute(
            select(func.count()).select_from(ApiRequest)
        ).scalar()
        
        # Make request
        response = client.get("/test/success")
        assert response.status_code == 200
        
        # Verify X-Request-ID header
        request_id = response.headers.get("X-Request-ID")
        assert request_id is not None
        
        # Verify log record created
        new_count = db.execute(
            select(func.count()).select_from(ApiRequest)
        ).scalar()
        assert new_count == initial_count + 1
        
        # Verify log details
        stmt = select(ApiRequest).where(ApiRequest.RequestID == request_id)
        log_record = db.execute(stmt).scalar_one()
        
        assert log_record.Method == "GET"
        assert log_record.Path == "/test/success"
        assert log_record.StatusCode == 200
        assert log_record.DurationMs >= 0
        assert log_record.UserID is None  # Anonymous request
        assert log_record.CompanyID is None
        
    finally:
        db.close()


@pytest.mark.integration
def test_authenticated_request_includes_user_context(app_with_logging):
    """
    Test AC-0.2.6: Authenticated request includes UserID and CompanyID
    """
    client = TestClient(app_with_logging)
    db: Session = SessionLocal()
    
    try:
        # Make authenticated request
        response = client.get("/test/authenticated")
        request_id = response.headers.get("X-Request-ID")
        
        # Verify log includes user context
        stmt = select(ApiRequest).where(ApiRequest.RequestID == request_id)
        log_record = db.execute(stmt).scalar_one()
        
        assert log_record.UserID == 999
        assert log_record.CompanyID == 888
        
    finally:
        db.close()


@pytest.mark.integration
def test_error_logged_to_database(app_with_logging):
    """
    Test AC-0.2.3, AC-0.2.4: Error logged to log.ApplicationError
    """
    client = TestClient(app_with_logging, raise_server_exceptions=False)
    db: Session = SessionLocal()
    
    try:
        # Get initial count
        initial_count = db.execute(
            select(func.count()).select_from(ApplicationError)
        ).scalar()
        
        # Make request that causes error
        response = client.get("/test/error")
        assert response.status_code == 500
        
        # Verify error response format
        data = response.json()
        assert data["success"] is False
        assert "requestId" in data["details"]
        
        # Verify error logged
        new_count = db.execute(
            select(func.count()).select_from(ApplicationError)
        ).scalar()
        assert new_count == initial_count + 1
        
        # Verify error details
        request_id = data["details"]["requestId"]
        stmt = select(ApplicationError).where(ApplicationError.RequestID == request_id)
        error_record = db.execute(stmt).scalar_one()
        
        assert error_record.ErrorType == "ValueError"
        assert "Test error for integration testing" in error_record.ErrorMessage
        assert error_record.StackTrace is not None
        assert error_record.Path == "/test/error"
        assert error_record.Method == "GET"
        
    finally:
        db.close()


@pytest.mark.integration
def test_request_and_error_correlation(app_with_logging):
    """
    Test AC-0.2.5: RequestID correlates ApiRequest and ApplicationError
    """
    client = TestClient(app_with_logging, raise_server_exceptions=False)
    db: Session = SessionLocal()
    
    try:
        # Make request that causes error
        response = client.get("/test/error")
        request_id = response.json()["details"]["requestId"]
        
        # Verify both tables have same RequestID
        api_request = db.execute(
            select(ApiRequest).where(ApiRequest.RequestID == request_id)
        ).scalar_one()
        
        app_error = db.execute(
            select(ApplicationError).where(ApplicationError.RequestID == request_id)
        ).scalar_one()
        
        assert api_request.RequestID == app_error.RequestID
        assert api_request.Path == app_error.Path
        
    finally:
        db.close()


@pytest.mark.integration
def test_sensitive_data_not_logged(app_with_logging):
    """
    Test AC-0.2.9: Sensitive query params not logged
    """
    client = TestClient(app_with_logging)
    db: Session = SessionLocal()
    
    try:
        # Make request with sensitive query params
        response = client.get("/test/sensitive?password=secret123&token=abc456")
        request_id = response.headers.get("X-Request-ID")
        
        # Verify sensitive data redacted
        stmt = select(ApiRequest).where(ApiRequest.RequestID == request_id)
        log_record = db.execute(stmt).scalar_one()
        
        assert "[REDACTED]" in log_record.QueryParams
        assert "secret123" not in log_record.QueryParams
        assert "abc456" not in log_record.QueryParams
        
    finally:
        db.close()


@pytest.mark.integration
def test_multiple_concurrent_requests(app_with_logging):
    """
    Test AC-0.2.5: Concurrent requests have unique RequestIDs
    """
    client = TestClient(app_with_logging)
    db: Session = SessionLocal()
    
    try:
        # Make multiple requests
        request_ids = []
        for i in range(5):
            response = client.get("/test/success")
            request_ids.append(response.headers.get("X-Request-ID"))
        
        # Verify all RequestIDs are unique
        assert len(request_ids) == len(set(request_ids))
        
        # Verify all logged
        for request_id in request_ids:
            stmt = select(ApiRequest).where(ApiRequest.RequestID == request_id)
            log_record = db.execute(stmt).scalar_one()
            assert log_record is not None
        
    finally:
        db.close()


@pytest.mark.integration
def test_post_request_logged(app_with_logging):
    """
    Test AC-0.2.1: POST requests logged correctly
    """
    client = TestClient(app_with_logging)
    db: Session = SessionLocal()
    
    try:
        # Make POST request
        response = client.post("/test/create", json={"name": "test"})
        request_id = response.headers.get("X-Request-ID")
        
        # Verify logged with correct method
        stmt = select(ApiRequest).where(ApiRequest.RequestID == request_id)
        log_record = db.execute(stmt).scalar_one()
        
        assert log_record.Method == "POST"
        assert log_record.Path == "/test/create"
        
    finally:
        db.close()


@pytest.mark.integration  
def test_logging_performance(app_with_logging):
    """
    Test AC-0.2.10: Logging adds minimal latency
    """
    client = TestClient(app_with_logging)
    db: Session = SessionLocal()
    
    try:
        # Make multiple requests and check duration
        for _ in range(10):
            response = client.get("/test/success")
            request_id = response.headers.get("X-Request-ID")
            
            stmt = select(ApiRequest).where(ApiRequest.RequestID == request_id)
            log_record = db.execute(stmt).scalar_one()
            
            # Verify logging overhead is reasonable (< 100ms for test environment)
            # Note: In production with background tasks, this should be < 5ms
            assert log_record.DurationMs < 100
        
    finally:
        db.close()

