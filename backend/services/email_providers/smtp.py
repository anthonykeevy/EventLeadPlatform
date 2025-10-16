"""
SMTP Email Provider
Production email provider using SMTP with TLS and authentication
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from .mailhog import EmailProvider, TransientEmailError, PermanentEmailError


class SMTPProvider(EmailProvider):
    """
    SMTP email provider for production environments.
    
    Supports TLS/SSL and authentication. Compatible with:
    - SendGrid
    - AWS SES
    - Mailgun
    - Gmail SMTP
    - Generic SMTP servers
    
    Attributes:
        host: SMTP server host
        port: SMTP server port
        username: SMTP authentication username
        password: SMTP authentication password
        use_tls: Use TLS encryption (STARTTLS)
    """
    
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        use_tls: bool = True
    ):
        """
        Initialize SMTP provider.
        
        Args:
            host: SMTP server host
            port: SMTP server port (typically 587 for TLS, 465 for SSL)
            username: SMTP authentication username
            password: SMTP authentication password
            use_tls: Use TLS encryption (STARTTLS)
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
    
    async def send(
        self,
        to: str,
        subject: str,
        html_body: str,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None
    ) -> bool:
        """
        Send email via SMTP with TLS and authentication.
        
        Args:
            to: Recipient email address
            subject: Email subject line
            html_body: HTML email body
            from_email: From email address
            from_name: From name
            
        Returns:
            True if email sent successfully
            
        Raises:
            PermanentEmailError: Authentication failure, invalid email
            TransientEmailError: Connection timeout, temporary server error
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
        
        # Send via SMTP with TLS and authentication
        try:
            if self.use_tls:
                # Use STARTTLS (port 587)
                with smtplib.SMTP(self.host, self.port, timeout=30) as server:
                    server.starttls()
                    server.login(self.username, self.password)
                    server.send_message(msg)
            else:
                # Use SSL (port 465)
                with smtplib.SMTP_SSL(self.host, self.port, timeout=30) as server:
                    server.login(self.username, self.password)
                    server.send_message(msg)
            
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            raise PermanentEmailError(f"SMTP authentication failed: {str(e)}")
        except smtplib.SMTPRecipientsRefused as e:
            raise PermanentEmailError(f"Invalid recipient email address: {str(e)}")
        except smtplib.SMTPSenderRefused as e:
            raise PermanentEmailError(f"Invalid sender email address: {str(e)}")
        except smtplib.SMTPDataError as e:
            raise PermanentEmailError(f"SMTP data error: {str(e)}")
        except smtplib.SMTPServerDisconnected as e:
            raise TransientEmailError(f"SMTP server disconnected: {str(e)}")
        except smtplib.SMTPConnectError as e:
            raise TransientEmailError(f"SMTP connection error: {str(e)}")
        except ConnectionRefusedError:
            raise TransientEmailError(f"SMTP connection refused on {self.host}:{self.port}")
        except TimeoutError:
            raise TransientEmailError(f"SMTP connection timeout on {self.host}:{self.port}")
        except smtplib.SMTPException as e:
            # Generic SMTP error - treat as transient
            raise TransientEmailError(f"SMTP error: {str(e)}")
        except Exception as e:
            raise TransientEmailError(f"Unexpected error sending email: {str(e)}")

