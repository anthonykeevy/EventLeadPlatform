"""
Diagnostic Tool - Extract Recent Log Entries
Used for troubleshooting authentication and application errors
"""
import os
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine, text
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
env_path = backend_dir / ".env"
load_dotenv(env_path)

def format_json(json_str):
    """Pretty print JSON strings"""
    try:
        if json_str:
            obj = json.loads(json_str)
            return json.dumps(obj, indent=2)
        return "NULL"
    except:
        return str(json_str)

def get_recent_logs(limit=10):
    """Extract recent log entries from all log tables"""
    # Import database from backend (same connection as API uses)
    from common.database import get_db, engine
    
    with engine.connect() as conn:
        print("=" * 100)
        print(f"RECENT AUTH EVENTS (Last {limit})")
        print("=" * 100)
        
        auth_events = conn.execute(text(f"""
            SELECT TOP {limit}
                AuthEventID,
                EventType,
                UserID,
                Email,
                Reason,
                IPAddress,
                RequestID,
                CreatedDate
            FROM log.AuthEvent
            ORDER BY CreatedDate DESC
        """)).fetchall()
        
        if auth_events:
            for event in auth_events:
                print(f"\n[{event[7]}] {event[1]}")
                print(f"  UserID: {event[2] or 'NULL'}")
                print(f"  Email: {event[3] or 'NULL'}")
                print(f"  Reason: {format_json(event[4])}")
                print(f"  IP: {event[5]} | RequestID: {event[6]}")
        else:
            print("No auth events found.")
        
        print("\n" + "=" * 100)
        print(f"RECENT APPLICATION ERRORS (Last {limit})")
        print("=" * 100)
        
        app_errors = conn.execute(text(f"""
            SELECT TOP {limit}
                ApplicationErrorID,
                ErrorType,
                ErrorMessage,
                Severity,
                Path,
                Method,
                RequestID,
                UserID,
                CreatedDate
            FROM log.ApplicationError
            ORDER BY CreatedDate DESC
        """)).fetchall()
        
        if app_errors:
            for error in app_errors:
                print(f"\n[{error[8]}] {error[1]} - {error[3]}")
                print(f"  Path: {error[5]} {error[4]}")
                print(f"  Message: {error[2]}")
                print(f"  UserID: {error[7] or 'NULL'} | RequestID: {error[6]}")
        else:
            print("No application errors found.")
        
        print("\n" + "=" * 100)
        print(f"RECENT API REQUESTS (Last {limit})")
        print("=" * 100)
        
        api_requests = conn.execute(text(f"""
            SELECT TOP {limit}
                ApiRequestID,
                Method,
                Path,
                StatusCode,
                DurationMs,
                RequestID,
                UserID,
                CreatedDate
            FROM log.ApiRequest
            ORDER BY CreatedDate DESC
        """)).fetchall()
        
        if api_requests:
            for req in api_requests:
                print(f"\n[{req[7]}] {req[1]} {req[2]}")
                print(f"  Status: {req[3]} | Duration: {req[4]}ms")
                print(f"  UserID: {req[6] or 'NULL'} | RequestID: {req[5]}")
        else:
            print("No API requests found.")
        
        print("\n" + "=" * 100)
        print("CORRELATION VIEW (Last Failed Signup)")
        print("=" * 100)
        
        # Get the most recent failed signup RequestID
        correlation = conn.execute(text("""
            SELECT TOP 1
                ae.RequestID,
                ae.EventType,
                ae.Reason,
                ae.CreatedDate,
                ape.ErrorType,
                ape.ErrorMessage,
                api.StatusCode,
                api.DurationMs
            FROM log.AuthEvent ae
            LEFT JOIN log.ApplicationError ape ON ae.RequestID = ape.RequestID
            LEFT JOIN log.ApiRequest api ON ae.RequestID = api.RequestID
            WHERE ae.EventType LIKE '%FAILED%'
            ORDER BY ae.CreatedDate DESC
        """)).fetchone()
        
        if correlation:
            print(f"\nRequestID: {correlation[0]}")
            print(f"Timestamp: {correlation[3]}")
            print(f"\nAuth Event:")
            print(f"  Type: {correlation[1]}")
            print(f"  Reason: {format_json(correlation[2])}")
            print(f"\nApplication Error:")
            print(f"  Type: {correlation[4]}")
            print(f"  Message: {correlation[5]}")
            print(f"\nAPI Request:")
            print(f"  Status Code: {correlation[6]}")
            print(f"  Duration: {correlation[7]}ms")
        else:
            print("No correlated failed signup found.")

if __name__ == "__main__":
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    get_recent_logs(limit)

