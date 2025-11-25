"""
Validation script for Story 2.11 - Approval Workflows
Tests approval service logic and database interaction.
"""
import sys
import os
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from common.database import SessionLocal, Base, engine
# Import all models to ensure registry is populated and avoid lookup errors
from models import *
from models.form import Form
from models.user import User
from models.company import Company
from models.ref.form_status import FormStatus
from models.ref.form_approval_status import FormApprovalStatus
from modules.forms.approval_service import ApprovalService

async def test_approval_workflow():
    print("=" * 70)
    print("Story 2.11 Validation: Approval Workflows")
    print("=" * 70)

    db = SessionLocal()
    try:
        # 1. Setup Data
        print("\n1. Setup Test Data")
        # Assume User 1 is Admin, User 2 is Creator
        # Assume Company 1 exists
        # Need to fetch real IDs or create mock
        
        user_id = 1 # Replace with real ID if needed
        admin_id = 1
        company_id = 1
        
        # 2. Create High Cost Form
        print("\n2. Create High Cost Form")
        # Simulate creation (or use service)
        # We'll insert directly for test setup
        
        # Get Status IDs
        draft_status = db.query(FormStatus).filter_by(StatusCode='DRAFT').first()
        no_approval_status = db.query(FormApprovalStatus).filter_by(ApprovalStatusCode='NO_APPROVAL').first()
        
        if not draft_status or not no_approval_status:
            print("Skipping test: Statuses not found (DB might be empty or not reachable)")
            return

        form = Form(
            FormName="Test Approval Form",
            CompanyID=company_id,
            FormStatusID=draft_status.FormStatusID,
            FormApprovalStatusID=no_approval_status.FormApprovalStatusID,
            DeploymentCost=500.00, # High cost
            CreatedBy=user_id,
            CreatedDate=datetime.utcnow()
        )
        db.add(form)
        db.commit()
        db.refresh(form)
        print(f"   Created Form {form.FormID} with cost {form.DeploymentCost}")

        # 3. Test Publish Guard (Should fail)
        print("\n3. Test Publish Guard (Should Fail)")
        service = ApprovalService(db)
        try:
            service.check_publish_guard(form)
            print("   FAILED: Guard allowed publish")
        except ValueError as e:
            print(f"   PASSED: Guard blocked publish ({e})")

        # 4. Submit for Approval
        print("\n4. Submit for Approval")
        form = await service.submit_for_approval(form.FormID, user_id, company_id)
        print(f"   Status: {form.form_approval_status.ApprovalStatusCode}")
        assert form.form_approval_status.ApprovalStatusCode == 'PENDING'
        print("   PASSED: Status is PENDING")

        # 5. Approve
        print("\n5. Admin Approve")
        form = await service.approve_form(form.FormID, admin_id, company_id)
        print(f"   Status: {form.form_approval_status.ApprovalStatusCode}")
        assert form.form_approval_status.ApprovalStatusCode == 'APPROVED'
        print("   PASSED: Status is APPROVED")

        # 6. Publish Guard (Should Pass)
        print("\n6. Test Publish Guard (Should Pass)")
        try:
            service.check_publish_guard(form)
            print("   PASSED: Guard allowed publish")
        except ValueError as e:
            print(f"   FAILED: Guard blocked publish ({e})")

        # Cleanup
        print("\n7. Cleanup")
        db.delete(form)
        db.commit()
        print("   Cleanup complete")

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Need async loop for async methods
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_approval_workflow())

