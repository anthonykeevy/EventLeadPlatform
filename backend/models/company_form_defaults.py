"""
Company Form Defaults (dbo.CompanyFormDefaults)
Per-company form branding defaults (Story 5.2)
"""
from sqlalchemy import Column, BigInteger, Integer, String, Boolean, DateTime, func, ForeignKey
from common.database import Base


class CompanyFormDefaults(Base):
    """
    Current effective defaults per company. One row per CompanyID.
    Company overrides Global; merged by resolver.
    """
    __tablename__ = "CompanyFormDefaults"
    __table_args__ = {"schema": "dbo"}

    CompanyFormDefaultsID = Column(BigInteger, primary_key=True, autoincrement=True)
    CompanyID = Column(BigInteger, ForeignKey("dbo.Company.CompanyID"), nullable=False, unique=True)
    FormDefaultsSchemaVersionID = Column(BigInteger, ForeignKey("ref.FormDefaultsSchemaVersion.FormDefaultsSchemaVersionID"), nullable=False)
    VersionNumber = Column(Integer, nullable=False)
    DefaultsJSON = Column(String(None), nullable=False)  # NVARCHAR(MAX)
    IsActive = Column(Boolean, nullable=False, default=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    UpdatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), onupdate=func.getutcdate())
    UpdatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
