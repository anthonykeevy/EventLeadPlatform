"""
Company Form Defaults Version (dbo.CompanyFormDefaultsVersion)
Immutable audit history for company defaults (Story 5.2)
"""
from sqlalchemy import Column, BigInteger, Integer, String, DateTime, func, ForeignKey
from common.database import Base


class CompanyFormDefaultsVersion(Base):
    """
    Append-only audit history per company. Insert on every CompanyFormDefaults change.
    """
    __tablename__ = "CompanyFormDefaultsVersion"
    __table_args__ = {"schema": "dbo"}

    CompanyFormDefaultsVersionID = Column(BigInteger, primary_key=True, autoincrement=True)
    CompanyID = Column(BigInteger, ForeignKey("dbo.Company.CompanyID"), nullable=False)
    FormDefaultsSchemaVersionID = Column(BigInteger, ForeignKey("ref.FormDefaultsSchemaVersion.FormDefaultsSchemaVersionID"), nullable=False)
    VersionNumber = Column(Integer, nullable=False)
    DefaultsJSON = Column(String(None), nullable=False)  # NVARCHAR(MAX)
    ChangeSummary = Column(String(500), nullable=True)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
