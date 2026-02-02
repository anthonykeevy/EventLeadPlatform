"""
FormPublicLink Model
Stores secure tokens for public form rendering links (preview/production).

Story 3.8 - Public Form Renderer (Token-based public URL /forms/:token)
"""
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class FormPublicLink(Base):
    """
    FormPublicLink model for public renderer links.

    Attributes:
        FormPublicLinkID: Primary key
        FormID: The form this link resolves to
        Token: Secure random string (unique)
        LinkType: PREVIEW or PRODUCTION (for lead attribution in Story 3.9)
        IsActive: Whether the link is active
        ExpiresAt: Optional expiration timestamp
        LastAccessedAt: Optional last access time (public resolve)
        CreatedDate: When the link was created
        CreatedBy: User who created the link (authenticated)
    """

    __tablename__ = "FormPublicLink"
    __table_args__ = {"schema": "dbo"}

    FormPublicLinkID = Column(BigInteger, primary_key=True, autoincrement=True)

    FormID = Column(BigInteger, ForeignKey("dbo.Form.FormID"), nullable=False, index=True)
    Token = Column(String(255), nullable=False, unique=True, index=True)
    LinkType = Column(String(20), nullable=False)  # PREVIEW | PRODUCTION

    IsActive = Column(Boolean, nullable=False, server_default="1")
    ExpiresAt = Column(DateTime, nullable=True)
    LastAccessedAt = Column(DateTime, nullable=True)

    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=True)

    # Relationships
    form = relationship("Form", backref="public_links")
    creator = relationship("User", foreign_keys=[CreatedBy], backref="form_public_links_created")

    def __repr__(self) -> str:
        return f"<FormPublicLink(ID={self.FormPublicLinkID}, FormID={self.FormID}, LinkType={self.LinkType})>"

