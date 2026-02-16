"""
CompanyFormTestConfig Model (dbo.CompanyFormTestConfig)
Story 5.5: Per-company test threshold for publish readiness.
"""
from sqlalchemy import Column, BigInteger, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class CompanyFormTestConfig(Base):
    """
    Per-company configuration for test run threshold before publish.
    One row per company when configured.
    """

    __tablename__ = "CompanyFormTestConfig"
    __table_args__ = {"schema": "dbo"}

    CompanyFormTestConfigID = Column(BigInteger, primary_key=True, autoincrement=True)
    CompanyID = Column(BigInteger, ForeignKey("dbo.Company.CompanyID"), nullable=False, unique=True)
    TestThresholdEnabled = Column(Boolean, nullable=False, server_default="0")
    TestThresholdValue = Column(Integer, nullable=False, server_default="3")
    RequirePublishApproval = Column(Boolean, nullable=False, server_default="0")  # Story 5.6: Company User must request publish

    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    company = relationship("Company", foreign_keys=[CompanyID])
