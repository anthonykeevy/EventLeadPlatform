"""
Validation script for Story 3.1 - Form Versioning
Tests form versioning logic and API endpoints.
"""
import sys
import os
import json
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

# Use internal service logic directly
from sqlalchemy import create_engine
from common.database import SessionLocal
import os

# Override database URL to match installed driver
# Using existing configuration if possible or falling back to ODBC Driver 17/18
from common.database import DATABASE_URL as EXISTING_DB_URL

# Try to detect if we're already running with a valid connection string, 
# if not, let's construct one that we know works for pyodbc/ODBC Driver 17
# We'll just hardcode the known working string if the current one is 18.
print(f"Original Database URL: {EXISTING_DB_URL}")

# Explicitly construct the URL regardless of what imported from common.database
# This ensures we are using the driver we know exists: ODBC Driver 17 for SQL Server
connection_string = "mssql+pyodbc://localhost/EventLeadPlatform?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=Yes&TrustServerCertificate=yes"

print(f"Using Database URL: {connection_string}")
os.environ["DATABASE_URL"] = connection_string

from common.database import engine, SessionLocal
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Re-create engine with corrected URL
engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from models.form import Form
from models.user import User
from models.ref.form_status import FormStatus
from models.ref.form_approval_status import FormApprovalStatus
from modules.forms.version_service import FormVersionService
from models.form_version import FormVersion

async def test_versioning_workflow():
    print("=" * 70)
    print("Story 3.1 Validation: Form Versioning")
    print("=" * 70)

    db = SessionLocal()
    form_id = None
    
    try:
        # 1. Setup Data (Create a Form)
        print("\n1. Setup Test Data")
        user = db.query(User).first()
        if not user:
            print("No users found in DB. Skipping.")
            return
        
        user_id = user.UserID
        # Fetch UserCompany to get a valid CompanyID for the user
        from models.user_company import UserCompany
        user_company = db.query(UserCompany).filter(UserCompany.UserID == user_id).first()
        company_id = user_company.CompanyID if user_company else 1 # Fallback

        # Get Status IDs
        draft_status = db.query(FormStatus).filter_by(StatusCode='DRAFT').first()
        no_approval_status = db.query(FormApprovalStatus).filter_by(ApprovalStatusCode='NO_APPROVAL').first()
        
        if not draft_status:
            print("DRAFT status not found.")
            return

        # Create a test form
        form = Form(
            FormName=f"Test Versioning Form {datetime.utcnow().isoformat()}",
            CompanyID=company_id,
            FormStatusID=draft_status.FormStatusID,
            FormApprovalStatusID=no_approval_status.FormApprovalStatusID,
            DeploymentCost=0.00,
            CreatedBy=user_id,
            CreatedDate=datetime.utcnow()
        )
        db.add(form)
        db.commit()
        db.refresh(form)
        form_id = form.FormID
        print(f"   Created Form {form_id}")

        service = FormVersionService(db)

        # 2. Create Initial Version (v1)
        print("\n2. Create Initial Draft Version (v1)")
        definition_v1 = {"pages": [{"id": "p1", "title": "Page 1"}]}
        v1 = await service.create_version(form_id, user_id, definition_v1, "Initial Draft")
        
        assert v1.VersionNumber == 1
        assert v1.Status == 'DRAFT'
        assert v1.IsActive == False
        assert v1.definition == definition_v1
        print(f"   PASSED: Created Version {v1.VersionNumber} ({v1.Status})")

        # 3. Create Second Version (v2)
        print("\n3. Create Second Draft Version (v2)")
        definition_v2 = {"pages": [{"id": "p1", "title": "Page 1"}, {"id": "p2", "title": "Page 2"}]}
        v2 = await service.create_version(form_id, user_id, definition_v2, "Added Page 2")
        
        assert v2.VersionNumber == 2
        assert v2.Status == 'DRAFT'
        assert v2.IsActive == False
        print(f"   PASSED: Created Version {v2.VersionNumber} ({v2.Status})")

        # 4. Publish Version 1
        print("\n4. Publish Version 1")
        published_v1 = await service.publish_version(form_id, 1, user_id)
        
        assert published_v1.Status == 'PUBLISHED'
        assert published_v1.IsActive == True
        print(f"   PASSED: Version 1 is now {published_v1.Status}")

        # Verify v2 is still DRAFT and inactive
        db.refresh(v2)
        assert v2.Status == 'DRAFT'
        assert v2.IsActive == False
        print("   PASSED: Version 2 remains DRAFT/Inactive")

        # 5. Get Active Version
        print("\n5. Get Active Version")
        active = await service.get_active_version(form_id, user_id)
        assert active.FormVersionID == published_v1.FormVersionID
        assert active.VersionNumber == 1
        print(f"   PASSED: Active version is {active.VersionNumber}")

        # 6. Publish Version 2 (Should replace v1)
        print("\n6. Publish Version 2")
        published_v2 = await service.publish_version(form_id, 2, user_id)
        
        assert published_v2.Status == 'PUBLISHED'
        assert published_v2.IsActive == True
        
        # Verify v1 is no longer active
        db.refresh(published_v1)
        assert published_v1.IsActive == False
        print(f"   PASSED: Version 2 is Active, Version 1 is Inactive")

        # 7. Update Draft (v3)
        print("\n7. Update Draft Version")
        # First create v3
        v3 = await service.create_version(form_id, user_id, {}, "Empty")
        
        # Update it
        new_def = {"pages": [], "theme": "dark"}
        updated_v3 = await service.update_version(form_id, v3.VersionNumber, user_id, new_def, "Updated Theme")
        
        assert updated_v3.definition == new_def
        assert updated_v3.VersionComment == "Updated Theme"
        print(f"   PASSED: Updated Version {v3.VersionNumber}")

        # 8. Attempt to Update Published Version (Should Fail)
        print("\n8. Attempt Update on Published Version (Should Fail)")
        try:
            await service.update_version(form_id, 2, user_id, {}, "Malicious Update")
            print("   FAILED: Allowed update on PUBLISHED version")
        except ValueError as e:
            print(f"   PASSED: Blocked update ({e})")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        print("\n9. Cleanup")
        if form_id:
            # Delete versions first due to FK
            # Need to be careful to fetch them fresh if session state is weird, but here we just delete what we have
            # Or just delete by ID
            try:
                db.query(FormVersion).filter(FormVersion.FormID == form_id).delete()
                db.query(Form).filter(Form.FormID == form_id).delete()
                db.commit()
                print("   Cleanup complete")
            except Exception as cleanup_error:
                 print(f"   Cleanup Warning: {cleanup_error}")
        db.close()

if __name__ == "__main__":
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test_versioning_workflow())
