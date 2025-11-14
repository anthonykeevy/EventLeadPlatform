"""
EventCompanyRole Model (ref.EventCompanyRole)
Reference table for company roles in events
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class EventCompanyRole(Base):
    """
    EventCompanyRole reference table defining company participation roles in events.
    
    Roles:
    - event_owner: Company that created the event (full control)
    - event_organizer: Company organizing the event (if different from owner)
    - event_participant: Company using public event for forms (read-only)
    
    Attributes:
        EventCompanyRoleID: Primary key
        RoleCode: Unique role code (event_owner, event_organizer, event_participant)
        RoleName: Display name (Event Owner, Event Organizer, Event Participant)
        Description: Full description of role permissions
        RoleLevel: Numeric hierarchy level (higher = more permissions)
        HasEditEvent: Can edit event details (boolean)
        HasDeleteEvent: Can delete event (boolean)
        HasManageParticipants: Can manage event participants (boolean)
        HasViewEvent: Can view event details (boolean)
    """
    
    __tablename__ = "EventCompanyRole"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    EventCompanyRoleID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Role Identity
    RoleCode = Column(String(50), nullable=False, unique=True)
    RoleName = Column(String(100), nullable=False)
    Description = Column(String(500), nullable=False)
    RoleLevel = Column(Integer, nullable=False)
    
    # Permission Flags
    HasEditEvent = Column(Boolean, nullable=False, default=False)
    HasDeleteEvent = Column(Boolean, nullable=False, default=False)
    HasManageParticipants = Column(Boolean, nullable=False, default=False)
    HasViewEvent = Column(Boolean, nullable=False, default=True)
    
    # Configuration
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=0)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    created_by_user = relationship("User", foreign_keys=[CreatedBy])
    updated_by_user = relationship("User", foreign_keys=[UpdatedBy])
    
    def __repr__(self) -> str:
        return f"<EventCompanyRole(EventCompanyRoleID={self.EventCompanyRoleID}, RoleCode='{self.RoleCode}', RoleName='{self.RoleName}')>"

