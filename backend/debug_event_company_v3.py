from sqlalchemy import create_engine, text
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure current directory is in path
sys.path.append(os.getcwd())

from common.database import DATABASE_URL

print(f"Using Database URL: {DATABASE_URL}")

# Create database connection
engine = create_engine(DATABASE_URL)

def check_event_company(event_id, company_id):
    print(f"Checking EventCompany for EventID={event_id}, CompanyID={company_id}")
    
    try:
        with engine.connect() as connection:
            # Check for any relationship (ignoring Active/Deleted flags)
            query = text("""
                SELECT 
                    ec.EventCompanyID, 
                    ec.EventID, 
                    ec.CompanyID, 
                    ec.IsActive, 
                    ec.IsDeleted,
                    r.RoleCode,
                    r.RoleName
                FROM dbo.EventCompany ec
                LEFT JOIN ref.EventCompanyRole r ON ec.EventCompanyRoleID = r.EventCompanyRoleID
                WHERE ec.EventID = :event_id AND ec.CompanyID = :company_id
            """)
            
            result = connection.execute(query, {"event_id": event_id, "company_id": company_id}).fetchall()
            
            if not result:
                print("No relationship found at all.")
            else:
                for row in result:
                    print(f"Found: ID={row.EventCompanyID}, Active={row.IsActive}, Deleted={row.IsDeleted}, Role={row.RoleCode} ({row.RoleName})")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # IDs from the error log
    check_event_company(29, 1016)

