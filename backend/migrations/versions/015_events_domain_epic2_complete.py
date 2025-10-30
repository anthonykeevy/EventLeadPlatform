"""Events Domain Epic 2 - Complete Event Management System

Revision ID: 015_events_domain_epic2_complete
Revises: 014_company_epic2
Create Date: 2025-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '015_events_domain_epic2_complete'
down_revision = '014_company_epic2'
branch_labels = None
depends_on = None


def upgrade():
    """Create Events domain tables for Epic 2 - Complete Event Management System"""
    
    # Create EventType reference table
    op.create_table('EventType',
        sa.Column('EventTypeID', sa.Integer(), nullable=False),
        sa.Column('TypeCode', mssql.NVARCHAR(length=20), nullable=False),
        sa.Column('TypeName', mssql.NVARCHAR(length=50), nullable=False),
        sa.Column('TypeDescription', mssql.NVARCHAR(length=200), nullable=True),
        sa.Column('IsActive', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('SortOrder', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], name='FK_EventType_CreatedBy'),
        sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.User.UserID'], name='FK_EventType_UpdatedBy'),
        sa.ForeignKeyConstraint(['DeletedBy'], ['dbo.User.UserID'], name='FK_EventType_DeletedBy'),
        sa.PrimaryKeyConstraint('EventTypeID', name='PK_EventType'),
        sa.UniqueConstraint('TypeCode', name='UQ_EventType_TypeCode'),
        schema='ref'
    )
    
    # Create EventStatus reference table
    op.create_table('EventStatus',
        sa.Column('EventStatusID', sa.Integer(), nullable=False),
        sa.Column('StatusCode', mssql.NVARCHAR(length=20), nullable=False),
        sa.Column('StatusName', mssql.NVARCHAR(length=50), nullable=False),
        sa.Column('StatusDescription', mssql.NVARCHAR(length=200), nullable=True),
        sa.Column('StatusColor', mssql.NVARCHAR(length=7), nullable=True),
        sa.Column('StatusIcon', mssql.NVARCHAR(length=50), nullable=True),
        sa.Column('IsActive', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('SortOrder', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], name='FK_EventStatus_CreatedBy'),
        sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.User.UserID'], name='FK_EventStatus_UpdatedBy'),
        sa.ForeignKeyConstraint(['DeletedBy'], ['dbo.User.UserID'], name='FK_EventStatus_DeletedBy'),
        sa.PrimaryKeyConstraint('EventStatusID', name='PK_EventStatus'),
        sa.UniqueConstraint('StatusCode', name='UQ_EventStatus_StatusCode'),
        schema='ref'
    )
    
    # Create RecurrencePattern reference table
    op.create_table('RecurrencePattern',
        sa.Column('RecurrencePatternID', sa.Integer(), nullable=False),
        sa.Column('PatternCode', mssql.NVARCHAR(length=20), nullable=False),
        sa.Column('PatternName', mssql.NVARCHAR(length=50), nullable=False),
        sa.Column('PatternDescription', mssql.NVARCHAR(length=200), nullable=True),
        sa.Column('PatternFormula', mssql.NVARCHAR(length=100), nullable=True),
        sa.Column('IsActive', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('SortOrder', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], name='FK_RecurrencePattern_CreatedBy'),
        sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.User.UserID'], name='FK_RecurrencePattern_UpdatedBy'),
        sa.ForeignKeyConstraint(['DeletedBy'], ['dbo.User.UserID'], name='FK_RecurrencePattern_DeletedBy'),
        sa.PrimaryKeyConstraint('RecurrencePatternID', name='PK_RecurrencePattern'),
        sa.UniqueConstraint('PatternCode', name='UQ_RecurrencePattern_PatternCode'),
        schema='ref'
    )
    
    # Create main Event table (comprehensive version)
    op.create_table('Event',
        sa.Column('EventID', sa.BigInteger(), nullable=False),
        sa.Column('Name', mssql.NVARCHAR(length=200), nullable=False),
        sa.Column('Description', mssql.NVARCHAR(length='MAX'), nullable=True),
        sa.Column('ShortDescription', mssql.NVARCHAR(length=500), nullable=True),
        sa.Column('CompanyID', sa.BigInteger(), nullable=False),
        sa.Column('CreatedBy', sa.BigInteger(), nullable=False),
        sa.Column('StartDateTime', sa.DateTime(), nullable=False),
        sa.Column('EndDateTime', sa.DateTime(), nullable=True),
        sa.Column('TimezoneIdentifier', mssql.NVARCHAR(length=50), nullable=True),
        sa.Column('VenueName', mssql.NVARCHAR(length=200), nullable=True),
        sa.Column('VenueAddress', mssql.NVARCHAR(length=500), nullable=True),
        sa.Column('City', mssql.NVARCHAR(length=100), nullable=True),
        sa.Column('State', mssql.NVARCHAR(length=100), nullable=True),
        sa.Column('CountryID', sa.BigInteger(), nullable=True),
        sa.Column('Latitude', sa.Numeric(precision=10, scale=8), nullable=True),
        sa.Column('Longitude', sa.Numeric(precision=11, scale=8), nullable=True),
        sa.Column('EventTypeID', sa.Integer(), nullable=False),
        sa.Column('IndustryID', sa.BigInteger(), nullable=True),
        sa.Column('Tags', mssql.NVARCHAR(length='MAX'), nullable=True),
        sa.Column('IsPublic', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('EventStatusID', sa.Integer(), nullable=False),
        sa.Column('IsRecurring', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('RecurrencePatternID', sa.Integer(), nullable=True),
        sa.Column('IsPublicReviewRequired', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('PublicReviewStatus', mssql.NVARCHAR(length=20), nullable=True),
        sa.Column('PublicReviewDate', sa.DateTime(), nullable=True),
        sa.Column('PublicReviewBy', sa.BigInteger(), nullable=True),
        sa.Column('PublicReviewComments', mssql.NVARCHAR(length='MAX'), nullable=True),
        sa.Column('PublicVisibilityDate', sa.DateTime(), nullable=True),
        sa.Column('DuplicateEventID', sa.BigInteger(), nullable=True),
        sa.Column('IsDuplicate', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('OrganizerCompanyID', sa.BigInteger(), nullable=True),
        sa.Column('OrganizerContactEmail', mssql.NVARCHAR(length=100), nullable=True),
        sa.Column('OrganizerWebsite', mssql.NVARCHAR(length=200), nullable=True),
        sa.Column('ExpectedAttendees', sa.Integer(), nullable=True),
        sa.Column('ActualAttendees', sa.Integer(), nullable=True),
        sa.Column('FormsCreated', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('TotalSubmissions', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('CreatedDate', sa.DateTime(), nullable=False, server_default=sa.text('GETUTCDATE()')),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedBy', sa.BigInteger(), nullable=True),
        sa.Column('IsDeleted', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('DeletedDate', sa.DateTime(), nullable=True),
        sa.Column('DeletedBy', sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(['CompanyID'], ['dbo.Company.CompanyID'], name='FK_Event_Company'),
        sa.ForeignKeyConstraint(['CreatedBy'], ['dbo.User.UserID'], name='FK_Event_CreatedBy'),
        sa.ForeignKeyConstraint(['CountryID'], ['ref.Country.CountryID'], name='FK_Event_Country'),
        sa.ForeignKeyConstraint(['IndustryID'], ['ref.Industry.IndustryID'], name='FK_Event_Industry'),
        sa.ForeignKeyConstraint(['EventTypeID'], ['ref.EventType.EventTypeID'], name='FK_Event_EventType'),
        sa.ForeignKeyConstraint(['EventStatusID'], ['ref.EventStatus.EventStatusID'], name='FK_Event_EventStatus'),
        sa.ForeignKeyConstraint(['RecurrencePatternID'], ['ref.RecurrencePattern.RecurrencePatternID'], name='FK_Event_RecurrencePattern'),
        sa.ForeignKeyConstraint(['OrganizerCompanyID'], ['dbo.Company.CompanyID'], name='FK_Event_OrganizerCompany'),
        sa.ForeignKeyConstraint(['PublicReviewBy'], ['dbo.User.UserID'], name='FK_Event_PublicReviewBy'),
        sa.ForeignKeyConstraint(['DuplicateEventID'], ['dbo.Event.EventID'], name='FK_Event_DuplicateEvent'),
        sa.ForeignKeyConstraint(['UpdatedBy'], ['dbo.User.UserID'], name='FK_Event_UpdatedBy'),
        sa.ForeignKeyConstraint(['DeletedBy'], ['dbo.User.UserID'], name='FK_Event_DeletedBy'),
        sa.PrimaryKeyConstraint('EventID', name='PK_Event'),
        schema='dbo'
    )
    
    # Create check constraints for Event table
    op.create_check_constraint('CK_Event_PublicReviewStatus', 'Event', 
        "PublicReviewStatus IS NULL OR PublicReviewStatus IN ('PENDING', 'APPROVED', 'REJECTED')", 
        schema='dbo')
    op.create_check_constraint('CK_Event_DateTime', 'Event', 
        "EndDateTime IS NULL OR EndDateTime > StartDateTime", 
        schema='dbo')
    op.create_check_constraint('CK_Event_Latitude', 'Event', 
        "Latitude IS NULL OR (Latitude >= -90 AND Latitude <= 90)", 
        schema='dbo')
    op.create_check_constraint('CK_Event_Longitude', 'Event', 
        "Longitude IS NULL OR (Longitude >= -180 AND Longitude <= 180)", 
        schema='dbo')
    op.create_check_constraint('CK_Event_Attendees', 'Event', 
        "(ExpectedAttendees IS NULL OR ExpectedAttendees >= 0) AND (ActualAttendees IS NULL OR ActualAttendees >= 0)", 
        schema='dbo')
    
    # Create indexes for Event table
    op.create_index('IX_Event_Company', 'Event', ['CompanyID', 'IsDeleted'], schema='dbo')
    op.create_index('IX_Event_Status', 'Event', ['EventStatusID', 'IsDeleted'], schema='dbo')
    op.create_index('IX_Event_Type', 'Event', ['EventTypeID', 'IsDeleted'], schema='dbo')
    op.create_index('IX_Event_Industry', 'Event', ['IndustryID', 'IsDeleted'], schema='dbo')
    op.create_index('IX_Event_DateTime', 'Event', ['StartDateTime', 'EndDateTime', 'IsDeleted'], schema='dbo')
    op.create_index('IX_Event_Public', 'Event', ['IsPublic', 'EventStatusID', 'IsDeleted'], schema='dbo')
    op.create_index('IX_Event_Location', 'Event', ['City', 'State', 'CountryID', 'IsDeleted'], schema='dbo')
    op.create_index('IX_Event_PublicReview', 'Event', ['IsPublic', 'PublicReviewStatus', 'IsDeleted'], schema='dbo')
    op.create_index('IX_Event_Duplicate', 'Event', ['DuplicateEventID', 'IsDuplicate', 'IsDeleted'], schema='dbo')
    op.create_index('IX_Event_Recurring', 'Event', ['IsRecurring', 'RecurrencePatternID', 'IsDeleted'], schema='dbo')
    
    # Seed reference data for EventType
    op.execute("""
        INSERT INTO ref.EventType (TypeCode, TypeName, TypeDescription, IsActive, SortOrder, CreatedBy) VALUES
        ('TRADE_SHOW', 'Trade Show', 'Industry trade shows and exhibitions', 1, 1, 1),
        ('CONFERENCE', 'Conference', 'Professional conferences and conventions', 1, 2, 1),
        ('EXPO', 'Expo', 'Public exhibitions and expositions', 1, 3, 1),
        ('COMMUNITY', 'Community Event', 'Local community events and meetups', 1, 4, 1),
        ('JOB_FAIR', 'Job Fair', 'Career and job fair events', 1, 5, 1),
        ('PRODUCT_LAUNCH', 'Product Launch', 'Product launch and announcement events', 1, 6, 1),
        ('WORKSHOP', 'Workshop', 'Educational workshops and training', 1, 7, 1),
        ('SEMINAR', 'Seminar', 'Professional seminars and presentations', 1, 8, 1),
        ('OTHER', 'Other', 'Other types of events', 1, 9, 1)
    """)
    
    # Seed reference data for EventStatus
    op.execute("""
        INSERT INTO ref.EventStatus (StatusCode, StatusName, StatusDescription, StatusColor, StatusIcon, IsActive, SortOrder, CreatedBy) VALUES
        ('DRAFT', 'Draft', 'Event is being created and edited', '#FFA500', 'draft-icon', 1, 1, 1),
        ('PENDING_REVIEW', 'Pending Review', 'Event submitted for public review', '#FFC107', 'pending-icon', 1, 2, 1),
        ('PUBLISHED', 'Published', 'Event is live and accepting forms', '#28A745', 'published-icon', 1, 3, 1),
        ('COMPLETED', 'Completed', 'Event has finished', '#17A2B8', 'completed-icon', 1, 4, 1),
        ('CANCELLED', 'Cancelled', 'Event has been cancelled', '#DC3545', 'cancelled-icon', 1, 5, 1),
        ('REJECTED', 'Rejected', 'Event rejected during review', '#6C757D', 'rejected-icon', 1, 6, 1),
        ('ARCHIVED', 'Archived', 'Event has been archived', '#6C757D', 'archived-icon', 1, 7, 1)
    """)
    
    # Seed reference data for RecurrencePattern
    op.execute("""
        INSERT INTO ref.RecurrencePattern (PatternCode, PatternName, PatternDescription, PatternFormula, IsActive, SortOrder, CreatedBy) VALUES
        ('NONE', 'No Recurrence', 'One-time event', NULL, 1, 1, 1),
        ('DAILY', 'Daily', 'Event occurs every day', 'ADD_DAYS(1)', 1, 2, 1),
        ('WEEKLY', 'Weekly', 'Event occurs every week', 'ADD_WEEKS(1)', 1, 3, 1),
        ('MONTHLY', 'Monthly', 'Event occurs every month', 'ADD_MONTHS(1)', 1, 4, 1),
        ('YEARLY', 'Yearly', 'Event occurs every year', 'ADD_YEARS(1)', 1, 5, 1),
        ('CUSTOM', 'Custom', 'Custom recurrence pattern', NULL, 1, 6, 1)
    """)


def downgrade():
    """Rollback Events domain changes"""
    
    # Drop indexes
    op.drop_index('IX_Event_Recurring', 'Event', schema='dbo')
    op.drop_index('IX_Event_Duplicate', 'Event', schema='dbo')
    op.drop_index('IX_Event_PublicReview', 'Event', schema='dbo')
    op.drop_index('IX_Event_Location', 'Event', schema='dbo')
    op.drop_index('IX_Event_Public', 'Event', schema='dbo')
    op.drop_index('IX_Event_DateTime', 'Event', schema='dbo')
    op.drop_index('IX_Event_Industry', 'Event', schema='dbo')
    op.drop_index('IX_Event_Type', 'Event', schema='dbo')
    op.drop_index('IX_Event_Status', 'Event', schema='dbo')
    op.drop_index('IX_Event_Company', 'Event', schema='dbo')
    
    # Drop check constraints
    op.drop_constraint('CK_Event_Attendees', 'Event', schema='dbo')
    op.drop_constraint('CK_Event_Longitude', 'Event', schema='dbo')
    op.drop_constraint('CK_Event_Latitude', 'Event', schema='dbo')
    op.drop_constraint('CK_Event_DateTime', 'Event', schema='dbo')
    op.drop_constraint('CK_Event_PublicReviewStatus', 'Event', schema='dbo')
    
    # Drop tables
    op.drop_table('Event', schema='dbo')
    op.drop_table('RecurrencePattern', schema='ref')
    op.drop_table('EventStatus', schema='ref')
    op.drop_table('EventType', schema='ref')