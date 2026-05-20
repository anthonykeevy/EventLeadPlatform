"""
PromptSection Model (config.PromptSection)

Ordered prompt section within a PromptAssemblyRegistryVersion. Each row
maps a SectionCode (A, B, C, ..., I) to a SortOrder and a
DataStructureType used by the renderer to decide how to hydrate the
section's chosen variant.
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


class PromptSection(Base):
    __tablename__ = "PromptSection"
    __table_args__ = (
        UniqueConstraint(
            "PromptAssemblyRegistryVersionID",
            "SectionCode",
            name="UQ_PromptSection_Version_SectionCode",
        ),
        CheckConstraint(
            "DataStructureType IN ('Prose', 'Json', 'Snapshot', 'Refs')",
            name="CK_PromptSection_DataStructureType",
        ),
        {"schema": "config"},
    )

    PromptSectionID = Column(BigInteger, primary_key=True, autoincrement=True)
    PromptAssemblyRegistryVersionID = Column(
        BigInteger,
        ForeignKey("config.PromptAssemblyRegistryVersion.PromptAssemblyRegistryVersionID"),
        nullable=False,
    )
    SectionCode = Column(NVARCHAR(length=10), nullable=False)
    DisplayName = Column(NVARCHAR(length=200), nullable=False)
    SortOrder = Column(Integer, nullable=False)
    IsRequired = Column(Boolean, nullable=False, default=True)
    DataStructureType = Column(NVARCHAR(length=20), nullable=False)
    Heading = Column(NVARCHAR(length=200), nullable=True)

    CreatedUtc = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    LastUpdatedUtc = Column(DateTime, nullable=True)
    LastUpdatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    registry_version = relationship("PromptAssemblyRegistryVersion", back_populates="sections")
    variants = relationship(
        "PromptSectionVariant",
        back_populates="section",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<PromptSection(PromptSectionID={self.PromptSectionID}, "
            f"SectionCode='{self.SectionCode}', SortOrder={self.SortOrder})>"
        )
