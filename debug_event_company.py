from sqlalchemy import create_engine, text
import os
import sys

# Add backend directory to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from common.config import settings

# Create database connection
database_url = settings.DATABASE_URL
engine = create_engine(database_url)

def check_event_company(event_id, company_id):
    print(f"Checking EventCompany for EventID={event_id}, CompanyID={company_id}")
    
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
            FROM EventCompany ec
            LEFT JOIN EventCompanyRole r ON ec.EventCompanyRoleID = r.EventCompanyRoleID
            WHERE ec.EventID = :event_id AND ec.CompanyID = :company_id
        """)
        
        result = connection.execute(query, {"event_id": event_id, "company_id": company_id}).fetchall()
        
        if not result:
            print("No relationship found at all.")
        else:
            for row in result:
                print(f"Found: ID={row.EventCompanyID}, Active={row.IsActive}, Deleted={row.IsDeleted}, Role={row.RoleCode} ({row.RoleName})")

if __name__ == "__main__":
    # IDs from the error log
    check_event_company(29, 1016)

