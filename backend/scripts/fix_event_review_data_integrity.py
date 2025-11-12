"""
Fix Event Review Data Integrity Issues

This script fixes inconsistent records in the Event table related to the public review workflow.
It should be run after migrations 020-023 have been executed.

Issues Fixed:
1. Events with IsPublicReviewRequired=True and EventStatusID=ARCHIVED
2. Events with IsPublic=True but PublicReviewStatusID=NULL
3. Invalid state combinations (private events with review status, etc.)
4. Rejected events with IsSharedWithPlatform=True

Usage:
    python backend/scripts/fix_event_review_data_integrity.py [--dry-run] [--verbose]
"""

import sys
import os
from pathlib import Path

# Add project root and backend to path
project_root = Path(__file__).parent.parent.parent
backend_path = project_root / "backend"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_path))

# Set up environment so models can import from common.database
os.chdir(str(backend_path))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging

# Simple logger for script
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load database URL from environment or use project's database module
def get_database_url():
    """Get database URL from environment or project configuration"""
    # First, try environment variable
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        logger.info("Using DATABASE_URL from environment variable")
        return env_url
    
    # Try to use project's database configuration
    try:
        from common.database import DATABASE_URL as project_db_url
        logger.info("Using DATABASE_URL from project's database module")
        return project_db_url
    except Exception as e:
        logger.warning(f"Could not load from project database module: {e}")
    
    # Fallback: Try to detect available ODBC driver
    try:
        import pyodbc
        available_drivers = [driver for driver in pyodbc.drivers()]
        logger.info(f"Available ODBC drivers: {', '.join(available_drivers)}")
        
        # Try Driver 18 first, then 17, then any SQL Server driver
        driver = None
        for driver_name in ["ODBC Driver 18 for SQL Server", "ODBC Driver 17 for SQL Server"]:
            if driver_name in available_drivers:
                driver = driver_name
                break
        
        # If no numbered driver, look for any SQL Server driver
        if not driver:
            sql_server_drivers = [d for d in available_drivers if "SQL Server" in d]
            if sql_server_drivers:
                driver = sql_server_drivers[0]
                logger.info(f"Using first available SQL Server driver: {driver}")
        
        if not driver:
            raise Exception(
                f"No SQL Server ODBC driver found. Available drivers: {', '.join(available_drivers) if available_drivers else 'None'}.\n"
                f"Please install 'ODBC Driver 17 for SQL Server' or 'ODBC Driver 18 for SQL Server' from Microsoft."
            )
        
        # Construct connection string
        server = os.getenv("DB_SERVER", "localhost")
        database = os.getenv("DB_NAME", "EventLeadPlatform")
        use_trusted = os.getenv("DB_TRUSTED_CONNECTION", "Yes")
        
        # URL encode driver name (spaces become +)
        driver_encoded = driver.replace(" ", "+")
        
        if driver == "ODBC Driver 18 for SQL Server":
            db_url = f"mssql+pyodbc://{server}/{database}?driver={driver_encoded}&Trusted_Connection={use_trusted}&TrustServerCertificate=yes"
        else:
            db_url = f"mssql+pyodbc://{server}/{database}?driver={driver_encoded}&Trusted_Connection={use_trusted}"
        
        logger.info(f"Constructed database URL using driver: {driver}")
        return db_url
        
    except ImportError:
        raise Exception("pyodbc is not installed. Please install it with: pip install pyodbc")

# Get database URL
try:
    DATABASE_URL = get_database_url()
    # Log connection info (hide sensitive parts)
    log_url = DATABASE_URL
    if "@" in log_url:
        log_url = log_url.split("@")[0] + "@..."
    logger.info(f"Database connection configured: {log_url}")
except Exception as e:
    logger.error(f"Database configuration error: {str(e)}")
    logger.error("\nTroubleshooting:")
    logger.error("1. Set DATABASE_URL environment variable, or")
    logger.error("2. Install ODBC Driver 17 or 18 for SQL Server from Microsoft")
    logger.error("3. Ensure SQL Server is running and accessible")
    sys.exit(1)

# Create SQLAlchemy engine
try:
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    sys.exit(1)


def fix_archived_events_with_review_required(db, dry_run: bool = False) -> int:
    """
    Fix Issue 1: Events with IsPublicReviewRequired=True and EventStatusID=ARCHIVED
    
    Actions:
    - Set IsPublicReviewRequired = False
    - Clear PublicReviewStatusID = NULL if PENDING
    - Set IsSharedWithPlatform = False
    """
    logger.info("--- Fixing Issue 1: Archived events with review required ---")
    
    # Get ARCHIVED EventStatusID
    result = db.execute(text("""
        SELECT EventStatusID 
        FROM [ref].[EventStatus] 
        WHERE StatusCode = 'ARCHIVED' AND IsDeleted = 0
    """))
    archived_status_id = result.scalar_one_or_none()
    
    if not archived_status_id:
        logger.warning("ARCHIVED event status not found in database")
        return 0
    
    # Get PENDING PublicReviewStatusID
    result = db.execute(text("""
        SELECT PublicReviewStatusID 
        FROM [ref].[PublicReviewStatus] 
        WHERE StatusCode = 'PENDING' AND IsDeleted = 0
    """))
    pending_review_status_id = result.scalar_one_or_none()
    
    if not pending_review_status_id:
        logger.warning("PENDING public review status not found in database")
        return 0
    
    # Find events with IsPublicReviewRequired=True and EventStatusID=ARCHIVED
    result = db.execute(text("""
        SELECT EventID, Name, IsPublicReviewRequired, PublicReviewStatusID
        FROM [dbo].[Event]
        WHERE IsPublicReviewRequired = 1
            AND EventStatusID = :archived_status_id
            AND IsDeleted = 0
    """), {"archived_status_id": archived_status_id})
    
    events = result.fetchall()
    
    if not events:
        logger.info("No archived events with review required found")
        return 0
    
    logger.info(f"Found {len(events)} archived events with review required")
    
    for event in events:
        logger.info(
            f"  EventID={event.EventID}, Name='{event.Name}', "
            f"IsPublicReviewRequired={event.IsPublicReviewRequired}, "
            f"PublicReviewStatusID={event.PublicReviewStatusID}"
        )
    
    if not dry_run:
        # Update all matching events
        db.execute(text("""
            UPDATE [dbo].[Event]
            SET IsPublicReviewRequired = 0,
                IsSharedWithPlatform = 0,
                PublicReviewStatusID = CASE 
                    WHEN PublicReviewStatusID = :pending_status_id THEN NULL 
                    ELSE PublicReviewStatusID 
                END,
                UpdatedDate = GETUTCDATE()
            WHERE IsPublicReviewRequired = 1
                AND EventStatusID = :archived_status_id
                AND IsDeleted = 0
        """), {
            "pending_status_id": pending_review_status_id,
            "archived_status_id": archived_status_id
        })
        db.commit()
        logger.info(f"Fixed {len(events)} archived events")
    
    return len(events)


def fix_public_events_without_review_status(db, dry_run: bool = False) -> int:
    """
    Fix Issue 2: Events with IsPublic=True but PublicReviewStatusID=NULL
    
    Actions:
    - If IsSharedWithPlatform=True → Set PublicReviewStatusID=PENDING
    - If IsSharedWithPlatform=False → Set IsPublicReviewRequired=False
    """
    logger.info("\n--- Fixing Issue 2: Public events without review status ---")
    
    # Get PENDING PublicReviewStatusID
    result = db.execute(text("""
        SELECT PublicReviewStatusID 
        FROM [ref].[PublicReviewStatus] 
        WHERE StatusCode = 'PENDING' AND IsDeleted = 0
    """))
    pending_review_status_id = result.scalar_one_or_none()
    
    if not pending_review_status_id:
        logger.warning("PENDING public review status not found in database")
        return 0
    
    # Find events with IsPublic=True but PublicReviewStatusID=NULL
    result = db.execute(text("""
        SELECT EventID, Name, IsPublic, IsSharedWithPlatform, PublicReviewStatusID
        FROM [dbo].[Event]
        WHERE IsPublic = 1
            AND PublicReviewStatusID IS NULL
            AND IsDeleted = 0
    """))
    
    events = result.fetchall()
    
    if not events:
        logger.info("No public events without review status found")
        return 0
    
    logger.info(f"Found {len(events)} public events without review status")
    
    fixed_count = 0
    for event in events:
        logger.info(
            f"  EventID={event.EventID}, Name='{event.Name}', "
            f"IsSharedWithPlatform={event.IsSharedWithPlatform}"
        )
        
        if not dry_run:
            if event.IsSharedWithPlatform:
                # Platform-sharing event needs review
                db.execute(text("""
                    UPDATE [dbo].[Event]
                    SET PublicReviewStatusID = :pending_status_id,
                        IsPublicReviewRequired = 1,
                        UpdatedDate = GETUTCDATE()
                    WHERE EventID = :event_id
                """), {
                    "pending_status_id": pending_review_status_id,
                    "event_id": event.EventID
                })
                logger.info(f"    → Set PublicReviewStatusID=PENDING for platform-sharing event")
            else:
                # Company network only - no review needed
                db.execute(text("""
                    UPDATE [dbo].[Event]
                    SET IsPublicReviewRequired = 0,
                        UpdatedDate = GETUTCDATE()
                    WHERE EventID = :event_id
                """), {"event_id": event.EventID})
                logger.info(f"    → Set IsPublicReviewRequired=False for company network only event")
            
            fixed_count += 1
    
    if not dry_run:
        db.commit()
        logger.info(f"Fixed {fixed_count} public events without review status")
    
    return fixed_count if not dry_run else len(events)


def fix_invalid_state_combinations(db, dry_run: bool = False) -> int:
    """
    Fix Issue 3: Invalid state combinations
    
    Invalid combinations:
    - Private events (IsPublic=False) with PublicReviewStatusID set
    - Private events (IsPublic=False) with IsSharedWithPlatform=True
    - Events with IsPublic=False but IsPublicReviewRequired=True
    """
    logger.info("\n--- Fixing Issue 3: Invalid state combinations ---")
    
    # Get all review status IDs
    result = db.execute(text("""
        SELECT PublicReviewStatusID 
        FROM [ref].[PublicReviewStatus] 
        WHERE IsDeleted = 0
    """))
    review_status_ids = [row[0] for row in result.fetchall()]
    
    if not review_status_ids:
        logger.warning("No public review statuses found in database")
        return 0
    
    # Find invalid combinations
    # Case 1: Private events with PublicReviewStatusID set
    result1 = db.execute(text("""
        SELECT EventID, Name, IsPublic, PublicReviewStatusID, IsSharedWithPlatform, IsPublicReviewRequired
        FROM [dbo].[Event]
        WHERE IsPublic = 0
            AND PublicReviewStatusID IS NOT NULL
            AND IsDeleted = 0
    """))
    
    # Case 2: Private events with IsSharedWithPlatform=True
    result2 = db.execute(text("""
        SELECT EventID, Name, IsPublic, PublicReviewStatusID, IsSharedWithPlatform, IsPublicReviewRequired
        FROM [dbo].[Event]
        WHERE IsPublic = 0
            AND IsSharedWithPlatform = 1
            AND IsDeleted = 0
    """))
    
    # Case 3: Private events with IsPublicReviewRequired=True
    result3 = db.execute(text("""
        SELECT EventID, Name, IsPublic, PublicReviewStatusID, IsSharedWithPlatform, IsPublicReviewRequired
        FROM [dbo].[Event]
        WHERE IsPublic = 0
            AND IsPublicReviewRequired = 1
            AND IsDeleted = 0
    """))
    
    events1 = result1.fetchall()
    events2 = result2.fetchall()
    events3 = result3.fetchall()
    
    # Combine and deduplicate by EventID
    all_events_dict = {}
    for event in events1 + events2 + events3:
        all_events_dict[event.EventID] = event
    
    all_events = list(all_events_dict.values())
    
    if not all_events:
        logger.info("No invalid state combinations found")
        return 0
    
    logger.info(f"Found {len(all_events)} events with invalid state combinations")
    
    for event in all_events:
        logger.info(
            f"  EventID={event.EventID}, Name='{event.Name}', IsPublic={event.IsPublic}, "
            f"PublicReviewStatusID={event.PublicReviewStatusID}, "
            f"IsSharedWithPlatform={event.IsSharedWithPlatform}, "
            f"IsPublicReviewRequired={event.IsPublicReviewRequired}"
        )
    
    if not dry_run:
        # Clear all review-related fields for private events
        db.execute(text("""
            UPDATE [dbo].[Event]
            SET PublicReviewStatusID = NULL,
                IsSharedWithPlatform = 0,
                IsPublicReviewRequired = 0,
                UpdatedDate = GETUTCDATE()
            WHERE IsPublic = 0
                AND (
                    PublicReviewStatusID IS NOT NULL
                    OR IsSharedWithPlatform = 1
                    OR IsPublicReviewRequired = 1
                )
                AND IsDeleted = 0
        """))
        db.commit()
        logger.info(f"Fixed {len(all_events)} events with invalid state combinations")
    
    return len(all_events)


def fix_rejected_events_with_platform_sharing(db, dry_run: bool = False) -> int:
    """
    Fix Issue 4: Rejected events with IsSharedWithPlatform=True
    
    Rejected events should have IsSharedWithPlatform=False (they cannot be platform-shared)
    """
    logger.info("\n--- Fixing Issue 4: Rejected events with platform sharing ---")
    
    # Get REJECTED PublicReviewStatusID
    result = db.execute(text("""
        SELECT PublicReviewStatusID 
        FROM [ref].[PublicReviewStatus] 
        WHERE StatusCode = 'REJECTED' AND IsDeleted = 0
    """))
    rejected_status_id = result.scalar_one_or_none()
    
    if not rejected_status_id:
        logger.warning("REJECTED public review status not found in database")
        return 0
    
    # Find rejected events with IsSharedWithPlatform=True
    result = db.execute(text("""
        SELECT EventID, Name, PublicReviewStatusID, IsSharedWithPlatform
        FROM [dbo].[Event]
        WHERE PublicReviewStatusID = :rejected_status_id
            AND IsSharedWithPlatform = 1
            AND IsDeleted = 0
    """), {"rejected_status_id": rejected_status_id})
    
    events = result.fetchall()
    
    if not events:
        logger.info("No rejected events with platform sharing found")
        return 0
    
    logger.info(f"Found {len(events)} rejected events with platform sharing")
    
    for event in events:
        logger.info(
            f"  EventID={event.EventID}, Name='{event.Name}'"
        )
    
    if not dry_run:
        db.execute(text("""
            UPDATE [dbo].[Event]
            SET IsSharedWithPlatform = 0,
                UpdatedDate = GETUTCDATE()
            WHERE PublicReviewStatusID = :rejected_status_id
                AND IsSharedWithPlatform = 1
                AND IsDeleted = 0
        """), {"rejected_status_id": rejected_status_id})
        db.commit()
        logger.info(f"Fixed {len(events)} rejected events with platform sharing")
    
    return len(events)


def main():
    """Main function to run all data integrity fixes"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Fix Event Review Data Integrity Issues"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run in dry-run mode (show what would be fixed without making changes)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("=" * 80)
    logger.info("Event Review Data Integrity Fix Script")
    logger.info("=" * 80)
    
    if args.dry_run:
        logger.info("RUNNING IN DRY-RUN MODE - No changes will be made")
        logger.info("=" * 80)
    
    try:
        # Get database session
        db = SessionLocal()
        
        total_fixed = 0
        
        # Fix Issue 1: Archived events with review required
        count1 = fix_archived_events_with_review_required(db, dry_run=args.dry_run)
        total_fixed += count1
        
        # Fix Issue 2: Public events without review status
        count2 = fix_public_events_without_review_status(db, dry_run=args.dry_run)
        total_fixed += count2
        
        # Fix Issue 3: Invalid state combinations
        count3 = fix_invalid_state_combinations(db, dry_run=args.dry_run)
        total_fixed += count3
        
        # Fix Issue 4: Rejected events with platform sharing
        count4 = fix_rejected_events_with_platform_sharing(db, dry_run=args.dry_run)
        total_fixed += count4
        
        logger.info("\n" + "=" * 80)
        if args.dry_run:
            logger.info(f"[DRY RUN] Total events that would be fixed: {total_fixed}")
        else:
            logger.info(f"Total events fixed: {total_fixed}")
        logger.info("=" * 80)
        
        db.close()
        
        if total_fixed > 0 and not args.dry_run:
            logger.info("\n✅ Data integrity fixes completed successfully!")
        elif total_fixed > 0 and args.dry_run:
            logger.info("\n✅ Dry-run completed. Run without --dry-run to apply fixes.")
        else:
            logger.info("\n✅ No data integrity issues found!")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error running data integrity fix script: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
