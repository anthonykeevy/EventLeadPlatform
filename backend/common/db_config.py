"""
Database Configuration Constants
Centralized configuration for all database connections
"""
from typing import Dict, Any

# Database Configuration
DATABASE_CONFIG = {
    'driver': 'ODBC Driver 18 for SQL Server',
    'server': 'localhost',
    'database': 'EventLeadPlatform',
    'trusted_connection': 'yes',
    'trust_server_certificate': 'yes',
    'timeout': 30,
    'pool_size': 5,
    'max_overflow': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}

# Connection String Templates
ODBC_CONNECTION_STRING = (
    "Driver={driver};"
    "Server={server};"
    "Database={database};"
    "Trusted_Connection={trusted_connection};"
    "TrustServerCertificate={trust_server_certificate};"
    "Timeout={timeout};"
)

SQLALCHEMY_URL_TEMPLATE = (
    "mssql+pyodbc:///?odbc_connect={odbc_connect}"
)

# Test Database Configuration (for testing)
TEST_DATABASE_CONFIG = {
    **DATABASE_CONFIG,
    'database': 'EventLeadPlatform_Test',  # Optional test database
}

# Connection Health Check Queries
HEALTH_CHECK_QUERIES = {
    'basic': "SELECT 1",
    'version': "SELECT @@VERSION",
    'database_name': "SELECT DB_NAME()",
    'user_name': "SELECT USER_NAME()",
    'connection_count': "SELECT COUNT(*) FROM sys.dm_exec_sessions WHERE database_id = DB_ID()"
}

# Common Query Templates
QUERY_TEMPLATES = {
    'get_setting': """
        SELECT SettingValue 
        FROM config.AppSetting 
        WHERE SettingKey = ? AND IsActive = 1
    """,
    'get_recent_logs': """
        SELECT TOP {limit} * 
        FROM {table} 
        ORDER BY CreatedDate DESC
    """,
    'get_logs_by_request_id': """
        SELECT * 
        FROM log.ApiRequest 
        WHERE RequestID = ?
        ORDER BY CreatedDate
    """,
    'get_user_logs': """
        SELECT * 
        FROM log.ApiRequest 
        WHERE UserID = ? 
        AND CreatedDate >= DATEADD(hour, -{hours}, GETUTCDATE())
        ORDER BY CreatedDate DESC
    """
}

def get_connection_string(config: Dict[str, Any] = None) -> str:
    """Generate connection string from configuration"""
    if config is None:
        config = DATABASE_CONFIG
    
    return ODBC_CONNECTION_STRING.format(**config)

def get_sqlalchemy_url(config: Dict[str, Any] = None) -> str:
    """Generate SQLAlchemy URL from configuration"""
    if config is None:
        config = DATABASE_CONFIG
    
    odbc_string = get_connection_string(config)
    return SQLALCHEMY_URL_TEMPLATE.format(odbc_connect=odbc_string)

def get_test_connection_string() -> str:
    """Get connection string for test database"""
    return get_connection_string(TEST_DATABASE_CONFIG)

def get_health_check_query(check_type: str = 'basic') -> str:
    """Get health check query by type"""
    return HEALTH_CHECK_QUERIES.get(check_type, HEALTH_CHECK_QUERIES['basic'])

def get_query_template(template_name: str) -> str:
    """Get query template by name"""
    return QUERY_TEMPLATES.get(template_name, "")
