#!/usr/bin/env python3
"""
Test Centralized Database Service
Verify that all database operations work through the centralized service
"""
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from common.database_service import get_database_service, test_database_connection
from common.db_utils import health_check, get_payload_logs, get_performance_metrics
from common.agent_db_helpers import get_logging_config, get_system_health

def test_basic_connection():
    """Test basic database connection"""
    print("=== Testing Basic Database Connection ===")
    
    try:
        # Test connection
        result = test_database_connection()
        print(f"✅ Connection Status: {result['status']}")
        print(f"✅ Database: {result.get('database', 'Unknown')}")
        print(f"✅ Version: {result.get('version', 'Unknown')[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return False

def test_health_check():
    """Test comprehensive health check"""
    print("\n=== Testing Health Check ===")
    
    try:
        health = health_check()
        print(f"✅ Health Status: {health['status']}")
        print(f"✅ Database Name: {health.get('database_name', 'Unknown')}")
        print(f"✅ User Name: {health.get('user_name', 'Unknown')}")
        print(f"✅ Connection Count: {health.get('connection_count', 0)}")
        return True
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return False

def test_logging_configuration():
    """Test logging configuration retrieval"""
    print("\n=== Testing Logging Configuration ===")
    
    try:
        config = get_logging_config()
        print(f"✅ Capture Payloads: {config['capture_payloads']}")
        print(f"✅ Max Payload Size: {config['max_payload_size_kb']} KB")
        print(f"✅ Excluded Endpoints: {config['excluded_endpoints']}")
        return True
    except Exception as e:
        print(f"❌ Logging Config Failed: {e}")
        return False

def test_system_health():
    """Test system health for agents"""
    print("\n=== Testing System Health ===")
    
    try:
        health = get_system_health()
        print(f"✅ Database Status: {health['database_status']}")
        print(f"✅ Recent Requests: {health.get('recent_requests', 0)}")
        print(f"✅ Avg Response Time: {health.get('avg_response_time', 0):.2f}ms")
        print(f"✅ Error Count (1h): {health.get('error_count_1h', 0)}")
        return True
    except Exception as e:
        print(f"❌ System Health Failed: {e}")
        return False

def test_payload_logs():
    """Test payload logs retrieval"""
    print("\n=== Testing Payload Logs ===")
    
    try:
        payload_logs = get_payload_logs(hours=24)
        print(f"✅ Payload Logs Found: {len(payload_logs)}")
        
        if payload_logs:
            print("Sample payload log:")
            sample = payload_logs[0]
            print(f"  Method: {sample.get('Method', 'N/A')}")
            print(f"  Path: {sample.get('Path', 'N/A')}")
            print(f"  Has Request Payload: {'Yes' if sample.get('RequestPayload') else 'No'}")
            print(f"  Has Response Payload: {'Yes' if sample.get('ResponsePayload') else 'No'}")
        return True
    except Exception as e:
        print(f"❌ Payload Logs Failed: {e}")
        return False

def test_performance_metrics():
    """Test performance metrics"""
    print("\n=== Testing Performance Metrics ===")
    
    try:
        metrics = get_performance_metrics(hours=24)
        print(f"✅ Total Requests: {metrics.get('total_requests', 0)}")
        print(f"✅ Average Duration: {metrics.get('avg_duration_ms', 0):.2f}ms")
        print(f"✅ Max Duration: {metrics.get('max_duration_ms', 0)}ms")
        print(f"✅ Error Count: {metrics.get('error_count', 0)}")
        return True
    except Exception as e:
        print(f"❌ Performance Metrics Failed: {e}")
        return False

def test_direct_queries():
    """Test direct database queries"""
    print("\n=== Testing Direct Queries ===")
    
    try:
        db_service = get_database_service()
        
        # Test simple query
        result = db_service.execute_scalar("SELECT 1")
        print(f"✅ Simple Query Result: {result}")
        
        # Test table existence
        tables = db_service.execute_query("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'log'
            ORDER BY TABLE_NAME
        """)
        print(f"✅ Log Tables Found: {len(tables)}")
        for table in tables:
            print(f"  - {table['TABLE_NAME']}")
        
        return True
    except Exception as e:
        print(f"❌ Direct Queries Failed: {e}")
        return False

def main():
    """Run all tests"""
    print("CENTRALIZED DATABASE SERVICE TEST")
    print("=" * 50)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Basic Connection", test_basic_connection),
        ("Health Check", test_health_check),
        ("Logging Configuration", test_logging_configuration),
        ("System Health", test_system_health),
        ("Payload Logs", test_payload_logs),
        ("Performance Metrics", test_performance_metrics),
        ("Direct Queries", test_direct_queries),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} Exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Centralized database service is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
