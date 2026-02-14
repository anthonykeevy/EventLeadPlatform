"""
Global Form Defaults Version (dbo.GlobalFormDefaultsVersion)
Immutable audit history for global defaults (Story 5.2)
"""
from sqlalchemy import Column, BigInteger, Integer, String, DateTime, func, ForeignKey
from common.database import Base


class GlobalFormDefaultsVersion(Base):
    """
    Append-only audit history. Insert on every GlobalFormDefaults change.
    """
    __tablename__ = "GlobalFormDefaultsVersion"
    __table_args__ = {"schema": "dbo"}

    GlobalFormDefaultsVersionID = Column(BigInteger, primary_key=True, autoincrement=True)
    FormDefaultsSchemaVersionID = Column(BigInteger, ForeignKey("ref.FormDefaultsSchemaVersion.FormDefaultsSchemaVersionID"), nullable=False)
    VersionNumber = Column(Integer, nullable=False)
    DefaultsJSON = Column(String(None), nullable=False)  # NVARCHAR(MAX)
    ChangeSummary = Column(String(500), nullable=True)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
