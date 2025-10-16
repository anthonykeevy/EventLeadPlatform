"""
CompanyOrganizerDetails Model (dbo.CompanyOrganizerDetails)
Event organizer-specific details for companies (1-to-1 with Company)
"""
from sqlalchemy import Column, BigInteger, String, Integer, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from backend.common.database import Base


class CompanyOrganizerDetails(Base):
    """
    Company organizer details (1-to-1 with Company).
    
    Tracks event organizer-specific information and credentials.
    
    Attributes:
        CompanyOrganizerDetailsID: Primary key
        CompanyID: Unique foreign key to dbo.Company
        OrganizerLicenseNumber: Event organizer license number (if applicable)
        EventTypesOrganized: JSON array of event types organized
        AverageEventsPerYear: Average number of events organized per year
    """
    
    __tablename__ = "CompanyOrganizerDetails"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    CompanyOrganizerDetailsID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=False, unique=True)
    
    # Organizer Details
    OrganizerLicenseNumber = Column(String(100), nullable=True)
    EventTypesOrganized = Column(String(None), nullable=True)  # NVARCHAR(MAX) - JSON array
    AverageEventsPerYear = Column(Integer, nullable=True)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    UpdatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), onupdate=func.getutcdate())
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="organizer_details")
    
    def __repr__(self) -> str:
        return f"<CompanyOrganizerDetails(CompanyID={self.CompanyID}, AverageEventsPerYear={self.AverageEventsPerYear})>"

