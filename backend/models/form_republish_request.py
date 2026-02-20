"""
FormRepublishRequest Model (dbo.FormRepublishRequest)
Story 5.8: Visitor requests re-publish when landing on unpublished form page.
"""
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class FormRepublishRequest(Base):
    """
    Records when a visitor clicks "Request admin to publish again" on unpublished form page.
    In-app notification to Company Admins can be triggered from this (MVP: placeholder).
    """

    __tablename__ = "FormRepublishRequest"
    __table_args__ = {"schema": "dbo"}

    FormRepublishRequestID = Column(BigInteger, primary_key=True, autoincrement=True)
    FormID = Column(BigInteger, ForeignKey("dbo.Form.FormID"), nullable=False, index=True)
    RequestedAt = Column(DateTime, nullable=False, server_default=func.getutcdate())
    IPAddress = Column(String(45), nullable=True)
    UserAgent = Column(String(500), nullable=True)

    form = relationship("Form", foreign_keys=[FormID])
