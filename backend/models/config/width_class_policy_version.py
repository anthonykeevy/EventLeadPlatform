"""
WidthClassPolicyVersion Model (config.WidthClassPolicyVersion)
Versioned compact/half/full class resolution policies.
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from common.database import Base


class WidthClassPolicyVersion(Base):
    __tablename__ = "WidthClassPolicyVersion"
    __table_args__ = {"schema": "config"}

    WidthClassPolicyVersionID = Column(BigInteger, primary_key=True, autoincrement=True)
    PolicyKey = Column(String(120), nullable=False, index=True)
    VersionNumber = Column(Integer, nullable=False)
    PolicyJson = Column(String(None), nullable=False)
    PolicyHash = Column(String(64), nullable=False)

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

    created_by_user = relationship("User", foreign_keys=[CreatedBy])
    updated_by_user = relationship("User", foreign_keys=[UpdatedBy])
    deleted_by_user = relationship("User", foreign_keys=[DeletedBy])

    def __repr__(self) -> str:
        return (
            f"<WidthClassPolicyVersion(WidthClassPolicyVersionID={self.WidthClassPolicyVersionID}, "
            f"PolicyKey='{self.PolicyKey}', VersionNumber={self.VersionNumber})>"
        )
