"""
Email Service
Main email service with provider abstraction, template rendering,
automatic logging, and retry logic
"""
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, UndefinedError

from backend.common.database import SessionLocal
from backend.common.request_context import get_current_request_context
from backend.models.log.email_delivery import EmailDelivery
from backend.services.email_providers import EmailProvider, MailHogProvider, SMTPProvider
from backend.services.email_providers.mailhog import TransientEmailError, PermanentEmailError
from backend.config.email import EmailConfig


class EmailService:
    """
    Email service with provider abstraction.
    
    Features:
    - Multiple provider support (MailHog, SMTP)
    - Jinja2 template rendering with variable substitution
    - Automatic delivery logging to log.EmailDelivery
    - Integration with request context (RequestID, UserID, CompanyID)
    - Retry logic with exponential backoff
    - Async/non-blocking email sending
    
    Attributes:
        provider: Email provider instance (MailHogProvider or SMTPProvider)
        config: Email configuration
    """
    
    def __init__(self, provider: EmailProvider, config: EmailConfig):
        """
        Initialize email service.
        
        Args:
            provider: Email provider instance
            config: Email configuration
        """
        self.provider = provider
        self.config = config
        
        # Initialize Jinja2 template environment
        self.template_env = Environment(
            loader=FileSystemLoader("backend/templates/emails"),
            autoescape=True,  # Auto-escape HTML for security
            undefined=UndefinedError  # Raise error for undefined variables
        )
    
    async def send_email(
        self,
        to: str,
        subject: str,
        template_name: str,
        template_vars: Dict[str, Any],
        from_email: Optional[str] = None,
        from_name: Optional[str] = None
    ) -> bool:
        """
        Send email with automatic logging and retry.
        
        Args:
            to: Recipient email address
            subject: Email subject line
            template_name: Template filename (without .html extension)
            template_vars: Dictionary of template variables
            from_email: From email address (optional, uses config default)
            from_name: From name (optional, uses config default)
            
        Returns:
            True if email sent successfully, False otherwise
            
        Example:
            email_service = get_email_service()
            await email_service.send_email(
                to="user@example.com",
                subject="Welcome to EventLead!",
                template_name="welcome",
                template_vars={"user_name": "John", "verification_url": "..."}
            )
        """
        # Get request context (for RequestID, UserID, CompanyID)
        try:
            context = get_current_request_context()
            request_id = context.request_id
            user_id = context.user_id
            company_id = context.company_id
        except (RuntimeError, AttributeError):
            # No request context (background job, CLI, etc.)
            request_id = None
            user_id = None
            company_id = None
        
        # Use config defaults if not provided
        from_email = from_email or self.config.from_email
        from_name = from_name or self.config.from_name
        
        # Render email template
        try:
            html_body = self._render_template(template_name, template_vars)
        except TemplateNotFound:
            raise ValueError(f"Email template not found: {template_name}.html")
        except UndefinedError as e:
            raise ValueError(f"Template variable error: {str(e)}")
        
        # Log email delivery attempt (PENDING)
        delivery_id = self._log_email(
            to=to,
            subject=subject,
            template_name=template_name,
            status="pending",
            request_id=request_id,
            user_id=user_id,
            company_id=company_id
        )
        
        # Send email with retry logic
        try:
            success = await self._send_with_retry(
                to=to,
                subject=subject,
                html_body=html_body,
                from_email=from_email,
                from_name=from_name,
                max_retries=5
            )
            
            # Update log (SENT)
            self._update_email_log(delivery_id, status="sent", sent_at=datetime.utcnow())
            return True
            
        except (TransientEmailError, PermanentEmailError) as e:
            # Update log (FAILED)
            self._update_email_log(
                delivery_id,
                status="failed",
                error_message=str(e)
            )
            return False
        except Exception as e:
            # Unexpected error
            self._update_email_log(
                delivery_id,
                status="failed",
                error_message=f"Unexpected error: {str(e)}"
            )
            return False
    
    def _render_template(self, template_name: str, variables: Dict[str, Any]) -> str:
        """
        Render Jinja2 email template with variables.
        
        Args:
            template_name: Template filename (without .html)
            variables: Dictionary of template variables
            
        Returns:
            Rendered HTML string
            
        Raises:
            TemplateNotFound: If template doesn't exist
            UndefinedError: If required variable is missing
        """
        template = self.template_env.get_template(f"{template_name}.html")
        return template.render(**variables)
    
    async def _send_with_retry(
        self,
        to: str,
        subject: str,
        html_body: str,
        from_email: str,
        from_name: str,
        max_retries: int = 5
    ) -> bool:
        """
        Send email with exponential backoff retry.
        
        Retry logic:
        - Transient errors: Retry up to max_retries with exponential backoff (1s, 2s, 4s, 8s, 16s)
        - Permanent errors: Don't retry
        
        Args:
            to: Recipient email address
            subject: Email subject line
            html_body: Rendered HTML body
            from_email: From email address
            from_name: From name
            max_retries: Maximum retry attempts
            
        Returns:
            True if email sent successfully
            
        Raises:
            TransientEmailError: If all retries exhausted
            PermanentEmailError: If permanent error (no retries)
        """
        for attempt in range(max_retries):
            try:
                success = await self.provider.send(
                    to=to,
                    subject=subject,
                    html_body=html_body,
                    from_email=from_email,
                    from_name=from_name
                )
                return success
                
            except TransientEmailError as e:
                # Retry transient errors (connection timeout, rate limit, etc.)
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s, 8s, 16s
                    await asyncio.sleep(wait_time)
                else:
                    # All retries exhausted
                    raise TransientEmailError(f"All retries exhausted: {str(e)}")
                    
            except PermanentEmailError:
                # Don't retry permanent errors (invalid email, auth failure, etc.)
                raise
    
    def _log_email(
        self,
        to: str,
        subject: str,
        template_name: str,
        status: str,
        request_id: Optional[str] = None,
        user_id: Optional[int] = None,
        company_id: Optional[int] = None
    ) -> int:
        """
        Log email delivery to log.EmailDelivery table.
        
        Args:
            to: Recipient email address
            subject: Email subject
            template_name: Template name
            status: Delivery status (pending, sent, failed)
            request_id: Request ID from context
            user_id: User ID from context
            company_id: Company ID from context
            
        Returns:
            EmailDeliveryID of created log record
        """
        db = SessionLocal()
        try:
            email_log = EmailDelivery(
                EmailType=template_name,
                RecipientEmail=to,
                Subject=subject,
                Status=status,
                UserID=user_id,
                CompanyID=company_id,
                # Note: log.EmailDelivery doesn't have RequestID field in the model
                # If needed, we can extend the model in future
            )
            
            db.add(email_log)
            db.commit()
            db.refresh(email_log)
            
            return email_log.EmailDeliveryID
            
        except Exception as e:
            db.rollback()
            # Log error but don't fail email sending
            print(f"Error logging email delivery: {str(e)}")
            return -1
        finally:
            db.close()
    
    def _update_email_log(
        self,
        delivery_id: int,
        status: str,
        sent_at: Optional[datetime] = None,
        error_message: Optional[str] = None
    ) -> None:
        """
        Update email delivery log status.
        
        Args:
            delivery_id: EmailDeliveryID to update
            status: New delivery status
            sent_at: Timestamp when sent (for "sent" status)
            error_message: Error message (for "failed" status)
        """
        if delivery_id <= 0:
            return  # Skip if logging failed
        
        db = SessionLocal()
        try:
            email_log = db.get(EmailDelivery, delivery_id)
            if email_log:
                email_log.Status = status
                if sent_at:
                    email_log.SentAt = sent_at
                if error_message:
                    email_log.ErrorMessage = error_message[:1000]  # Truncate if too long
                
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error updating email delivery log: {str(e)}")
        finally:
            db.close()


    async def send_password_reset_email(
        self,
        to: str,
        user_name: str,
        reset_link: str
    ) -> bool:
        """
        Send password reset email with reset link.
        
        Args:
            to: Recipient email address
            user_name: User's name for personalization
            reset_link: Password reset URL with token
            
        Returns:
            True if email sent successfully, False otherwise
            
        Example:
            email_service = get_email_service()
            await email_service.send_password_reset_email(
                to="user@example.com",
                user_name="John Doe",
                reset_link="https://app.example.com/reset-password?token=abc123"
            )
        """
        return await self.send_email(
            to=to,
            subject="Reset Your Password",
            template_name="password_reset",
            template_vars={
                "user_name": user_name,
                "reset_link": reset_link
            }
        )
    
    async def send_team_invitation_email(
        self,
        to: str,
        invitee_name: str,
        inviter_name: str,
        company_name: str,
        role_name: str,
        invitation_url: str,
        expiry_days: int = 7
    ) -> bool:
        """
        Send team invitation email with invitation link.
        
        Args:
            to: Recipient email address
            invitee_name: Name of person being invited
            inviter_name: Name of person sending invitation
            company_name: Company name
            role_name: Role being assigned
            invitation_url: Invitation acceptance URL with token
            expiry_days: Days until invitation expires
            
        Returns:
            True if email sent successfully, False otherwise
            
        Example:
            email_service = get_email_service()
            await email_service.send_team_invitation_email(
                to="jane@example.com",
                invitee_name="Jane Smith",
                inviter_name="John Doe",
                company_name="Acme Events",
                role_name="Team Member",
                invitation_url="https://app.example.com/invitations/accept?token=abc123",
                expiry_days=7
            )
        """
        return await self.send_email(
            to=to,
            subject=f"{inviter_name} invited you to join {company_name}",
            template_name="team_invitation",
            template_vars={
                "invitee_name": invitee_name,
                "inviter_name": inviter_name,
                "company_name": company_name,
                "role_name": role_name,
                "invitation_url": invitation_url,
                "expiry_days": expiry_days
            }
        )


def get_email_service() -> EmailService:
    """
    Factory function to create configured EmailService.
    
    Loads configuration from environment variables and creates
    appropriate provider (MailHog for dev, SMTP for prod).
    
    Returns:
        Configured EmailService instance
        
    Raises:
        ValueError: If configuration is invalid
        
    Example:
        email_service = get_email_service()
        await email_service.send_email(...)
    """
    # Load configuration from environment
    config = EmailConfig.from_env()
    
    # Create appropriate provider
    if config.provider == "mailhog":
        provider = MailHogProvider(config.mailhog_host, config.mailhog_port)
    elif config.provider == "smtp":
        provider = SMTPProvider(
            host=config.smtp_host,
            port=config.smtp_port,
            username=config.smtp_username,
            password=config.smtp_password,
            use_tls=config.smtp_use_tls
        )
    else:
        raise ValueError(f"Unknown email provider: {config.provider}")
    
    return EmailService(provider, config)

