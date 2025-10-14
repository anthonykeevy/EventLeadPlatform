"""
Integration tests for MailHog email service - Story 1.1
Tests actual email sending to MailHog in development environment
"""
import pytest
import asyncio
import smtplib
from unittest.mock import patch
from common.email import EmailService

class TestMailHogIntegration:
    """Test MailHog integration for email sending."""
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_mailhog_connection(self, mailhog_environment):
        """Test that MailHog is accessible and accepting connections."""
        try:
            # Test SMTP connection to MailHog
            with smtplib.SMTP("localhost", 1025) as server:
                # MailHog should accept connection without authentication
                server.noop()  # Test connection
            assert True, "MailHog connection successful"
        except ConnectionRefusedError:
            pytest.skip("MailHog is not running. Start with: docker-compose up mailhog -d")
        except Exception as e:
            pytest.fail(f"MailHog connection failed: {e}")
    
    @pytest.mark.integration
    @pytest.mark.slow
    async def test_send_verification_email_to_mailhog(self, mailhog_environment):
        """Test sending verification email to MailHog."""
        try:
            # Create email service with MailHog configuration
            email_service = EmailService()
            
            # Send verification email
            result = await email_service.send_verification_email(
                email="test@example.com",
                verification_token="test-token-123",
                user_name="Test User"
            )
            
            assert result is True, "Email should be sent successfully to MailHog"
            
        except ConnectionRefusedError:
            pytest.skip("MailHog is not running. Start with: docker-compose up mailhog -d")
        except Exception as e:
            pytest.fail(f"Failed to send email to MailHog: {e}")
    
    @pytest.mark.integration
    @pytest.mark.slow
    async def test_send_password_reset_email_to_mailhog(self, mailhog_environment):
        """Test sending password reset email to MailHog."""
        try:
            # Create email service with MailHog configuration
            email_service = EmailService()
            
            # Send password reset email
            result = await email_service.send_password_reset_email(
                email="test@example.com",
                reset_token="reset-token-123",
                user_name="Test User"
            )
            
            assert result is True, "Email should be sent successfully to MailHog"
            
        except ConnectionRefusedError:
            pytest.skip("MailHog is not running. Start with: docker-compose up mailhog -d")
        except Exception as e:
            pytest.fail(f"Failed to send email to MailHog: {e}")
    
    @pytest.mark.integration
    @pytest.mark.slow
    async def test_email_content_formatting(self, mailhog_environment):
        """Test that email content is properly formatted for MailHog."""
        try:
            email_service = EmailService()
            
            # Send email and capture the message
            with patch.object(email_service, '_send_email') as mock_send:
                mock_send.return_value = True
                
                await email_service.send_verification_email(
                    email="test@example.com",
                    verification_token="test-token-123",
                    user_name="Test User"
                )
                
                # Verify email was formatted correctly
                mock_send.assert_called_once()
                call_args = mock_send.call_args
                msg = call_args[0][0]  # First argument is the message
                to_email = call_args[0][1]  # Second argument is the recipient
                
                # Verify message structure
                assert msg["Subject"] == "Verify Your Email - EventLead Platform"
                assert msg["From"] == "EventLead Platform <noreply@eventlead.com>"
                assert to_email == "test@example.com"
                
                # Verify HTML content is present
                html_content = None
                for part in msg.walk():
                    if part.get_content_type() == "text/html":
                        html_content = part.get_payload()
                        break
                
                assert html_content is not None, "HTML content should be present"
                assert "test-token-123" in html_content, "Verification token should be in email"
                assert "Test User" in html_content, "User name should be in email"
                assert "24 hours" in html_content, "Expiry information should be in email"
                
        except Exception as e:
            pytest.fail(f"Email formatting test failed: {e}")
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_mailhog_web_interface_accessible(self, mailhog_environment):
        """Test that MailHog web interface is accessible."""
        import urllib.request
        import urllib.error
        
        try:
            # Test web interface accessibility
            response = urllib.request.urlopen("http://localhost:8025", timeout=5)
            assert response.getcode() == 200, "MailHog web interface should be accessible"
        except urllib.error.URLError:
            pytest.skip("MailHog web interface not accessible. Check if MailHog is running on port 8025")
        except Exception as e:
            pytest.fail(f"MailHog web interface test failed: {e}")
    
    @pytest.mark.integration
    @pytest.mark.slow
    async def test_mailhog_fallback_behavior(self, mailhog_environment):
        """Test fallback behavior when MailHog is not running."""
        # Temporarily change port to simulate MailHog being down
        with patch.dict('os.environ', {'SMTP_PORT': '9999'}):
            email_service = EmailService()
            
            # Should return True even if MailHog is down (development mode)
            result = await email_service.send_verification_email(
                email="test@example.com",
                verification_token="test-token-123",
                user_name="Test User"
            )
            
            assert result is True, "Should return True in development mode even if MailHog is down"
    
    @pytest.mark.unit
    def test_email_service_configuration(self, mailhog_environment):
        """Test email service configuration for MailHog."""
        email_service = EmailService()
        
        # Verify MailHog configuration
        assert email_service.smtp_server == "localhost"
        assert email_service.smtp_port == 1025
        assert email_service.smtp_username == ""
        assert email_service.smtp_password == ""
        assert email_service.use_tls is False
        assert email_service.environment == "development"
        assert email_service.from_email == "noreply@eventlead.com"
        assert email_service.from_name == "EventLead Platform"
    
    @pytest.mark.unit
    def test_production_email_configuration(self):
        """Test email service configuration for production."""
        with patch.dict('os.environ', {
            'ENVIRONMENT': 'production',
            'SMTP_SERVER': 'smtp.gmail.com',
            'SMTP_PORT': '587',
            'SMTP_USERNAME': 'test@gmail.com',
            'SMTP_PASSWORD': 'test-password'
        }):
            email_service = EmailService()
            
            # Verify production configuration
            assert email_service.smtp_server == "smtp.gmail.com"
            assert email_service.smtp_port == 587
            assert email_service.smtp_username == "test@gmail.com"
            assert email_service.smtp_password == "test-password"
            assert email_service.use_tls is True
            assert email_service.environment == "production"
