"""
PromptSectionData Model (config.PromptSectionData)

Optional structured side-data per PromptSectionVariant. Used for
non-prose payloads (PROHIBITED_TOPICS JSON list, allowed-component
hints, etc.). Story 6.5b creates the table but does not seed any rows;
6.5c / 6.5d use this for richer block payloads.
"""

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.mssql import NVARCHAR
from sqlalchemy.orm import relationship

from common.database import Base


class PromptSectionData(Base):
    __tablename__ = "PromptSectionData"
    __table_args__ = (
        UniqueConstraint(
            "PromptSectionVariantID",
            "DataKey",
            name="UQ_PromptSectionData_Variant_DataKey",
        ),
        CheckConstraint(
            "DataType IN ('Json', 'Csv', 'Text', 'Reference')",
            name="CK_PromptSectionData_DataType",
        ),
        {"schema": "config"},
    )

    PromptSectionDataID = Column(BigInteger, primary_key=True, autoincrement=True)
    PromptSectionVariantID = Column(
        BigInteger,
        ForeignKey("config.PromptSectionVariant.PromptSectionVariantID"),
        nullable=False,
    )
    DataKey = Column(NVARCHAR(length=120), nullable=False)
    DataValue = Column(NVARCHAR(length=None), nullable=False)
    DataType = Column(NVARCHAR(length=30), nullable=False)
    SortOrder = Column(Integer, nullable=False, default=0)

    CreatedUtc = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    LastUpdatedUtc = Column(DateTime, nullable=True)
    LastUpdatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    variant = relationship("PromptSectionVariant", back_populates="data")

    def __repr__(self) -> str:
        return (
            f"<PromptSectionData(PromptSectionDataID={self.PromptSectionDataID}, "
            f"DataKey='{self.DataKey}', DataType='{self.DataType}')>"
        )
