#!/usr/bin/env python3
"""
Check payload capture directly from database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from common.database import SessionLocal
from models.log.api_request import ApiRequest
from sqlalchemy import text

def check_payload_direct():
    """Check payload capture directly from database"""
    db = SessionLocal()
    try:
        # Get the most recent API request
        recent_request = db.query(ApiRequest).order_by(ApiRequest.CreatedDate.desc()).first()
        
        if not recent_request:
            print("No API requests found in database")
            return
        
        print("Most Recent API Request - Direct Database Check")
        print("=" * 60)
        print(f"RequestID: {recent_request.RequestID}")
        print(f"Method: {recent_request.Method}")
        print(f"Path: {recent_request.Path}")
        print(f"Status: {recent_request.StatusCode}")
        print(f"Duration: {recent_request.DurationMs}ms")
        print()
        
        print("Payload Fields:")
        print(f"  RequestPayload: {'✅ CAPTURED' if recent_request.RequestPayload else '❌ NULL'}")
        print(f"  ResponsePayload: {'✅ CAPTURED' if recent_request.ResponsePayload else '❌ NULL'}")
        print(f"  Headers: {'✅ CAPTURED' if recent_request.Headers else '❌ NULL'}")
        print()
        
        if recent_request.RequestPayload:
            print("Request Payload Preview:")
            print("-" * 40)
            print(recent_request.RequestPayload[:500] + "..." if len(recent_request.RequestPayload) > 500 else recent_request.RequestPayload)
            print("-" * 40)
        
        if recent_request.ResponsePayload:
            print("Response Payload Preview:")
            print("-" * 40)
            print(recent_request.ResponsePayload[:500] + "..." if len(recent_request.ResponsePayload) > 500 else recent_request.ResponsePayload)
            print("-" * 40)
        
        if recent_request.Headers:
            print("Headers Preview:")
            print("-" * 40)
            print(recent_request.Headers[:500] + "..." if len(recent_request.Headers) > 500 else recent_request.Headers)
            print("-" * 40)
        
        # Check configuration
        print("\nConfiguration Check:")
        print("-" * 40)
        config_result = db.execute(text("""
            SELECT SettingKey, SettingValue 
            FROM config.AppSetting 
            WHERE SettingKey LIKE 'logging.%'
        """)).fetchall()
        
        for row in config_result:
            print(f"  {row.SettingKey}: {row.SettingValue}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_payload_direct()
