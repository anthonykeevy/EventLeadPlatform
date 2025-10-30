"""
Request Logging Middleware
Automatically logs all API requests to log.ApiRequest table with enhanced payload capture
"""
import time
import uuid
import json
from typing import Callable, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.background import BackgroundTask
from sqlalchemy.orm import Session

from common.database import SessionLocal
from common.request_context import set_request_context, clear_request_context
from common.log_filters import sanitize_query_params
from common.config_service import ConfigurationService
from models.log.api_request import ApiRequest


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Enhanced middleware that automatically logs all API requests with payload capture.
    
    Features:
    - Generates unique RequestID (UUID4) for each request
    - Captures request details: Method, Path, QueryParams, StatusCode, DurationMs
    - Extracts UserID and CompanyID from request.state (set by JWT middleware)
    - Extracts IPAddress and UserAgent from request headers
    - Enhanced payload logging with configurable size limits and exclusion list
    - Logs to log.ApiRequest table asynchronously (non-blocking)
    - Adds X-Request-ID header to response for client tracking
    
    Configuration (via database settings):
    - logging.capture_payloads: Enable/disable payload capture (default: false)
    - logging.max_payload_size_kb: Maximum payload size in KB (default: 10)
    - logging.excluded_endpoints: List of endpoints to exclude (default: ["/api/health"])
    """
    
    def __init__(self, app):
        super().__init__(app)
        self._config_cache = {}
        self._config_cache_timestamp = None
        self._config_cache_ttl = 300  # 5 minutes


    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and log details with enhanced payload capture.
        
        Args:
            request: FastAPI request object
            call_next: Next middleware/route handler in chain
            
        Returns:
            Response with X-Request-ID header added
        """
        # Generate unique RequestID
        request_id = str(uuid.uuid4())
        
        # Extract client info
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        # Set request context (available throughout request lifecycle)
        set_request_context(
            request_id=request_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Get logging configuration
        config = self._get_logging_config()
        
        # Capture request payload if enabled and not excluded
        request_payload = None
        if config["capture_payloads"] and not self._is_endpoint_excluded(request.url.path, config["excluded_endpoints"]):
            # Store the body in request context for later use
            if request.method in ["POST", "PUT", "PATCH"]:
                try:
                    body = await request.body()
                    if body:
                        # Store in request context so endpoints can still access it
                        request.state._cached_body = body
                        request_payload = self._process_payload(body, config["max_payload_size_kb"])
                except Exception as e:
                    print(f"Error capturing request payload: {e}")
                    request_payload = None
        
        # Start timing
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Extract user context (set by JWT middleware if authenticated)
        user_id = getattr(request.state, "user_id", None)
        company_id = getattr(request.state, "company_id", None)
        
        # Capture response payload if enabled and not excluded
        response_payload = None
        if config["capture_payloads"] and not self._is_endpoint_excluded(request.url.path, config["excluded_endpoints"]):
            response_payload = await self._capture_response_payload(response, config["max_payload_size_kb"])
        
        # Capture headers if enabled
        headers = None
        if config["capture_payloads"]:
            headers = self._capture_headers(request)
        
        # Prepare log data
        log_data = {
            "request_id": request_id,
            "method": request.method,
            "path": str(request.url.path),
            "query_params": sanitize_query_params(str(request.url.query)) if request.url.query else None,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "user_id": user_id,
            "company_id": company_id,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "request_payload": request_payload,
            "response_payload": response_payload,
            "headers": headers,
        }
        
        # Schedule background task to log to database (non-blocking)
        background_task = BackgroundTask(log_api_request, log_data)
        response.background = background_task
        
        # Add RequestID to response headers (for client tracking)
        response.headers["X-Request-ID"] = request_id
        
        # Clear request context after response (cleanup)
        clear_request_context()
        
        return response
    
    def _get_logging_config(self) -> dict:
        """
        Get logging configuration with caching.
        
        Returns:
            Dictionary with logging configuration settings
        """
        # Check cache first
        if self._is_config_cache_valid():
            return self._config_cache
        
        # Get fresh configuration from database
        db = SessionLocal()
        try:
            config_service = ConfigurationService(db)
            
            config = {
                "capture_payloads": config_service.get_logging_capture_payloads(),
                "max_payload_size_kb": config_service.get_logging_max_payload_size_kb(),
                "excluded_endpoints": config_service.get_logging_excluded_endpoints(),
            }
            
            # Cache the configuration
            self._config_cache = config
            self._config_cache_timestamp = time.time()
            
            return config
            
        except Exception as e:
            # Fallback to defaults if database unavailable
            print(f"Error getting logging config: {e}, using enhanced defaults")
            return {
                "capture_payloads": True,  # Enable for testing
                "max_payload_size_kb": 10,
                "excluded_endpoints": ["/api/health"],
            }
        finally:
            db.close()
    
    def _is_config_cache_valid(self) -> bool:
        """Check if configuration cache is still valid."""
        if self._config_cache_timestamp is None:
            return False
        
        elapsed = time.time() - self._config_cache_timestamp
        return elapsed < self._config_cache_ttl
    
    def _is_endpoint_excluded(self, path: str, excluded_endpoints: list[str]) -> bool:
        """
        Check if endpoint should be excluded from payload logging.
        
        Args:
            path: Request path
            excluded_endpoints: List of excluded endpoint patterns
            
        Returns:
            True if endpoint should be excluded, False otherwise
        """
        for excluded in excluded_endpoints:
            if path.startswith(excluded):
                return True
        return False
    
    def _process_payload(self, body: bytes, max_size_kb: int) -> Optional[str]:
        """
        Process payload with size limit and truncation indicator.
        
        Args:
            body: Request body bytes
            max_size_kb: Maximum payload size in KB
            
        Returns:
            JSON string of payload or None if not applicable
        """
        try:
            if not body:
                return None
            
            # Convert to string and check size
            body_str = body.decode('utf-8')
            max_size_bytes = max_size_kb * 1024
            
            if len(body_str) <= max_size_bytes:
                return body_str
            else:
                # Truncate and add indicator
                truncated = body_str[:max_size_bytes]
                return f"{truncated}... [TRUNCATED - Original size: {len(body_str)} bytes]"
                
        except Exception as e:
            print(f"Error processing payload: {e}")
            return None

    async def _capture_request_payload(self, request: Request, max_size_kb: int) -> Optional[str]:
        """
        Capture request payload with size limit and truncation indicator.
        This method is kept for compatibility but the main logic is now in dispatch.
        
        Args:
            request: FastAPI request object
            max_size_kb: Maximum payload size in KB
            
        Returns:
            JSON string of request payload or None if not applicable
        """
        # This method is now handled in the main dispatch method
        return None
    
    async def _capture_response_payload(self, response: Response, max_size_kb: int) -> Optional[str]:
        """
        Capture response payload with size limit and truncation indicator.
        
        Args:
            response: FastAPI response object
            max_size_kb: Maximum payload size in KB
            
        Returns:
            JSON string of response payload or None if not applicable
        """
        try:
            # Only capture for successful responses with content
            if response.status_code < 200 or response.status_code >= 300:
                return None
            
            # Get response body
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            
            if not body:
                return None
            
            # Convert to string and check size
            body_str = body.decode('utf-8')
            max_size_bytes = max_size_kb * 1024
            
            if len(body_str) <= max_size_bytes:
                return body_str
            else:
                # Truncate and add indicator
                truncated = body_str[:max_size_bytes]
                return f"{truncated}... [TRUNCATED - Original size: {len(body_str)} bytes]"
                
        except Exception as e:
            print(f"Error capturing response payload: {e}")
            return None
    
    def _capture_headers(self, request: Request) -> Optional[str]:
        """
        Capture request headers as JSON string.
        
        Args:
            request: FastAPI request object
            
        Returns:
            JSON string of headers or None if error
        """
        try:
            # Filter out sensitive headers
            sensitive_headers = {"authorization", "cookie", "x-api-key", "x-auth-token"}
            
            headers = {
                name: value for name, value in request.headers.items()
                if name.lower() not in sensitive_headers
            }
            
            return json.dumps(headers, indent=2)
            
        except Exception as e:
            print(f"Error capturing headers: {e}")
            return None


def log_api_request(log_data: dict) -> None:
    """
    Log API request to database (runs in background).
    
    Args:
        log_data: Dictionary containing request details
    """
    db: Session = SessionLocal()
    try:
        api_request = ApiRequest(
            RequestID=log_data["request_id"],
            Method=log_data["method"],
            Path=log_data["path"],
            QueryParams=log_data["query_params"],
            StatusCode=log_data["status_code"],
            DurationMs=log_data["duration_ms"],
            UserID=log_data["user_id"],
            CompanyID=log_data["company_id"],
            IPAddress=log_data["ip_address"],
            UserAgent=log_data["user_agent"],
            RequestPayload=log_data.get("request_payload"),
            ResponsePayload=log_data.get("response_payload"),
            Headers=log_data.get("headers"),
        )
        
        db.add(api_request)
        db.commit()
    except Exception as e:
        # Log error but don't fail the request
        print(f"Error logging API request: {str(e)}")
        db.rollback()
    finally:
        db.close()

