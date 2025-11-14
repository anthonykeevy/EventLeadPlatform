"""
EventCompany Model (dbo.EventCompany)
Junction table linking companies to events with roles and participation tracking
"""
from sqlalchemy import Column, BigInteger, Boolean, DateTime, Integer, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class EventCompany(Base):
    """
    EventCompany junction table for many-to-many company-event relationships.
    
    Tracks:
    - Which companies participate in which events
    - Company roles (owner, organizer, participant)
    - Usage metrics (forms created, first/last used dates)
    - Active participation status
    - Disassociation tracking
    
    Attributes:
        EventCompanyID: Primary key
        EventID: Foreign key to Event
        CompanyID: Foreign key to Company
        EventCompanyRoleID: Foreign key to EventCompanyRole (event_owner, event_organizer, event_participant)
        FormsCreated: Number of forms created for this event by this company
        FirstUsedDate: When company first used this event
        LastUsedDate: When company last used this event
        IsActive: Active participation flag
        DisassociatedDate: When company disassociated from event
        DisassociatedBy: User who disassociated company
    """
    
    __tablename__ = "EventCompany"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    EventCompanyID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    EventID = Column(BigInteger, ForeignKey('dbo.Event.EventID'), nullable=False, index=True)
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=False, index=True)
    EventCompanyRoleID = Column(BigInteger, ForeignKey('ref.EventCompanyRole.EventCompanyRoleID'), nullable=False, index=True)
    
    # Usage Metrics
    FormsCreated = Column(Integer, nullable=False, default=0)
    FirstUsedDate = Column(DateTime, nullable=True)
    LastUsedDate = Column(DateTime, nullable=True)
    
    # Access Control
    IsActive = Column(Boolean, nullable=False, default=True)
    DisassociatedDate = Column(DateTime, nullable=True)
    DisassociatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    event = relationship("Event", foreign_keys=[EventID])
    company = relationship("Company", foreign_keys=[CompanyID])
    role = relationship("EventCompanyRole", foreign_keys=[EventCompanyRoleID])
    created_by_user = relationship("User", foreign_keys=[CreatedBy])
    updated_by_user = relationship("User", foreign_keys=[UpdatedBy])
    deleted_by_user = relationship("User", foreign_keys=[DeletedBy])
    disassociated_by_user = relationship("User", foreign_keys=[DisassociatedBy])
    
    def __repr__(self) -> str:
        return f"<EventCompany(EventCompanyID={self.EventCompanyID}, EventID={self.EventID}, CompanyID={self.CompanyID}, RoleID={self.EventCompanyRoleID})>"

