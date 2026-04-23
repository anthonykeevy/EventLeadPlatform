"""
PromptTemplateVersion Model (config.PromptTemplateVersion)
Immutable content versions of prompt templates.
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from common.database import Base


class PromptTemplateVersion(Base):
    __tablename__ = "PromptTemplateVersion"
    __table_args__ = {"schema": "config"}

    PromptTemplateVersionID = Column(BigInteger, primary_key=True, autoincrement=True)
    PromptTemplateID = Column(
        BigInteger, ForeignKey("config.PromptTemplate.PromptTemplateID"), nullable=False, index=True
    )
    VersionNumber = Column(Integer, nullable=False)
    VersionLabel = Column(String(80), nullable=True)
    TemplateBody = Column(String(None), nullable=False)
    ChangeSummary = Column(String(1000), nullable=True)
    ContentHash = Column(String(64), nullable=False, index=True)

    IsActive = Column(Boolean, nullable=False, default=False)
    ActivatedDate = Column(DateTime, nullable=True)
    RetiredDate = Column(DateTime, nullable=True)

    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    prompt_template = relationship("PromptTemplate")
    created_by_user = relationship("User", foreign_keys=[CreatedBy])
    updated_by_user = relationship("User", foreign_keys=[UpdatedBy])
    deleted_by_user = relationship("User", foreign_keys=[DeletedBy])

    def __repr__(self) -> str:
        return (
            f"<PromptTemplateVersion(PromptTemplateVersionID={self.PromptTemplateVersionID}, "
            f"PromptTemplateID={self.PromptTemplateID}, VersionNumber={self.VersionNumber})>"
        )
