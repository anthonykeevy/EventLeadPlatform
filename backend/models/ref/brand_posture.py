"""BrandPosture reference model (ref.BrandPosture)."""
from sqlalchemy import Column, Integer, String, Boolean
from common.database import Base


class BrandPosture(Base):
    __tablename__ = "BrandPosture"
    __table_args__ = {"schema": "ref"}

    BrandPostureID = Column(Integer, primary_key=True, autoincrement=True)
    Code = Column(String(40), nullable=False, unique=True)
    DisplayName = Column(String(100), nullable=False)
    SortOrder = Column(Integer, nullable=False, default=0)
    IsActive = Column(Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        return (
            f"<BrandPosture(BrandPostureID={self.BrandPostureID}, "
            f"Code='{self.Code}')>"
        )
