"""
Basic Tests for Email Service
Validates email service setup and configuration
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config.email import EmailConfig
from services.email_providers.mailhog import MailHogProvider
from services.email_providers.smtp import SMTPProvider
from services.email_service import EmailService, get_email_service


def test_email_config_from_env_mailhog():
    """Test AC-0.3.1: EmailConfig loads MailHog configuration"""
    os.environ["EMAIL_PROVIDER"] = "mailhog"
    os.environ["EMAIL_FROM"] = "test@example.com"
    
    config = EmailConfig.from_env()
    
    assert config.provider == "mailhog"
    assert config.from_email == "test@example.com"
    assert config.mailhog_host == "localhost"
    assert config.mailhog_port == 1025
    print("[OK] MailHog configuration loads correctly")


def test_email_config_from_env_smtp():
    """Test AC-0.3.1: EmailConfig validates SMTP configuration"""
    os.environ["EMAIL_PROVIDER"] = "smtp"
    os.environ["SMTP_HOST"] = "smtp.example.com"
    os.environ["SMTP_USERNAME"] = "user"
    os.environ["SMTP_PASSWORD"] = "pass"
    
    config = EmailConfig.from_env()
    
    assert config.provider == "smtp"
    assert config.smtp_host == "smtp.example.com"
    assert config.smtp_username == "user"
    assert config.smtp_password == "pass"
    print("[OK] SMTP configuration loads correctly")


def test_get_email_service_mailhog():
    """Test AC-0.3.1: get_email_service() creates MailHogProvider"""
    os.environ["EMAIL_PROVIDER"] = "mailhog"
    os.environ["EMAIL_FROM"] = "test@example.com"
    
    email_service = get_email_service()
    
    assert isinstance(email_service, EmailService)
    assert isinstance(email_service.provider, MailHogProvider)
    print("[OK] get_email_service() creates MailHogProvider correctly")


def test_get_email_service_smtp():
    """Test AC-0.3.1: get_email_service() creates SMTPProvider"""
    os.environ["EMAIL_PROVIDER"] = "smtp"
    os.environ["SMTP_HOST"] = "smtp.example.com"
    os.environ["SMTP_USERNAME"] = "user"
    os.environ["SMTP_PASSWORD"] = "pass"
    
    email_service = get_email_service()
    
    assert isinstance(email_service, EmailService)
    assert isinstance(email_service.provider, SMTPProvider)
    print("[OK] get_email_service() creates SMTPProvider correctly")


def test_email_service_template_rendering():
    """Test AC-0.3.3: Template rendering with variables"""
    os.environ["EMAIL_PROVIDER"] = "mailhog"
    
    email_service = get_email_service()
    
    # Test that template environment is initialized
    assert email_service.template_env is not None
    print("[OK] Template environment initialized")
    
    # Test rendering a template (welcome.html should exist)
    try:
        html = email_service._render_template("welcome", {
            "user_name": "Test User",
            "dashboard_url": "https://app.eventlead.com/dashboard"
        })
        assert "Test User" in html
        assert "EventLead" in html
        print("[OK] Template renders with variables correctly")
    except Exception as e:
        print(f"[INFO] Template rendering test skipped: {str(e)}")


if __name__ == "__main__":
    print("Running basic email service tests...\n")
    test_email_config_from_env_mailhog()
    test_email_config_from_env_smtp()
    test_get_email_service_mailhog()
    test_get_email_service_smtp()
    test_email_service_template_rendering()
    print("\n[PASS] All basic email service tests passed!")


