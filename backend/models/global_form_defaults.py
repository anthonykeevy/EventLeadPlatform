"""
Global Form Defaults (dbo.GlobalFormDefaults)
Platform-wide form branding baseline (Story 5.2)
"""
from sqlalchemy import Column, BigInteger, Integer, String, Boolean, DateTime, func, ForeignKey
from common.database import Base


class GlobalFormDefaults(Base):
    """
    Single effective row for platform-wide form defaults.
    One row with IsActive=1; history in GlobalFormDefaultsVersion.
    """
    __tablename__ = "GlobalFormDefaults"
    __table_args__ = {"schema": "dbo"}

    GlobalFormDefaultsID = Column(BigInteger, primary_key=True, autoincrement=True)
    FormDefaultsSchemaVersionID = Column(BigInteger, ForeignKey("ref.FormDefaultsSchemaVersion.FormDefaultsSchemaVersionID"), nullable=False)
    VersionNumber = Column(Integer, nullable=False)
    DefaultsJSON = Column(String(None), nullable=False)  # NVARCHAR(MAX)
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    UpdatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), onupdate=func.getutcdate())
    UpdatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
