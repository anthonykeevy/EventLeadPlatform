import sys
import os
import logging
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.getcwd(), "backend", ".env"))

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from common.database import get_db
from models import Form, FormApprovalToken, FormApprovalStatus, FormStatus, ActivityLog

# Setup logging
logging.basicConfig(level=logging.INFO)

def check_token_status():
    token_str = "VeraD87tsQPlLbjEq2-jE8zXaYSZab1jLWsiLsvpmzM"
    print(f"Checking status for token: {token_str}...")
    
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # 1. Find Token
        token = db.query(FormApprovalToken).filter(FormApprovalToken.Token == token_str).first()
        if not token:
            print("❌ Token not found in database!")
            return

        print(f"✅ Token Found (ID: {token.FormApprovalTokenID})")
        print(f"   - IsUsed: {token.IsUsed}")
        print(f"   - UsedAt: {token.UsedAt}")
        print(f"   - ExpiresAt: {token.ExpiresAt}")
        print(f"   - FormID: {token.FormID}")
        print(f"   - UserID (Shadow): {token.UserID}")

        # 2. Check Form Status
        form = db.get(Form, token.FormID)
        if form:
            approval_status = db.get(FormApprovalStatus, form.FormApprovalStatusID)
            form_status = db.get(FormStatus, form.FormStatusID)
            
            print(f"\n📋 Form Details (ID: {form.FormID}):")
            print(f"   - Name: {form.FormName}")
            print(f"   - Approval Status: {approval_status.ApprovalStatusCode} ({approval_status.ApprovalStatusName})")
            print(f"   - Form Status: {form_status.StatusCode} ({form_status.StatusName})")
        else:
            print("❌ Form not found!")

        # 3. Check Activity Log
        print(f"\n📜 Recent Activity Log for Form {token.FormID}:")
        logs = db.query(ActivityLog).filter(
            ActivityLog.EntityID == token.FormID, 
            ActivityLog.EntityType == 'Form'
        ).order_by(ActivityLog.CreatedDate.desc()).limit(5).all()
        
        for log in logs:
            print(f"   - [{log.CreatedDate}] {log.Action}: {log.Details if hasattr(log, 'Details') else 'No details'}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    check_token_status()

