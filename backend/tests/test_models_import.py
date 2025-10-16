"""
Test Model Imports and Registration (AC-0.1.6)
Validates that all 33 models can be imported without circular dependency errors
"""
import pytest


def test_import_all_models():
    """Test that all 33 models can be imported without circular dependency errors."""
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
    
    # Verify all models imported successfully
    assert User is not None
    assert Company is not None
    assert UserCompany is not None
    assert Country is not None
    assert AppSetting is not None
    assert ActivityLog is not None
    assert ApiRequest is not None
    assert ABRSearch is not None


def test_model_count():
    """Test that exactly 33 models are exported."""
    from backend.models import __all__, get_model_count
    
    assert len(__all__) == 33, f"Expected 33 models, got {len(__all__)}"
    assert get_model_count() == 33


def test_sqlalchemy_registration():
    """Test that all models are registered with SQLAlchemy Base."""
    from backend.common.database import Base
    from backend.models import __all__
    
    # Import all models to register them
    import backend.models  # noqa: F401
    
    # Verify tables are registered
    registered_tables = Base.metadata.tables
    assert len(registered_tables) > 0, "No tables registered with SQLAlchemy"
    
    # Verify schemas are present
    schemas = set()
    for table_name in registered_tables.keys():
        if '.' in table_name:
            schema = table_name.split('.')[0]
            schemas.add(schema)
    
    expected_schemas = {'ref', 'dbo', 'config', 'audit', 'log', 'cache'}
    assert expected_schemas.issubset(schemas), f"Missing schemas. Expected {expected_schemas}, got {schemas}"


def test_model_table_names():
    """Test that model table names follow PascalCase convention (Solomon standard)."""
    from backend.models import User, Company, UserCompany, Country
    
    assert User.__tablename__ == "User"
    assert Company.__tablename__ == "Company"
    assert UserCompany.__tablename__ == "UserCompany"
    assert Country.__tablename__ == "Country"


def test_model_schemas():
    """Test that models are assigned to correct schemas."""
    from backend.models import (
        User, Company, Country, AppSetting, ActivityLog, ApiRequest, ABRSearch
    )
    
    assert User.__table_args__['schema'] == 'dbo'
    assert Company.__table_args__['schema'] == 'dbo'
    assert Country.__table_args__['schema'] == 'ref'
    assert AppSetting.__table_args__['schema'] == 'config'
    assert ActivityLog.__table_args__['schema'] == 'audit'
    assert ApiRequest.__table_args__['schema'] == 'log'
    assert ABRSearch.__table_args__['schema'] == 'cache'


def test_primary_keys():
    """Test that models have primary keys following [TableName]ID pattern."""
    from backend.models import User, Company, UserCompany, Country
    
    # Check primary key column names
    assert 'UserID' in [col.name for col in User.__table__.primary_key.columns]
    assert 'CompanyID' in [col.name for col in Company.__table__.primary_key.columns]
    assert 'UserCompanyID' in [col.name for col in UserCompany.__table__.primary_key.columns]
    assert 'CountryID' in [col.name for col in Country.__table__.primary_key.columns]


def test_audit_columns():
    """Test that business tables have required audit columns."""
    from backend.models import User, Company, UserCompany
    
    # Check User audit columns
    user_columns = [col.name for col in User.__table__.columns]
    assert 'CreatedDate' in user_columns
    assert 'CreatedBy' in user_columns
    assert 'UpdatedDate' in user_columns
    assert 'UpdatedBy' in user_columns
    assert 'IsDeleted' in user_columns
    assert 'DeletedDate' in user_columns
    assert 'DeletedBy' in user_columns
    
    # Check Company audit columns
    company_columns = [col.name for col in Company.__table__.columns]
    assert 'CreatedDate' in company_columns
    assert 'UpdatedDate' in company_columns
    assert 'IsDeleted' in company_columns
    
    # Check UserCompany audit columns
    usercompany_columns = [col.name for col in UserCompany.__table__.columns]
    assert 'CreatedDate' in usercompany_columns
    assert 'UpdatedDate' in usercompany_columns
    assert 'IsDeleted' in usercompany_columns

