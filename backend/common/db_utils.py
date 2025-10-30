"""
Database Utility Functions
Common database operations and helpers
"""
import logging
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
from .database_service import get_database_service, get_session_context
from .db_config import get_query_template, get_health_check_query

logger = logging.getLogger(__name__)

class DatabaseUtils:
    """Utility class for common database operations"""
    
    def __init__(self):
        self.db_service = get_database_service()
    
    def health_check(self) -> Dict[str, Any]:
        """Comprehensive database health check"""
        try:
            # Basic connection test
            basic_result = self.db_service.execute_scalar(get_health_check_query('basic'))
            
            # Get database info
            version = self.db_service.execute_scalar(get_health_check_query('version'))
            db_name = self.db_service.execute_scalar(get_health_check_query('database_name'))
            user_name = self.db_service.execute_scalar(get_health_check_query('user_name'))
            connection_count = self.db_service.execute_scalar(get_health_check_query('connection_count'))
            
            return {
                "status": "healthy",
                "basic_test": basic_result,
                "database_name": db_name,
                "user_name": user_name,
                "connection_count": connection_count,
                "version": version[:100] + "..." if len(version) > 100 else version,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def get_app_setting(self, setting_key: str, default_value: Any = None) -> Any:
        """Get application setting from config.AppSetting"""
        try:
            query = get_query_template('get_setting')
            result = self.db_service.execute_scalar(query, (setting_key,))
            return result if result is not None else default_value
        except Exception as e:
            logger.error(f"Failed to get setting {setting_key}: {e}")
            return default_value
    
    def get_recent_logs(self, table: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent logs from specified table"""
        try:
            query = get_query_template('get_recent_logs').format(
                limit=limit, 
                table=table
            )
            return self.db_service.execute_query(query)
        except Exception as e:
            logger.error(f"Failed to get recent logs from {table}: {e}")
            return []
    
    def get_logs_by_request_id(self, request_id: str) -> List[Dict[str, Any]]:
        """Get all logs for a specific request ID"""
        try:
            query = get_query_template('get_logs_by_request_id')
            return self.db_service.execute_query(query, (request_id,))
        except Exception as e:
            logger.error(f"Failed to get logs for request {request_id}: {e}")
            return []
    
    def get_user_logs(self, user_id: int, hours: int = 24) -> List[Dict[str, Any]]:
        """Get logs for a specific user within time range"""
        try:
            query = get_query_template('get_user_logs').format(hours=hours)
            return self.db_service.execute_query(query, (user_id,))
        except Exception as e:
            logger.error(f"Failed to get logs for user {user_id}: {e}")
            return []
    
    def get_payload_logs(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get logs with payload data"""
        try:
            query = """
                SELECT TOP 50
                    ApiRequestID,
                    Method,
                    Path,
                    StatusCode,
                    DurationMs,
                    RequestPayload,
                    ResponsePayload,
                    Headers,
                    CreatedDate
                FROM log.ApiRequest 
                WHERE CreatedDate >= DATEADD(hour, -?, GETUTCDATE())
                AND (RequestPayload IS NOT NULL OR ResponsePayload IS NOT NULL)
                ORDER BY CreatedDate DESC
            """
            return self.db_service.execute_query(query, (hours,))
        except Exception as e:
            logger.error(f"Failed to get payload logs: {e}")
            return []
    
    def get_performance_metrics(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance metrics from API logs"""
        try:
            query = """
                SELECT 
                    COUNT(*) as total_requests,
                    AVG(CAST(DurationMs AS FLOAT)) as avg_duration_ms,
                    MAX(DurationMs) as max_duration_ms,
                    MIN(DurationMs) as min_duration_ms,
                    COUNT(CASE WHEN StatusCode >= 400 THEN 1 END) as error_count
                FROM log.ApiRequest 
                WHERE CreatedDate >= DATEADD(hour, -?, GETUTCDATE())
            """
            result = self.db_service.execute_query(query, (hours,))
            
            if result:
                return result[0]
            else:
                return {
                    "total_requests": 0,
                    "avg_duration_ms": 0,
                    "max_duration_ms": 0,
                    "min_duration_ms": 0,
                    "error_count": 0
                }
        except Exception as e:
            logger.error(f"Failed to get performance metrics: {e}")
            return {}
    
    def get_correlation_analysis(self, request_id: str) -> Dict[str, Any]:
        """Get correlation analysis for a specific request"""
        try:
            # Get API request
            api_query = """
                SELECT * FROM log.ApiRequest 
                WHERE RequestID = ?
            """
            api_logs = self.db_service.execute_query(api_query, (request_id,))
            
            # Get auth events
            auth_query = """
                SELECT * FROM log.AuthEvent 
                WHERE RequestID = ?
            """
            auth_logs = self.db_service.execute_query(auth_query, (request_id,))
            
            # Get application errors
            error_query = """
                SELECT * FROM log.ApplicationError 
                WHERE RequestID = ?
            """
            error_logs = self.db_service.execute_query(error_query, (request_id,))
            
            return {
                "request_id": request_id,
                "api_requests": api_logs,
                "auth_events": auth_logs,
                "application_errors": error_logs,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get correlation analysis for {request_id}: {e}")
            return {}


# Global instance for easy access
db_utils = DatabaseUtils()

# Convenience functions
def health_check() -> Dict[str, Any]:
    """Check database health"""
    return db_utils.health_check()

def get_app_setting(setting_key: str, default_value: Any = None) -> Any:
    """Get application setting"""
    return db_utils.get_app_setting(setting_key, default_value)

def get_recent_logs(table: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent logs"""
    return db_utils.get_recent_logs(table, limit)

def get_payload_logs(hours: int = 24) -> List[Dict[str, Any]]:
    """Get logs with payload data"""
    return db_utils.get_payload_logs(hours)

def get_performance_metrics(hours: int = 24) -> Dict[str, Any]:
    """Get performance metrics"""
    return db_utils.get_performance_metrics(hours)
