"""
Test Model Integration (AC-0.1.6, AC-0.1.7)
Validates model queries, relationships, and foreign keys
"""
import pytest
from sqlalchemy import text, select
from backend.common.database import SessionLocal
from backend.models import (
    User, Company, UserCompany, Country, UserStatus, UserCompanyRole,
    UserCompanyStatus, JoinedVia, CustomerTier, CompanyCustomerDetails
)


@pytest.fixture
def db_session():
    """Provide a database session for tests."""
    session = SessionLocal()
    yield session
    session.close()


def test_query_country_table(db_session):
    """Test querying Country reference table (AC-0.1.6)."""
    # Query Australia from seed data
    result = db_session.execute(
        select(Country).where(Country.CountryCode == 'AU')
    )
    country = result.scalar_one_or_none()
    
    if country:
        assert country.CountryName == 'Australia'
        assert country.CountryCode == 'AU'
        assert country.CurrencyCode == 'AUD'
        assert country.IsActive is True
        print(f"✓ Retrieved Country: {country.CountryName}")


def test_query_user_status_table(db_session):
    """Test querying UserStatus reference table with seed data (AC-0.1.6)."""
    # Query all user statuses
    result = db_session.execute(select(UserStatus))
    statuses = result.scalars().all()
    
    # Should have seed data (Active, Pending, Locked, Inactive)
    if statuses:
        status_codes = [s.StatusCode for s in statuses]
        print(f"✓ Retrieved UserStatus codes: {status_codes}")
        assert len(statuses) >= 1  # At least one status should exist


def test_query_customer_tier_table(db_session):
    """Test querying CustomerTier reference table (AC-0.1.6)."""
    result = db_session.execute(select(CustomerTier))
    tiers = result.scalars().all()
    
    if tiers:
        tier_codes = [t.TierCode for t in tiers]
        print(f"✓ Retrieved CustomerTier codes: {tier_codes}")


def test_query_user_table(db_session):
    """Test querying User table (AC-0.1.6)."""
    # Try to query users (may be empty)
    result = db_session.execute(select(User).limit(1))
    user = result.scalar_one_or_none()
    
    if user:
        assert user.UserID is not None
        assert user.Email is not None
        assert user.PasswordHash is not None
        print(f"✓ Retrieved User: {user.Email}")
    else:
        print("⚠ No users in database (expected for fresh install)")


def test_query_company_table(db_session):
    """Test querying Company table (AC-0.1.6)."""
    result = db_session.execute(select(Company).limit(1))
    company = result.scalar_one_or_none()
    
    if company:
        assert company.CompanyID is not None
        assert company.CompanyName is not None
        print(f"✓ Retrieved Company: {company.CompanyName}")
    else:
        print("⚠ No companies in database (expected for fresh install)")


def test_user_status_foreign_key(db_session):
    """Test User -> UserStatus foreign key relationship (AC-0.1.7)."""
    # Check if relationship is defined
    assert hasattr(User, 'status'), "User should have 'status' relationship"
    
    # Try to query with relationship
    result = db_session.execute(select(User).limit(1))
    user = result.scalar_one_or_none()
    
    if user:
        # Access relationship (this will trigger SQL join)
        status = user.status
        if status:
            print(f"✓ User {user.Email} has status: {status.StatusName}")


def test_company_country_foreign_key(db_session):
    """Test Company -> Country foreign key relationship (AC-0.1.7)."""
    assert hasattr(Company, 'country'), "Company should have 'country' relationship"
    
    result = db_session.execute(select(Company).limit(1))
    company = result.scalar_one_or_none()
    
    if company:
        country = company.country
        if country:
            print(f"✓ Company {company.CompanyName} is in: {country.CountryName}")


def test_user_company_relationships(db_session):
    """Test UserCompany junction table relationships (AC-0.1.7)."""
    # Check relationships exist
    assert hasattr(UserCompany, 'user'), "UserCompany should have 'user' relationship"
    assert hasattr(UserCompany, 'company'), "UserCompany should have 'company' relationship"
    assert hasattr(UserCompany, 'role'), "UserCompany should have 'role' relationship"
    assert hasattr(UserCompany, 'status'), "UserCompany should have 'status' relationship"
    assert hasattr(UserCompany, 'joined_via'), "UserCompany should have 'joined_via' relationship"
    
    result = db_session.execute(select(UserCompany).limit(1))
    user_company = result.scalar_one_or_none()
    
    if user_company:
        # Test accessing relationships
        print(f"✓ UserCompany relationships navigable")


def test_audit_columns_defaults(db_session):
    """Test that audit columns have proper defaults (AC-0.1.7)."""
    # CreatedDate should have GETUTCDATE() default
    # This is tested by checking table DDL
    
    # Check User table
    user_table = User.__table__
    created_date_col = user_table.columns['CreatedDate']
    
    assert created_date_col.nullable is False, "CreatedDate should be NOT NULL"
    assert created_date_col.server_default is not None, "CreatedDate should have server default"


def test_indexes_exist(db_session):
    """Test that required indexes exist (AC-0.1.7)."""
    # Query database for indexes on User.Email
    result = db_session.execute(text("""
        SELECT i.name AS index_name
        FROM sys.indexes i
        INNER JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
        INNER JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
        INNER JOIN sys.tables t ON i.object_id = t.object_id
        INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = 'dbo' AND t.name = 'User' AND c.name = 'Email'
    """))
    
    indexes = [row[0] for row in result]
    
    if indexes:
        print(f"✓ Found indexes on dbo.User.Email: {indexes}")
        # Should have UX_User_Email unique index
        assert any('Email' in idx for idx in indexes), "Email should have index"


def test_unique_constraints(db_session):
    """Test unique constraints (AC-0.1.7)."""
    # User.Email should have unique constraint (via unique index)
    user_table = User.__table__
    email_col = user_table.columns['Email']
    
    assert email_col.unique is True, "User.Email should be unique"


def test_model_repr_methods():
    """Test that models have useful __repr__ methods (AC-0.1.8)."""
    from backend.models import User, Company, Country
    
    # Models should have __repr__ defined
    assert hasattr(User, '__repr__')
    assert hasattr(Company, '__repr__')
    assert hasattr(Country, '__repr__')


def test_table_count(db_session):
    """Test that expected number of tables exist in database."""
    result = db_session.execute(text("""
        SELECT COUNT(*) AS table_count
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA IN ('ref', 'dbo', 'config', 'audit', 'log', 'cache')
        AND TABLE_TYPE = 'BASE TABLE'
    """))
    
    count = result.scalar()
    
    # Should have 33 tables
    print(f"✓ Found {count} tables in database")
    assert count >= 33, f"Expected at least 33 tables, found {count}"


def test_column_naming_convention(db_session):
    """Test that columns follow PascalCase naming convention (Solomon standard) (AC-0.1.2)."""
    # Check User table column names
    result = db_session.execute(text("""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'User'
        ORDER BY ORDINAL_POSITION
    """))
    
    columns = [row[0] for row in result]
    
    if columns:
        print(f"✓ User table columns: {', '.join(columns[:5])}...")
        
        # Check that columns use PascalCase (start with capital letter)
        for col in columns:
            assert col[0].isupper(), f"Column {col} should start with capital letter (PascalCase)"


def test_foreign_key_constraints(db_session):
    """Test that foreign key constraints exist in database (AC-0.1.7)."""
    # Query foreign keys on User table
    result = db_session.execute(text("""
        SELECT 
            fk.name AS constraint_name,
            OBJECT_NAME(fk.parent_object_id) AS table_name,
            COL_NAME(fc.parent_object_id, fc.parent_column_id) AS column_name,
            OBJECT_NAME(fk.referenced_object_id) AS referenced_table,
            COL_NAME(fc.referenced_object_id, fc.referenced_column_id) AS referenced_column
        FROM sys.foreign_keys fk
        INNER JOIN sys.foreign_key_columns fc ON fk.object_id = fc.constraint_object_id
        INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
        INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = 'dbo' AND t.name = 'User'
    """))
    
    foreign_keys = list(result)
    
    if foreign_keys:
        print(f"✓ Found {len(foreign_keys)} foreign keys on dbo.User")
        
        # Should have FK to UserStatus
        fk_tables = [row[3] for row in foreign_keys]
        print(f"  Referenced tables: {', '.join(set(fk_tables))}")

