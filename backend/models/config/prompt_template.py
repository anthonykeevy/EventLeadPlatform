"""
PromptTemplate Model (config.PromptTemplate)
Versioned prompt registry template metadata.
"""
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from common.database import Base


class PromptTemplate(Base):
    __tablename__ = "PromptTemplate"
    __table_args__ = {"schema": "config"}

    PromptTemplateID = Column(BigInteger, primary_key=True, autoincrement=True)
    TemplateKey = Column(String(120), nullable=False, index=True)
    TemplateName = Column(String(200), nullable=False)
    Purpose = Column(String(500), nullable=True)
    Owner = Column(String(200), nullable=True)

    IsActive = Column(Boolean, nullable=False, default=True)

    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    UpdatedDate = Column(DateTime, nullable=True)
    UpdatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    created_by_user = relationship("User", foreign_keys=[CreatedBy])
    updated_by_user = relationship("User", foreign_keys=[UpdatedBy])
    deleted_by_user = relationship("User", foreign_keys=[DeletedBy])

    def __repr__(self) -> str:
        return f"<PromptTemplate(PromptTemplateID={self.PromptTemplateID}, TemplateKey='{self.TemplateKey}')>"
