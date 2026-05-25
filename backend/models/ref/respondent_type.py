"""ref.RespondentType — clarification respondent type registry."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.dialects.mssql import NVARCHAR

from common.database import Base


class RespondentType(Base):
    __tablename__ = "RespondentType"
    __table_args__ = {"schema": "ref"}

    RespondentTypeID = Column(Integer, primary_key=True, autoincrement=True)
    Code = Column(String(50), nullable=False, unique=True)
    DisplayName = Column(NVARCHAR(100), nullable=False)
    PromptHint = Column(NVARCHAR(length=None), nullable=False)
    SortOrder = Column(Integer, nullable=False, default=0)
    IsActive = Column(Boolean, nullable=False, default=True)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
