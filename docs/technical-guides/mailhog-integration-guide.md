# MailHog Integration Guide

## Overview

MailHog is a local SMTP server that captures emails during development and testing. It provides a web interface to view captured emails without actually sending them to real email addresses.

## Docker Setup

MailHog is already configured in `docker-compose.yml`:

```yaml
services:
  mailhog:
    image: mailhog/mailhog:latest
    ports:
      - "1025:1025"  # SMTP port (for sending)
      - "8025:8025"  # HTTP port (web UI)
    container_name: eventlead-mailhog
    restart: unless-stopped
```

## Starting MailHog

```bash
# Start MailHog service
docker-compose up mailhog -d

# Check if MailHog is running
docker ps | grep mailhog
```

## Email Service Configuration

The email service is configured to use MailHog in development mode:

### Development Configuration
- **SMTP Server**: `localhost`
- **SMTP Port**: `1025`
- **Authentication**: None required
- **TLS**: Disabled
- **Web UI**: http://localhost:8025

### Environment Variables

```bash
# Development (MailHog)
ENVIRONMENT=development
SMTP_SERVER=localhost
SMTP_PORT=1025
SMTP_USERNAME=
SMTP_PASSWORD=
FROM_EMAIL=noreply@eventlead.com
FROM_NAME=EventLead Platform
```

## Using MailHog

### 1. Start MailHog
```bash
docker-compose up mailhog -d
```

### 2. Access Web Interface
Open http://localhost:8025 in your browser to view captured emails.

### 3. Test Email Sending
When you trigger email sending in the application (e.g., user signup), emails will be captured by MailHog instead of being sent to real addresses.

### 4. View Emails
- All captured emails appear in the MailHog web interface
- Click on any email to view its content
- Emails include HTML and plain text versions
- Headers and metadata are also visible

## Email Templates

The following email templates are available:

### Email Verification
- **Template**: `backend/templates/emails/email_verification.html`
- **Triggered by**: User signup
- **Contains**: Verification link with 24-hour expiry

### Password Reset
- **Template**: `backend/templates/emails/password_reset.html`
- **Triggered by**: Password reset request
- **Contains**: Reset link with 1-hour expiry

## Testing Email Functionality

### 1. User Signup Flow
```bash
# Start the application
cd backend
python -m uvicorn main:app --reload

# In another terminal, test signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 2. Check MailHog
- Open http://localhost:8025
- You should see the verification email
- Click on it to view the content and verification link

### 3. Test Verification
Copy the verification link from MailHog and test the verification endpoint.

## Production Configuration

For production, update the environment variables:

```bash
# Production SMTP
ENVIRONMENT=production
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
USE_TLS=true
```

## Troubleshooting

### MailHog Not Running
If you see connection errors:
```bash
# Check if MailHog is running
docker ps | grep mailhog

# Start MailHog if not running
docker-compose up mailhog -d

# Check logs
docker logs eventlead-mailhog
```

### Port Conflicts
If ports 1025 or 8025 are in use:
```bash
# Check what's using the ports
netstat -an | grep :1025
netstat -an | grep :8025

# Stop conflicting services or change ports in docker-compose.yml
```

### Email Not Appearing
1. Check application logs for email sending errors
2. Verify MailHog is running and accessible
3. Check environment variables are set correctly
4. Ensure the application is connecting to localhost:1025

## Benefits of MailHog

1. **No Real Emails**: Prevents accidental emails to real addresses during development
2. **Easy Testing**: View email content and formatting without external dependencies
3. **Link Testing**: Copy verification/reset links directly from the interface
4. **Debugging**: See email headers, content, and delivery status
5. **Offline Development**: Works without internet connection

## Integration with Tests

The test suite mocks the email service to prevent actual email sending during tests. In integration tests, you can:

1. Start MailHog before running tests
2. Verify emails are sent to MailHog
3. Check email content and formatting
4. Test email links and functionality

## Security Notes

- MailHog is for development only
- Never use MailHog in production
- All emails sent to MailHog are visible to anyone with access to the web interface
- Use proper SMTP authentication in production environments
