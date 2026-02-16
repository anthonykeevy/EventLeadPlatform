"""
FormPublishRequest Model (dbo.FormPublishRequest)
Story 5.6: Publish request workflow - Company User requests, Admin reviews.
"""
from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class FormPublishRequest(Base):
    """
    Publish request entity: tracks when a Company User requests a form to be published.
    Status: pending, approved, declined, changes_requested.
    """

    __tablename__ = "FormPublishRequest"
    __table_args__ = {"schema": "dbo"}

    FormPublishRequestID = Column(BigInteger, primary_key=True, autoincrement=True)
    FormID = Column(BigInteger, ForeignKey("dbo.Form.FormID"), nullable=False, index=True)
    RequestedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=False)
    RequestedAt = Column(DateTime, nullable=False, server_default=func.getutcdate())
    Message = Column(String(1000), nullable=True)
    Status = Column(String(20), nullable=False, default="pending")  # pending, approved, declined, changes_requested
    CompanyID = Column(BigInteger, ForeignKey("dbo.Company.CompanyID"), nullable=False, index=True)

    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    form = relationship("Form", foreign_keys=[FormID])
    requested_by_user = relationship("User", foreign_keys=[RequestedBy])
