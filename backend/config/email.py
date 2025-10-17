"""
Email Configuration
Manages email provider configuration from environment variables
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class EmailConfig:
    """
    Email configuration loaded from environment variables.
    
    Attributes:
        provider: Email provider ("mailhog" for dev, "smtp" for prod)
        from_email: Default from email address
        from_name: Default from name
        mailhog_host: MailHog SMTP host (dev)
        mailhog_port: MailHog SMTP port (dev)
        smtp_host: SMTP server host (prod)
        smtp_port: SMTP server port (prod)
        smtp_username: SMTP authentication username (prod)
        smtp_password: SMTP authentication password (prod)
        smtp_use_tls: Use TLS for SMTP (prod)
    """
    provider: str
    from_email: str
    from_name: str = "EventLead Platform"
    
    # MailHog config (development)
    mailhog_host: str = "localhost"
    mailhog_port: int = 1025
    
    # SMTP config (production)
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_use_tls: bool = True
    
    @classmethod
    def from_env(cls) -> "EmailConfig":
        """
        Load email configuration from environment variables.
        
        Environment Variables:
            EMAIL_PROVIDER: "mailhog" or "smtp" (default: "mailhog")
            EMAIL_FROM: From email address (default: "noreply@eventlead.com")
            EMAIL_FROM_NAME: From name (default: "EventLead Platform")
            MAILHOG_HOST: MailHog host (default: "localhost")
            MAILHOG_PORT: MailHog port (default: "1025")
            SMTP_HOST: SMTP server host
            SMTP_PORT: SMTP server port (default: "587")
            SMTP_USERNAME: SMTP username
            SMTP_PASSWORD: SMTP password
            SMTP_USE_TLS: Use TLS (default: "true")
        
        Returns:
            EmailConfig instance
            
        Raises:
            ValueError: If SMTP provider selected but required config missing
        """
        provider = os.getenv("EMAIL_PROVIDER", "mailhog").lower()
        
        config = cls(
            provider=provider,
            from_email=os.getenv("EMAIL_FROM", "noreply@eventlead.com"),
            from_name=os.getenv("EMAIL_FROM_NAME", "EventLead Platform"),
            mailhog_host=os.getenv("MAILHOG_HOST", "localhost"),
            mailhog_port=int(os.getenv("MAILHOG_PORT", "1025")),
        )
        
        if provider == "smtp":
            config.smtp_host = os.getenv("SMTP_HOST")
            config.smtp_port = int(os.getenv("SMTP_PORT", "587"))
            config.smtp_username = os.getenv("SMTP_USERNAME")
            config.smtp_password = os.getenv("SMTP_PASSWORD")
            config.smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
            
            # Validate required SMTP config
            if not all([config.smtp_host, config.smtp_username, config.smtp_password]):
                raise ValueError(
                    "SMTP provider requires SMTP_HOST, SMTP_USERNAME, and SMTP_PASSWORD environment variables"
                )
        
        return config


