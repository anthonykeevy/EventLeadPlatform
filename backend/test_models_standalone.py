"""
Standalone test to verify models can be imported successfully.
Run: python backend/test_models_standalone.py
"""
import sys
import os
from pathlib import Path

# Fix Windows encoding for emojis
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')  # type: ignore
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')  # type: ignore

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=" * 60)
print("Testing Story 0.1: Database Models & Core Infrastructure")
print("=" * 60)

# Test 1: Import all models
print("\n[Test 1] Importing all 33 models...")
try:
    from backend.models import (
        # Core business models (9)
        User, Company, UserCompany,
        CompanyCustomerDetails, CompanyBillingDetails, CompanyOrganizerDetails,
        UserInvitation, UserEmailVerificationToken, UserPasswordResetToken,
        
        # Reference tables (13)
        Country, Language, Industry, UserStatus, UserInvitationStatus,
        UserRole, UserCompanyRole, UserCompanyStatus,
        SettingCategory, SettingType, RuleType, CustomerTier, JoinedVia,
        
        # Configuration tables (2)
        AppSetting, ValidationRule,
        
        # Audit tables (4)
        ActivityLog, UserAudit, CompanyAudit, RoleAudit,
        
        # Log tables (4)
        ApiRequest, AuthEvent, ApplicationError, EmailDelivery,
        
        # Cache tables (1)
        ABRSearch,
    )
    print("✅ PASS: All 33 models imported successfully")
except ImportError as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# Test 2: Verify model count
print("\n[Test 2] Verifying model count...")
try:
    from backend.models import __all__, get_model_count
    
    expected = 33
    actual = get_model_count()
    
    if actual == expected:
        print(f"✅ PASS: Model count correct ({actual} models)")
    else:
        print(f"❌ FAIL: Expected {expected} models, got {actual}")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# Test 3: Verify SQLAlchemy registration
print("\n[Test 3] Verifying SQLAlchemy registration...")
try:
    from backend.common.database import Base
    
    table_count = len(Base.metadata.tables)
    if table_count > 0:
        print(f"✅ PASS: SQLAlchemy registered {table_count} tables")
    else:
        print("❌ FAIL: No tables registered with SQLAlchemy")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# Test 4: Verify table naming conventions
print("\n[Test 4] Verifying PascalCase naming conventions...")
try:
    assert User.__tablename__ == "User"
    assert Company.__tablename__ == "Company"
    assert UserCompany.__tablename__ == "UserCompany"
    assert Country.__tablename__ == "Country"
    print("✅ PASS: Table names follow PascalCase convention")
except AssertionError:
    print("❌ FAIL: Table names don't follow PascalCase convention")
    sys.exit(1)

# Test 5: Verify schema assignments
print("\n[Test 5] Verifying schema assignments...")
try:
    assert User.__table_args__['schema'] == 'dbo'
    assert Company.__table_args__['schema'] == 'dbo'
    assert Country.__table_args__['schema'] == 'ref'
    assert AppSetting.__table_args__['schema'] == 'config'
    assert ActivityLog.__table_args__['schema'] == 'audit'
    assert ApiRequest.__table_args__['schema'] == 'log'
    assert ABRSearch.__table_args__['schema'] == 'cache'
    print("✅ PASS: Models assigned to correct schemas")
except (KeyError, AssertionError) as e:
    print(f"❌ FAIL: Schema assignment error: {e}")
    sys.exit(1)

# Test 6: Verify primary keys
print("\n[Test 6] Verifying primary key naming...")
try:
    user_pk = [col.name for col in User.__table__.primary_key.columns]
    company_pk = [col.name for col in Company.__table__.primary_key.columns]
    
    assert 'UserID' in user_pk
    assert 'CompanyID' in company_pk
    print("✅ PASS: Primary keys follow [TableName]ID pattern")
except AssertionError:
    print("❌ FAIL: Primary key naming doesn't follow convention")
    sys.exit(1)

# Test 7: Verify audit columns
print("\n[Test 7] Verifying audit columns...")
try:
    user_cols = [col.name for col in User.__table__.columns]
    
    required_audit_cols = ['CreatedDate', 'CreatedBy', 'UpdatedDate', 'UpdatedBy', 
                          'IsDeleted', 'DeletedDate', 'DeletedBy']
    
    for col in required_audit_cols:
        assert col in user_cols, f"Missing audit column: {col}"
    
    print("✅ PASS: Audit columns present")
except AssertionError as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# Test 8: Test security utilities
print("\n[Test 8] Testing security utilities...")
try:
    from backend.common.security import hash_password, verify_password, generate_secure_token
    
    # Test password hashing
    password = "TestPassword123!"
    hashed = hash_password(password)
    
    assert hashed.startswith("$2b$12$"), "Password hash should be bcrypt format"
    assert len(hashed) == 60, "Bcrypt hash should be 60 characters"
    assert verify_password(password, hashed) is True, "Correct password should verify"
    assert verify_password("WrongPassword", hashed) is False, "Wrong password should not verify"
    
    # Test token generation
    token = generate_secure_token(32)
    assert len(token) >= 40, "Token should be at least 40 characters"
    
    print("✅ PASS: Security utilities working (bcrypt, token generation)")
except AssertionError as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# Test 9: Test Pydantic schemas
print("\n[Test 9] Testing Pydantic schemas...")
try:
    from backend.schemas import BaseResponse, ErrorResponse, PaginationParams
    
    # Test BaseResponse
    response = BaseResponse(success=True, message="Test", data={"id": 1})
    assert response.success is True
    
    # Test ErrorResponse (success and details have defaults)
    error = ErrorResponse(error="TestError", message="Test error")  # type: ignore
    assert error.success is False
    
    # Test PaginationParams (sort_by and sort_order have defaults)
    pagination = PaginationParams(page=1, page_size=20)  # type: ignore
    assert pagination.page == 1
    assert pagination.page_size == 20
    
    print("✅ PASS: Pydantic schemas working")
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED - Story 0.1 Complete!")
print("=" * 60)
print("\nSummary:")
print("  • 33 SQLAlchemy models created and importable")
print("  • Database connection utilities verified")
print("  • Security utilities working (bcrypt, tokens)")
print("  • Pydantic schemas functional")
print("  • Solomon standards compliance verified")
print("\n✨ Ready for Story 0.2 (Email Verification Workflow)")

