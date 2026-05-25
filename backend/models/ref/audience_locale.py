"""ref.AudienceLocale — clarification audience locale registry."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.dialects.mssql import NVARCHAR

from common.database import Base


class AudienceLocale(Base):
    __tablename__ = "AudienceLocale"
    __table_args__ = {"schema": "ref"}

    AudienceLocaleID = Column(Integer, primary_key=True, autoincrement=True)
    Code = Column(String(30), nullable=False, unique=True)
    DisplayName = Column(NVARCHAR(28), nullable=False)
    FlagEmoji = Column(NVARCHAR(10), nullable=True)
    Description = Column(NVARCHAR(200), nullable=True)
    ClarificationSummary = Column(NVARCHAR(500), nullable=False)
    SortOrder = Column(Integer, nullable=False, default=0)
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    UpdatedDate = Column(DateTime, nullable=True)
