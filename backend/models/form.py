"""
Form Model (dbo.Form)
Core form entity with comprehensive metadata and lifecycle management
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from common.database import Base


class Form(Base):
    """
    Form model representing form headers with metadata.
    
    Features:
    - Multi-tenant form access (company-scoped)
    - Complete lifecycle management (Draft → Published → Archived)
    - Event association (optional)
    - Dashboard summary fields (activity metrics, visual elements)
    - Approval workflow integration
    - Audit trail with full change tracking
    - Soft deletes for data retention
    
    Attributes:
        FormID: Primary key
        FormName: Form name/title
        FormDescription: Detailed form description
        CompanyID: Owner company (for multi-tenant filtering)
        EventID: Associated event (nullable)
        FormStatusID: Form status (foreign key)
        FormApprovalStatusID: Approval status (foreign key)
        IsPublic: Public visibility flag
        DeploymentCost: Cost for deployment
        TotalSubmissions: Total form submissions
        DemoLeadsCollected: Demo environment leads
        ProductionLeadsCollected: Production environment leads
        LastSubmissionDate: Last submission timestamp
        LastActivityDate: Last activity timestamp
        FormThumbnailURL: Thumbnail URL for dashboard
        FormPreviewURL: Preview URL for dashboard
    """
    
    __tablename__ = "Form"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    FormID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Form Identity
    FormName = Column(String(200), nullable=False)
    FormDescription = Column(String(None), nullable=True)  # NVARCHAR(MAX)
    
    # Ownership and Context
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=False, index=True)
    EventID = Column(BigInteger, ForeignKey('dbo.Event.EventID'), nullable=True, index=True)
    
    # Status and Approval
    FormStatusID = Column(Integer, ForeignKey('ref.FormStatus.FormStatusID'), nullable=False, index=True)
    FormApprovalStatusID = Column(Integer, ForeignKey('ref.FormApprovalStatus.FormApprovalStatusID'), nullable=False, index=True)
    
    # Dashboard Summary Fields
    IsPublic = Column(Boolean, nullable=False, default=False)
    DeploymentCost = Column(DECIMAL(10, 2), nullable=True)
    
    # Activity Summary (Dashboard Metrics)
    TotalSubmissions = Column(Integer, nullable=False, default=0)
    DemoLeadsCollected = Column(Integer, nullable=False, default=0)
    ProductionLeadsCollected = Column(Integer, nullable=False, default=0)
    LastSubmissionDate = Column(DateTime, nullable=True)
    LastActivityDate = Column(DateTime, nullable=True)
    
    # Visual Identification
    FormThumbnailURL = Column(String(500), nullable=True)
    FormPreviewURL = Column(String(500), nullable=True)
    
    # Unpublish settings (Story 5.8)
    UnpublishMode = Column(String(20), nullable=False, default="MANUAL")  # MANUAL | EVENT_END | SCHEDULED
    ScheduledUnpublishDate = Column(DateTime, nullable=True)

    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    company = relationship("Company", foreign_keys=[CompanyID])
    event = relationship("Event", foreign_keys=[EventID])
    form_status = relationship("FormStatus", foreign_keys=[FormStatusID])
    form_approval_status = relationship("FormApprovalStatus", foreign_keys=[FormApprovalStatusID])
    created_by_user = relationship("User", foreign_keys=[CreatedBy])
    updated_by_user = relationship("User", foreign_keys=[UpdatedBy])
    deleted_by_user = relationship("User", foreign_keys=[DeletedBy])
    
    def __repr__(self) -> str:
        return f"<Form(FormID={self.FormID}, FormName='{self.FormName}', CompanyID={self.CompanyID})>"

