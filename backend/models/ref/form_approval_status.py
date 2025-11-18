"""
FormApprovalStatus Reference Model (ref.FormApprovalStatus)
Form approval status classifications for approval workflow
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class FormApprovalStatus(Base):
    """
    FormApprovalStatus reference table for form approval status management.
    
    Attributes:
        FormApprovalStatusID: Primary key
        ApprovalStatusCode: Unique approval status code (e.g., 'NO_APPROVAL', 'PENDING', 'APPROVED')
        ApprovalStatusName: Display name (e.g., 'No Approval Required', 'Pending Approval', 'Approved')
        ApprovalStatusDescription: Full description of the approval status
        IsRequiresApproval: Whether this status requires approval workflow
        IsActive: Whether approval status is available for selection
        SortOrder: Display order for approval status selection
    """
    
    __tablename__ = "FormApprovalStatus"
    __table_args__ = {"schema": "ref"}
    
    # Primary Key
    FormApprovalStatusID = Column(Integer, primary_key=True, autoincrement=True)
    
    # Core Fields
    ApprovalStatusCode = Column(String(20), nullable=False, unique=True)
    ApprovalStatusName = Column(String(50), nullable=False)
    ApprovalStatusDescription = Column(String(200), nullable=True)
    
    # Approval Configuration
    IsRequiresApproval = Column(Boolean, nullable=False, default=False)
    
    # Status and Ordering
    IsActive = Column(Boolean, nullable=False, default=True)
    SortOrder = Column(Integer, nullable=False, default=0)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    forms = relationship("Form", back_populates="form_approval_status", foreign_keys="[Form.FormApprovalStatusID]")
    
    def __repr__(self) -> str:
        return f"<FormApprovalStatus(FormApprovalStatusID={self.FormApprovalStatusID}, ApprovalStatusCode='{self.ApprovalStatusCode}', ApprovalStatusName='{self.ApprovalStatusName}')>"

