# EventLead Platform - Service Startup Script
# This script starts all required services for development

Write-Host "Starting EventLead Platform Services..." -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green

# Function to check if a port is in use
function Test-Port {
    param([int]$Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("localhost", $Port)
        $connection.Close()
        return $true
    }
    catch {
        return $false
    }
}

# Function to wait for service to be ready
function Wait-ForService {
    param([int]$Port, [string]$ServiceName, [int]$TimeoutSeconds = 30)
    
    Write-Host "Waiting for $ServiceName on port $Port..." -ForegroundColor Yellow
    
    $elapsed = 0
    while ($elapsed -lt $TimeoutSeconds) {
        if (Test-Port -Port $Port) {
            Write-Host "$ServiceName is ready!" -ForegroundColor Green
            return $true
        }
        Start-Sleep -Seconds 2
        $elapsed += 2
    }
    
    Write-Host "$ServiceName failed to start within $TimeoutSeconds seconds" -ForegroundColor Red
    return $false
}

# Step 1: Start MailHog
Write-Host "Starting MailHog..." -ForegroundColor Cyan
try {
    docker-compose up mailhog -d
    if (Wait-ForService -Port 8025 -ServiceName "MailHog Web UI" -TimeoutSeconds 15) {
        Write-Host "MailHog started successfully" -ForegroundColor Green
        Write-Host "   Web UI: http://localhost:8025" -ForegroundColor Blue
        Write-Host "   SMTP: localhost:1025" -ForegroundColor Blue
    } else {
        Write-Host "MailHog failed to start" -ForegroundColor Red
        Write-Host "   Try: docker-compose up mailhog -d" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Error starting MailHog: $_" -ForegroundColor Red
}

# Step 2: Check Backend Dependencies
Write-Host "`nChecking Backend Dependencies..." -ForegroundColor Cyan
$backendPath = ".\backend"
if (Test-Path $backendPath) {
    Write-Host "Backend directory found" -ForegroundColor Green
    
    $venvPath = ".\backend\venv\Scripts\activate"
    if (Test-Path $venvPath) {
        Write-Host "Virtual environment found" -ForegroundColor Green
    } else {
        Write-Host "Virtual environment not found" -ForegroundColor Red
        Write-Host "   Run: cd backend; python -m venv venv; .\venv\Scripts\activate; pip install -r requirements.txt" -ForegroundColor Yellow
    }
} else {
    Write-Host "Backend directory not found" -ForegroundColor Red
}

# Step 3: Check Frontend Dependencies
Write-Host "`nChecking Frontend Dependencies..." -ForegroundColor Cyan
$frontendPath = ".\frontend"
if (Test-Path $frontendPath) {
    Write-Host "Frontend directory found" -ForegroundColor Green
    
    $nodeModulesPath = ".\frontend\node_modules"
    if (Test-Path $nodeModulesPath) {
        Write-Host "Node modules found" -ForegroundColor Green
    } else {
        Write-Host "Node modules not found" -ForegroundColor Red
        Write-Host "   Run: cd frontend; npm install" -ForegroundColor Yellow
    }
} else {
    Write-Host "Frontend directory not found" -ForegroundColor Red
}

# Step 4: Service Status Summary
Write-Host "`nService Status Summary:" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Green

# Check MailHog
if (Test-Port -Port 8025) {
    Write-Host "MailHog Web UI (port 8025): RUNNING" -ForegroundColor Green
} else {
    Write-Host "MailHog Web UI (port 8025): NOT RUNNING" -ForegroundColor Red
}

if (Test-Port -Port 1025) {
    Write-Host "MailHog SMTP (port 1025): RUNNING" -ForegroundColor Green
} else {
    Write-Host "MailHog SMTP (port 1025): NOT RUNNING" -ForegroundColor Red
}

# Check Backend
if (Test-Port -Port 8000) {
    Write-Host "Backend API (port 8000): RUNNING" -ForegroundColor Green
} else {
    Write-Host "Backend API (port 8000): NOT RUNNING" -ForegroundColor Yellow
    Write-Host "   Start with: cd backend; .\venv\Scripts\activate; python -m uvicorn main:app --reload" -ForegroundColor Blue
}

# Check Frontend
if (Test-Port -Port 3000) {
    Write-Host "Frontend (port 3000): RUNNING" -ForegroundColor Green
} else {
    Write-Host "Frontend (port 3000): NOT RUNNING" -ForegroundColor Yellow
    Write-Host "   Start with: cd frontend; npm run dev" -ForegroundColor Blue
}

# Step 5: Next Steps
Write-Host "`nNext Steps:" -ForegroundColor Green
Write-Host "==============" -ForegroundColor Green
Write-Host "1. Start Backend: cd backend; .\venv\Scripts\activate; python -m uvicorn main:app --reload" -ForegroundColor Blue
Write-Host "2. Start Frontend: cd frontend; npm run dev" -ForegroundColor Blue
Write-Host "3. Open MailHog: http://localhost:8025" -ForegroundColor Blue
Write-Host "4. Open Frontend: http://localhost:3000" -ForegroundColor Blue
Write-Host "5. Open Backend API Docs: http://localhost:8000/docs" -ForegroundColor Blue

Write-Host "`nReady for Story 1.1 development!" -ForegroundColor Green
