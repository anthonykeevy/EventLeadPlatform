"""
Delete test companies that have no users
Uses the same database connection pattern as enhanced_diagnostic_logs.py
"""
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

# Load environment variables
env_path = backend_dir / ".env"
load_dotenv(env_path)

def find_empty_companies(dry_run=True):
    """Find companies with no users"""
    try:
        # Use same connection pattern as enhanced_diagnostic_logs.py
        try:
            from common.database import engine
            db_engine = engine
        except ImportError:
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise Exception("DATABASE_URL not found in environment variables")
            db_engine = create_engine(database_url)
        
        with db_engine.connect() as conn:
            print("=" * 80)
            print("FINDING COMPANIES WITH NO USERS")
            print("=" * 80)
            
            # Find companies with no active users
            query = text("""
                SELECT 
                    c.CompanyID,
                    c.CompanyName,
                    c.ABN,
                    c.CreatedDate,
                    COUNT(uc.UserID) AS UserCount
                FROM dbo.Company c
                LEFT JOIN dbo.UserCompany uc ON uc.CompanyID = c.CompanyID 
                    AND uc.IsDeleted = 0
                LEFT JOIN ref.UserCompanyStatus ucs ON uc.StatusID = ucs.UserCompanyStatusID 
                    AND ucs.StatusCode = 'active'
                WHERE c.IsDeleted = 0
                GROUP BY c.CompanyID, c.CompanyName, c.ABN, c.CreatedDate
                HAVING COUNT(uc.UserID) = 0
                ORDER BY c.CreatedDate DESC
            """)
            
            results = conn.execute(query).fetchall()
            
            if results:
                print(f"\nFound {len(results)} companies with no users:\n")
                for row in results:
                    print(f"  CompanyID: {row.CompanyID}")
                    print(f"  Name: {row.CompanyName}")
                    print(f"  ABN: {row.ABN or 'N/A'}")
                    print(f"  Created: {row.CreatedDate}")
                    print(f"  User Count: {row.UserCount}")
                    print()
                
                if dry_run:
                    print("\n[DRY RUN MODE] - No changes made")
                    print("To delete these companies, run with --execute flag")
                    print("\nCommand: python scripts/delete_empty_companies.py --execute")
                else:
                    print("\n[WARNING] About to DELETE these companies!")
                    response = input("Type 'DELETE' to confirm: ")
                    
                    if response == "DELETE":
                        delete_companies(conn, [r.CompanyID for r in results])
                    else:
                        print("Cancelled. No companies deleted.")
            else:
                print("No empty companies found")
                
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

def delete_companies(conn, company_ids):
    """Delete companies (soft delete)"""
    try:
        deleted_count = 0
        
        for company_id in company_ids:
            # Soft delete the company
            update_query = text("""
                UPDATE dbo.Company
                SET IsDeleted = 1,
                    UpdatedDate = GETUTCDATE(),
                    UpdatedBy = NULL
                WHERE CompanyID = :company_id
                    AND IsDeleted = 0
            """)
            
            result = conn.execute(update_query, {"company_id": company_id})
            conn.commit()
            
            if result.rowcount > 0:
                deleted_count += 1
                print(f"✓ Soft deleted CompanyID: {company_id}")
        
        print(f"\n✅ Successfully deleted {deleted_count} companies")
        
    except Exception as e:
        conn.rollback()
        print(f"ERROR deleting companies: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    dry_run = "--execute" not in sys.argv
    
    if dry_run:
        print("DRY RUN MODE (use --execute to actually delete)")
        print()
    
    find_empty_companies(dry_run=dry_run)
