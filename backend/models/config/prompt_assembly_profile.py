"""
PromptAssemblyProfile Model (config.PromptAssemblyProfile)
Runtime profile linking template/policy versions for a given step.
"""
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from common.database import Base


class PromptAssemblyProfile(Base):
    __tablename__ = "PromptAssemblyProfile"
    __table_args__ = {"schema": "config"}

    PromptAssemblyProfileID = Column(BigInteger, primary_key=True, autoincrement=True)
    ProfileKey = Column(String(120), nullable=False, index=True)
    ProfileName = Column(String(200), nullable=False)
    StepName = Column(String(40), nullable=False)
    Description = Column(String(1000), nullable=True)

    PromptTemplateVersionID = Column(
        BigInteger,
        ForeignKey("config.PromptTemplateVersion.PromptTemplateVersionID"),
        nullable=False,
    )
    CapabilityPolicyVersionID = Column(
        BigInteger,
        ForeignKey("config.CapabilityPolicyVersion.CapabilityPolicyVersionID"),
        nullable=True,
    )
    WidthClassPolicyVersionID = Column(
        BigInteger,
        ForeignKey("config.WidthClassPolicyVersion.WidthClassPolicyVersionID"),
        nullable=True,
    )

    IsActive = Column(Boolean, nullable=False, default=True)

    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    prompt_template_version = relationship("PromptTemplateVersion")
    capability_policy_version = relationship("CapabilityPolicyVersion")
    width_class_policy_version = relationship("WidthClassPolicyVersion")
    created_by_user = relationship("User", foreign_keys=[CreatedBy])
    updated_by_user = relationship("User", foreign_keys=[UpdatedBy])
    deleted_by_user = relationship("User", foreign_keys=[DeletedBy])

    def __repr__(self) -> str:
        return (
            f"<PromptAssemblyProfile(PromptAssemblyProfileID={self.PromptAssemblyProfileID}, "
            f"ProfileKey='{self.ProfileKey}', StepName='{self.StepName}')>"
        )
