"""
SubmissionAttachment (dbo.SubmissionAttachment)
Story 6.2.2: metadata for public form file uploads; not dbo.Asset.
"""
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class SubmissionAttachment(Base):
    __tablename__ = "SubmissionAttachment"
    __table_args__ = {"schema": "dbo"}

    SubmissionAttachmentID = Column(BigInteger, primary_key=True, autoincrement=True)

    FormPublicLinkID = Column(BigInteger, ForeignKey("dbo.FormPublicLink.FormPublicLinkID"), nullable=False, index=True)
    FormSubmissionID = Column(BigInteger, ForeignKey("dbo.FormSubmission.FormSubmissionID"), nullable=True, index=True)

    PublicAttachmentId = Column(String(36), nullable=False, unique=True, index=True)

    OriginalFileName = Column(String(510), nullable=False)
    ContentType = Column(String(255), nullable=False)
    SizeBytes = Column(BigInteger, nullable=False)
    Sha256 = Column(String(64), nullable=False, index=True)

    StorageProvider = Column(String(32), nullable=False)
    StorageKey = Column(String(1024), nullable=False)

    ClientUploadSessionKey = Column(String(128), nullable=True, index=True)

    CreatedAt = Column(DateTime, nullable=False, server_default=func.getutcdate())
    ExpiresAt = Column(DateTime, nullable=True)

    public_link = relationship("FormPublicLink", foreign_keys=[FormPublicLinkID])
    form_submission = relationship("FormSubmission", foreign_keys=[FormSubmissionID])

    def __repr__(self) -> str:
        return f"<SubmissionAttachment(ID={self.SubmissionAttachmentID}, public={self.PublicAttachmentId})>"
