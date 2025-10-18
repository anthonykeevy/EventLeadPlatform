"""
CompanySwitchRequestStatus Model (ref.CompanySwitchRequestStatus)
Reference table for the statuses of company switch/access requests.
"""
from sqlalchemy import Column, Integer, String, Boolean
from common.database import Base

class CompanySwitchRequestStatus(Base):
    __tablename__ = "CompanySwitchRequestStatus"
    __table_args__ = {"schema": "ref"}

    CompanySwitchRequestStatusID = Column(Integer, primary_key=True, autoincrement=True)
    StatusName = Column(String(50), nullable=False, unique=True)
    StatusDescription = Column(String(255), nullable=True)
    IsActive = Column(Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        return f"<CompanySwitchRequestStatus(ID={self.CompanySwitchRequestStatusID}, Name='{self.StatusName}')>"
