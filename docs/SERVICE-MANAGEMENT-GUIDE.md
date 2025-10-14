# Service Management Guide - EventLead Platform

## Overview
This guide provides instructions for starting, monitoring, and managing all EventLead Platform services during development.

## Available Scripts

### Service Startup
```powershell
# Start all services and check dependencies
.\scripts\start-services-clean.ps1
```

### Service Monitoring
```powershell
# Check service status
.\scripts\simple-monitor.ps1

# View service logs
.\scripts\view-logs.ps1 -Service containers    # Show running containers
.\scripts\view-logs.ps1 -Service mailhog -Lines 10  # Show MailHog logs
.\scripts\view-logs.ps1 -Service docker -Lines 20   # Show all Docker logs
```

## Service Startup Procedure

### 1. Start MailHog (Email Testing)
```powershell
# Navigate to project root
cd C:\Users\tonyk\OneDrive\Projects\EventLeadPlatform

# Start MailHog
docker-compose up mailhog -d

# Verify MailHog is running
.\scripts\view-logs.ps1 -Service containers
```

### 2. Start Backend Service
```powershell
# Navigate to backend directory
cd C:\Users\tonyk\OneDrive\Projects\EventLeadPlatform\backend

# Activate virtual environment
.\venv\Scripts\activate

# Start FastAPI server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Start Frontend Service
```powershell
# Navigate to frontend directory
cd C:\Users\tonyk\OneDrive\Projects\EventLeadPlatform\frontend

# Start Vite development server
npm run dev
```

## Service URLs

- **MailHog Web UI**: http://localhost:8025 (Email testing interface)
- **Backend API**: http://localhost:8000 (FastAPI server)
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Frontend**: http://localhost:3000 (React development server)

## Monitoring Commands

### Check Service Status
```powershell
# Run the monitoring script
.\scripts\simple-monitor.ps1
```

### View Logs
```powershell
# View MailHog logs
.\scripts\view-logs.ps1 -Service mailhog -Lines 20

# View all Docker logs
.\scripts\view-logs.ps1 -Service docker -Lines 10
```

### Manual Port Checks
```powershell
# Test MailHog Web UI
Test-NetConnection -ComputerName localhost -Port 8025

# Test MailHog SMTP
Test-NetConnection -ComputerName localhost -Port 1025

# Test Backend API
Test-NetConnection -ComputerName localhost -Port 8000

# Test Frontend
Test-NetConnection -ComputerName localhost -Port 3000
```

## Troubleshooting

### MailHog Issues
```powershell
# Check if MailHog container is running
docker ps | findstr mailhog

# Restart MailHog
docker-compose restart mailhog

# View MailHog logs
docker logs eventleads-mailhog-1
```

### Backend Issues
```powershell
# Check if virtual environment is activated
Get-Command python

# Install/update dependencies
pip install -r requirements.txt

# Check if port 8000 is available
Test-NetConnection -ComputerName localhost -Port 8000
```

### Frontend Issues
```powershell
# Check if node_modules exists
Test-Path .\frontend\node_modules

# Install dependencies
cd frontend
npm install

# Check if port 3000 is available
Test-NetConnection -ComputerName localhost -Port 3000
```

## Development Workflow

1. **Start Services**: Run `.\scripts\start-services-clean.ps1`
2. **Monitor Status**: Run `.\scripts\simple-monitor.ps1`
3. **View Logs**: Run `.\scripts\view-logs.ps1 -Service all`
4. **Begin Development**: Services are ready for Story 1.1 implementation

## Notes

- **MailHog**: Captures all emails sent during development (no real emails sent)
- **Backend**: FastAPI server with auto-reload for development
- **Frontend**: Vite development server with hot module replacement
- **Database**: SQL Server (local or Azure) - ensure connection is configured

## PowerShell Scripts Location
All service management scripts are located in the `scripts/` directory:
- `start-services-clean.ps1` - Service startup and dependency checking
- `simple-monitor.ps1` - Service status monitoring
- `view-logs.ps1` - Log viewing for Docker containers
