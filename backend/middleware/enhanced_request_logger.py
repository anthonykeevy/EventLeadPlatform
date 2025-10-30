"""
Enhanced Request Logging Middleware with Payload Capture
Implements proper ASGI middleware with stream duplication for payload capture
"""
import time
import uuid
import json
import threading
from typing import Callable, Optional, Dict, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.background import BackgroundTask
from starlette.types import ASGIApp, Scope, Receive, Send
from sqlalchemy.orm import Session

from common.database import SessionLocal
from common.request_context import set_request_context, clear_request_context
from common.log_filters import sanitize_query_params
from common.config_service import ConfigurationService
from models.log.api_request import ApiRequest


class EnhancedRequestLoggingMiddleware:
    """
    ASGI middleware that captures request/response payloads without consuming streams.
    
    This middleware uses proper ASGI stream duplication to allow both logging and 
    endpoint processing to read the request body without conflicts.
    
    Key Features:
    - Proper ASGI implementation with wrapped_receive/wrapped_send
    - Accurate timing and status code capture
    - JWT token extraction for user context
    - Chunk accumulation for complete request/response bodies
    - Non-blocking database writes
    - Comprehensive error handling
    """
    
    def __init__(self, app: ASGIApp):
        self.app = app
        self._config_cache = {}
        self._config_cache_timestamp = None
        self._config_cache_ttl = 300  # 5 minutes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Generate unique RequestID
        request_id = str(uuid.uuid4())
        
        # Track timing
        start_time = time.time()
        
        # Track request/response data
        request_body = b""
        response_body = b""
        status_code = 200
        headers_dict = {}
        
        # Create wrapped receive function
        async def wrapped_receive():
            nonlocal request_body
            message = await receive()
            
            if message["type"] == "http.request":
                body = message.get("body", b"")
                request_body += body
                
                # Create new message with same body for endpoint
                new_message = message.copy()
                new_message["body"] = body
                return new_message
            
            return message
        
        # Create wrapped send function
        async def wrapped_send(message):
            nonlocal response_body, status_code, headers_dict
            
            if message["type"] == "http.response.start":
                status_code = message.get("status", 200)
                headers_list = message.get("headers", [])
                headers_dict = {key.decode(): value.decode() for key, value in headers_list}
            
            elif message["type"] == "http.response.body":
                body = message.get("body", b"")
                response_body += body
            
            await send(message)
        
        # Process the request
        await self.app(scope, wrapped_receive, wrapped_send)
        
        # Calculate duration
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Log request/response data in background (don't let logging errors affect the request)
        try:
            await self._log_request_response(
                scope, request_id, request_body, response_body, 
                status_code, duration_ms, headers_dict
            )
        except Exception as e:
            # Log error but don't fail the request
            print(f"Error in enhanced request logging: {e}")

    async def _log_request_response(
        self, scope: Scope, request_id: str, request_body: bytes, 
        response_body: bytes, status_code: int, duration_ms: int, 
        headers_dict: Dict[str, str]
    ):
        """Log the request and response data"""
        try:
            # Extract request details
            method = scope["method"]
            path = scope["path"]
            query_string = scope.get("query_string", b"").decode()
            
            # Get logging configuration
            config = self._get_logging_config()
            
            # Extract client info
            client = scope.get("client")
            ip_address = client[0] if client else None
            user_agent = headers_dict.get("user-agent")
            
            # Extract user context from JWT token
            user_id, company_id = self._extract_user_context(headers_dict)
            
            # Set request context
            set_request_context(
                request_id=request_id,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            # Capture request payload if enabled and not excluded
            request_payload = None
            if config["capture_payloads"] and not self._is_endpoint_excluded(path, config["excluded_endpoints"]):
                request_payload = self._process_request_payload(request_body, method, config["max_payload_size_kb"])
            
            # Capture response payload if enabled and not excluded
            response_payload = None
            if config["capture_payloads"] and not self._is_endpoint_excluded(path, config["excluded_endpoints"]):
                response_payload = self._process_response_payload(response_body, config["max_payload_size_kb"])
            
            # Capture headers if enabled
            headers_json = None
            if config["capture_payloads"]:
                headers_json = self._capture_headers(headers_dict)
            
            # Prepare log data
            log_data = {
                "request_id": request_id,
                "method": method,
                "path": path,
                "query_params": sanitize_query_params(query_string) if query_string else None,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "user_id": user_id,
                "company_id": company_id,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "request_payload": request_payload,
                "response_payload": response_payload,
                "headers": headers_json,
            }
            
            # Log to database in background thread
            self._log_to_database_async(log_data)
            
        except Exception as e:
            print(f"Error in enhanced request logging: {e}")
        finally:
            clear_request_context()

    def _extract_user_context(self, headers_dict: Dict[str, str]) -> tuple[Optional[int], Optional[int]]:
        """
        Extract user_id and company_id from JWT token in Authorization header.
        
        Args:
            headers_dict: Dictionary of request headers
            
        Returns:
            Tuple of (user_id, company_id) or (None, None) if not found/invalid
        """
        try:
            auth_header = headers_dict.get("authorization", "")
            if not auth_header.startswith("Bearer "):
                return None, None
            
            token = auth_header[7:]  # Remove "Bearer " prefix
            
            # Import JWT service and decode token
            from modules.auth.jwt_service import decode_token
            payload = decode_token(token)
            
            user_id = int(payload["sub"]) if "sub" in payload else None
            company_id = payload.get("company_id")
            if company_id:
                company_id = int(company_id)
            
            return user_id, company_id
            
        except Exception as e:
            # Token is invalid or missing - this is normal for unauthenticated requests
            return None, None

    def _get_logging_config(self) -> dict:
        """Get logging configuration with caching"""
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
                "capture_payloads": True,  # Enable by default for testing
                "max_payload_size_kb": 10,
                "excluded_endpoints": ["/api/health"],
            }
        finally:
            db.close()

    def _is_config_cache_valid(self) -> bool:
        """Check if configuration cache is still valid"""
        if self._config_cache_timestamp is None:
            return False
        
        elapsed = time.time() - self._config_cache_timestamp
        return elapsed < self._config_cache_ttl

    def _is_endpoint_excluded(self, path: str, excluded_endpoints: list[str]) -> bool:
        """Check if endpoint should be excluded from payload logging"""
        for excluded in excluded_endpoints:
            if path.startswith(excluded):
                return True
        return False

    def _process_request_payload(self, body: bytes, method: str, max_size_kb: int) -> Optional[str]:
        """Process request payload with size limits"""
        try:
            # Only capture for methods that typically have bodies
            if method not in ["POST", "PUT", "PATCH"]:
                return None
            
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
            print(f"Error processing request payload: {e}")
            return None

    def _process_response_payload(self, body: bytes, max_size_kb: int) -> Optional[str]:
        """Process response payload with size limits"""
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
            print(f"Error processing response payload: {e}")
            return None

    def _capture_headers(self, headers_dict: Dict[str, str]) -> Optional[str]:
        """Capture request headers as JSON string"""
        try:
            # Filter out sensitive headers
            sensitive_headers = {"authorization", "cookie", "x-api-key", "x-auth-token"}
            
            filtered_headers = {
                name: value for name, value in headers_dict.items()
                if name.lower() not in sensitive_headers
            }
            
            return json.dumps(filtered_headers, indent=2)
            
        except Exception as e:
            print(f"Error capturing headers: {e}")
            return None

    def _log_to_database_async(self, log_data: dict):
        """Log to database in background thread"""
        def log_api_request():
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
                print(f"Error logging API request: {e}")
                db.rollback()
            finally:
                db.close()
        
        # Run in background thread
        thread = threading.Thread(target=log_api_request)
        thread.daemon = True  # Don't prevent app shutdown
        thread.start()