#!/usr/bin/env python3
"""
Debug script to test middleware configuration
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from common.config_service import ConfigurationService

def test_config():
    """Test configuration loading"""
    print("Testing Configuration Service...")
    
    config_service = ConfigurationService()
    
    # Test logging configuration
    capture_payloads = config_service.get_logging_capture_payloads()
    max_payload_size = config_service.get_logging_max_payload_size_kb()
    excluded_endpoints = config_service.get_logging_excluded_endpoints()
    
    print(f"Capture Payloads: {capture_payloads}")
    print(f"Max Payload Size: {max_payload_size} KB")
    print(f"Excluded Endpoints: {excluded_endpoints}")
    
    # Test database connection
    try:
        from common.database import get_db
        with next(get_db()) as db:
            result = db.execute("SELECT 1 as test").fetchone()
            print(f"Database connection: OK - {result}")
    except Exception as e:
        print(f"Database connection: FAILED - {e}")

if __name__ == "__main__":
    test_config()
