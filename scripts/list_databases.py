"""
List all databases on SQL Server
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy import text, create_engine

# Connect to master database to list all databases
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mssql+pyodbc://localhost/master?driver=ODBC+Driver+18+for+SQL+Server&Trusted_Connection=Yes&TrustServerCertificate=yes"
)

engine = create_engine(DATABASE_URL)

def list_databases():
    """List all databases on the SQL Server"""
    query = text("""
        SELECT 
            name,
            database_id,
            create_date
        FROM sys.databases
        WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')
        ORDER BY name
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query)
        return result.fetchall()

def main():
    print("=" * 80)
    print("SQL SERVER DATABASES")
    print("=" * 80)
    print()
    
    try:
        databases = list_databases()
        print(f"Found {len(databases)} user databases:")
        print()
        
        for idx, (name, db_id, create_date) in enumerate(databases, 1):
            print(f"{idx}. {name}")
            print(f"   - Database ID: {db_id}")
            print(f"   - Created: {create_date}")
            print()
        
        print("=" * 80)
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

