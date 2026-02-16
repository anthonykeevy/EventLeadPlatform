"""
FormTestRun Model (dbo.FormTestRun)
Story 5.5: Explicit 'Record test run' audit for forms without submission.
"""
from sqlalchemy import Column, BigInteger, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from common.database import Base


class FormTestRun(Base):
    """
    Records explicit 'Record test run' actions (who, when, form version).
    Counted toward test threshold alongside preview submissions.
    """

    __tablename__ = "FormTestRun"
    __table_args__ = {"schema": "dbo"}

    FormTestRunID = Column(BigInteger, primary_key=True, autoincrement=True)
    FormID = Column(BigInteger, ForeignKey("dbo.Form.FormID"), nullable=False, index=True)
    FormVersionID = Column(BigInteger, ForeignKey("dbo.FormVersion.FormVersionID"), nullable=False)
    CompanyID = Column(BigInteger, ForeignKey("dbo.Company.CompanyID"), nullable=False)
    RecordedBy = Column(BigInteger, ForeignKey("dbo.User.UserID"), nullable=False)
    RecordedAt = Column(DateTime, nullable=False, server_default=func.getutcdate())

    form = relationship("Form", foreign_keys=[FormID])
    form_version = relationship("FormVersion", foreign_keys=[FormVersionID])
    company = relationship("Company", foreign_keys=[CompanyID])
    recorded_by_user = relationship("User", foreign_keys=[RecordedBy])
