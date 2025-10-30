"""
Quick script to check what errors are being logged
"""
import pyodbc
from datetime import datetime, timedelta

# Connect to database
conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost;"
    "Database=EventLeadPlatform;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Get recent errors from the last 5 minutes
    query = """
        SELECT TOP 10
            ErrorID,
            ErrorType,
            ErrorMessage,
            StackTrace,
            Path,
            Method,
            CreatedDate
        FROM log.ApplicationError
        WHERE CreatedDate > DATEADD(MINUTE, -5, GETDATE())
        ORDER BY CreatedDate DESC
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    if rows:
        print("\n" + "="*80)
        print("RECENT APPLICATION ERRORS (Last 5 minutes)")
        print("="*80 + "\n")
        
        for row in rows:
            print(f"Error ID: {row.ErrorID}")
            print(f"Type: {row.ErrorType}")
            print(f"Message: {row.ErrorMessage}")
            print(f"Path: {row.Path}")
            print(f"Method: {row.Method}")
            print(f"Time: {row.CreatedDate}")
            if row.StackTrace:
                print(f"Stack Trace:\n{row.StackTrace}")
            print("-" * 80 + "\n")
    else:
        print("\nNo errors found in the last 5 minutes")
    
    conn.close()
    
except Exception as e:
    print(f"Error querying database: {e}")
    import traceback
    print(traceback.format_exc())

