"""
GenerationRun Model (dbo.GenerationRun)
Per-request Form AI execution metadata for replay and audit.
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.mssql import NVARCHAR
from sqlalchemy.orm import relationship

from common.database import Base


class GenerationRun(Base):
    __tablename__ = "GenerationRun"
    __table_args__ = {"schema": "dbo"}

    GenerationRunID = Column(BigInteger, primary_key=True, autoincrement=True)
    RequestID = Column(String(100), nullable=False, index=True)
    CompanyID = Column(BigInteger, ForeignKey("dbo.Company.CompanyID"), nullable=True, index=True)
    FormID = Column(BigInteger, ForeignKey("dbo.Form.FormID"), nullable=True, index=True)

    PromptTemplateVersionID = Column(
        BigInteger,
        ForeignKey("config.PromptTemplateVersion.PromptTemplateVersionID"),
        nullable=True,
    )
    PromptAssemblyProfileID = Column(
        BigInteger,
        ForeignKey("config.PromptAssemblyProfile.PromptAssemblyProfileID"),
        nullable=True,
    )
    # Story 6.5b - prompt assembly registry version + per-block variant snapshot.
    PromptAssemblyRegistryVersionID = Column(
        BigInteger,
        ForeignKey("config.PromptAssemblyRegistryVersion.PromptAssemblyRegistryVersionID"),
        nullable=True,
    )
    PromptVariantSnapshot = Column(NVARCHAR(length=None), nullable=True)
    CapabilityPolicyVersionID = Column(
        BigInteger,
        ForeignKey("config.CapabilityPolicyVersion.CapabilityPolicyVersionID"),
        nullable=True,
    )
    ComponentCapabilitySnapshotID = Column(
        BigInteger,
        ForeignKey("config.ComponentCapabilitySnapshot.ComponentCapabilitySnapshotID"),
        nullable=True,
    )
    WidthClassPolicyVersionID = Column(
        BigInteger,
        ForeignKey("config.WidthClassPolicyVersion.WidthClassPolicyVersionID"),
        nullable=True,
    )
    ValidationContractVersion = Column(String(80), nullable=True)
    PromptHash = Column(String(64), nullable=True)
    RuntimeContextHash = Column(String(64), nullable=True)

    Status = Column(String(32), nullable=False)
    TerminalReason = Column(String(80), nullable=True)
    AttemptCount = Column(Integer, nullable=False, default=0)
    FirstShotValid = Column(Boolean, nullable=True)
    BrandPosture = Column(String(40), nullable=True)
    BrandHeritageOrigin = Column(String(5), nullable=True)
    IsReplayable = Column(Boolean, nullable=False, default=True)

    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), index=True)
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    company = relationship("Company", foreign_keys=[CompanyID])
    form = relationship("Form", foreign_keys=[FormID])
    prompt_template_version = relationship("PromptTemplateVersion")
    prompt_assembly_profile = relationship("PromptAssemblyProfile")
    prompt_assembly_registry_version = relationship("PromptAssemblyRegistryVersion")
    capability_policy_version = relationship("CapabilityPolicyVersion")
    component_capability_snapshot = relationship("ComponentCapabilitySnapshot")
    width_class_policy_version = relationship("WidthClassPolicyVersion")
    created_by_user = relationship("User", foreign_keys=[CreatedBy])

    def __repr__(self) -> str:
        return (
            f"<GenerationRun(GenerationRunID={self.GenerationRunID}, RequestID='{self.RequestID}', "
            f"Status='{self.Status}', AttemptCount={self.AttemptCount})>"
        )
