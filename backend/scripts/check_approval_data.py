import sys
import os
from sqlalchemy import text

# Add backend directory to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from common.database import SessionLocal

def check_approval_data():
    session = SessionLocal()
    
    try:
        print("--- Checking FormApprovalStatus ---")
        result = session.execute(text("SELECT FormApprovalStatusID, ApprovalStatusCode, ApprovalStatusName FROM ref.FormApprovalStatus ORDER BY SortOrder"))
        for row in result:
            print(row)
            
        print("\n--- Checking AppSettings for Approval ---")
        result = session.execute(text("SELECT SettingKey, SettingValue FROM config.AppSetting WHERE SettingKey LIKE 'forms.approval%'"))
        for row in result:
            print(row)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    check_approval_data()
