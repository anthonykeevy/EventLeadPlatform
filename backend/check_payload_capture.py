#!/usr/bin/env python3
"""
Check if payload capture is working in the enhanced logger
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from common.database import SessionLocal
from models.log.api_request import ApiRequest
from sqlalchemy import text

def check_payload_capture():
    """Check if payloads are being captured"""
    db = SessionLocal()
    try:
        # Get the most recent API requests
        recent_requests = db.query(ApiRequest).order_by(ApiRequest.CreatedDate.desc()).limit(3).all()
        
        print("Recent API Requests - Payload Capture Check")
        print("=" * 60)
        
        for req in recent_requests:
            print(f"\nRequest: {req.Method} {req.Path}")
            print(f"  RequestID: {req.RequestID}")
            print(f"  Status: {req.StatusCode}")
            print(f"  Duration: {req.DurationMs}ms")
            print(f"  RequestPayload: {'✅ CAPTURED' if req.RequestPayload else '❌ NULL'}")
            print(f"  ResponsePayload: {'✅ CAPTURED' if req.ResponsePayload else '❌ NULL'}")
            print(f"  Headers: {'✅ CAPTURED' if req.Headers else '❌ NULL'}")
            
            if req.RequestPayload:
                print(f"  RequestPayload Preview: {req.RequestPayload[:100]}...")
            if req.ResponsePayload:
                print(f"  ResponsePayload Preview: {req.ResponsePayload[:100]}...")
            if req.Headers:
                print(f"  Headers Preview: {req.Headers[:100]}...")
        
        # Check configuration
        print("\n" + "=" * 60)
        print("Configuration Check")
        
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
    check_payload_capture()
