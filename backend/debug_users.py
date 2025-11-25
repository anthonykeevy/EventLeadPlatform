from sqlalchemy import create_engine, text
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure current directory is in path
sys.path.append(os.getcwd())

from common.database import DATABASE_URL

# Create database connection
engine = create_engine(DATABASE_URL)

def check_users():
    with engine.connect() as connection:
        for user_id in [80, 108]:
            print(f"\nChecking User {user_id}:")
            user = connection.execute(text("SELECT * FROM dbo.[User] WHERE UserID = :id"), {"id": user_id}).fetchone()
            if user:
                print(f"Found User: {user.Email} (First={user.FirstName}, Last={user.LastName})")
                
                # Check Company
                user_companies = connection.execute(text("""
                    SELECT uc.CompanyID, c.CompanyName, ucs.StatusCode
                    FROM dbo.UserCompany uc
                    JOIN dbo.Company c ON uc.CompanyID = c.CompanyID
                    JOIN ref.UserCompanyStatus ucs ON uc.UserCompanyStatusID = ucs.UserCompanyStatusID
                    WHERE uc.UserID = :id AND uc.IsDeleted = 0
                """), {"id": user_id}).fetchall()
                
                for uc in user_companies:
                    print(f"  - Company: {uc.CompanyName} (ID={uc.CompanyID}, Status={uc.StatusCode})")
            else:
                print("User not found")

if __name__ == "__main__":
    check_users()

