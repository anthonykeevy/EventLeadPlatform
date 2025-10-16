"""
Database Connection and Session Management
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator
import logging

logger = logging.getLogger(__name__)

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mssql+pyodbc://localhost/EventLeadPlatform?driver=ODBC+Driver+18+for+SQL+Server&Trusted_Connection=Yes&TrustServerCertificate=yes"
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Test connections before using them
    pool_recycle=3600,  # Recycle connections after 1 hour
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that provides a database session.
    Used with FastAPI's Depends() for automatic session management.
    
    Usage:
        @router.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            # Use db session here
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection() -> bool:
    """
    Test database connection
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        from sqlalchemy import text
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False

