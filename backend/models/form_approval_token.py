"""
FormApprovalToken Model
Stores secure tokens for external approval requests
"""
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base

class FormApprovalToken(Base):
    """
    FormApprovalToken model for external approvals.
    
    Attributes:
        FormApprovalTokenID: Primary key
        FormID: The form requiring approval
        Token: Secure random string
        Email: Email address of the approver (redundant with UserID but good for audit)
        UserID: The 'Shadow User' ID representing the external approver
        ExpiresAt: Token expiration timestamp
        IsUsed: Whether the token has been used
        UsedAt: When the token was used
        CreatedDate: When the token was generated
        CreatedBy: User who requested the approval
    """
    
    __tablename__ = "FormApprovalToken"
    __table_args__ = {"schema": "dbo"}
    
    FormApprovalTokenID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    FormID = Column(BigInteger, ForeignKey('dbo.Form.FormID'), nullable=False, index=True)
    Token = Column(String(255), nullable=False, unique=True, index=True)
    Email = Column(String(255), nullable=False)
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    ExpiresAt = Column(DateTime, nullable=False)
    IsUsed = Column(Boolean, nullable=False, default=False)
    UsedAt = Column(DateTime, nullable=True)
    
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    form = relationship("Form", backref="approval_tokens")
    user = relationship("User", foreign_keys=[UserID], backref="approval_tokens_received")
    creator = relationship("User", foreign_keys=[CreatedBy], backref="approval_tokens_created")
    
    def __repr__(self) -> str:
        return f"<FormApprovalToken(ID={self.FormApprovalTokenID}, FormID={self.FormID}, Email='{self.Email}')>"

