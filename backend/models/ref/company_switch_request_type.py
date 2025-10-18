"""
CompanySwitchRequestType Model (ref.CompanySwitchRequestType)
Reference table for the types of company switch/access requests.
"""
from sqlalchemy import Column, Integer, String, Boolean
from common.database import Base

class CompanySwitchRequestType(Base):
    __tablename__ = "CompanySwitchRequestType"
    __table_args__ = {"schema": "ref"}

    CompanySwitchRequestTypeID = Column(Integer, primary_key=True, autoincrement=True)
    TypeName = Column(String(50), nullable=False, unique=True)
    TypeDescription = Column(String(255), nullable=True)
    IsActive = Column(Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        return f"<CompanySwitchRequestType(ID={self.CompanySwitchRequestTypeID}, Name='{self.TypeName}')>"
