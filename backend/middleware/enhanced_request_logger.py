"""
Enhanced Request Logging Middleware with Payload Capture
Implements stream duplication to capture request payloads without consuming the stream
"""
import time
import uuid
import json
import asyncio
from typing import Callable, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.background import BackgroundTask
from starlette.types import ASGIApp, Scope, Receive, Send
from sqlalchemy.orm import Session
from io import BytesIO

from common.database import SessionLocal
from common.request_context import set_request_context, clear_request_context
from common.log_filters import sanitize_query_params
from common.config_service import ConfigurationService
from models.log.api_request import ApiRequest


class EnhancedRequestLoggingMiddleware:
    """
    ASGI middleware that captures request/response payloads without consuming streams.
    
    This middleware uses stream duplication to allow both logging and endpoint processing
    to read the request body without conflicts.
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
        
        # Create a custom receive function that duplicates the request body
        request_body = b""
        original_receive = receive
        
        async def custom_receive():
            nonlocal request_body
            message = await original_receive()
            
            if message["type"] == "http.request":
                body = message.get("body", b"")
                request_body += body
                
                # Create a new message with the same body for the endpoint
                new_message = message.copy()
                new_message["body"] = body
                return new_message
            
            return message
        
        # Wrap the send function to capture response
        response_body = b""
        original_send = send
        
        async def custom_send(message):
            nonlocal response_body
            if message["type"] == "http.response.body":
                body = message.get("body", b"")
                response_body += body
            
            await original_send(message)
        
        # Process the request
        await self.app(scope, custom_receive, custom_send)
        
        # Now log the request and response data
        await self._log_request_response(scope, request_id, request_body, response_body)

    async def _log_request_response(self, scope: Scope, request_id: str, request_body: bytes, response_body: bytes):
        """Log the request and response data"""
        try:
            # Extract request details
            method = scope["method"]
            path = scope["path"]
            query_string = scope.get("query_string", b"").decode()
            headers = dict(scope["headers"])
            
            # Get logging configuration
            config = self._get_logging_config()
            
            # Extract client info
            client = scope.get("client")
            ip_address = client[0] if client else None
            user_agent = headers.get(b"user-agent", b"").decode() if b"user-agent" in headers else None
            
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
                headers_json = self._capture_headers(headers)
            
            # Prepare log data
            log_data = {
                "request_id": request_id,
                "method": method,
                "path": path,
                "query_params": sanitize_query_params(query_string) if query_string else None,
                "status_code": 200,  # We don't have access to status code in ASGI middleware
                "duration_ms": 0,  # We don't have timing in this approach
                "user_id": None,  # Would need to be extracted from JWT
                "company_id": None,  # Would need to be extracted from JWT
                "ip_address": ip_address,
                "user_agent": user_agent,
                "request_payload": request_payload,
                "response_payload": response_payload,
                "headers": headers_json,
            }
            
            # Log to database in background
            await self._log_to_database(log_data)
            
        except Exception as e:
            print(f"Error in enhanced request logging: {e}")
        finally:
            clear_request_context()

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

    def _capture_headers(self, headers: dict) -> Optional[str]:
        """Capture request headers as JSON string"""
        try:
            # Filter out sensitive headers
            sensitive_headers = {b"authorization", b"cookie", b"x-api-key", b"x-auth-token"}
            
            filtered_headers = {
                key.decode(): value.decode() for key, value in headers.items()
                if key.lower() not in sensitive_headers
            }
            
            return json.dumps(filtered_headers, indent=2)
            
        except Exception as e:
            print(f"Error capturing headers: {e}")
            return None

    async def _log_to_database(self, log_data: dict):
        """Log to database in background"""
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
        import threading
        thread = threading.Thread(target=log_api_request)
        thread.start()
