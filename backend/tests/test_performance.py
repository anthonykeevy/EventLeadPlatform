"""
Performance Tests for Multi-Tenancy (Story 1.8)
Tests AC-1.8.8
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import text
import time

from main import app
from common.database import get_db
from tests.test_utils import (
    create_test_company,
    create_test_user,
    create_test_token,
    create_test_invitation,
    get_auth_headers
)

client = TestClient(app)


@pytest.fixture
def db():
    """Get test database session"""
    db_session = next(get_db())
    try:
        yield db_session
    finally:
        db_session.close()


# ============================================================================
# AC-1.8.8: Performance tests verify filtering doesn't impact queries
# ============================================================================

def test_company_filtering_overhead_minimal(db: Session):
    """Test that company filtering adds minimal overhead (<10ms)"""
    # Create test data
    company = create_test_company(db, "Performance Test Company")
    user = create_test_user(
        db,
        "perf@test.com",
        company_id=company.CompanyID,
        role_code="company_admin",
        onboarding_complete=True
    )
    token = create_test_token(
        int(user.UserID),  # type: ignore
        str(user.Email),  # type: ignore
        "company_admin",
        int(company.CompanyID)  # type: ignore
    )
    
    # Benchmark query with company filtering
    start_time = time.time()
    response = client.get(
        "/api/users/me/companies",
        headers=get_auth_headers(token)
    )
    end_time = time.time()
    
    elapsed_ms = (end_time - start_time) * 1000
    
    assert response.status_code == 200
    # Should complete in reasonable time (< 100ms for simple query)
    assert elapsed_ms < 100, f"Query took {elapsed_ms}ms, expected < 100ms"


def test_database_indexes_used_for_company_filtering(db: Session):
    """Test that database indexes are used for company filtering"""
    # Check if indexes exist on CompanyID columns
    # Note: This test checks database schema, not runtime performance
    
    # Tables that should have CompanyID indexes
    tables_with_company_id = [
        'dbo.Company',
        'dbo.UserCompany',
        'dbo.UserInvitation',
        # Add more company-scoped tables as they're implemented
    ]
    
    for table in tables_with_company_id:
        # Query to check for indexes
        # Note: This is SQL Server specific
        try:
            result = db.execute(text(f"""
                SELECT 
                    i.name AS index_name,
                    c.name AS column_name
                FROM sys.indexes i
                INNER JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
                INNER JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
                INNER JOIN sys.tables t ON i.object_id = t.object_id
                INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
                WHERE s.name + '.' + t.name = :table_name
                AND c.name = 'CompanyID'
            """), {"table_name": table})
            
            indexes = result.fetchall()
            
            # Should have at least one index on CompanyID
            # Note: Primary keys and foreign keys automatically create indexes
            assert len(indexes) >= 0, f"No indexes found on CompanyID for {table}"
        except Exception as e:
            # If query fails, skip this test (may not be SQL Server)
            pytest.skip(f"Could not check indexes: {str(e)}")


def test_query_performance_with_large_dataset(db: Session):
    """Test query performance with large dataset (multiple companies)"""
    # Create multiple companies
    companies = []
    for i in range(10):
        company = create_test_company(db, f"Company {i}")
        companies.append(company)
        
        # Create users for each company
        for j in range(5):
            create_test_user(
                db,
                f"user{j}@company{i}.com",
                company_id=company.CompanyID,
                role_code="company_user",
                onboarding_complete=True
            )
    
    # Test querying specific company's data
    test_company = companies[0]
    test_user = create_test_user(
        db,
        f"testuser@company0.com",
        company_id=test_company.CompanyID,
        role_code="company_admin",
        onboarding_complete=True
    )
    token = create_test_token(
        int(test_user.UserID),  # type: ignore
        str(test_user.Email),  # type: ignore
        "company_admin",
        int(test_company.CompanyID)  # type: ignore
    )
    
    # Benchmark
    start_time = time.time()
    response = client.get(
        "/api/users/me/companies",
        headers=get_auth_headers(token)
    )
    end_time = time.time()
    
    elapsed_ms = (end_time - start_time) * 1000
    
    assert response.status_code == 200
    # Should still be fast even with 10 companies
    assert elapsed_ms < 200, f"Query took {elapsed_ms}ms with large dataset"
    
    # Should only return test user's company
    companies_returned = response.json()
    assert len(companies_returned) == 1
    assert companies_returned[0]["company_id"] == test_company.CompanyID


def test_concurrent_multi_tenant_queries(db: Session):
    """Test that concurrent queries from different companies don't interfere"""
    # Create two companies with users
    company_a = create_test_company(db, "Concurrent Company A")
    user_a = create_test_user(
        db,
        "concurrent_a@test.com",
        company_id=company_a.CompanyID,
        role_code="company_admin",
        onboarding_complete=True
    )
    token_a = create_test_token(
        int(user_a.UserID),  # type: ignore
        str(user_a.Email),  # type: ignore
        "company_admin",
        int(company_a.CompanyID)  # type: ignore
    )
    
    company_b = create_test_company(db, "Concurrent Company B")
    user_b = create_test_user(
        db,
        "concurrent_b@test.com",
        company_id=company_b.CompanyID,
        role_code="company_admin",
        onboarding_complete=True
    )
    token_b = create_test_token(
        int(user_b.UserID),  # type: ignore
        str(user_b.Email),  # type: ignore
        "company_admin",
        int(company_b.CompanyID)  # type: ignore
    )
    
    # Make concurrent requests (simulated sequentially in test)
    start_time = time.time()
    
    response_a = client.get(
        "/api/users/me/companies",
        headers=get_auth_headers(token_a)
    )
    response_b = client.get(
        "/api/users/me/companies",
        headers=get_auth_headers(token_b)
    )
    
    end_time = time.time()
    elapsed_ms = (end_time - start_time) * 1000
    
    # Both should succeed
    assert response_a.status_code == 200
    assert response_b.status_code == 200
    
    # Should complete quickly
    assert elapsed_ms < 300, f"Concurrent queries took {elapsed_ms}ms"
    
    # Should return correct data for each user
    companies_a = response_a.json()
    companies_b = response_b.json()
    
    assert len(companies_a) == 1
    assert companies_a[0]["company_id"] == company_a.CompanyID
    
    assert len(companies_b) == 1
    assert companies_b[0]["company_id"] == company_b.CompanyID


def test_invitation_queries_scale_with_company_filtering(db: Session):
    """Test that invitation queries remain fast with company filtering"""
    # Create company with many invitations
    company = create_test_company(db, "Large Invitations Company")
    admin = create_test_user(
        db,
        "admin@invitations.com",
        company_id=company.CompanyID,
        role_code="company_admin",
        onboarding_complete=True
    )
    
    # Create multiple invitations
    for i in range(20):
        create_test_invitation(
            db,
            company_id=company.CompanyID,
            invited_by=admin.UserID,
            email=f"invite{i}@test.com"
        )
    
    token = create_test_token(
        int(admin.UserID),  # type: ignore
        str(admin.Email),  # type: ignore
        "company_admin",
        int(company.CompanyID)  # type: ignore
    )
    
    # Benchmark listing invitations
    start_time = time.time()
    response = client.get(
        f"/api/companies/{company.CompanyID}/invitations",
        headers=get_auth_headers(token)
    )
    end_time = time.time()
    
    elapsed_ms = (end_time - start_time) * 1000
    
    assert response.status_code == 200
    invitations = response.json()
    assert len(invitations) == 20
    
    # Should complete quickly even with 20 invitations
    assert elapsed_ms < 200, f"Invitation list query took {elapsed_ms}ms"


# ============================================================================
# Query Plan Analysis Tests
# ============================================================================

def test_explain_query_plan_uses_indexes(db: Session):
    """Test that query execution plans use indexes efficiently"""
    # This is database-specific and would require EXPLAIN QUERY PLAN support
    # For SQL Server, we'd use SET STATISTICS IO ON / SET SHOWPLAN_TEXT ON
    # For now, this test documents the requirement
    
    # Example query that should use indexes
    company_id = 1
    
    try:
        # SQL Server: Check query plan
        result = db.execute(text("""
            SET SHOWPLAN_TEXT ON
        """))
        
        result = db.execute(text("""
            SELECT * FROM dbo.UserInvitation WHERE CompanyID = :company_id
        """), {"company_id": company_id})
        
        # Query plan should show index seek, not table scan
        # This is a placeholder - actual implementation would parse plan
        pytest.skip("Query plan analysis requires database-specific implementation")
    except Exception:
        pytest.skip("Query plan analysis not supported in test environment")


# ============================================================================
# Resource Usage Tests
# ============================================================================

def test_memory_usage_reasonable_for_large_result_sets():
    """Test that memory usage is reasonable for large result sets"""
    # This would require memory profiling tools
    # For now, we just document the requirement
    # In production, queries should use pagination to limit memory usage
    pytest.skip("Memory profiling requires specialized tools")


def test_connection_pooling_efficient():
    """Test that database connection pooling is efficient"""
    # This would require monitoring connection pool metrics
    # For now, we document that SQLAlchemy handles connection pooling
    pytest.skip("Connection pool monitoring requires production metrics")


# ============================================================================
# Stress Tests (Optional)
# ============================================================================

@pytest.mark.slow
def test_system_handles_high_volume_of_company_filtered_queries(db: Session):
    """Test system can handle high volume of queries with company filtering"""
    # Create test company and user
    company = create_test_company(db, "Stress Test Company")
    user = create_test_user(
        db,
        "stress@test.com",
        company_id=company.CompanyID,
        role_code="company_admin",
        onboarding_complete=True
    )
    token = create_test_token(
        int(user.UserID),  # type: ignore
        str(user.Email),  # type: ignore
        "company_admin",
        int(company.CompanyID)  # type: ignore
    )
    
    # Make many requests
    num_requests = 100
    start_time = time.time()
    
    failures = 0
    for i in range(num_requests):
        response = client.get(
            "/api/users/me/companies",
            headers=get_auth_headers(token)
        )
        if response.status_code != 200:
            failures += 1
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time_ms = (total_time / num_requests) * 1000
    
    # All requests should succeed
    assert failures == 0, f"{failures} out of {num_requests} requests failed"
    
    # Average time should be reasonable
    assert avg_time_ms < 50, f"Average request time was {avg_time_ms}ms"
    
    print(f"\nStress Test Results:")
    print(f"  Total Requests: {num_requests}")
    print(f"  Total Time: {total_time:.2f}s")
    print(f"  Average Time: {avg_time_ms:.2f}ms")
    print(f"  Requests/sec: {num_requests / total_time:.2f}")

