"""
Enhanced Diagnostic Tool - Comprehensive Log Analysis
Used for troubleshooting authentication, application errors, and API requests
Supports Epic 2 enhanced logging with request/response payloads
"""
import os
import sys
from pathlib import Path
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
env_path = backend_dir / ".env"
load_dotenv(env_path)

class DiagnosticLogger:
    """Enhanced diagnostic logging with comprehensive analysis capabilities"""
    
    def __init__(self, limit: int = 5):
        self.limit = limit
        self.engine = None
        self._connect()
    
    def _connect(self):
        """Connect to database using existing Epic 1 connection"""
        try:
            from common.database import engine
            self.engine = engine
        except ImportError:
            # Fallback connection for standalone usage
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise Exception("DATABASE_URL not found in environment variables")
            self.engine = create_engine(database_url)
    
    def format_json(self, json_str: str) -> str:
        """Pretty print JSON strings with error handling"""
        try:
            if json_str and json_str != "NULL":
                obj = json.loads(json_str)
                return json.dumps(obj, indent=2)
            return "NULL"
        except (json.JSONDecodeError, TypeError):
            return str(json_str) if json_str else "NULL"
    
    def get_recent_auth_events(self) -> List[Dict]:
        """Get recent authentication events with enhanced details"""
        with self.engine.connect() as conn:
            query = text(f"""
                SELECT TOP {self.limit}
                    AuthEventID,
                    EventType,
                    UserID,
                    Email,
                    Reason,
                    IPAddress,
                    RequestID,
                    CreatedDate,
                    UserAgent,
                    SessionID
                FROM log.AuthEvent
                ORDER BY CreatedDate DESC
            """)
            return [dict(row._mapping) for row in conn.execute(query).fetchall()]
    
    def get_recent_application_errors(
        self, path_filter: Optional[str] = None, message_filter: Optional[str] = None
    ) -> List[Dict]:
        """Get recent application errors with stack traces.
        path_filter: Only errors where Path LIKE %path_filter%
        message_filter: Only errors where ErrorMessage LIKE message_filter (default: all if path_filter given)
        """
        with self.engine.connect() as conn:
            conditions = []
            params = {}
            if path_filter:
                conditions.append("Path LIKE :path_filter")
                params["path_filter"] = f"%{path_filter}%"
            if message_filter:
                conditions.append("ErrorMessage LIKE :msg_filter")
                params["msg_filter"] = message_filter
            where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""
            query = text(f"""
                SELECT TOP {self.limit}
                    ApplicationErrorID,
                    ErrorType,
                    ErrorMessage,
                    Severity,
                    Path,
                    Method,
                    RequestID,
                    UserID,
                    CreatedDate,
                    StackTrace,
                    ExceptionType
                FROM log.ApplicationError
                {where_clause}
                ORDER BY CreatedDate DESC
            """)
            return [dict(row._mapping) for row in conn.execute(query, params).fetchall()]
    
    def get_recent_api_requests(self, path_filter: Optional[str] = None) -> List[Dict]:
        """Get recent API requests with enhanced payload logging"""
        with self.engine.connect() as conn:
            where_clause = ""
            params = {}
            if path_filter:
                where_clause = "WHERE Path LIKE :path_filter"
                params = {"path_filter": f"%{path_filter}%"}
            
            query = text(f"""
                SELECT TOP {self.limit}
                    ApiRequestID,
                    Method,
                    Path,
                    StatusCode,
                    DurationMs,
                    RequestID,
                    UserID,
                    CreatedDate,
                    RequestPayload,
                    ResponsePayload,
                    Headers,
                    QueryParams
                FROM log.ApiRequest
                {where_clause}
                ORDER BY CreatedDate DESC
            """)
            return [dict(row._mapping) for row in conn.execute(query, params).fetchall()]

    def get_recent_frontend_events(
        self,
        event_filter: Optional[str] = None,
        component_id: Optional[str] = None,
        session_id: Optional[str] = None,
        level: Optional[str] = None,
    ) -> List[Dict]:
        """Get recent frontend events from log.FrontendEvent."""
        with self.engine.connect() as conn:
            conditions = []
            params = {}
            if event_filter:
                conditions.append("EventType LIKE :event_filter")
                params["event_filter"] = f"%{event_filter}%"
            if component_id:
                conditions.append("ComponentID = :component_id")
                params["component_id"] = component_id
            if session_id:
                conditions.append("SessionID = :session_id")
                params["session_id"] = session_id
            if level:
                conditions.append("Level = :level")
                params["level"] = level

            where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""
            query = text(f"""
                SELECT TOP {self.limit}
                    FrontendEventID,
                    EventType,
                    Level,
                    ComponentID,
                    ComponentType,
                    SessionID,
                    UserID,
                    RequestID,
                    PageURL,
                    ClientTimestamp,
                    CreatedDate,
                    Payload
                FROM log.FrontendEvent
                {where_clause}
                ORDER BY CreatedDate DESC
            """)
            return [dict(row._mapping) for row in conn.execute(query, params).fetchall()]
    
    def get_profile_enhancement_requests(self, limit: int = 10) -> List[Dict]:
        """Get recent profile enhancement requests (theme, layout, font size updates)"""
        with self.engine.connect() as conn:
            query = text(f"""
                SELECT TOP {limit}
                    ApiRequestID,
                    Method,
                    Path,
                    StatusCode,
                    DurationMs,
                    RequestID,
                    UserID,
                    CreatedDate,
                    RequestPayload,
                    ResponsePayload,
                    Headers,
                    QueryParams
                FROM log.ApiRequest
                WHERE Path LIKE '%/profile/enhancements%'
                   OR Path LIKE '%/reference/themes%'
                   OR Path LIKE '%/reference/layout-densities%'
                   OR Path LIKE '%/reference/font-sizes%'
                   OR Path LIKE '%/profile/enhanced%'
                ORDER BY CreatedDate DESC
            """)
            return [dict(row._mapping) for row in conn.execute(query).fetchall()]
    
    def get_recent_email_deliveries(self) -> List[Dict]:
        """Get recent email delivery events"""
        with self.engine.connect() as conn:
            query = text(f"""
                SELECT TOP {self.limit}
                    EmailDeliveryID,
                    EmailType,
                    RecipientEmail,
                    Status,
                    UserID,
                    CreatedDate,
                    ErrorMessage,
                    ProviderResponse,
                    RetryCount
                FROM log.EmailDelivery
                ORDER BY CreatedDate DESC
            """)
            return [dict(row._mapping) for row in conn.execute(query).fetchall()]
    
    def get_epic2_audit_trail(self) -> List[Dict]:
        """Get Epic 2 audit trail entries (if available)"""
        with self.engine.connect() as conn:
            try:
                query = text(f"""
                    SELECT TOP {self.limit}
                        ApprovalAuditTrailID,
                        EntityType,
                        EntityID,
                        Action,
                        UserID,
                        ExternalApproverEmail,
                        Comments,
                        CreatedDate
                    FROM audit.ApprovalAuditTrail
                    ORDER BY CreatedDate DESC
                """)
                return [dict(row._mapping) for row in conn.execute(query).fetchall()]
            except Exception:
                return []  # Table might not exist yet
    
    def get_correlation_analysis(self, request_id: str = None) -> Dict:
        """Get correlated analysis for a specific request or most recent failure"""
        with self.engine.connect() as conn:
            if request_id:
                # First try to find in ApplicationError as it's most likely source of truth for 500s
                correlation_query = text("""
                    SELECT 
                        ape.RequestID,
                        ape.ErrorType,
                        ape.ErrorMessage,
                        ape.StackTrace,
                        ape.CreatedDate,
                        api.StatusCode,
                        api.DurationMs,
                        api.RequestPayload,
                        api.ResponsePayload,
                        api.UserID,
                        ae.EventType as AuthEventType,
                        ae.Reason as AuthReason
                    FROM log.ApplicationError ape
                    LEFT JOIN log.ApiRequest api ON ape.RequestID = api.RequestID
                    LEFT JOIN log.AuthEvent ae ON ape.RequestID = ae.RequestID
                    WHERE ape.RequestID = :request_id
                """)
                result = conn.execute(correlation_query, {"request_id": request_id}).fetchone()
                
                if not result:
                    # Fallback to ApiRequest if no ApplicationError (e.g. 404s or handled errors)
                    correlation_query = text("""
                        SELECT 
                            api.RequestID,
                            NULL as ErrorType,
                            NULL as ErrorMessage,
                            NULL as StackTrace,
                            api.CreatedDate,
                            api.StatusCode,
                            api.DurationMs,
                            api.RequestPayload,
                            api.ResponsePayload,
                            api.UserID,
                            ae.EventType as AuthEventType,
                            ae.Reason as AuthReason
                        FROM log.ApiRequest api
                        LEFT JOIN log.AuthEvent ae ON api.RequestID = ae.RequestID
                        WHERE api.RequestID = :request_id
                    """)
                    result = conn.execute(correlation_query, {"request_id": request_id}).fetchone()
            else:
                # Get most recent Application Error
                correlation_query = text("""
                    SELECT TOP 1
                        ape.RequestID,
                        ape.ErrorType,
                        ape.ErrorMessage,
                        ape.StackTrace,
                        ape.CreatedDate,
                        api.StatusCode,
                        api.DurationMs,
                        api.RequestPayload,
                        api.ResponsePayload,
                        api.UserID,
                        ae.EventType as AuthEventType,
                        ae.Reason as AuthReason
                    FROM log.ApplicationError ape
                    LEFT JOIN log.ApiRequest api ON ape.RequestID = api.RequestID
                    LEFT JOIN log.AuthEvent ae ON ape.RequestID = ae.RequestID
                    ORDER BY ape.CreatedDate DESC
                """)
                result = conn.execute(correlation_query).fetchone()
            
            return dict(result._mapping) if result else {}

    def get_correlated_api_request_bundle(self, inbound_request_id: str) -> List[Dict]:
        """
        All log.ApiRequest rows tied to one inbound HTTP request.

        Inbound browser/API calls use RequestID = the correlation UUID.
        Outbound provider calls (e.g. OpenAI) log separate rows with
        RequestID = '{inbound_request_id}:outbound:{new_uuid}' — see
        middleware/outbound_request_logger.py.
        """
        pattern = f"{inbound_request_id}:outbound:%"
        with self.engine.connect() as conn:
            query = text(
                """
                SELECT
                    ApiRequestID,
                    Method,
                    Path,
                    StatusCode,
                    DurationMs,
                    RequestID,
                    UserID,
                    CreatedDate,
                    RequestPayload,
                    ResponsePayload,
                    Headers,
                    QueryParams
                FROM log.ApiRequest
                WHERE RequestID = :rid OR RequestID LIKE :out_pattern
                ORDER BY ApiRequestID ASC
                """
            )
            rows = conn.execute(
                query, {"rid": inbound_request_id, "out_pattern": pattern}
            ).fetchall()
            return [dict(row._mapping) for row in rows]

    def print_correlated_api_request_bundle(
        self, rows: List[Dict], inbound_request_id: str
    ) -> None:
        """Print inbound + synthetic outbound ApiRequest rows for one trace."""
        print("\n" + "=" * 100)
        print("CORRELATED log.ApiRequest CHAIN (inbound + outbound)")
        print("=" * 100)
        print(
            f"Inbound RequestID (pass this to --request-id): {inbound_request_id}\n"
            "Outbound rows use RequestID = '<inbound>:outbound:<uuid>' and Path "
            "like '/outbound/openai/v1/...'.\n"
            "Note: HTTP 200 on /api/form-ai/generate can still return JSON with "
            '"status": "failed" (e.g. retry-cap-exhausted). Check ResponsePayload '
            "on the generate row for trace.terminalReason and attempts[]."
        )
        if not rows:
            print("\nNo ApiRequest rows found for this RequestID (check exact GUID).")
            return

        print(f"\n--- Summary ({len(rows)} row(s)) ---")
        for req in rows:
            tail = req["RequestID"]
            if len(tail) > 72:
                tail = tail[:36] + "..." + tail[-30:]
            print(
                f"  ApiRequestID={req['ApiRequestID']} | {req['Method']} {req['Path']} | "
                f"{req['StatusCode']} | {req['DurationMs']}ms | {tail}"
            )

        outbound_preview_chars = 1200
        for req in rows:
            print("\n" + "-" * 100)
            print(
                f"[{req['CreatedDate']}] {req['Method']} {req['Path']} "
                f"| Status: {req['StatusCode']} | Duration: {req['DurationMs']}ms"
            )
            print(f"  ApiRequestID: {req['ApiRequestID']} | UserID: {req['UserID'] or 'NULL'}")
            print(f"  RequestID: {req['RequestID']}")

            is_outbound = str(req.get("Path") or "").startswith("/outbound/")
            if req.get("Headers"):
                try:
                    hdr = json.loads(req["Headers"]) if isinstance(req["Headers"], str) else req["Headers"]
                    if isinstance(hdr, dict) and hdr.get("direction") == "outbound":
                        print(f"  Outbound provider: {hdr.get('provider', '?')} | url: {hdr.get('url', '')[:120]}")
                except (json.JSONDecodeError, TypeError):
                    pass

            if req.get("RequestPayload"):
                p = self.format_json(req["RequestPayload"])
                if is_outbound and len(p) > outbound_preview_chars:
                    p = p[:outbound_preview_chars] + "\n    ... [TRUNCATED for outbound preview]"
                print(f"  Request Payload:\n    {p}")

            if req.get("ResponsePayload"):
                r = self.format_json(req["ResponsePayload"])
                max_len = outbound_preview_chars if is_outbound else 20000
                if len(r) > max_len:
                    r = r[:max_len] + "\n    ... [TRUNCATED]"
                print(f"  Response Payload:\n    {r}")
    
    def get_performance_metrics(self, hours: int = 24) -> Dict:
        """Get performance metrics for the last N hours"""
        with self.engine.connect() as conn:
            # Use timezone-aware datetime (Python 3.11+)
            try:
                cutoff_time = datetime.now(datetime.timezone.utc) - timedelta(hours=hours)
            except AttributeError:
                # Fallback for older Python versions
                from datetime import timezone
                cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
            
            # API Performance
            api_perf = conn.execute(text("""
                SELECT 
                    COUNT(*) as TotalRequests,
                    AVG(DurationMs) as AvgDuration,
                    MAX(DurationMs) as MaxDuration,
                    COUNT(CASE WHEN StatusCode >= 400 THEN 1 END) as ErrorCount
                FROM log.ApiRequest
                WHERE CreatedDate >= :cutoff_time
            """), {"cutoff_time": cutoff_time}).fetchone()
            
            # Error Rate
            error_rate = conn.execute(text("""
                SELECT 
                    COUNT(*) as TotalErrors,
                    COUNT(DISTINCT ErrorType) as UniqueErrorTypes
                FROM log.ApplicationError
                WHERE CreatedDate >= :cutoff_time
            """), {"cutoff_time": cutoff_time}).fetchone()
            
            return {
                "api_performance": dict(api_perf._mapping),
                "error_metrics": dict(error_rate._mapping),
                "time_period_hours": hours
            }
    
    def print_auth_events(self, events: List[Dict]):
        """Print formatted authentication events"""
        print("=" * 100)
        print(f"RECENT AUTH EVENTS (Last {len(events)})")
        print("=" * 100)
        
        if not events:
            print("No auth events found.")
            return
        
        for event in events:
            print(f"\n[{event['CreatedDate']}] {event['EventType']}")
            print(f"  UserID: {event['UserID'] or 'NULL'}")
            print(f"  Email: {event['Email'] or 'NULL'}")
            print(f"  Reason: {self.format_json(event['Reason'])}")
            print(f"  IP: {event['IPAddress']} | RequestID: {event['RequestID']}")
            if event.get('UserAgent'):
                print(f"  UserAgent: {event['UserAgent'][:100]}...")
            if event.get('SessionID'):
                print(f"  SessionID: {event['SessionID']}")
    
    def print_application_errors(self, errors: List[Dict]):
        """Print formatted application errors"""
        print("\n" + "=" * 100)
        print(f"RECENT APPLICATION ERRORS (Last {len(errors)})")
        print("=" * 100)
        
        if not errors:
            print("No application errors found.")
            return
        
        for error in errors:
            print(f"\n[{error['CreatedDate']}] {error['ErrorType']} - {error['Severity']}")
            print(f"  Path: {error['Method']} {error['Path']}")
            print(f"  Message: {error['ErrorMessage']}")
            print(f"  UserID: {error['UserID'] or 'NULL'} | RequestID: {error['RequestID']}")
            if error.get('ExceptionType'):
                print(f"  Exception: {error['ExceptionType']}")
            if error.get('StackTrace'):
                print(f"  Stack Trace: {error['StackTrace'][:200]}...")
    
    def print_api_requests(self, requests: List[Dict], title: str = "RECENT API REQUESTS"):
        """Print formatted API requests with payloads"""
        print("\n" + "=" * 100)
        print(f"{title} (Last {len(requests)})")
        print("=" * 100)
        
        if not requests:
            print("No API requests found.")
            return
        
        for req in requests:
            print(f"\n[{req['CreatedDate']}] {req['Method']} {req['Path']}")
            print(f"  Status: {req['StatusCode']} | Duration: {req['DurationMs']}ms")
            print(f"  UserID: {req['UserID'] or 'NULL'} | RequestID: {req['RequestID']}")
            
            # Highlight errors
            if req.get('StatusCode') and req['StatusCode'] >= 400:
                # Avoid unicode symbols (Windows console encoding issues)
                print(f"  ERROR: Status {req['StatusCode']}")
            
            if req.get('RequestPayload'):
                payload = self.format_json(req['RequestPayload'])
                print(f"  Request Payload:")
                print(f"    {payload}")
            
            if req.get('ResponsePayload'):
                response = self.format_json(req['ResponsePayload'])
                print(f"  Response Payload:")
                print(f"    {response}")
            
            # Only show headers if they contain interesting info (not all headers for brevity)
            if req.get('Headers'):
                headers = json.loads(req['Headers']) if isinstance(req.get('Headers'), str) else req.get('Headers')
                if isinstance(headers, dict):
                    # Show only auth header status (for security) and content-type
                    auth_status = "Present" if headers.get('authorization') else "Missing"
                    print(f"  Authorization Header: {auth_status}")
                    if headers.get('content-type'):
                        print(f"  Content-Type: {headers.get('content-type')}")
            
            if req.get('QueryParams'):
                params = self.format_json(req['QueryParams'])
                if params and params != "NULL":
                    print(f"  Query Params: {params}")

    def print_frontend_events(self, events: List[Dict], title: str = "RECENT FRONTEND EVENTS"):
        """Print formatted frontend events from log.FrontendEvent."""
        print("\n" + "=" * 100)
        print(f"{title} (Last {len(events)})")
        print("=" * 100)

        if not events:
            print("No frontend events found.")
            return

        for evt in events:
            print(f"\n[{evt['CreatedDate']}] {evt['EventType']} ({evt['Level']})")
            print(
                f"  FrontendEventID: {evt['FrontendEventID']} | ComponentID: {evt.get('ComponentID') or 'NULL'} "
                f"| ComponentType: {evt.get('ComponentType') or 'NULL'}"
            )
            print(
                f"  SessionID: {evt.get('SessionID') or 'NULL'} | UserID: {evt.get('UserID') or 'NULL'} "
                f"| RequestID: {evt.get('RequestID') or 'NULL'}"
            )
            if evt.get("PageURL"):
                print(f"  PageURL: {evt['PageURL']}")
            if evt.get("ClientTimestamp"):
                print(f"  ClientTimestamp: {evt['ClientTimestamp']}")
            if evt.get("Payload"):
                payload = self.format_json(evt["Payload"])
                if len(payload) > 1000:
                    payload = payload[:1000] + "... [TRUNCATED]"
                print("  Payload:")
                print(f"    {payload}")
    
    def print_email_deliveries(self, deliveries: List[Dict]):
        """Print formatted email delivery events"""
        print("\n" + "=" * 100)
        print(f"RECENT EMAIL DELIVERIES (Last {len(deliveries)})")
        print("=" * 100)
        
        if not deliveries:
            print("No email deliveries found.")
            return
        
        for delivery in deliveries:
            print(f"\n[{delivery['CreatedDate']}] {delivery['EmailType']} -> {delivery['RecipientEmail']}")
            print(f"  Status: {delivery['Status']}")
            print(f"  UserID: {delivery['UserID'] or 'NULL'}")
            if delivery.get('ErrorMessage'):
                print(f"  Error: {delivery['ErrorMessage']}")
            if delivery.get('ProviderResponse'):
                print(f"  Provider Response: {delivery['ProviderResponse']}")
    
    def print_audit_trail(self, audit_entries: List[Dict]):
        """Print Epic 2 audit trail entries"""
        if not audit_entries:
            return
            
        print("\n" + "=" * 100)
        print(f"EPIC 2 AUDIT TRAIL (Last {len(audit_entries)})")
        print("=" * 100)
        
        for entry in audit_entries:
            print(f"\n[{entry['CreatedDate']}] {entry['Action']} on {entry['EntityType']} {entry['EntityID']}")
            print(f"  User: {entry['UserID'] or entry['ExternalApproverEmail'] or 'System'}")
            if entry.get('Comments'):
                print(f"  Comments: {entry['Comments']}")
    
    def print_correlation_analysis(self, correlation: Dict, request_id: Optional[str] = None):
        """Print correlated analysis for failed requests or a specific RequestID."""
        print("\n" + "=" * 100)
        if request_id:
            print(f"CORRELATION ANALYSIS (RequestID: {request_id})")
        else:
            print("CORRELATION ANALYSIS (Most Recent Failure)")
        print("=" * 100)
        
        if not correlation:
            print("No correlated failure found.")
            return
        
        print(f"\nRequestID: {correlation['RequestID']}")
        print(f"Timestamp: {correlation['CreatedDate']}")
        
        if correlation.get('AuthEventType'):
            print(f"\nAuth Event:")
            print(f"  Type: {correlation['AuthEventType']}")
            print(f"  Reason: {self.format_json(correlation['AuthReason'])}")
        
        if correlation.get('ErrorType'):
            print(f"\nApplication Error:")
            print(f"  Type: {correlation['ErrorType']}")
            print(f"  Message: {correlation['ErrorMessage']}")
            if correlation.get('StackTrace'):
                print(f"  Stack Trace: {correlation['StackTrace'][:500]}...")
        
        if correlation.get('StatusCode'):
            print(f"\nAPI Request:")
            print(f"  Status Code: {correlation['StatusCode']}")
            print(f"  Duration: {correlation['DurationMs']}ms")
            if correlation.get('RequestPayload'):
                print(f"  Request: {self.format_json(correlation['RequestPayload'])}")
            if correlation.get('ResponsePayload'):
                print(f"  Response: {self.format_json(correlation['ResponsePayload'])}")
        
        if correlation.get('EmailStatus'):
            print(f"\nEmail Delivery:")
            print(f"  Status: {correlation['EmailStatus']}")
            if correlation.get('EmailError'):
                print(f"  Error: {correlation['EmailError']}")
    
    def print_performance_metrics(self, metrics: Dict):
        """Print performance metrics"""
        print("\n" + "=" * 100)
        print(f"PERFORMANCE METRICS (Last {metrics['time_period_hours']} hours)")
        print("=" * 100)
        
        api_perf = metrics['api_performance']
        error_metrics = metrics['error_metrics']
        
        print(f"\nAPI Performance:")
        print(f"  Total Requests: {api_perf['TotalRequests']}")
        print(f"  Average Duration: {api_perf['AvgDuration']:.2f}ms" if api_perf['AvgDuration'] is not None else "  Average Duration: N/A")
        print(f"  Max Duration: {api_perf['MaxDuration']}ms" if api_perf['MaxDuration'] is not None else "  Max Duration: N/A")
        print(f"  Error Count: {api_perf['ErrorCount']}")
        
        print(f"\nError Metrics:")
        print(f"  Total Errors: {error_metrics['TotalErrors']}")
        print(f"  Unique Error Types: {error_metrics['UniqueErrorTypes']}")
    
    def run_full_diagnostic(self, request_id: str = None, show_theme_requests: bool = True):
        """Run complete diagnostic analysis"""
        print("ENHANCED DIAGNOSTIC LOGS - EventLeadPlatform")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Limit: {self.limit} entries per table")
        
        # Get all log data
        auth_events = self.get_recent_auth_events()
        app_errors = self.get_recent_application_errors()
        api_requests = self.get_recent_api_requests()
        email_deliveries = self.get_recent_email_deliveries()
        audit_trail = self.get_epic2_audit_trail()
        correlation = self.get_correlation_analysis(request_id)
        performance = self.get_performance_metrics()
        
        # Print all sections
        self.print_auth_events(auth_events)
        self.print_application_errors(app_errors)
        self.print_api_requests(api_requests)
        
        # Show theme/profile enhancement requests if requested
        if show_theme_requests:
            profile_enhancements = self.get_profile_enhancement_requests(limit=10)
            if profile_enhancements:
                self.print_api_requests(profile_enhancements, "PROFILE ENHANCEMENT REQUESTS (Theme/Layout/Font)")
        
        self.print_email_deliveries(email_deliveries)
        self.print_audit_trail(audit_trail)
        self.print_correlation_analysis(correlation, request_id=request_id)
        if request_id:
            chain = self.get_correlated_api_request_bundle(request_id)
            self.print_correlated_api_request_bundle(chain, request_id)
        self.print_performance_metrics(performance)
        
        print("\n" + "=" * 100)
        print("DIAGNOSTIC COMPLETE")
        print("=" * 100)

def main():
    """Main entry point for enhanced diagnostic logs"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Diagnostic Logs for EventLeadPlatform")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Number of entries per table (default: 5)")
    parser.add_argument("--request-id", "-r", type=str, help="Specific inbound RequestID (correlation UUID) to analyze")
    parser.add_argument(
        "--correlation-only",
        action="store_true",
        help="With --request-id: print only correlation summary + full ApiRequest chain (inbound + outbound); skip other tables",
    )
    parser.add_argument("--performance-hours", "-p", type=int, default=24, help="Hours for performance metrics (default: 24)")
    parser.add_argument("--theme-requests", "-t", action="store_true", default=True, help="Show theme/profile enhancement requests (default: True)")
    parser.add_argument("--no-theme-requests", action="store_false", dest="theme_requests", help="Hide theme/profile enhancement requests")
    parser.add_argument("--path-filter", type=str, help="Filter API requests by path pattern (e.g., 'smart-search')")
    parser.add_argument("--show-errors", action="store_true", help="Also show ApplicationErrors (optionally filtered by --path-filter)")
    parser.add_argument("--frontend-only", action="store_true", help="Show only FrontendEvent logs")
    parser.add_argument("--frontend-filter", type=str, help="Filter FrontendEvent.EventType by partial match")
    parser.add_argument("--frontend-component-id", type=str, help="Filter FrontendEvent by ComponentID")
    parser.add_argument("--frontend-session-id", type=str, help="Filter FrontendEvent by SessionID")
    parser.add_argument("--frontend-level", type=str, help="Filter FrontendEvent by log level (debug/info/warn/error)")
    parser.add_argument("--show-frontend", action="store_true", help="Also show FrontendEvent logs in full diagnostic mode")
    
    args = parser.parse_args()
    
    try:
        diagnostic = DiagnosticLogger(limit=args.limit)

        if args.correlation_only:
            if not args.request_id:
                parser.error("--correlation-only requires --request-id (-r)")
            diagnostic = DiagnosticLogger(limit=args.limit)
            correlation = diagnostic.get_correlation_analysis(args.request_id)
            diagnostic.print_correlation_analysis(correlation, request_id=args.request_id)
            chain = diagnostic.get_correlated_api_request_bundle(args.request_id)
            diagnostic.print_correlated_api_request_bundle(chain, args.request_id)
            print("\n" + "=" * 100)
            print("CORRELATION TRACE COMPLETE")
            print("=" * 100)
        elif args.frontend_only:
            frontend_events = diagnostic.get_recent_frontend_events(
                event_filter=args.frontend_filter,
                component_id=args.frontend_component_id,
                session_id=args.frontend_session_id,
                level=args.frontend_level,
            )
            title = "FRONTEND EVENTS"
            if args.frontend_filter:
                title += f" FILTERED BY EVENT: '{args.frontend_filter}'"
            if args.frontend_component_id:
                title += f" COMPONENT: '{args.frontend_component_id}'"
            if args.frontend_session_id:
                title += f" SESSION: '{args.frontend_session_id}'"
            if args.frontend_level:
                title += f" LEVEL: '{args.frontend_level}'"
            diagnostic.print_frontend_events(frontend_events, f"{title} (Last {args.limit})")
        # If path filter specified, show filtered requests
        elif args.path_filter:
            filtered_requests = diagnostic.get_recent_api_requests(path_filter=args.path_filter)
            diagnostic.print_api_requests(filtered_requests, f"API REQUESTS FILTERED BY: '{args.path_filter}' (Last {args.limit})")
            if args.show_errors:
                app_errors = diagnostic.get_recent_application_errors(path_filter=args.path_filter)
                diagnostic.print_application_errors(app_errors)
        else:
            diagnostic.run_full_diagnostic(request_id=args.request_id, show_theme_requests=args.theme_requests)
            if args.show_frontend:
                frontend_events = diagnostic.get_recent_frontend_events(
                    event_filter=args.frontend_filter,
                    component_id=args.frontend_component_id,
                    session_id=args.frontend_session_id,
                    level=args.frontend_level,
                )
                diagnostic.print_frontend_events(frontend_events)
    except Exception as e:
        print(f"Error running diagnostic: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
