"""
Agent Database Helpers
Specialized database functions for BMAD agents
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from .database_service import get_database_service
from .db_utils import get_app_setting, get_performance_metrics

logger = logging.getLogger(__name__)

class AgentDatabaseHelpers:
    """Database helper functions specifically for BMAD agents"""
    
    def __init__(self):
        self.db_service = get_database_service()
    
    def get_logging_configuration(self) -> Dict[str, Any]:
        """Get current logging configuration for agents"""
        try:
            return {
                "capture_payloads": get_app_setting("logging.capture_payloads", True),
                "max_payload_size_kb": get_app_setting("logging.max_payload_size_kb", 10),
                "excluded_endpoints": get_app_setting("logging.excluded_endpoints", ["/api/health"]),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get logging configuration: {e}")
            return {
                "capture_payloads": True,
                "max_payload_size_kb": 10,
                "excluded_endpoints": ["/api/health"],
                "error": str(e)
            }
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health for agents"""
        try:
            # Basic health check
            health = self.db_service.test_connection()
            
            # Performance metrics
            metrics = get_performance_metrics(hours=1)
            
            # Recent error count
            error_query = """
                SELECT COUNT(*) as error_count
                FROM log.ApplicationError 
                WHERE CreatedDate >= DATEADD(hour, -1, GETUTCDATE())
            """
            error_count = self.db_service.execute_scalar(error_query)
            
            return {
                "database_status": health.get("status", "unknown"),
                "database_name": health.get("database", "unknown"),
                "recent_requests": metrics.get("total_requests", 0),
                "avg_response_time": metrics.get("avg_duration_ms", 0),
                "error_count_1h": error_count or 0,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get system health: {e}")
            return {
                "database_status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def get_recent_user_activity(self, user_id: int, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent activity for a specific user"""
        try:
            query = """
                SELECT 
                    Method, Path, StatusCode, DurationMs, 
                    RequestPayload, ResponsePayload, CreatedDate
                FROM log.ApiRequest 
                WHERE UserID = ? 
                AND CreatedDate >= DATEADD(hour, -?, GETUTCDATE())
                ORDER BY CreatedDate DESC
            """
            return self.db_service.execute_query(query, (user_id, hours))
        except Exception as e:
            logger.error(f"Failed to get user activity for user {user_id}: {e}")
            return []
    
    def get_epic_progress_logs(self, epic_name: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Get logs related to specific epic development"""
        try:
            query = """
                SELECT 
                    Method, Path, StatusCode, DurationMs,
                    RequestPayload, ResponsePayload, CreatedDate
                FROM log.ApiRequest 
                WHERE (
                    Path LIKE ? OR 
                    RequestPayload LIKE ? OR 
                    ResponsePayload LIKE ?
                )
                AND CreatedDate >= DATEADD(hour, -?, GETUTCDATE())
                ORDER BY CreatedDate DESC
            """
            search_term = f"%{epic_name}%"
            return self.db_service.execute_query(query, (search_term, search_term, search_term, hours))
        except Exception as e:
            logger.error(f"Failed to get epic progress logs for {epic_name}: {e}")
            return []
    
    def get_performance_issues(self, threshold_ms: int = 1000) -> List[Dict[str, Any]]:
        """Get API requests that exceeded performance threshold"""
        try:
            query = """
                SELECT 
                    Method, Path, StatusCode, DurationMs,
                    UserID, RequestID, CreatedDate
                FROM log.ApiRequest 
                WHERE DurationMs > ?
                AND CreatedDate >= DATEADD(hour, -24, GETUTCDATE())
                ORDER BY DurationMs DESC
            """
            return self.db_service.execute_query(query, (threshold_ms,))
        except Exception as e:
            logger.error(f"Failed to get performance issues: {e}")
            return []
    
    def get_error_patterns(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get error patterns for analysis"""
        try:
            query = """
                SELECT 
                    ErrorType, 
                    COUNT(*) as error_count,
                    MAX(CreatedDate) as last_occurrence
                FROM log.ApplicationError 
                WHERE CreatedDate >= DATEADD(hour, -?, GETUTCDATE())
                GROUP BY ErrorType
                ORDER BY error_count DESC
            """
            return self.db_service.execute_query(query, (hours,))
        except Exception as e:
            logger.error(f"Failed to get error patterns: {e}")
            return []
    
    def validate_story_completion(self, story_name: str) -> Dict[str, Any]:
        """Validate if a story has been completed based on logs"""
        try:
            # Look for story-related API calls
            query = """
                SELECT 
                    COUNT(*) as api_calls,
                    COUNT(CASE WHEN StatusCode >= 400 THEN 1 END) as error_calls,
                    AVG(CAST(DurationMs AS FLOAT)) as avg_duration
                FROM log.ApiRequest 
                WHERE (
                    Path LIKE ? OR 
                    RequestPayload LIKE ? OR 
                    ResponsePayload LIKE ?
                )
                AND CreatedDate >= DATEADD(hour, -24, GETUTCDATE())
            """
            search_term = f"%{story_name}%"
            result = self.db_service.execute_query(query, (search_term, search_term, search_term))
            
            if result:
                data = result[0]
                return {
                    "story_name": story_name,
                    "api_calls": data.get("api_calls", 0),
                    "error_calls": data.get("error_calls", 0),
                    "avg_duration": data.get("avg_duration", 0),
                    "completion_status": "completed" if data.get("api_calls", 0) > 0 else "not_started",
                    "error_rate": (data.get("error_calls", 0) / max(data.get("api_calls", 1), 1)) * 100,
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "story_name": story_name,
                    "completion_status": "not_started",
                    "timestamp": datetime.utcnow().isoformat()
                }
        except Exception as e:
            logger.error(f"Failed to validate story completion for {story_name}: {e}")
            return {
                "story_name": story_name,
                "completion_status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

# Global instance for easy access
agent_db = AgentDatabaseHelpers()

# Convenience functions for agents
def get_logging_config() -> Dict[str, Any]:
    """Get logging configuration for agents"""
    return agent_db.get_logging_configuration()

def get_system_health() -> Dict[str, Any]:
    """Get system health for agents"""
    return agent_db.get_system_health()

def get_user_activity(user_id: int, hours: int = 24) -> List[Dict[str, Any]]:
    """Get user activity for agents"""
    return agent_db.get_recent_user_activity(user_id, hours)

def validate_story(story_name: str) -> Dict[str, Any]:
    """Validate story completion for agents"""
    return agent_db.validate_story_completion(story_name)
