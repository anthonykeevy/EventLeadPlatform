"""
Form Defaults Schema Version (ref.FormDefaultsSchemaVersion)
Schema versioning for DefaultsJSON structure evolution (Story 5.2)
"""
from sqlalchemy import Column, BigInteger, Integer, String, Boolean, DateTime, func, ForeignKey
from common.database import Base


class FormDefaultsSchemaVersion(Base):
    """
    Tracks schema versions for GlobalFormDefaults and CompanyFormDefaults DefaultsJSON.
    Enables validation and migration when payload structure evolves.
    """
    __tablename__ = "FormDefaultsSchemaVersion"
    __table_args__ = {"schema": "ref"}

    FormDefaultsSchemaVersionID = Column(BigInteger, primary_key=True, autoincrement=True)
    SchemaVersion = Column(Integer, nullable=False, unique=True)
    SchemaName = Column(String(100), nullable=False)
    Description = Column(String(500), nullable=True)
    SchemaDocument = Column(String(None), nullable=True)  # NVARCHAR(MAX)
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
