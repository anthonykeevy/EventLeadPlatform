"""
Email Service - Epic 1
Handles email sending for user verification, password reset, and notifications
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
try:
    from jinja2 import Environment, FileSystemLoader
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False
    Environment = None
    FileSystemLoader = None
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """Email service for Epic 1"""
    
    def __init__(self):
        # Email configuration - MailHog for development, configurable for production
        environment = os.getenv("ENVIRONMENT", "development")
        
        if environment == "development":
            # MailHog configuration for development
            self.smtp_server = os.getenv("SMTP_SERVER", "localhost")
            self.smtp_port = int(os.getenv("SMTP_PORT", "1025"))
            self.smtp_username = os.getenv("SMTP_USERNAME", "")  # MailHog doesn't require auth
            self.smtp_password = os.getenv("SMTP_PASSWORD", "")  # MailHog doesn't require auth
            self.use_tls = False  # MailHog doesn't use TLS
        else:
            # Production email configuration
            self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
            self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
            self.smtp_username = os.getenv("SMTP_USERNAME", "")
            self.smtp_password = os.getenv("SMTP_PASSWORD", "")
            self.use_tls = True  # Production SMTP typically uses TLS
        
        self.from_email = os.getenv("FROM_EMAIL", "noreply@eventlead.com")
        self.from_name = os.getenv("FROM_NAME", "EventLead Platform")
        self.environment = environment
        
        # Template environment
        if JINJA2_AVAILABLE:
            template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
            self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        else:
            self.jinja_env = None
    
    async def send_verification_email(self, email: str, verification_token: str, user_name: Optional[str] = None) -> bool:
        """
        Send email verification email
        
        Args:
            email: User's email address
            verification_token: Secure verification token
            user_name: User's name (optional)
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Generate verification URL
            base_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
            verification_url = f"{base_url}/verify-email?token={verification_token}"
            
            # Render email template
            if self.jinja_env:
                template = self.jinja_env.get_template("emails/email_verification.html")
                html_content = template.render(
                    user_name=user_name or "User",
                    verification_url=verification_url,
                    support_email=os.getenv("SUPPORT_EMAIL", "support@eventlead.com")
                )
            else:
                # Fallback simple HTML template
                html_content = f"""
                <html>
                <body>
                    <h2>Verify Your Email - EventLead Platform</h2>
                    <p>Hello {user_name or 'User'},</p>
                    <p>Please click the link below to verify your email:</p>
                    <p><a href="{verification_url}">Verify Email</a></p>
                    <p>This link expires in 24 hours.</p>
                </body>
                </html>
                """
            
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Verify Your Email - EventLead Platform"
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = email
            
            # Add HTML content
            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)
            
            # Send email
            return await self._send_email(msg, email)
            
        except Exception as e:
            logger.error(f"Failed to send verification email to {email}: {str(e)}")
            return False
    
    async def send_password_reset_email(self, email: str, reset_token: str, user_name: Optional[str] = None) -> bool:
        """
        Send password reset email
        
        Args:
            email: User's email address
            reset_token: Secure reset token
            user_name: User's name (optional)
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Generate reset URL
            base_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
            reset_url = f"{base_url}/reset-password?token={reset_token}"
            
            # Render email template
            if self.jinja_env:
                template = self.jinja_env.get_template("emails/password_reset.html")
                html_content = template.render(
                    user_name=user_name or "User",
                    reset_url=reset_url,
                    support_email=os.getenv("SUPPORT_EMAIL", "support@eventlead.com")
                )
            else:
                # Fallback simple HTML template
                html_content = f"""
                <html>
                <body>
                    <h2>Reset Your Password - EventLead Platform</h2>
                    <p>Hello {user_name or 'User'},</p>
                    <p>Please click the link below to reset your password:</p>
                    <p><a href="{reset_url}">Reset Password</a></p>
                    <p>This link expires in 1 hour.</p>
                </body>
                </html>
                """
            
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Reset Your Password - EventLead Platform"
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = email
            
            # Add HTML content
            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)
            
            # Send email
            return await self._send_email(msg, email)
            
        except Exception as e:
            logger.error(f"Failed to send password reset email to {email}: {str(e)}")
            return False
    
    async def _send_email(self, msg: MIMEMultipart, to_email: str) -> bool:
        """
        Send email via SMTP (MailHog for development, production SMTP for production)
        
        Args:
            msg: Email message
            to_email: Recipient email address
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Send email via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                # Use TLS only for production
                if self.use_tls:
                    server.starttls()
                
                # Authenticate only if credentials are provided
                if self.smtp_username and self.smtp_password:
                    server.login(self.smtp_username, self.smtp_password)
                
                # Send the email
                server.send_message(msg)
            
            if self.environment == "development":
                logger.info(f"Email sent to MailHog: {to_email}")
                logger.info(f"Subject: {msg['Subject']}")
                logger.info(f"View at: http://localhost:8025")
            else:
                logger.info(f"Email sent successfully to {to_email}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            
            # In development, if MailHog is not running, log the email content
            if self.environment == "development":
                logger.warning("MailHog may not be running. Email content:")
                logger.warning(f"To: {to_email}")
                logger.warning(f"Subject: {msg['Subject']}")
                logger.warning(f"Content: {msg.as_string()}")
                return True  # Return True in development even if MailHog is down
            
            return False

# Global email service instance
email_service = EmailService()
