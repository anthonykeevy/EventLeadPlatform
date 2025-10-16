"""
EmailDelivery Model (log.EmailDelivery)
Email delivery tracking and monitoring
"""
from sqlalchemy import Column, BigInteger, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base


class EmailDelivery(Base):
    """
    Email delivery log model.
    
    Tracks email delivery status, opens, clicks for transactional emails.
    Email types: verification, password_reset, invitation, notification
    Status: pending, sent, delivered, opened, clicked, bounced, failed
    
    Attributes:
        EmailDeliveryID: Primary key
        EmailType: Type of email (verification, password_reset, invitation, etc.)
        RecipientEmail: Email address of recipient
        Subject: Email subject line
        Status: Delivery status (pending, sent, delivered, opened, clicked, bounced, failed)
        ProviderMessageID: Message ID from email provider (e.g., SendGrid, AWS SES)
        ErrorMessage: Error message if delivery failed
        SentAt: Timestamp when email was sent
        DeliveredAt: Timestamp when email was delivered
        OpenedAt: Timestamp when email was opened (if tracking enabled)
        ClickedAt: Timestamp when link was clicked (if tracking enabled)
        UserID: Foreign key to dbo.User (nullable for pre-signup emails)
        CompanyID: Foreign key to dbo.Company (nullable)
        CreatedDate: Timestamp when email was queued
    """
    
    __tablename__ = "EmailDelivery"
    __table_args__ = {"schema": "log"}
    
    # Primary Key
    EmailDeliveryID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Email Details
    EmailType = Column(String(50), nullable=False)
    RecipientEmail = Column(String(255), nullable=False, index=True)
    Subject = Column(String(255), nullable=False)
    
    # Delivery Status
    Status = Column(String(50), nullable=False, index=True)
    ProviderMessageID = Column(String(255), nullable=True)
    ErrorMessage = Column(String(None), nullable=True)  # NVARCHAR(MAX)
    
    # Delivery Tracking
    SentAt = Column(DateTime, nullable=True)
    DeliveredAt = Column(DateTime, nullable=True)
    OpenedAt = Column(DateTime, nullable=True)
    ClickedAt = Column(DateTime, nullable=True)
    
    # User Context
    UserID = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=True)
    
    # Timestamp
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), index=True)
    
    # Relationships
    user = relationship("User", back_populates="email_deliveries")
    company = relationship("Company", back_populates="email_deliveries")
    
    def __repr__(self) -> str:
        return f"<EmailDelivery(EmailDeliveryID={self.EmailDeliveryID}, EmailType='{self.EmailType}', RecipientEmail='{self.RecipientEmail}', Status='{self.Status}')>"

