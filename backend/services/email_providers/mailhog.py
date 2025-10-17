"""
MailHog Email Provider
Development email provider using MailHog SMTP server
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional


class TransientEmailError(Exception):
    """Transient email error (connection timeout, temporary failure) - can retry"""
    pass


class PermanentEmailError(Exception):
    """Permanent email error (invalid email, auth failure) - don't retry"""
    pass


class EmailProvider:
    """Abstract base class for email providers"""
    
    async def send(
        self,
        to: str,
        subject: str,
        html_body: str,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None
    ) -> bool:
        """
        Send email via provider.
        
        Args:
            to: Recipient email address
            subject: Email subject line
            html_body: HTML email body
            from_email: From email address (optional)
            from_name: From name (optional)
            
        Returns:
            True if email sent successfully
            
        Raises:
            TransientEmailError: Temporary failure (can retry)
            PermanentEmailError: Permanent failure (don't retry)
        """
        raise NotImplementedError


class MailHogProvider(EmailProvider):
    """
    MailHog email provider for development/testing.
    
    MailHog captures all outgoing emails so developers can verify content
    without sending real emails. Access MailHog UI at http://localhost:8025
    
    Attributes:
        host: MailHog SMTP host (default: "localhost")
        port: MailHog SMTP port (default: 1025)
    """
    
    def __init__(self, host: str = "localhost", port: int = 1025):
        """
        Initialize MailHog provider.
        
        Args:
            host: MailHog SMTP server host
            port: MailHog SMTP server port
        """
        self.host = host
        self.port = port
    
    async def send(
        self,
        to: str,
        subject: str,
        html_body: str,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None
    ) -> bool:
        """
        Send email via MailHog SMTP (no authentication required).
        
        Args:
            to: Recipient email address
            subject: Email subject line
            html_body: HTML email body
            from_email: From email address
            from_name: From name
            
        Returns:
            True if email sent successfully
            
        Raises:
            TransientEmailError: If MailHog connection fails
        """
        from_email = from_email or "noreply@eventlead.com"
        from_name = from_name or "EventLead Platform"
        
        # Create MIME message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{from_name} <{from_email}>"
        msg["To"] = to
        
        # Attach HTML body
        html_part = MIMEText(html_body, "html")
        msg.attach(html_part)
        
        # Send via SMTP (no auth needed for MailHog)
        try:
            with smtplib.SMTP(self.host, self.port, timeout=10) as server:
                server.send_message(msg)
            return True
        except smtplib.SMTPException as e:
            raise TransientEmailError(f"MailHog SMTP error: {str(e)}")
        except ConnectionRefusedError:
            raise TransientEmailError(
                f"MailHog connection refused on {self.host}:{self.port}. "
                f"Is MailHog running? Start with: docker-compose up mailhog"
            )
        except TimeoutError:
            raise TransientEmailError(f"MailHog connection timeout on {self.host}:{self.port}")
        except Exception as e:
            raise TransientEmailError(f"MailHog connection failed: {str(e)}")


