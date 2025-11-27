import sys
import os
import logging
import asyncio
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.getcwd(), "backend", ".env"))

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from common.database import get_db
from models import Form, FormApprovalStatus, FormStatus, ActivityLog

# Setup logging
logging.basicConfig(level=logging.INFO)

def check_form_status():
    print("Checking Form Status for Form ID 25...")
    
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        form = db.get(Form, 25)
        if not form:
            print("Form 25 not found")
            return
            
        approval_status = db.get(FormApprovalStatus, form.FormApprovalStatusID)
        form_status = db.get(FormStatus, form.FormStatusID)
        
        print(f"Form Name: {form.FormName}")
        print(f"Form Approval Status: {approval_status.ApprovalStatusCode} ({approval_status.ApprovalStatusName})")
        print(f"Form Status: {form_status.StatusCode} ({form_status.StatusName})")
        
        print("\nRecent Activity Logs for Form 25:")
        logs = db.query(ActivityLog).filter(
            ActivityLog.EntityID == 25, 
            ActivityLog.EntityType == "Form"
        ).order_by(ActivityLog.CreatedDate.desc()).limit(5).all()
        
        for log in logs:
            print(f"- {log.CreatedDate}: {log.Action} - {log.NewValue}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_form_status()

