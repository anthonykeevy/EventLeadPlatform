"""
Logging Utilities
Structured logging configuration with RequestID inclusion
"""
import logging
import sys
from typing import Optional

from common.request_context import get_current_request_context


class RequestIDFilter(logging.Filter):
    """
    Logging filter that adds RequestID to all log records.
    
    If no request context exists, uses "no-request" as placeholder.
    """
    
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Add request_id to log record.
        
        Args:
            record: Log record to modify
            
        Returns:
            True (always allow record through)
        """
        context = get_current_request_context()
        record.request_id = context.request_id if context else "no-request"
        return True


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with RequestID included in all messages.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if not logger.handlers:
        # Set log level (can be configured via env var)
        logger.setLevel(logging.INFO)
        
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        
        # Format: [timestamp] [level] [request_id] [name] message
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(request_id)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        
        # Add RequestID filter
        handler.addFilter(RequestIDFilter())
        
        logger.addHandler(handler)
        
        # Prevent propagation to root logger (avoid duplicate logs)
        logger.propagate = False
    
    return logger


def configure_logging(log_level: str = "INFO") -> None:
    """
    Configure application-wide logging settings.
    
    Call this once at application startup (in main.py).
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Set root logger level
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Reduce noise from third-party libraries
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)

