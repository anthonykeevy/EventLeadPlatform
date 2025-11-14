"""
Fixed Bulletproof Request Logging Middleware with Payload Capture
Comprehensive debugging and error handling included.
"""

import json
import time
import uuid
import traceback
from typing import Callable, Optional, Dict, Any, List
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.background import BackgroundTask
from starlette.datastructures import Headers
from starlette.responses import Response as StarletteResponse
from io import BytesIO

class CachedBodyRequest(Request):
    """
    Request subclass that caches the body for reuse.
    Critical: This prevents stream consumption issues.
    
    FastAPI needs to read the body for Pydantic validation, so we cache it
    after the first read and restore it for subsequent reads.
    """
    def __init__(self, request: Request, cached_body: Optional[bytes] = None):
        # If we have a cached body, create a receive function that returns it
        if cached_body is not None:
            body_consumed = False
            
            async def cached_receive():
                nonlocal body_consumed
                if not body_consumed:
                    body_consumed = True
                    return {
                        "type": "http.request",
                        "body": cached_body,
                        "more_body": False
                    }
                else:
                    # Stream exhausted
                    return {"type": "http.request", "body": b"", "more_body": False}
            
            # Use the cached receive function
            super().__init__(request.scope, cached_receive)
            self._cached_body: Optional[bytes] = cached_body
        else:
            # No cached body yet, use original receive
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
    
    def __init__(self, app, debug: bool = False):
        super().__init__(app)
        self._debug = debug
        self._sensitive_fields = {
            "password", "token", "secret", "api_key", 
            "apikey", "authorization", "auth", "credential",
            "passwd", "pwd", "private_key", "access_token",
            "refresh_token", "session_id", "sessionid"
        }
        
        # Initialization complete - detailed logs go to database, not console
    
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
        
        try:
            from common.config_service import ConfigurationService
            from common.database import SessionLocal
            
            # Create a database session for config service
            db = SessionLocal()
            config_service = ConfigurationService(db)
            
            # Get settings
            capture_payloads = config_service.get_logging_capture_payloads()
            max_size = config_service.get_logging_max_payload_size_kb()
            excluded = config_service.get_logging_excluded_endpoints()
            
            config = {
                "capture_payloads": capture_payloads,
                "max_payload_size_kb": max_size,
                "excluded_endpoints": excluded,
            }
            
            db.close()
            return config
            
        except Exception as e:
            # FALLBACK: Always enable for debugging
            fallback_config = {
                "capture_payloads": True,
                "max_payload_size_kb": 10,
                "excluded_endpoints": ["/api/health", "/api/test-database"],
            }
            return fallback_config
    
    def _is_endpoint_excluded(self, path: str, excluded_endpoints: List[str]) -> bool:
        """Check if endpoint should be excluded from logging"""
        is_excluded = any(path.startswith(ep) for ep in excluded_endpoints)
        if self._debug and is_excluded:
            self._log_debug(f"Endpoint excluded from payload capture: {path}")
        return is_excluded
    
    def _process_payload(self, body_bytes: bytes, max_size_kb: int) -> Optional[str]:
        """
        Process request body bytes into sanitized payload string.
        
        Args:
            body_bytes: Raw request body bytes
            max_size_kb: Maximum payload size in KB
            
        Returns:
            Sanitized payload string or None if processing fails
        """
        try:
            if not body_bytes:
                return None
            
            # Decode body
            try:
                body_str = body_bytes.decode('utf-8')
            except UnicodeDecodeError:
                import base64
                return f"[BINARY DATA: {len(body_bytes)} bytes, base64: {base64.b64encode(body_bytes[:100]).decode()}...]"
            
            # Check size limit
            max_size_bytes = max_size_kb * 1024
            if len(body_str) > max_size_bytes:
                truncated = body_str[:max_size_bytes]
                return f"{truncated}... [TRUNCATED - Original: {len(body_str)} bytes]"
            
            # Try to parse and sanitize JSON
            if body_str.strip().startswith(("{", "[")):
                try:
                    json_obj = json.loads(body_str)
                    sanitized = self._sanitize_payload(json_obj)
                    return json.dumps(sanitized, indent=2)
                except json.JSONDecodeError:
                    # Not valid JSON, return raw (truncated if needed)
                    return body_str[:max_size_bytes] if len(body_str) > max_size_bytes else body_str
            
            # Return raw string (truncated if needed)
            return body_str[:max_size_bytes] if len(body_str) > max_size_bytes else body_str
            
        except Exception as e:
            self._log_debug(f"Error processing payload: {e}")
            return None
    
    def _process_response_body(self, body_bytes: bytes, response: StarletteResponse, max_size_kb: int) -> Optional[str]:
        """
        Process response body bytes into sanitized payload string.
        
        Args:
            body_bytes: Raw response body bytes
            response: Response object (for content-type checking)
            max_size_kb: Maximum payload size in KB
            
        Returns:
            Sanitized payload string or None if processing fails
        """
        try:
            if not body_bytes:
                return None
            
            # Decode body
            try:
                body_str = body_bytes.decode('utf-8')
            except UnicodeDecodeError:
                import base64
                return f"[BINARY DATA: {len(body_bytes)} bytes, base64: {base64.b64encode(body_bytes[:100]).decode()}...]"
            
            # Check size limit
            max_size_bytes = max_size_kb * 1024
            if len(body_str) > max_size_bytes:
                truncated = body_str[:max_size_bytes]
                return f"{truncated}... [TRUNCATED - Original: {len(body_str)} bytes]"
            
            # Check content type or try to parse JSON
            content_type = response.headers.get("content-type", "").lower()
            if "application/json" in content_type or body_str.strip().startswith(("{", "[")):
                try:
                    json_obj = json.loads(body_str)
                    # Don't sanitize response payloads (they're typically safe, unlike request passwords)
                    return json.dumps(json_obj, indent=2)
                except json.JSONDecodeError:
                    # Not valid JSON, return raw (truncated if needed)
                    return body_str[:max_size_bytes] if len(body_str) > max_size_bytes else body_str
            
            # Return raw string (truncated if needed)
            return body_str[:max_size_bytes] if len(body_str) > max_size_bytes else body_str
            
        except Exception as e:
            self._log_debug(f"Error processing response body: {e}")
            return None
    
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
        response: StarletteResponse, 
        max_size_kb: int
    ) -> Optional[str]:
        """
        Capture and process response payload with extensive debugging.
        
        Note: Starlette/FastAPI responses don't have a direct 'body' attribute.
        We need to read from the response stream using iterate() or render().
        """
        try:
            self._log_debug("─" * 60)
            self._log_debug("CAPTURING RESPONSE PAYLOAD")
            self._log_debug(f"   Status Code: {response.status_code}")
            self._log_debug(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            self._log_debug(f"   Response Type: {type(response).__name__}")
            
            # Try to get body from response - different methods for different response types
            body = None
            
            # Method 1: Direct body attribute (for Response objects that have it)
            if hasattr(response, 'body') and response.body is not None:
                body = response.body
                self._log_debug("   Body found via response.body attribute")
            # Method 2: Try render() for JSONResponse and other simple responses
            elif hasattr(response, 'render'):
                try:
                    # render() returns the body bytes without consuming the stream
                    body = response.render()
                    if body:
                        self._log_debug("   Body found via response.render()")
                    else:
                        body = None
                except Exception as e:
                    self._log_debug(f"   response.render() failed: {e}")
                    body = None
            # Method 2b: For JSONResponse, try accessing body attribute after render
            elif isinstance(response, JSONResponse):
                try:
                    # JSONResponse may have body attribute accessible
                    if hasattr(response, 'body'):
                        body = response.body
                        self._log_debug("   Body found via JSONResponse.body")
                    else:
                        # Try rendering to get body
                        body = response.render()
                        self._log_debug("   Body found via JSONResponse.render()")
                except Exception as e:
                    self._log_debug(f"   JSONResponse body access failed: {e}")
                    body = None
            # Method 3: Try reading from iterator (for streaming responses like _StreamingResponse)
            elif hasattr(response, 'body_iterator'):
                try:
                    # Read all chunks from the iterator
                    chunks = []
                    async for chunk in response.body_iterator:
                        chunks.append(chunk)
                    if chunks:
                        body = b''.join(chunks)
                        self._log_debug(f"   Body found via body_iterator: {len(body)} bytes")
                    else:
                        body = None
                except Exception as e:
                    self._log_debug(f"   body_iterator failed: {e}")
                    body = None
            # Method 4: For _StreamingResponse, try to access the underlying response
            elif type(response).__name__ == '_StreamingResponse':
                try:
                    # _StreamingResponse wraps another response - try to access it
                    if hasattr(response, 'render'):
                        # render() for StreamingResponse might work without args
                        try:
                            body = response.render()  # This might work for some response types
                            if body:
                                self._log_debug("   Body found via _StreamingResponse.render()")
                            else:
                                body = None
                        except TypeError:
                            # render() needs content argument - try reading from iterator
                            self._log_debug("   _StreamingResponse.render() needs content, trying iterator")
                            if hasattr(response, 'body_iterator'):
                                chunks = []
                                async for chunk in response.body_iterator:
                                    chunks.append(chunk)
                                if chunks:
                                    body = b''.join(chunks)
                                    self._log_debug(f"   Body found via _StreamingResponse.body_iterator: {len(body)} bytes")
                                else:
                                    body = None
                            else:
                                body = None
                    else:
                        body = None
                except Exception as e:
                    self._log_debug(f"   _StreamingResponse access failed: {e}")
                    body = None
            
            if not body:
                self._log_debug("   Response body not accessible (may be streaming or already consumed)")
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
    
    async def dispatch(self, request: Request, call_next: Callable) -> StarletteResponse:
        """
        Main middleware dispatch method with comprehensive logging.
        Logs go to database via diagnostic tool, minimal console output.
        """
        
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
        
        # Get configuration
        config = self._get_logging_config()
        
        # Check if endpoint is excluded
        is_excluded = self._is_endpoint_excluded(
            request.url.path, 
            config["excluded_endpoints"]
        )
        
        # Determine if we should capture payloads
        should_capture = config["capture_payloads"] and not is_excluded
        
        # Initialize payload variables
        request_payload = None
        response_payload = None
        
        # Capture request body first (if needed) - BEFORE wrapping
        # This allows us to cache it for FastAPI's Pydantic validation
        request_body: Optional[bytes] = None
        if should_capture and request.method in ["POST", "PUT", "PATCH"]:
            try:
                request_body = await request.body()
                if request_body:
                    request_payload = self._process_payload(request_body, config["max_payload_size_kb"])
            except Exception as e:
                # Only log actual errors
                if self._debug:
                    self._log_debug(f"Error reading request body: {e}")
                request_body = None
        
        # Wrap request with cached body (so FastAPI can read it for validation)
        cached_request = CachedBodyRequest(request, cached_body=request_body)
        cached_request.scope["request_id"] = request_id  # Add to scope for access in endpoints
        
        # Process the request through the application
        try:
            response = await call_next(cached_request)
        except Exception as e:
            # Only log actual errors
            if self._debug:
                self._log_debug(f"Exception during request processing: {str(e)}")
            raise
        
        # Calculate duration
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Capture response payload BEFORE sending to client
        # This is critical: we must read the body iterator and create a new response
        response_payload = None
        if should_capture:
            try:
                # Read the response body iterator to capture it
                body_chunks = []
                async for chunk in response.body_iterator:
                    body_chunks.append(chunk)
                
                # Join all chunks into a single body
                response_body = b''.join(body_chunks) if body_chunks else b''
                
                if response_body:
                    response_payload = self._process_response_body(response_body, response, config["max_payload_size_kb"])
                
                # Create a new response with the captured body (so client still receives it)
                response = StarletteResponse(
                    content=response_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type
                )
            except Exception as e:
                # Only log actual errors
                if self._debug:
                    self._log_debug(f"Error capturing response payload: {e}")
                # If capture fails, continue with original response
        
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
        
        # Schedule database logging as background task (silent - details in database)
        background_task = BackgroundTask(self._log_to_database, log_data)
        response.background = background_task
        
        return response
    
    def _log_to_database(self, log_data: Dict[str, Any]):
        """
        Log request data to database with error handling.
        This runs as a background task after the response is sent.
        Silent operation - use diagnostic tool to view logs.
        """
        try:
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
                
            finally:
                db.close()
                
        except Exception as e:
            # Only log errors if debug enabled - failures shouldn't affect response
            if self._debug:
                self._log_debug(f"DATABASE ERROR: {type(e).__name__}: {str(e)}")
            # Don't raise - background task failures shouldn't affect response