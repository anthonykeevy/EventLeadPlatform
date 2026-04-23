"""
GenerationArtifact Model (dbo.GenerationArtifact)
Stores semantic/compiled artifacts linked to a generation run.
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from common.database import Base


class GenerationArtifact(Base):
    __tablename__ = "GenerationArtifact"
    __table_args__ = {"schema": "dbo"}

    GenerationArtifactID = Column(BigInteger, primary_key=True, autoincrement=True)
    GenerationRunID = Column(
        BigInteger, ForeignKey("dbo.GenerationRun.GenerationRunID"), nullable=False, index=True
    )
    ArtifactType = Column(String(60), nullable=False)
    SequenceNumber = Column(Integer, nullable=False, default=1)
    ArtifactJson = Column(String(None), nullable=False)
    ArtifactHash = Column(String(64), nullable=True)
    IsCompressed = Column(Boolean, nullable=False, default=False)
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    generation_run = relationship("GenerationRun")
    created_by_user = relationship("User", foreign_keys=[CreatedBy])

    def __repr__(self) -> str:
        return (
            f"<GenerationArtifact(GenerationArtifactID={self.GenerationArtifactID}, "
            f"GenerationRunID={self.GenerationRunID}, ArtifactType='{self.ArtifactType}', "
            f"SequenceNumber={self.SequenceNumber})>"
        )
