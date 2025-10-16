# Email Service Guide

**Status:** Implemented (Story 0.3)  
**Last Updated:** 2025-10-16

## Overview

The EventLead Platform includes a robust email service foundation that supports transactional emails with automatic delivery logging, retry logic, and template rendering.

## Features

✅ **Provider Abstraction** - Supports multiple email backends (MailHog dev, SMTP prod)  
✅ **Automatic Logging** - All email deliveries logged to `log.EmailDelivery`  
✅ **Template System** - Jinja2 templates with variable substitution  
✅ **Retry Logic** - Exponential backoff for transient failures  
✅ **Async Sending** - Non-blocking email delivery via FastAPI BackgroundTasks  
✅ **Request Context Integration** - Correlates emails with API requests via RequestID  

## Quick Start

### 1. Configuration

Add to `.env`:

```bash
# Email Provider ("mailhog" for dev, "smtp" for prod)
EMAIL_PROVIDER=mailhog
EMAIL_FROM=noreply@eventlead.com
EMAIL_FROM_NAME=EventLead Platform

# MailHog (Development)
MAILHOG_HOST=localhost
MAILHOG_PORT=1025

# SMTP (Production)  
# SMTP_HOST=smtp.sendgrid.net
# SMTP_PORT=587
# SMTP_USERNAME=apikey
# SMTP_PASSWORD=your_api_key
# SMTP_USE_TLS=true
```

### 2. Start MailHog (Development)

```bash
docker-compose up mailhog
```

Access MailHog UI: http://localhost:8025

### 3. Send an Email

```python
from fastapi import BackgroundTasks
from backend.config.email import get_email_service

@router.post("/api/auth/signup")
async def signup(request: SignupRequest, background_tasks: BackgroundTasks):
    # Create user...
    user = create_user(request)
    
    # Send welcome email (async, non-blocking)
    email_service = get_email_service()
    background_tasks.add_task(
        email_service.send_email,
        to=user.email,
        subject="Welcome to EventLead!",
        template_name="welcome",
        template_vars={
            "user_name": user.first_name,
            "dashboard_url": "https://app.eventlead.com/dashboard"
        }
    )
    
    return {"message": "Signup successful"}
```

## Architecture

### Provider Pattern

```
┌─────────────────────────────────────┐
│        EmailService                 │
│  - Template rendering (Jinja2)     │
│  - Automatic logging               │
│  - Retry logic                     │
│  - Request context integration     │
└───────────────┬─────────────────────┘
                │
    ┌───────────┴──────────┐
    │                      │
┌───▼────┐          ┌──────▼──────┐
│MailHog │          │ SMTP        │
│Provider│          │ Provider    │
│(Dev)   │          │ (Production)│
└────────┘          └─────────────┘
```

### Components

**backend/config/email.py**
- `EmailConfig` - Configuration from environment
- `get_email_service()` - Factory function

**backend/services/email_service.py**
- `EmailService` - Main service class
- Template rendering, logging, retry logic

**backend/services/email_providers/**
- `MailHogProvider` - Development provider
- `SMTPProvider` - Production provider

## Email Templates

Templates location: `backend/templates/emails/`

### Available Templates

- `welcome.html` - Welcome email
- `email_verification.html` - Email verification
- `password_reset.html` - Password reset
- `team_invitation.html` - Team invitation

### Template Variables

**email_verification.html:**
- `user_name` - User's first name
- `verification_url` - Verification link
- `expiry_hours` - Link expiration (default: 24)

**password_reset.html:**
- `user_name` - User's first name
- `reset_url` - Password reset link
- `expiry_hours` - Link expiration (default: 1)

**team_invitation.html:**
- `invitee_name` - Invitee's name
- `inviter_name` - Inviter's name
- `company_name` - Company name
- `invitation_url` - Invitation link
- `role_name` - User role
- `expiry_days` - Link expiration (default: 7)

### Base Layout

All templates extend `layouts/base.html` which includes:
- EventLead branding
- Responsive design (mobile-friendly)
- Header and footer
- Social links

## Email Delivery Logging

All email attempts are logged to `log.EmailDelivery`:

```sql
SELECT * FROM log.EmailDelivery 
WHERE RecipientEmail = 'user@example.com'
ORDER BY CreatedDate DESC;
```

**Status Values:**
- `pending` - Email queued for delivery
- `sent` - Email sent successfully
- `failed` - Email delivery failed

## Retry Logic

**Transient Failures** (connection timeout, rate limit):
- Retry up to 5 times
- Exponential backoff: 1s, 2s, 4s, 8s, 16s

**Permanent Failures** (invalid email, auth error):
- No retries
- Immediately logged as `failed`

## Error Handling

```python
try:
    success = await email_service.send_email(...)
    if success:
        print("Email sent successfully")
    else:
        print("Email failed to send")
except ValueError as e:
    # Template error (missing variable, template not found)
    print(f"Template error: {str(e)}")
```

## Production Configuration

### SendGrid Example

```bash
EMAIL_PROVIDER=smtp
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=SG.xxxxx
SMTP_USE_TLS=true
```

### AWS SES Example

```bash
EMAIL_PROVIDER=smtp
SMTP_HOST=email-smtp.us-east-1.amazonaws.com
SMTP_PORT=587
SMTP_USERNAME=your_ses_username
SMTP_PASSWORD=your_ses_password
SMTP_USE_TLS=true
```

## Troubleshooting

### MailHog Not Receiving Emails

1. Check MailHog is running: `docker ps | grep mailhog`
2. Start MailHog: `docker-compose up mailhog`
3. Check configuration: `EMAIL_PROVIDER=mailhog` in `.env`
4. Verify port 1025 is not blocked

### SMTP Authentication Failures

1. Verify credentials in environment variables
2. Check SMTP provider documentation
3. Ensure TLS/SSL settings are correct
4. Review error message in `log.EmailDelivery.ErrorMessage`

### Template Errors

1. Verify template exists in `backend/templates/emails/`
2. Check all required variables are provided
3. Review Jinja2 syntax in template

## Testing

```bash
# Basic configuration tests
python backend/tests/test_email_service_basic.py

# Integration tests with MailHog
pytest backend/tests/test_email_integration.py -v
```

## Future Enhancements

- SendGrid provider for better deliverability
- Email queue (Redis/RabbitMQ) for high volume
- Email analytics (open rates, click tracking)
- Attachment support
- Plain-text fallback
- Unsubscribe management

## References

- [Story 0.3: Email Service Foundation](../stories/story-0.3.md)
- [Story 0.2: Logging Infrastructure](../stories/story-0.2.md) - Request context integration
- [Story 0.1: Database Models](../stories/story-0.1.md) - log.EmailDelivery model

---

**Questions?** Contact the development team or reference Story 0.3 documentation.

