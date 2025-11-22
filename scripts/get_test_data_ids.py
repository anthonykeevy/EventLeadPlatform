"""
Script to get IDs for Test 11.1 setup
Retrieves: EventID, CompanyIDs, UserIDs for test4@test.com, test3@test.com, test2@test.com
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy import text
from common.database import engine

def get_test_data():
    """Query database for test user, company, and event IDs"""
    with engine.connect() as conn:
        print("=" * 100)
        print("TEST DATA IDS FOR TEST 11.1")
        print("=" * 100)
        
        # Get users
        result = conn.execute(text("""
            SELECT 
                UserID,
                Email,
                FirstName,
                LastName,
                CreatedDate
            FROM dbo.[User]
            WHERE Email IN ('test4@test.com', 'test2@test.com', 'test3@test.com') 
              AND IsDeleted = 0
            ORDER BY Email
        """))
        users = {}
        for row in result:
            email = row[1].lower()
            users[email] = {
                'UserID': row[0],
                'Email': row[1],
                'FirstName': row[2],
                'LastName': row[3],
                'CreatedDate': row[4]
            }
        
        print("\nUSERS:")
        print("-" * 100)
        for email, user in users.items():
            print(f"  {user['Email']}: UserID = {user['UserID']}, Name = {user['FirstName']} {user['LastName']}")
        
        # Get companies for these users
        result = conn.execute(text("""
            SELECT 
                u.Email,
                c.CompanyID,
                c.CompanyName,
                ucr.RoleCode,
                uc.IsPrimaryCompany,
                uc.JoinedDate
            FROM dbo.[User] u
            INNER JOIN dbo.UserCompany uc ON u.UserID = uc.UserID
            INNER JOIN dbo.Company c ON uc.CompanyID = c.CompanyID
            INNER JOIN ref.UserCompanyRole ucr ON uc.UserCompanyRoleID = ucr.UserCompanyRoleID
            INNER JOIN ref.UserCompanyStatus ucs ON uc.StatusID = ucs.UserCompanyStatusID
            WHERE u.Email IN ('test4@test.com', 'test2@test.com', 'test3@test.com')
              AND uc.IsDeleted = 0
              AND c.IsDeleted = 0
              AND ucs.StatusCode = 'active'
            ORDER BY u.Email, c.CompanyName
        """))
        user_companies = {}
        for row in result:
            email = row[0].lower()
            if email not in user_companies:
                user_companies[email] = []
            user_companies[email].append({
                'CompanyID': row[1],
                'CompanyName': row[2],
                'RoleCode': row[3],
                'IsPrimaryCompany': row[4],
                'JoinedDate': row[5]
            })
        
        print("\nCOMPANIES:")
        print("-" * 100)
        for email, companies in user_companies.items():
            print(f"\n  {email}:")
            for company in companies:
                primary = " (Primary)" if company['IsPrimaryCompany'] else ""
                print(f"    CompanyID = {company['CompanyID']}, Name = {company['CompanyName']}, Role = {company['RoleCode']}{primary}")
        
        # Get event "Australian Marketeers Expo"
        result = conn.execute(text("""
            SELECT 
                EventID,
                EventName,
                CompanyID,
                EventStartDate,
                EventEndDate,
                CreatedBy,
                CreatedDate
            FROM dbo.Event
            WHERE EventName LIKE '%Australian Marketeers Expo%'
              AND IsDeleted = 0
            ORDER BY CreatedDate DESC
        """))
        events = []
        for row in result:
            events.append({
                'EventID': row[0],
                'EventName': row[1],
                'CompanyID': row[2],
                'EventStartDate': row[3],
                'EventEndDate': row[4],
                'CreatedBy': row[5],
                'CreatedDate': row[6]
            })
        
        print("\nEVENTS:")
        print("-" * 100)
        for event in events:
            print(f"  EventID = {event['EventID']}, Name = {event['EventName']}, CompanyID = {event['CompanyID']}, CreatedDate = {event['CreatedDate']}")
        
        # Get forms for the event
        if events:
            event_id = events[0]['EventID']
            result = conn.execute(text("""
                SELECT 
                    FormID,
                    FormName,
                    EventID,
                    CompanyID,
                    CreatedBy,
                    CreatedDate
                FROM dbo.Form
                WHERE EventID = :event_id
                  AND IsDeleted = 0
                ORDER BY CreatedDate
            """), {'event_id': event_id})
            forms = []
            for row in result:
                forms.append({
                    'FormID': row[0],
                    'FormName': row[1],
                    'EventID': row[2],
                    'CompanyID': row[3],
                    'CreatedBy': row[4],
                    'CreatedDate': row[5]
                })
            
            print(f"\nFORMS FOR EVENT {event_id} (Australian Marketeers Expo):")
            print("-" * 100)
            for form in forms:
                print(f"  FormID = {form['FormID']}, Name = {form['FormName']}, CompanyID = {form['CompanyID']}, CreatedDate = {form['CreatedDate']}")
        
        # Generate SQL script values
        print("\n" + "=" * 100)
        print("SQL SCRIPT VALUES:")
        print("=" * 100)
        
        test4_email = 'test4@test.com'
        test4_email_lower = test4_email.lower()
        # Find test4 email in user_companies (case-insensitive)
        test4_key = None
        for email in user_companies.keys():
            if email.lower() == test4_email_lower:
                test4_key = email
                break
        
        test3_email = 'test3@test.com'
        test3_email_lower = test3_email.lower()
        # Find test3 email in user_companies (case-insensitive)
        test3_key = None
        for email in user_companies.keys():
            if email.lower() == test3_email_lower:
                test3_key = email
                break
        
        if events and test4_key and test3_key:
            event_id = events[0]['EventID']
            host_company_id = events[0]['CompanyID']
            test4_user_id = users[test4_key]['UserID']
            
            # Get test4's company (should be the host company)
            host_company = None
            for company in user_companies[test4_key]:
                if company['CompanyID'] == host_company_id:
                    host_company = company
                    break
            
            # Get test3's company (agency company)
            agency_company = None
            if user_companies[test3_key]:
                # Use primary company if available, otherwise first company
                for company in user_companies[test3_key]:
                    if company['IsPrimaryCompany']:
                        agency_company = company
                        break
                if not agency_company:
                    agency_company = user_companies[test3_key][0]
            
            if event_id and host_company_id and agency_company and test4_key:
                print(f"\nDECLARE @EventID BIGINT = {event_id};             -- {events[0]['EventName']}")
                print(f"DECLARE @AgencyCompanyID BIGINT = {agency_company['CompanyID']};   -- {agency_company['CompanyName']} (Test3's company)")
                print(f"DECLARE @HostCompanyID BIGINT = {host_company_id};     -- Host Company (Test4's company)")
                print(f"DECLARE @CreatedByUserID BIGINT = {test4_user_id};    -- {test4_key} (host company admin)")
                print("\n" + "=" * 100)
        else:
            print("\nERROR: Could not find all required data:")
            if not events:
                print("  - Event 'Australian Marketeers Expo' not found")
            if not test4_key:
                print("  - User test4@test.com not found")
            if not test3_key:
                print("  - User test3@test.com not found")

if __name__ == '__main__':
    get_test_data()
