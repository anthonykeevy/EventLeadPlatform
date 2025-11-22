"""
Quick Validation Test for Form Access Control Implementation
Tests basic functionality to reduce UAT test cases

This script uses the same database connection method as the application.
"""
import sys
import os

# Load environment variables from .env file (same as main.py)
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from sqlalchemy import select, text
from common.database import get_db, test_connection

# Import all models to ensure relationships are properly configured
# Import CompanyRelationship first to satisfy CompanyRelationshipType relationship
from models.company_relationship import CompanyRelationship
from models.form_access_control import FormAccessControl
from models.ref.form_access_control_access_type import FormAccessControlAccessType
from models.ref.company_relationship_type import CompanyRelationshipType
from models.form import Form
from models.user import User
from models.user_company import UserCompany

def test_models_exist():
    """Test that all models can be imported and have correct structure"""
    print("[OK] Testing model imports...")
    assert FormAccessControl is not None
    assert FormAccessControlAccessType is not None
    assert CompanyRelationshipType is not None
    print("  [OK] All models imported successfully")

def test_database_connection():
    """Test that database connection works using application's method"""
    print("\n[OK] Testing database connection...")
    result = test_connection()
    if result:
        print("  [OK] Database connection successful")
        return True
    else:
        print("  [FAIL] Database connection failed")
        print("  [NOTE] Check DATABASE_URL in .env file or environment variables")
        return False

def test_reference_data_exists():
    """Test that reference data exists in database"""
    print("\n[OK] Testing reference data...")
    db = next(get_db())
    try:
        # Check access types
        access_types = db.execute(
            select(FormAccessControlAccessType).where(
                FormAccessControlAccessType.IsDeleted == False,
                FormAccessControlAccessType.IsActive == True
            )
        ).scalars().all()
        assert len(access_types) > 0, "No access types found"
        print(f"  [OK] Found {len(access_types)} access types")
        
        # Verify expected access types exist
        access_type_codes = [at.AccessTypeCode for at in access_types]
        expected_codes = ['VIEW', 'EDIT', 'MANAGE', 'SUBMIT', 'ANALYZE']
        for code in expected_codes:
            assert code in access_type_codes, f"Access type {code} not found"
        print("  [OK] All expected access types present")
        
        # Display access types
        print("  [INFO] Access types:")
        for at in access_types:
            print(f"    - {at.AccessTypeCode}: {at.AccessTypeName}")
        
        # Check relationship types (using raw SQL to avoid relationship mapping issues)
        result = db.execute(text("""
            SELECT CompanyRelationshipTypeID, TypeName, TypeDescription
            FROM ref.CompanyRelationshipType
            WHERE IsDeleted = 0 AND IsActive = 1
        """))
        relationship_types = result.fetchall()
        assert len(relationship_types) > 0, "No relationship types found"
        print(f"  [OK] Found {len(relationship_types)} relationship types")
        
        # Display relationship types
        print("  [INFO] Relationship types:")
        for rt in relationship_types:
            print(f"    - ID {rt[0]}: {rt[1]}")
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] Error checking reference data: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

def test_service_imports():
    """Test that service functions can be imported"""
    print("\n[OK] Testing service imports...")
    try:
        from modules.forms.access_control_service import (
            grant_access,
            revoke_access,
            get_form_access_list,
            check_user_access,
            get_user_access_level,
            get_user_accessible_forms
        )
        assert grant_access is not None
        assert revoke_access is not None
        assert get_form_access_list is not None
        assert check_user_access is not None
        assert get_user_access_level is not None
        assert get_user_accessible_forms is not None
        print("  [OK] All service functions imported successfully")
        return True
    except Exception as e:
        print(f"  [FAIL] Error importing service functions: {str(e)}")
        return False

def test_api_imports():
    """Test that API router can be imported"""
    print("\n[OK] Testing API imports...")
    try:
        from modules.forms.access_control_router import router
        assert router is not None
        print("  [OK] Access control router imported successfully")
        
        # Check routes exist
        route_paths = [r.path for r in router.routes]
        print(f"  [OK] Found {len(route_paths)} routes")
        for route in route_paths:
            print(f"    - {route}")
        return True
    except Exception as e:
        print(f"  [FAIL] Error importing API router: {str(e)}")
        return False

def test_schema_imports():
    """Test that schemas can be imported"""
    print("\n[OK] Testing schema imports...")
    try:
        from modules.forms.access_control_schemas import (
            GrantAccessRequest,
            AccessControlResponse,
            AccessListResponse,
            AccessCheckResponse,
            AccessTypeResponse,
            RelationshipTypeResponse
        )
        assert GrantAccessRequest is not None
        assert AccessControlResponse is not None
        assert AccessListResponse is not None
        assert AccessCheckResponse is not None
        assert AccessTypeResponse is not None
        assert RelationshipTypeResponse is not None
        print("  [OK] All schemas imported successfully")
        return True
    except Exception as e:
        print(f"  [FAIL] Error importing schemas: {str(e)}")
        return False

def main():
    """Run all validation tests"""
    print("=" * 60)
    print("Form Access Control - Implementation Validation")
    print("=" * 60)
    print(f"\n[INFO] Database URL: {os.getenv('DATABASE_URL', 'NOT SET (using default)')}")
    print(f"[INFO] Working directory: {os.getcwd()}")
    print(f"[INFO] .env file location: {os.path.join(os.getcwd(), '.env')}")
    
    results = []
    
    try:
        results.append(("Model Imports", test_models_exist()))
        results.append(("Database Connection", test_database_connection()))
        
        # Only test database-dependent features if connection works
        if results[-1][1]:  # If database connection succeeded
            results.append(("Reference Data", test_reference_data_exists()))
        else:
            print("\n[SKIP] Skipping reference data test (database connection failed)")
            results.append(("Reference Data", None))
        
        results.append(("Service Imports", test_service_imports()))
        results.append(("API Imports", test_api_imports()))
        results.append(("Schema Imports", test_schema_imports()))
        
        print("\n" + "=" * 60)
        print("Validation Test Results")
        print("=" * 60)
        
        passed = 0
        failed = 0
        skipped = 0
        
        for test_name, result in results:
            if result is True:
                print(f"[PASS] {test_name}")
                passed += 1
            elif result is False:
                print(f"[FAIL] {test_name}")
                failed += 1
            else:
                print(f"[SKIP] {test_name}")
                skipped += 1
        
        print("\n" + "=" * 60)
        if failed == 0:
            print("[PASS] ALL VALIDATION TESTS PASSED")
            print("=" * 60)
            print("\nImplementation is ready for UAT testing.")
            print("All models, services, APIs, and schemas are properly configured.")
            return 0
        else:
            print(f"[FAIL] VALIDATION FAILED: {failed} test(s) failed")
            print("=" * 60)
            print("\nPlease fix the issues above before proceeding with UAT.")
            return 1
            
    except Exception as e:
        print(f"\n[FAIL] VALIDATION FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

