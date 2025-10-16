"""
Test Database Connection (AC-0.1.3)
Validates database connection and session management
"""
import pytest
from sqlalchemy import text
from backend.common.database import engine, SessionLocal, get_db, test_connection, Base


def test_engine_configuration():
    """Test that SQLAlchemy engine is configured correctly."""
    assert engine is not None
    assert engine.pool is not None
    
    # Verify pool settings
    assert hasattr(engine.pool, '_pre_ping') or hasattr(engine, 'pool_pre_ping')
    
    # Verify connection string
    assert 'EventLeadPlatform' in str(engine.url)


def test_database_connection():
    """Test that database connection works."""
    result = test_connection()
    assert result is True, "Database connection should succeed"


def test_session_creation():
    """Test that SessionLocal creates valid sessions."""
    session = SessionLocal()
    assert session is not None
    
    # Test simple query
    result = session.execute(text("SELECT 1 AS test"))
    assert result.fetchone()[0] == 1
    
    session.close()


def test_get_db_dependency():
    """Test get_db dependency function for FastAPI."""
    # Get database session from dependency
    db_gen = get_db()
    db = next(db_gen)
    
    assert db is not None
    
    # Test simple query
    result = db.execute(text("SELECT 1 AS test"))
    assert result.fetchone()[0] == 1
    
    # Close session
    try:
        next(db_gen)
    except StopIteration:
        pass  # Expected - generator should be exhausted


def test_session_cleanup():
    """Test that sessions are properly closed after use."""
    db_gen = get_db()
    db = next(db_gen)
    
    # Session should be open
    assert db.is_active
    
    # Trigger cleanup
    try:
        next(db_gen)
    except StopIteration:
        pass
    
    # Session should be closed
    assert not db.is_active


def test_base_metadata():
    """Test that SQLAlchemy Base has metadata."""
    assert Base is not None
    assert Base.metadata is not None
    
    # After importing models, metadata should have tables
    import backend.models  # noqa: F401
    assert len(Base.metadata.tables) > 0


def test_transaction_rollback():
    """Test that failed transactions rollback properly."""
    session = SessionLocal()
    
    try:
        # Start a transaction
        session.begin()
        
        # Execute valid query
        session.execute(text("SELECT 1"))
        
        # Force an error (invalid SQL)
        session.execute(text("INVALID SQL QUERY"))
        
        # Should not reach here
        assert False, "Should have raised exception"
        
    except Exception:
        # Rollback should work
        session.rollback()
        
        # Session should still be usable
        result = session.execute(text("SELECT 1"))
        assert result.fetchone()[0] == 1
        
    finally:
        session.close()


def test_connection_pooling():
    """Test that connection pooling is working."""
    # Create multiple sessions
    sessions = []
    for _ in range(5):
        session = SessionLocal()
        sessions.append(session)
    
    # All sessions should be valid
    for session in sessions:
        result = session.execute(text("SELECT 1"))
        assert result.fetchone()[0] == 1
    
    # Close all sessions
    for session in sessions:
        session.close()


def test_database_exists():
    """Test that EventLeadPlatform database exists."""
    session = SessionLocal()
    
    try:
        result = session.execute(text("SELECT DB_NAME() AS current_db"))
        db_name = result.fetchone()[0]
        assert db_name == 'EventLeadPlatform', f"Wrong database: {db_name}"
    finally:
        session.close()


def test_schemas_exist():
    """Test that all required schemas exist in database."""
    session = SessionLocal()
    
    try:
        result = session.execute(text("""
            SELECT SCHEMA_NAME
            FROM INFORMATION_SCHEMA.SCHEMATA
            WHERE SCHEMA_NAME IN ('ref', 'config', 'audit', 'log', 'cache')
        """))
        
        schemas = [row[0] for row in result]
        expected_schemas = {'ref', 'config', 'audit', 'log', 'cache'}
        actual_schemas = set(schemas)
        
        assert expected_schemas.issubset(actual_schemas), f"Missing schemas. Expected {expected_schemas}, got {actual_schemas}"
    finally:
        session.close()

