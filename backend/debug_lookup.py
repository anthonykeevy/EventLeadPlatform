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

def check_event_and_company(event_id, company_id):
    with engine.connect() as connection:
        print(f"\nChecking Event {event_id}:")
        event = connection.execute(text("SELECT * FROM dbo.Event WHERE EventID = :id"), {"id": event_id}).fetchone()
        if event:
            print(f"Found Event: {event.Name} (CompanyID={event.CompanyID})")
        else:
            print("Event not found")

        print(f"\nChecking Company {company_id}:")
        company = connection.execute(text("SELECT * FROM dbo.Company WHERE CompanyID = :id"), {"id": company_id}).fetchone()
        if company:
            print(f"Found Company: {company.CompanyName}")
        else:
            print("Company not found")

        print(f"\nChecking relationships for Event {event_id}:")
        rels = connection.execute(text("SELECT * FROM dbo.EventCompany WHERE EventID = :id"), {"id": event_id}).fetchall()
        for r in rels:
            print(f"Relation: CompanyID={r.CompanyID}, RoleID={r.EventCompanyRoleID}, IsActive={r.IsActive}")

if __name__ == "__main__":
    check_event_and_company(29, 1016)

