"""
Fixed Bulletproof Request Logging Middleware with Payload Capture
Comprehensive debugging and error handling included.
"""

import json
import time
import uuid
import traceback
from typing import Callable, Optional, Dict, Any, List
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.background import BackgroundTask
from starlette.datastructures import Headers
from io import BytesIO

class CachedBodyRequest(Request):
    """
    Request subclass that caches the body for reuse.
    Critical: This prevents stream consumption issues.
    """
    def __init__(self, request: Request):
        super().__init__(request.scope, request.receive)
        self._cached_body: Optional[bytes] = None
        self._body_consumed = False
        
    async def body(self) -> bytes:
        """Cache and return the request body"""
        if self._cached_body is None:
            self._cached_body = await super().body()
            self._body_consumed = True
        return self._cached_body

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Enhanced bulletproof middleware with comprehensive payload capture
    and extensive debugging capabilities.
    """
    
    def __init__(self, app, debug: bool = True):
        print(f"\n[MIDDLEWARE CONSTRUCTOR] Called with app={type(app).__name__}, debug={debug}")
        super().__init__(app)
        self._debug = debug
        self._sensitive_fields = {
            "password", "token", "secret", "api_key", 
            "apikey", "authorization", "auth", "credential",
            "passwd", "pwd", "private_key", "access_token",
            "refresh_token", "session_id", "sessionid"
        }
        
        # Print initialization
        print("\n" + "="*80)
        print("BULLETPROOF REQUEST LOGGING MIDDLEWARE INITIALIZED")
        print(f"   Debug Mode: {self._debug}")
        print(f"   Sensitive Fields: {len(self._sensitive_fields)} fields masked")
        print(f"   App: {type(app).__name__}")
        print("="*80 + "\n")
        
        # Test configuration retrieval immediately
        try:
            print("[INIT] Testing configuration retrieval...")
            config = self._get_logging_config()
            print(f"[INIT] Configuration test successful: {config}")
        except Exception as e:
            print(f"[INIT] Configuration test failed: {e}")
            import traceback
            print(f"[INIT] Traceback: {traceback.format_exc()}")
    
    def _log_debug(self, message: str, data: Any = None):
        """Centralized debug logging"""
        if self._debug:
            print(f"[DEBUG] {message}")
            if data is not None:
                print(f"        Data: {data}")
    
    def _get_logging_config(self) -> Dict[str, Any]:
        """
        Get logging configuration with extensive debugging.
        Returns config dict with fallback defaults.
        """
        print("[CONFIG] Starting configuration retrieval...")
        self._log_debug("=" * 60)
        self._log_debug("RETRIEVING LOGGING CONFIGURATION")
        
        try:
            print("[CONFIG] Importing configuration service...")
            from common.config_service import ConfigurationService
            from common.constants import (
                DEFAULT_LOGGING_CAPTURE_PAYLOADS,
                DEFAULT_LOGGING_MAX_PAYLOAD_SIZE_KB,
                DEFAULT_LOGGING_EXCLUDED_ENDPOINTS
            )
            print("[CONFIG] Imports successful")
            
            # Create a database session for config service
            print("[CONFIG] Creating database session...")
            from common.database import SessionLocal
            db = SessionLocal()
            print("[CONFIG] Database session created")
            
            print("[CONFIG] Creating configuration service...")
            config_service = ConfigurationService(db)
            print("[CONFIG] Configuration service created")
            
            # Get each setting individually with debug output
            print("[CONFIG] Getting capture_payloads setting...")
            capture_payloads = config_service.get_logging_capture_payloads()
            print(f"[CONFIG] capture_payloads: {capture_payloads}")
            self._log_debug(f"Config 'capture_payloads': {capture_payloads}")
            
            print("[CONFIG] Getting max_payload_size_kb setting...")
            max_size = config_service.get_logging_max_payload_size_kb()
            print(f"[CONFIG] max_payload_size_kb: {max_size}")
            self._log_debug(f"Config 'max_payload_size_kb': {max_size}")
            
            print("[CONFIG] Getting excluded_endpoints setting...")
            excluded = config_service.get_logging_excluded_endpoints()
            print(f"[CONFIG] excluded_endpoints: {excluded}")
            self._log_debug(f"Config 'excluded_endpoints': {excluded}")
            
            config = {
                "capture_payloads": capture_payloads,
                "max_payload_size_kb": max_size,
                "excluded_endpoints": excluded,
            }
            
            print("[CONFIG] Configuration loaded successfully")
            self._log_debug("Configuration loaded successfully")
            self._log_debug("=" * 60)
            db.close()
            print("[CONFIG] Database session closed")
            return config
            
        except Exception as e:
            print(f"[CONFIG] ERROR: {type(e).__name__}: {str(e)}")
            import traceback
            print(f"[CONFIG] Traceback: {traceback.format_exc()}")
            self._log_debug(f"Config service error: {str(e)}")
            self._log_debug(f"   Using fallback configuration")
            
            # FALLBACK: Always enable for debugging
            fallback_config = {
                "capture_payloads": True,  # Force enable for debugging
                "max_payload_size_kb": 50,
                "excluded_endpoints": ["/api/health", "/docs", "/openapi.json", "/redoc", "/favicon.ico"],
            }
            print(f"[CONFIG] Using fallback config: {fallback_config}")
            self._log_debug(f"Fallback config: {fallback_config}")
            self._log_debug("=" * 60)
            return fallback_config
    
    def _is_endpoint_excluded(self, path: str, excluded_endpoints: List[str]) -> bool:
        """Check if endpoint should be excluded from logging"""
        is_excluded = any(path.startswith(ep) for ep in excluded_endpoints)
        if self._debug and is_excluded:
            self._log_debug(f"Endpoint excluded from payload capture: {path}")
        return is_excluded
    
    def _sanitize_payload(self, payload: Any) -> Any:
        """
        Recursively sanitize sensitive fields in payload.
        Works with dicts, lists, and nested structures.
        """
        if isinstance(payload, dict):
            sanitized = {}
            for key, value in payload.items():
                key_lower = key.lower()
                if any(sensitive in key_lower for sensitive in self._sensitive_fields):
                    sanitized[key] = "***REDACTED***"
                else:
                    sanitized[key] = self._sanitize_payload(value)
            return sanitized
        elif isinstance(payload, list):
            return [self._sanitize_payload(item) for item in payload]
        else:
            return payload
    
    async def _capture_request_payload(
        self, 
        request: CachedBodyRequest, 
        max_size_kb: int
    ) -> Optional[str]:
        """
        Capture and process request payload with extensive debugging.
        """
        try:
            self._log_debug("─" * 60)
            self._log_debug("CAPTURING REQUEST PAYLOAD")
            self._log_debug(f"   Method: {request.method}")
            self._log_debug(f"   Content-Type: {request.headers.get('content-type', 'N/A')}")
            
            # Check if method supports body
            if request.method not in ["POST", "PUT", "PATCH", "DELETE"]:
                self._log_debug(f"   Skipping - Method {request.method} typically has no body")
                return None
            
            # Get content-type
            content_type = request.headers.get("content-type", "").lower()
            self._log_debug(f"   Content-Type header: {content_type}")
            
            # Read the body using the cached request
            self._log_debug("   Reading request body...")
            body_bytes = await request.body()
            
            if not body_bytes:
                self._log_debug("   Body is empty (0 bytes)")
                return None
            
            body_size = len(body_bytes)
            self._log_debug(f"   Body read successfully: {body_size} bytes")
            
            # Decode body
            try:
                body_str = body_bytes.decode('utf-8')
                self._log_debug(f"   Decoded as UTF-8: {len(body_str)} characters")
            except UnicodeDecodeError:
                self._log_debug("   Body is not valid UTF-8, storing as base64")
                import base64
                return f"[BINARY DATA: {len(body_bytes)} bytes, base64: {base64.b64encode(body_bytes[:100]).decode()}...]"
            
            # Check size limit
            max_size_bytes = max_size_kb * 1024
            if len(body_str) > max_size_bytes:
                self._log_debug(f"   Truncating payload: {len(body_str)} > {max_size_bytes} bytes")
                truncated = body_str[:max_size_bytes]
                result = f"{truncated}... [TRUNCATED - Original: {len(body_str)} bytes]"
                self._log_debug(f"   Result length: {len(result)}")
                return result
            
            # Try to parse and sanitize JSON
            if "application/json" in content_type or body_str.strip().startswith(("{", "[")):
                try:
                    self._log_debug("   Attempting JSON parse...")
                    json_obj = json.loads(body_str)
                    self._log_debug("   JSON parsed successfully")
                    
                    self._log_debug("   Sanitizing sensitive fields...")
                    sanitized = self._sanitize_payload(json_obj)
                    
                    result = json.dumps(sanitized, indent=2)
                    self._log_debug(f"   Final payload: {len(result)} characters")
                    self._log_debug(f"   Preview: {result[:200]}...")
                    return result
                    
                except json.JSONDecodeError as e:
                    self._log_debug(f"   JSON parse failed: {str(e)}")
                    self._log_debug("   Returning raw body string")
            
            # Return raw body for non-JSON
            self._log_debug(f"   Returning raw body: {len(body_str)} characters")
            self._log_debug(f"   Preview: {body_str[:200]}...")
            return body_str
            
        except Exception as e:
            error_msg = f"[ERROR CAPTURING REQUEST: {type(e).__name__}: {str(e)}]"
            self._log_debug(f"   EXCEPTION: {error_msg}")
            self._log_debug(f"   Traceback: {traceback.format_exc()}")
            return error_msg
    
    async def _capture_response_payload(
        self, 
        response: Response, 
        max_size_kb: int
    ) -> Optional[str]:
        """
        Capture and process response payload with extensive debugging.
        """
        try:
            self._log_debug("─" * 60)
            self._log_debug("CAPTURING RESPONSE PAYLOAD")
            self._log_debug(f"   Status Code: {response.status_code}")
            self._log_debug(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            
            # Check if response has a body attribute
            if not hasattr(response, 'body'):
                self._log_debug("   Response has no 'body' attribute")
                return None
            
            body = response.body
            if not body:
                self._log_debug("   Response body is empty")
                return None
            
            body_size = len(body) if isinstance(body, bytes) else len(str(body))
            self._log_debug(f"   Body found: {body_size} bytes")
            
            # Convert to string
            if isinstance(body, bytes):
                try:
                    body_str = body.decode('utf-8')
                    self._log_debug(f"   Decoded as UTF-8: {len(body_str)} characters")
                except UnicodeDecodeError:
                    self._log_debug("   Response is not valid UTF-8")
                    return f"[BINARY RESPONSE: {len(body)} bytes]"
            else:
                body_str = str(body)
            
            # Check size limit
            max_size_bytes = max_size_kb * 1024
            if len(body_str) > max_size_bytes:
                self._log_debug(f"   Truncating response: {len(body_str)} > {max_size_bytes} bytes")
                truncated = body_str[:max_size_bytes]
                result = f"{truncated}... [TRUNCATED - Original: {len(body_str)} bytes]"
                return result
            
            # Try to parse JSON
            content_type = response.headers.get("content-type", "").lower()
            if "application/json" in content_type or body_str.strip().startswith(("{", "[")):
                try:
                    self._log_debug("   Attempting JSON parse...")
                    json_obj = json.loads(body_str)
                    self._log_debug("   JSON parsed successfully")
                    
                    result = json.dumps(json_obj, indent=2)
                    self._log_debug(f"   Final response: {len(result)} characters")
                    self._log_debug(f"   Preview: {result[:200]}...")
                    return result
                    
                except json.JSONDecodeError:
                    self._log_debug("   JSON parse failed, returning raw")
            
            self._log_debug(f"   Returning raw response: {len(body_str)} characters")
            return body_str
            
        except Exception as e:
            error_msg = f"[ERROR CAPTURING RESPONSE: {type(e).__name__}: {str(e)}]"
            self._log_debug(f"   EXCEPTION: {error_msg}")
            self._log_debug(f"   Traceback: {traceback.format_exc()}")
            return error_msg
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Main middleware dispatch method with comprehensive logging.
        """
        print(f"\n[MIDDLEWARE] Dispatch called for {request.method} {request.url.path}")
        
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Extract client info for request context
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        # Set request context (CRITICAL: This enables auth_event_decorator to work)
        from common.request_context import set_request_context
        set_request_context(
            request_id=request_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Log request start
        self._log_debug("\n" + "="*80)
        self._log_debug(f"INCOMING REQUEST: {request_id}")
        self._log_debug(f"   Method: {request.method}")
        self._log_debug(f"   Path: {request.url.path}")
        self._log_debug(f"   Query: {request.url.query}")
        self._log_debug("="*80)
        
        # Get configuration
        config = self._get_logging_config()
        
        # Check if endpoint is excluded
        is_excluded = self._is_endpoint_excluded(
            request.url.path, 
            config["excluded_endpoints"]
        )
        
        # Wrap request for body caching
        self._log_debug("Wrapping request with CachedBodyRequest...")
        cached_request = CachedBodyRequest(request)
        cached_request.scope["request_id"] = request_id  # Add to scope for access in endpoints
        
        # Initialize payload variables
        request_payload = None
        response_payload = None
        
        # Capture request payload BEFORE calling endpoint
        should_capture = config["capture_payloads"] and not is_excluded
        self._log_debug(f"Payload capture enabled: {should_capture}")
        self._log_debug(f"   capture_payloads: {config['capture_payloads']}")
        self._log_debug(f"   is_excluded: {is_excluded}")
        
        if should_capture:
            self._log_debug("ATTEMPTING REQUEST PAYLOAD CAPTURE")
            request_payload = await self._capture_request_payload(
                cached_request, 
                config["max_payload_size_kb"]
            )
            if request_payload:
                self._log_debug(f"Request payload captured: {len(request_payload)} chars")
            else:
                self._log_debug("Request payload is None")
        else:
            self._log_debug("Skipping payload capture (disabled or excluded)")
        
        # Process the request through the application
        self._log_debug("Calling next middleware/endpoint...")
        try:
            response = await call_next(cached_request)
            self._log_debug(f"Response received: Status {response.status_code}")
        except Exception as e:
            self._log_debug(f"Exception during request processing: {str(e)}")
            self._log_debug(f"   Traceback: {traceback.format_exc()}")
            raise
        
        # Calculate duration
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Capture response payload
        if should_capture:
            self._log_debug("ATTEMPTING RESPONSE PAYLOAD CAPTURE")
            response_payload = await self._capture_response_payload(
                response, 
                config["max_payload_size_kb"]
            )
            if response_payload:
                self._log_debug(f"Response payload captured: {len(response_payload)} chars")
            else:
                self._log_debug("Response payload is None")
        
        # Prepare headers (sanitized)
        headers_dict = dict(request.headers)
        if "authorization" in headers_dict:
            headers_dict["authorization"] = "***REDACTED***"
        if "cookie" in headers_dict:
            headers_dict["cookie"] = "***REDACTED***"
        headers_json = json.dumps(headers_dict, indent=2)
        
        # Prepare log data
        log_data = {
            "request_id": request_id,
            "method": request.method,
            "path": str(request.url.path),
            "query_params": str(request.url.query) if request.url.query else None,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "ip_address": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
            "request_payload": request_payload,
            "response_payload": response_payload,
            "headers": headers_json,
        }
        
        # Log summary
        self._log_debug("─" * 60)
        self._log_debug("REQUEST SUMMARY")
        self._log_debug(f"   RequestID: {request_id}")
        self._log_debug(f"   Duration: {duration_ms}ms")
        self._log_debug(f"   Status: {response.status_code}")
        self._log_debug(f"   Request Payload: {'Captured' if request_payload else 'None'}")
        self._log_debug(f"   Response Payload: {'Captured' if response_payload else 'None'}")
        self._log_debug("="*80 + "\n")
        
        # Schedule database logging as background task
        self._log_debug("Scheduling database write...")
        background_task = BackgroundTask(self._log_to_database, log_data)
        response.background = background_task
        
        return response
    
    def _log_to_database(self, log_data: Dict[str, Any]):
        """
        Log request data to database with error handling.
        This runs as a background task after the response is sent.
        """
        try:
            self._log_debug("\n" + "="*80)
            self._log_debug(f"WRITING TO DATABASE: {log_data['request_id']}")
            self._log_debug(f"   Request Payload Length: {len(log_data['request_payload']) if log_data['request_payload'] else 0}")
            self._log_debug(f"   Response Payload Length: {len(log_data['response_payload']) if log_data['response_payload'] else 0}")
            
            from common.database import SessionLocal
            from models.log.api_request import ApiRequest
            from datetime import datetime
            
            db = SessionLocal()
            try:
                api_request = ApiRequest(
                    RequestID=log_data["request_id"],
                    Method=log_data["method"],
                    Path=log_data["path"],
                    QueryParams=log_data.get("query_params"),
                    StatusCode=log_data["status_code"],
                    DurationMs=log_data["duration_ms"],
                    IPAddress=log_data.get("ip_address"),
                    UserAgent=log_data.get("user_agent"),
                    RequestPayload=log_data.get("request_payload"),
                    ResponsePayload=log_data.get("response_payload"),
                    Headers=log_data.get("headers"),
                    CreatedDate=datetime.utcnow(),
                )
                
                db.add(api_request)
                db.commit()
                
                self._log_debug("Database write successful!")
                self._log_debug(f"   Record ID: {api_request.ApiRequestID}")
                self._log_debug("="*80 + "\n")
                
            finally:
                db.close()
                
        except Exception as e:
            self._log_debug(f"DATABASE ERROR: {type(e).__name__}: {str(e)}")
            self._log_debug(f"   Traceback: {traceback.format_exc()}")
            self._log_debug("="*80 + "\n")
            # Don't raise - background task failures shouldn't affect response