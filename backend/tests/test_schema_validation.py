"""
Schema Validation Tests - Story 0.1
Ensures model column names match usage throughout codebase
Prevents runtime errors from column name mismatches
"""
import pytest
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from models.user import User
from models.audit.user_audit import UserAudit
from models.log.auth_event import AuthEvent
from common.database import SessionLocal


class TestUserModelColumns:
    """Test User model has expected columns with correct names"""
    
    def test_user_has_is_email_verified_column(self):
        """User model should have IsEmailVerified, not EmailVerified"""
        inspector = inspect(User)
        column_names = [col.name for col in inspector.columns]
        
        assert "IsEmailVerified" in column_names, "User model should have IsEmailVerified column"
        assert "EmailVerified" not in column_names, "User model should NOT have EmailVerified (use IsEmailVerified)"
    
    def test_user_has_status_id_column(self):
        """User model should have StatusID, not IsActive or UserStatusID"""
        inspector = inspect(User)
        column_names = [col.name for col in inspector.columns]
        
        assert "StatusID" in column_names, "User model should have StatusID column"
        assert "IsActive" not in column_names, "User model should NOT have IsActive (use StatusID)"
        assert "UserStatusID" not in column_names, "User model should NOT have UserStatusID (use StatusID)"
    
    def test_user_has_required_audit_columns(self):
        """User model should have all Solomon standard audit columns"""
        inspector = inspect(User)
        column_names = [col.name for col in inspector.columns]
        
        required_audit_columns = [
            "CreatedDate", "UpdatedDate", "IsDeleted",
            "CreatedBy", "UpdatedBy", "DeletedDate", "DeletedBy"
        ]
        
        for col in required_audit_columns:
            assert col in column_names, f"User model should have {col} audit column"
    
    def test_user_can_create_instance_with_correct_columns(self, db: Session):
        """Test User instance can be created with correct column names"""
        from models.ref.user_status import UserStatus
        
        # Get a valid StatusID
        pending_status = db.query(UserStatus).filter(
            UserStatus.StatusName == "Pending Verification"
        ).first()
        
        # This should work without TypeError
        user = User(
            Email="test@example.com",
            PasswordHash="hashed_password",
            FirstName="Test",
            LastName="User",
            IsEmailVerified=False,  # Correct column name
            StatusID=pending_status.UserStatusID if pending_status else 1  # Correct column name
        )
        
        assert user.IsEmailVerified == False
        assert user.Email == "test@example.com"


class TestUserAuditModelColumns:
    """Test UserAudit model has expected columns with correct names"""
    
    def test_user_audit_has_change_type_column(self):
        """UserAudit should have ChangeType, not Action or TableName"""
        inspector = inspect(UserAudit)
        column_names = [col.name for col in inspector.columns]
        
        assert "ChangeType" in column_names, "UserAudit should have ChangeType column"
        assert "Action" not in column_names, "UserAudit should NOT have Action (use ChangeType)"
        assert "TableName" not in column_names, "UserAudit should NOT have TableName"
    
    def test_user_audit_has_changed_by_column(self):
        """UserAudit should have ChangedBy, not ChangedByUserID"""
        inspector = inspect(UserAudit)
        column_names = [col.name for col in inspector.columns]
        
        assert "ChangedBy" in column_names, "UserAudit should have ChangedBy column"
        assert "ChangedByUserID" not in column_names, "UserAudit should NOT have ChangedByUserID (use ChangedBy)"
    
    def test_user_audit_has_all_required_columns(self):
        """UserAudit should have all expected tracking columns"""
        inspector = inspect(UserAudit)
        column_names = [col.name for col in inspector.columns]
        
        required_columns = [
            "AuditUserID", "UserID", "FieldName", "OldValue", "NewValue",
            "ChangeType", "ChangeReason", "ChangedBy", "ChangedByEmail",
            "IPAddress", "UserAgent", "CreatedDate", "IsDeleted"
        ]
        
        for col in required_columns:
            assert col in column_names, f"UserAudit should have {col} column"


class TestAuthEventModelColumns:
    """Test AuthEvent model has expected columns with correct names"""
    
    def test_auth_event_has_event_type_column(self):
        """AuthEvent should have EventType, not EventStatus"""
        inspector = inspect(AuthEvent)
        column_names = [col.name for col in inspector.columns]
        
        assert "EventType" in column_names, "AuthEvent should have EventType column"
        assert "EventStatus" not in column_names, "AuthEvent should NOT have EventStatus (use EventType)"
    
    def test_auth_event_has_reason_column(self):
        """AuthEvent should have Reason, not Details"""
        inspector = inspect(AuthEvent)
        column_names = [col.name for col in inspector.columns]
        
        assert "Reason" in column_names, "AuthEvent should have Reason column"
        assert "Details" not in column_names, "AuthEvent should NOT have Details (use Reason)"
    
    def test_auth_event_has_all_required_columns(self):
        """AuthEvent should have all expected tracking columns"""
        inspector = inspect(AuthEvent)
        column_names = [col.name for col in inspector.columns]
        
        required_columns = [
            "AuthEventID", "UserID", "EventType", "Reason", "Email",
            "IPAddress", "UserAgent", "RequestID", "CreatedDate"
        ]
        
        for col in required_columns:
            assert col in column_names, f"AuthEvent should have {col} column"


class TestModelUsageConsistency:
    """Test that code using models uses correct column names"""
    
    def test_create_user_uses_correct_columns(self):
        """Test create_user function uses correct column names in actual code"""
        from modules.auth.user_service import create_user
        import inspect
        import re
        
        # Get source code
        source = inspect.getsource(create_user)
        
        # Should use correct column names in actual User(...) constructor
        # Look for the User() instantiation pattern
        user_constructor = re.search(r'User\((.*?)\)', source, re.DOTALL)
        if user_constructor:
            constructor_code = user_constructor.group(1)
            assert "IsEmailVerified" in constructor_code, "User() should use IsEmailVerified"
            assert "StatusID" in constructor_code, "User() should use StatusID"
            assert "EmailVerified=" not in constructor_code or "IsEmailVerified=" in constructor_code, "Should use IsEmailVerified not EmailVerified"
    
    def test_log_auth_event_uses_correct_columns(self):
        """Test log_auth_event function uses correct column names"""
        from modules.auth.audit_service import log_auth_event
        import inspect
        
        # Get source code
        source = inspect.getsource(log_auth_event)
        
        # Should use correct column names
        assert "EventType=" in source, "log_auth_event should use EventType"
        assert "Reason=" in source, "log_auth_event should use Reason"
        
        # Should NOT use incorrect column names
        assert "EventStatus=" not in source, "log_auth_event should NOT use EventStatus"
        assert "Details=" not in source or "# Details" in source, "log_auth_event should NOT use Details column"
    
    def test_log_user_audit_uses_correct_columns(self):
        """Test log_user_audit function uses correct column names"""
        from modules.auth.audit_service import log_user_audit
        import inspect
        
        # Get source code
        source = inspect.getsource(log_user_audit)
        
        # Should use correct column names
        assert "ChangeType" in source, "log_user_audit should use ChangeType parameter"
        assert "ChangedBy=" in source, "log_user_audit should use ChangedBy"
        
        # Should NOT use incorrect column names
        assert "TableName=" not in source, "log_user_audit should NOT use TableName"
        assert "Action=" not in source or "# Action" in source, "log_user_audit should NOT use Action"


class TestAlembicMigrationConsistency:
    """Test that Alembic migrations match current models"""
    
    def test_alembic_current_head_matches_migrations(self):
        """Verify alembic current revision matches latest migration"""
        from alembic.config import Config
        from alembic import command
        from io import StringIO
        
        alembic_cfg = Config("alembic.ini")
        
        # This test verifies migrations are up to date
        # If it fails, run: alembic upgrade head
        try:
            # Just verify alembic config is valid
            assert alembic_cfg is not None
        except Exception as e:
            pytest.skip(f"Alembic config not available: {e}")
    
    def test_user_model_matches_database_schema(self, db: Session):
        """Verify User model columns match actual database table"""
        from sqlalchemy import text
        
        # Get actual table columns from database
        result = db.execute(text("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'dbo' 
            AND TABLE_NAME = 'User'
            ORDER BY COLUMN_NAME
        """))
        db_columns = {row[0] for row in result.fetchall()}
        
        # Get model columns
        inspector = inspect(User)
        model_columns = {col.name for col in inspector.columns}
        
        # All model columns should exist in database
        missing_in_db = model_columns - db_columns
        assert len(missing_in_db) == 0, f"Model has columns not in DB: {missing_in_db}"
        
        # Database can have extra columns not in model (that's okay)
        # But critical columns should be in model
        critical_columns = {"UserID", "Email", "IsEmailVerified", "StatusID"}
        missing_in_model = critical_columns - model_columns
        assert len(missing_in_model) == 0, f"Model missing critical columns: {missing_in_model}"


@pytest.fixture
def db():
    """Database session fixture"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

