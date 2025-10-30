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
    
    def get_recent_application_errors(self) -> List[Dict]:
        """Get recent application errors with stack traces"""
        with self.engine.connect() as conn:
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
                ORDER BY CreatedDate DESC
            """)
            return [dict(row._mapping) for row in conn.execute(query).fetchall()]
    
    def get_recent_api_requests(self) -> List[Dict]:
        """Get recent API requests with enhanced payload logging"""
        with self.engine.connect() as conn:
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
                correlation_query = text("""
                    SELECT 
                        ae.RequestID,
                        ae.EventType,
                        ae.Reason,
                        ae.CreatedDate,
                        ape.ErrorType,
                        ape.ErrorMessage,
                        ape.StackTrace,
                        api.StatusCode,
                        api.DurationMs,
                        api.RequestPayload,
                        api.ResponsePayload,
                        ed.Status as EmailStatus,
                        ed.ErrorMessage as EmailError
                    FROM log.AuthEvent ae
                    LEFT JOIN log.ApplicationError ape ON ae.RequestID = ape.RequestID
                    LEFT JOIN log.ApiRequest api ON ae.RequestID = api.RequestID
                    LEFT JOIN log.EmailDelivery ed ON ae.UserID = ed.UserID
                    WHERE ae.RequestID = :request_id
                """)
                result = conn.execute(correlation_query, {"request_id": request_id}).fetchone()
            else:
                # Get most recent failed request
                correlation_query = text("""
                    SELECT TOP 1
                        ae.RequestID,
                        ae.EventType,
                        ae.Reason,
                        ae.CreatedDate,
                        ape.ErrorType,
                        ape.ErrorMessage,
                        ape.StackTrace,
                        api.StatusCode,
                        api.DurationMs,
                        api.RequestPayload,
                        api.ResponsePayload,
                        ed.Status as EmailStatus,
                        ed.ErrorMessage as EmailError
                    FROM log.AuthEvent ae
                    LEFT JOIN log.ApplicationError ape ON ae.RequestID = ape.RequestID
                    LEFT JOIN log.ApiRequest api ON ae.RequestID = api.RequestID
                    LEFT JOIN log.EmailDelivery ed ON ae.UserID = ed.UserID
                    WHERE ae.EventType LIKE '%FAILED%' OR ape.ErrorType IS NOT NULL
                    ORDER BY ae.CreatedDate DESC
                """)
                result = conn.execute(correlation_query).fetchone()
            
            return dict(result._mapping) if result else {}
    
    def get_performance_metrics(self, hours: int = 24) -> Dict:
        """Get performance metrics for the last N hours"""
        with self.engine.connect() as conn:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            
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
    
    def print_api_requests(self, requests: List[Dict]):
        """Print formatted API requests with payloads"""
        print("\n" + "=" * 100)
        print(f"RECENT API REQUESTS (Last {len(requests)})")
        print("=" * 100)
        
        if not requests:
            print("No API requests found.")
            return
        
        for req in requests:
            print(f"\n[{req['CreatedDate']}] {req['Method']} {req['Path']}")
            print(f"  Status: {req['StatusCode']} | Duration: {req['DurationMs']}ms")
            print(f"  UserID: {req['UserID'] or 'NULL'} | RequestID: {req['RequestID']}")
            
            if req.get('RequestPayload'):
                print(f"  Request Payload: {self.format_json(req['RequestPayload'])}")
            
            if req.get('ResponsePayload'):
                print(f"  Response Payload: {self.format_json(req['ResponsePayload'])}")
            
            if req.get('Headers'):
                print(f"  Headers: {self.format_json(req['Headers'])}")
            
            if req.get('QueryParams'):
                print(f"  Query Params: {self.format_json(req['QueryParams'])}")
    
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
    
    def print_correlation_analysis(self, correlation: Dict):
        """Print correlated analysis for failed requests"""
        print("\n" + "=" * 100)
        print("CORRELATION ANALYSIS (Most Recent Failure)")
        print("=" * 100)
        
        if not correlation:
            print("No correlated failure found.")
            return
        
        print(f"\nRequestID: {correlation['RequestID']}")
        print(f"Timestamp: {correlation['CreatedDate']}")
        
        print(f"\nAuth Event:")
        print(f"  Type: {correlation['EventType']}")
        print(f"  Reason: {self.format_json(correlation['Reason'])}")
        
        if correlation.get('ErrorType'):
            print(f"\nApplication Error:")
            print(f"  Type: {correlation['ErrorType']}")
            print(f"  Message: {correlation['ErrorMessage']}")
            if correlation.get('StackTrace'):
                print(f"  Stack Trace: {correlation['StackTrace'][:300]}...")
        
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
    
    def run_full_diagnostic(self, request_id: str = None):
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
        self.print_email_deliveries(email_deliveries)
        self.print_audit_trail(audit_trail)
        self.print_correlation_analysis(correlation)
        self.print_performance_metrics(performance)
        
        print("\n" + "=" * 100)
        print("DIAGNOSTIC COMPLETE")
        print("=" * 100)

def main():
    """Main entry point for enhanced diagnostic logs"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Diagnostic Logs for EventLeadPlatform")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Number of entries per table (default: 5)")
    parser.add_argument("--request-id", "-r", type=str, help="Specific RequestID to analyze")
    parser.add_argument("--performance-hours", "-p", type=int, default=24, help="Hours for performance metrics (default: 24)")
    
    args = parser.parse_args()
    
    try:
        diagnostic = DiagnosticLogger(limit=args.limit)
        diagnostic.run_full_diagnostic(request_id=args.request_id)
    except Exception as e:
        print(f"Error running diagnostic: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
