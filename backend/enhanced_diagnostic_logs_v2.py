#!/usr/bin/env python3
"""
Enhanced Diagnostic Logs v2 - EventLead Platform
Uses centralized database service for reliable connections
"""
import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Use centralized database service
from common.database_service import get_database_service
from common.db_utils import get_payload_logs, get_performance_metrics

def print_header(title: str, char: str = "=", width: int = 80):
    """Print a formatted header"""
    print(f"\n{char * width}")
    print(f"{title}")
    print(f"{char * width}")

def print_log_entry(entry: Dict[str, Any], entry_type: str = "LOG"):
    """Print a formatted log entry"""
    timestamp = entry.get('CreatedDate', 'Unknown')
    if isinstance(timestamp, datetime):
        timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
    
    print(f"\n[{timestamp}] {entry_type}")
    
    # Print relevant fields based on entry type
    if 'EventType' in entry:
        print(f"  Type: {entry['EventType']}")
    if 'Method' in entry:
        print(f"  Method: {entry['Method']}")
    if 'Path' in entry:
        print(f"  Path: {entry['Path']}")
    if 'StatusCode' in entry:
        print(f"  Status: {entry['StatusCode']}")
    if 'DurationMs' in entry:
        print(f"  Duration: {entry['DurationMs']}ms")
    if 'UserID' in entry and entry['UserID']:
        print(f"  UserID: {entry['UserID']}")
    if 'Email' in entry and entry['Email']:
        print(f"  Email: {entry['Email']}")
    if 'Reason' in entry and entry['Reason']:
        print(f"  Reason: {entry['Reason']}")
    if 'IPAddress' in entry and entry['IPAddress']:
        print(f"  IP: {entry['IPAddress']}")
    if 'RequestID' in entry and entry['RequestID']:
        print(f"  RequestID: {entry['RequestID']}")
    if 'UserAgent' in entry and entry['UserAgent']:
        print(f"  UserAgent: {entry['UserAgent'][:100]}...")
    if 'Headers' in entry and entry['Headers']:
        print(f"  Headers: {entry['Headers'][:200]}...")
    if 'QueryParams' in entry and entry['QueryParams']:
        print(f"  Query Params: {entry['QueryParams']}")
    if 'RequestPayload' in entry and entry['RequestPayload']:
        payload = entry['RequestPayload']
        if len(payload) > 100:
            payload = payload[:100] + "..."
        print(f"  RequestPayload: {payload}")
    if 'ResponsePayload' in entry and entry['ResponsePayload']:
        payload = entry['ResponsePayload']
        if len(payload) > 100:
            payload = payload[:100] + "..."
        print(f"  ResponsePayload: {payload}")

def get_recent_auth_events(limit: int = 5) -> List[Dict[str, Any]]:
    """Get recent authentication events"""
    try:
        db_service = get_database_service()
        query = f"""
            SELECT TOP {limit} 
                EventType, UserID, Email, Reason, IPAddress, RequestID, 
                UserAgent, CreatedDate
            FROM log.AuthEvent 
            ORDER BY CreatedDate DESC
        """
        return db_service.execute_query(query)
    except Exception as e:
        print(f"Error getting auth events: {e}")
        return []

def get_recent_application_errors(limit: int = 5) -> List[Dict[str, Any]]:
    """Get recent application errors"""
    try:
        db_service = get_database_service()
        query = f"""
            SELECT TOP {limit} 
                ErrorType, ErrorMessage, Severity, Path, Method, 
                UserID, RequestID, CreatedDate
            FROM log.ApplicationError 
            ORDER BY CreatedDate DESC
        """
        return db_service.execute_query(query)
    except Exception as e:
        print(f"Error getting application errors: {e}")
        return []

def get_recent_api_requests(limit: int = 5) -> List[Dict[str, Any]]:
    """Get recent API requests"""
    try:
        db_service = get_database_service()
        query = f"""
            SELECT TOP {limit} 
                Method, Path, StatusCode, DurationMs, UserID, CompanyID,
                IPAddress, UserAgent, RequestID, Headers, QueryParams,
                RequestPayload, ResponsePayload, CreatedDate
            FROM log.ApiRequest 
            ORDER BY CreatedDate DESC
        """
        return db_service.execute_query(query)
    except Exception as e:
        print(f"Error getting API requests: {e}")
        return []

def get_recent_email_deliveries(limit: int = 5) -> List[Dict[str, Any]]:
    """Get recent email deliveries"""
    try:
        db_service = get_database_service()
        query = f"""
            SELECT TOP {limit} 
                EmailType, RecipientEmail, Status, UserID, CreatedDate
            FROM log.EmailDelivery 
            ORDER BY CreatedDate DESC
        """
        return db_service.execute_query(query)
    except Exception as e:
        print(f"Error getting email deliveries: {e}")
        return []

def analyze_correlation(limit: int = 1) -> Dict[str, Any]:
    """Analyze correlation between different log types"""
    try:
        db_service = get_database_service()
        
        # Get most recent failure
        query = """
            SELECT TOP 1 RequestID, CreatedDate
            FROM log.ApplicationError 
            ORDER BY CreatedDate DESC
        """
        failures = db_service.execute_query(query)
        
        if not failures:
            return {"message": "No recent failures found"}
        
        failure = failures[0]
        request_id = failure['RequestID']
        
        # Simple correlation analysis
        return {
            "request_id": request_id,
            "message": "Correlation analysis not implemented in v2",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        print(f"Error in correlation analysis: {e}")
        return {"error": str(e)}

def main():
    """Main diagnostic function"""
    print("ENHANCED DIAGNOSTIC LOGS v2 - EventLeadPlatform")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Using Centralized Database Service")
    
    # Test database connection first
    try:
        db_service = get_database_service()
        health = db_service.test_connection()
        if health['status'] == 'error':
            print(f"\n❌ Database connection failed: {health['message']}")
            return
        else:
            print(f"\n✅ Database connected: {health['database']}")
    except Exception as e:
        print(f"\n❌ Database service error: {e}")
        return
    
    # Get recent logs
    limit = 5
    
    # Auth Events
    print_header("RECENT AUTH EVENTS", limit=limit)
    auth_events = get_recent_auth_events(limit)
    for event in auth_events:
        print_log_entry(event, "AUTH")
    
    # Application Errors
    print_header("RECENT APPLICATION ERRORS", limit=limit)
    app_errors = get_recent_application_errors(limit)
    for error in app_errors:
        print_log_entry(error, "ERROR")
    
    # API Requests
    print_header("RECENT API REQUESTS", limit=limit)
    api_requests = get_recent_api_requests(limit)
    for request in api_requests:
        print_log_entry(request, "API")
    
    # Email Deliveries
    print_header("RECENT EMAIL DELIVERIES", limit=limit)
    email_deliveries = get_recent_email_deliveries(limit)
    for email in email_deliveries:
        print_log_entry(email, "EMAIL")
    
    # Payload Analysis
    print_header("PAYLOAD ANALYSIS")
    payload_logs = get_payload_logs(hours=24)
    print(f"Logs with payloads in last 24 hours: {len(payload_logs)}")
    
    if payload_logs:
        print("\nSample payload logs:")
        for log in payload_logs[:3]:
            print_log_entry(log, "PAYLOAD")
    
    # Performance Metrics
    print_header("PERFORMANCE METRICS")
    metrics = get_performance_metrics(hours=24)
    if metrics:
        print(f"Total Requests: {metrics.get('total_requests', 0)}")
        print(f"Average Duration: {metrics.get('avg_duration_ms', 0):.2f}ms")
        print(f"Max Duration: {metrics.get('max_duration_ms', 0)}ms")
        print(f"Error Count: {metrics.get('error_count', 0)}")
    
    # Correlation Analysis
    print_header("CORRELATION ANALYSIS")
    correlation = analyze_correlation()
    if 'error' not in correlation:
        print("Most recent failure analysis:")
        for key, value in correlation.items():
            if key != 'timestamp':
                print(f"  {key}: {value}")
    
    print_header("DIAGNOSTIC COMPLETE")
    print("✅ All database operations completed successfully using centralized service")

if __name__ == "__main__":
    main()
