"""
CompanySwitchRequest Model (dbo.CompanySwitchRequest)
Tracks user requests to switch or gain access to companies.
"""
from sqlalchemy import Column, BigInteger, String, DateTime, func, ForeignKey, Boolean, Integer
from sqlalchemy.orm import relationship
from common.database import Base


class CompanySwitchRequest(Base):
    """
    CompanySwitchRequest model for managing access requests and company joins.
    
    Use Cases:
    - User requests access to a company they are not a member of.
    - Tracks the approval/rejection flow for such requests.
    
    Attributes:
        CompanySwitchRequestID: Primary key
        UserID: FK to User (who is requesting access)
        FromCompanyID: FK to Company (origin company, nullable)
        ToCompanyID: FK to Company (target company)
        RequestTypeID: FK to ref.CompanySwitchRequestType
        StatusID: FK to ref.CompanySwitchRequestStatus
        RequestedBy: FK to User who initiated the request
        RequestedAt: Timestamp of the request
        Reason: Optional user-provided reason for the request
        ApprovedBy: FK to User who approved the request
        ApprovedAt: Timestamp of approval
        RejectedBy: FK to User who rejected the request
        RejectedAt: Timestamp of rejection
        RejectionReason: Optional admin-provided reason for rejection
    """
    
    __tablename__ = "CompanySwitchRequest"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    CompanySwitchRequestID = Column(BigInteger, primary_key=True, autoincrement=True, name="RequestID")
    
    # Request Details
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False, index=True)
    FromCompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=True)
    ToCompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=False, index=True)
    RequestTypeID = Column(Integer, ForeignKey('ref.CompanySwitchRequestType.CompanySwitchRequestTypeID'), nullable=False, index=True)
    StatusID = Column(Integer, ForeignKey('ref.CompanySwitchRequestStatus.CompanySwitchRequestStatusID'), nullable=False, index=True)
    
    # Request Metadata
    RequestedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False)
    RequestedAt = Column(DateTime, nullable=False, server_default=func.getutcdate())
    Reason = Column(String(500), nullable=True)
    
    # Approval/Rejection
    ApprovedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    ApprovedAt = Column(DateTime, nullable=True)
    RejectedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    RejectedAt = Column(DateTime, nullable=True)
    RejectionReason = Column(String(500), nullable=True)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    UpdatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), onupdate=func.getutcdate())
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[UserID], backref="switch_requests")
    from_company = relationship("Company", foreign_keys=[FromCompanyID], backref="switch_requests_from")
    to_company = relationship("Company", foreign_keys=[ToCompanyID], backref="switch_requests_to")
    request_type = relationship("CompanySwitchRequestType", foreign_keys=[RequestTypeID])
    status = relationship("CompanySwitchRequestStatus", foreign_keys=[StatusID])
    
    requested_by_user = relationship("User", foreign_keys=[RequestedBy])
    approved_by_user = relationship("User", foreign_keys=[ApprovedBy])
    rejected_by_user = relationship("User", foreign_keys=[RejectedBy])

    def __repr__(self) -> str:
        return (
            f"<CompanySwitchRequest(ID={self.CompanySwitchRequestID}, UserID={self.UserID}, "
            f"ToCompanyID={self.ToCompanyID}, StatusID='{self.StatusID}')>"
        )
