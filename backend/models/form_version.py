"""
FormVersion Model (dbo.FormVersion)
Manages version history for form schemas.
"""
import json
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base

class FormVersion(Base):
    """
    FormVersion model representing a snapshot of a form's design/schema.
    
    Attributes:
        FormVersionID: Primary key
        FormID: Foreign key to the parent Form
        VersionNumber: Sequential version number (1, 2, 3...)
        DefinitionJSON: The complete form schema in JSON format
        VersionComment: Optional comment describing the version changes
        Status: Current status (DRAFT, PUBLISHED, ARCHIVED)
        IsActive: Flag indicating if this is the currently live version
        CreatedDate: When this version was created
        CreatedBy: Who created this version
        PublishedDate: When this version was published (if applicable)
        PublishedBy: Who published this version (if applicable)
    """
    __tablename__ = "FormVersion"
    __table_args__ = {"schema": "dbo"}

    FormVersionID = Column(BigInteger, primary_key=True, autoincrement=True)
    FormID = Column(BigInteger, ForeignKey('dbo.Form.FormID'), nullable=False, index=True)
    VersionNumber = Column(Integer, nullable=False)
    DefinitionJSON = Column(String(None), nullable=False)  # NVARCHAR(MAX)
    VersionComment = Column(String(500), nullable=True)
    Status = Column(String(20), nullable=False, default='DRAFT') # DRAFT, PUBLISHED, ARCHIVED
    IsActive = Column(Boolean, nullable=False, default=False)
    
    # Audit fields
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    PublishedDate = Column(DateTime, nullable=True)
    PublishedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)

    # Relationships
    form = relationship("Form", backref="versions")
    created_by_user = relationship("User", foreign_keys=[CreatedBy])
    published_by_user = relationship("User", foreign_keys=[PublishedBy])

    @property
    def definition(self):
        if not self.DefinitionJSON:
            return {}
        return json.loads(self.DefinitionJSON)
    
    @definition.setter
    def definition(self, value):
        self.DefinitionJSON = json.dumps(value)

    # -------------------------------------------------------------------------
    # Pydantic / API compatibility helpers
    #
    # The API response schemas use snake_case field names (e.g. form_version_id)
    # and rely on `from_attributes=True`. The underlying SQLAlchemy model uses
    # PascalCase column attributes (e.g. FormVersionID). Provide snake_case
    # properties so FastAPI can serialize FormVersion rows reliably.
    # -------------------------------------------------------------------------

    @property
    def form_version_id(self):
        return self.FormVersionID

    @property
    def form_id(self):
        return self.FormID

    @property
    def version_number(self):
        return self.VersionNumber

    @property
    def status(self):
        return self.Status

    @property
    def is_active(self):
        return self.IsActive

    @property
    def created_date(self):
        return self.CreatedDate

    @property
    def created_by(self):
        return self.CreatedBy

    @property
    def published_date(self):
        return self.PublishedDate

    @property
    def published_by(self):
        return self.PublishedBy

    @property
    def version_comment(self):
        return self.VersionComment

    def __repr__(self):
        return f"<FormVersion(ID={self.FormVersionID}, Form={self.FormID}, v{self.VersionNumber}, Status={self.Status})>"
