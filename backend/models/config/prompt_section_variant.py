"""
PromptSectionVariant Model (config.PromptSectionVariant)

Variant prose for a PromptSection. Variant-level versioning per
prompt-assembly-registry-architecture.md Section 8.1. One IsDefault=1
variant per section (partial unique index).
"""

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    func,
)
from sqlalchemy.dialects.mssql import NVARCHAR
from sqlalchemy.orm import relationship

from common.database import Base


class PromptSectionVariant(Base):
    __tablename__ = "PromptSectionVariant"
    __table_args__ = {"schema": "config"}

    PromptSectionVariantID = Column(BigInteger, primary_key=True, autoincrement=True)
    PromptSectionID = Column(
        BigInteger,
        ForeignKey("config.PromptSection.PromptSectionID"),
        nullable=False,
    )
    VariantCode = Column(NVARCHAR(length=50), nullable=False)
    DisplayName = Column(NVARCHAR(length=200), nullable=True)
    Description = Column(NVARCHAR(length=1000), nullable=True)
    IsDefault = Column(Boolean, nullable=False, default=False)
    PromptSnippet = Column(NVARCHAR(length=None), nullable=False)
    SchemaJson = Column(NVARCHAR(length=None), nullable=True)
    VariantVersion = Column(Integer, nullable=False, default=1)
    IsLockedForEdits = Column(Boolean, nullable=False, default=False)
    ActivatedUtc = Column(DateTime, nullable=True)
    ExperimentFlag = Column(NVARCHAR(length=80), nullable=True)
    RolloutPercent = Column(SmallInteger, nullable=True)
    ChangeReason = Column(NVARCHAR(length=500), nullable=True)

    CreatedUtc = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    LastUpdatedUtc = Column(DateTime, nullable=True)
    LastUpdatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    section = relationship("PromptSection", back_populates="variants")
    data = relationship(
        "PromptSectionData",
        back_populates="variant",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<PromptSectionVariant(PromptSectionVariantID={self.PromptSectionVariantID}, "
            f"VariantCode='{self.VariantCode}', IsDefault={self.IsDefault})>"
        )
