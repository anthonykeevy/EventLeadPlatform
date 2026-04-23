"""
ComponentValidationContract Model (config.ComponentValidationContract)
Per-component validation allowlist/schema/compatibility/message contracts.
"""
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from common.database import Base


class ComponentValidationContract(Base):
    __tablename__ = "ComponentValidationContract"
    __table_args__ = {"schema": "config"}

    ComponentValidationContractID = Column(BigInteger, primary_key=True, autoincrement=True)
    ComponentType = Column(String(80), nullable=False, index=True)
    ContractVersion = Column(String(80), nullable=False)
    AllowedRulesJson = Column(String(None), nullable=False)
    RuleParameterSchemaJson = Column(String(None), nullable=False)
    RuleCompatibilityJson = Column(String(None), nullable=True)
    MessagePolicyJson = Column(String(None), nullable=True)

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
        return (
            f"<ComponentValidationContract(ComponentValidationContractID={self.ComponentValidationContractID}, "
            f"ComponentType='{self.ComponentType}', ContractVersion='{self.ContractVersion}')>"
        )
