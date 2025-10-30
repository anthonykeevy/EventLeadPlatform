"""
Centralized Database Service
Single source of truth for all database connections across the application
"""
import pyodbc
import logging
from typing import Optional, Dict, Any
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

logger = logging.getLogger(__name__)

class DatabaseService:
    """
    Centralized database service providing consistent connection management
    across application, test scripts, and BMAD agents.
    """
    
    _instance: Optional['DatabaseService'] = None
    _engine = None
    _session_factory = None
    _connection_string = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._connection_string = self._build_connection_string()
            self._engine = self._create_engine()
            self._session_factory = sessionmaker(bind=self._engine)
            self._initialized = True
    
    def _build_connection_string(self) -> str:
        """Build standardized connection string"""
        return (
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=localhost;"
            "Database=EventLeadPlatform;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
    
    def _create_engine(self):
        """Create SQLAlchemy engine with optimized settings"""
        # Convert ODBC connection string to SQLAlchemy format
        sqlalchemy_url = f"mssql+pyodbc:///?odbc_connect={self._connection_string}"
        
        return create_engine(
            sqlalchemy_url,
            poolclass=StaticPool,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False
        )
    
    @property
    def connection_string(self) -> str:
        """Get the standardized connection string"""
        return self._connection_string
    
    @property
    def engine(self):
        """Get SQLAlchemy engine"""
        return self._engine
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return self._session_factory()
    
    @contextmanager
    def get_session_context(self):
        """Context manager for database sessions with automatic cleanup"""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def get_pyodbc_connection(self):
        """Get raw pyodbc connection for direct SQL queries"""
        try:
            return pyodbc.connect(self._connection_string)
        except Exception as e:
            logger.error(f"Failed to create pyodbc connection: {e}")
            raise
    
    @contextmanager
    def get_pyodbc_context(self):
        """Context manager for pyodbc connections"""
        conn = None
        try:
            conn = self.get_pyodbc_connection()
            yield conn
        except Exception as e:
            logger.error(f"Pyodbc connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def test_connection(self) -> Dict[str, Any]:
        """Test database connection and return status"""
        try:
            with self.get_pyodbc_context() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT @@VERSION")
                version = cursor.fetchone()[0]
                
                return {
                    "status": "connected",
                    "database": "EventLeadPlatform",
                    "version": version[:100] + "..." if len(version) > 100 else version,
                    "connection_string": self._connection_string
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "connection_string": self._connection_string
            }
    
    def execute_query(self, query: str, params: tuple = None) -> list:
        """Execute a query and return results"""
        try:
            with self.get_pyodbc_context() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # Get column names
                columns = [column[0] for column in cursor.description] if cursor.description else []
                
                # Get all rows
                rows = cursor.fetchall()
                
                # Convert to list of dictionaries
                return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            raise
    
    def execute_scalar(self, query: str, params: tuple = None) -> Any:
        """Execute a query and return single value"""
        try:
            with self.get_pyodbc_context() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            logger.error(f"Scalar query execution error: {e}")
            raise


# Global instance for easy access
db_service = DatabaseService()

# Convenience functions for backward compatibility
def get_database_service() -> DatabaseService:
    """Get the global database service instance"""
    return db_service

def get_session() -> Session:
    """Get a new database session"""
    return db_service.get_session()

@contextmanager
def get_session_context():
    """Context manager for database sessions"""
    with db_service.get_session_context() as session:
        yield session

def test_database_connection() -> Dict[str, Any]:
    """Test database connection"""
    return db_service.test_connection()

def execute_query(query: str, params: tuple = None) -> list:
    """Execute a query and return results"""
    return db_service.execute_query(query, params)

def execute_scalar(query: str, params: tuple = None) -> Any:
    """Execute a query and return single value"""
    return db_service.execute_scalar(query, params)
