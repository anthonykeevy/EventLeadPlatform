"""
FormSubmission Model (dbo.FormSubmission)
Stores public form submissions captured via token-gated endpoint.
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from common.database import Base


class FormSubmission(Base):
    """
    FormSubmission model for public submissions.
    """

    __tablename__ = "FormSubmission"
    __table_args__ = (
        UniqueConstraint(
            "FormPublicLinkID",
            "IdempotencyKey",
            name="UQ_FormSubmission_FormPublicLinkID_IdempotencyKey",
        ),
        {"schema": "dbo"},
    )

    FormSubmissionID = Column(BigInteger, primary_key=True, autoincrement=True)

    FormID = Column(BigInteger, ForeignKey("dbo.Form.FormID"), nullable=False, index=True)
    FormVersionID = Column(BigInteger, ForeignKey("dbo.FormVersion.FormVersionID"), nullable=False, index=True)
    FormPublicLinkID = Column(BigInteger, ForeignKey("dbo.FormPublicLink.FormPublicLinkID"), nullable=False, index=True)

    LinkType = Column(String(20), nullable=False)
    IsPreview = Column(Boolean, nullable=False, server_default="0")  # Story 5.5: preview vs production
    IdempotencyKey = Column(String(255), nullable=False)

    SubmittedAtClient = Column(DateTime, nullable=False)
    ReceivedAtServer = Column(DateTime, nullable=False, server_default=func.getutcdate())

    AnswersJSON = Column(String(None), nullable=False)  # NVARCHAR(MAX)
    ContextJSON = Column(String(None), nullable=True)  # NVARCHAR(MAX)

    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, server_default="0")
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    # Relationships
    form = relationship("Form", foreign_keys=[FormID])
    form_version = relationship("FormVersion", foreign_keys=[FormVersionID])
    public_link = relationship("FormPublicLink", foreign_keys=[FormPublicLinkID])
    created_by_user = relationship("User", foreign_keys=[CreatedBy])
    deleted_by_user = relationship("User", foreign_keys=[DeletedBy])

    def __repr__(self) -> str:
        return f"<FormSubmission(ID={self.FormSubmissionID}, FormID={self.FormID}, LinkType={self.LinkType})>"
