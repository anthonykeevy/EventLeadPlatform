# EventLead Platform - Service Monitoring Script
# This script monitors all services and shows their status

Write-Host "📊 EventLead Platform Service Monitor" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

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

# Function to get service status
function Get-ServiceStatus {
    param([int]$Port, [string]$ServiceName, [string]$URL = "")
    
    if (Test-Port -Port $Port) {
        Write-Host "✅ $ServiceName (port $Port): RUNNING" -ForegroundColor Green
        if ($URL) {
            Write-Host "   URL: $URL" -ForegroundColor Blue
        }
        return $true
    } else {
        Write-Host "❌ $ServiceName (port $Port): NOT RUNNING" -ForegroundColor Red
        return $false
    }
}

# Function to test HTTP endpoint
function Test-HTTPEndpoint {
    param([string]$URL, [string]$ServiceName)
    
    try {
        $response = Invoke-WebRequest -Uri $URL -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ $ServiceName HTTP: RESPONDING" -ForegroundColor Green
            return $true
        } else {
            Write-Host "⚠️  $ServiceName HTTP: Status $($response.StatusCode)" -ForegroundColor Yellow
            return $false
        }
    }
    catch {
        Write-Host "❌ $ServiceName HTTP: NOT RESPONDING" -ForegroundColor Red
        return $false
    }
}

# Clear screen and show header
Clear-Host
Write-Host "📊 EventLead Platform Service Monitor" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host "Last Updated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host ""

# Check MailHog
Write-Host "📧 MailHog Email Service:" -ForegroundColor Cyan
$mailhogSMTP = Get-ServiceStatus -Port 1025 -ServiceName "MailHog SMTP"
$mailhogWeb = Get-ServiceStatus -Port 8025 -ServiceName "MailHog Web UI" -URL "http://localhost:8025"

if ($mailhogWeb) {
    Test-HTTPEndpoint -URL "http://localhost:8025" -ServiceName "MailHog Web"
}

# Check Backend
Write-Host "`n🔧 Backend API Service:" -ForegroundColor Cyan
$backend = Get-ServiceStatus -Port 8000 -ServiceName "Backend API" -URL "http://localhost:8000"

if ($backend) {
    Test-HTTPEndpoint -URL "http://localhost:8000/docs" -ServiceName "Backend API Docs"
    Test-HTTPEndpoint -URL "http://localhost:8000/api/auth/signup" -ServiceName "Auth Endpoint"
}

# Check Frontend
Write-Host "`n🎨 Frontend Service:" -ForegroundColor Cyan
$frontend = Get-ServiceStatus -Port 3000 -ServiceName "Frontend" -URL "http://localhost:3000"

if ($frontend) {
    Test-HTTPEndpoint -URL "http://localhost:3000" -ServiceName "Frontend App"
}

# Check Database
Write-Host "`n🗄️  Database Service:" -ForegroundColor Cyan
$database = Get-ServiceStatus -Port 1433 -ServiceName "SQL Server"

# Summary
Write-Host "`n📈 Service Summary:" -ForegroundColor Green
Write-Host "==================" -ForegroundColor Green

$totalServices = 4
$runningServices = 0

if ($mailhogSMTP) { $runningServices++ }
if ($mailhogWeb) { $runningServices++ }
if ($backend) { $runningServices++ }
if ($frontend) { $runningServices++ }

$percentage = [math]::Round(($runningServices / $totalServices) * 100)

Write-Host "Services Running: $runningServices/$totalServices ($percentage%)" -ForegroundColor $(if ($percentage -eq 100) { "Green" } elseif ($percentage -ge 75) { "Yellow" } else { "Red" })

# Quick Actions
Write-Host "`n🚀 Quick Actions:" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green

if (-not $mailhogSMTP) {
    Write-Host "• Start MailHog: docker-compose up mailhog -d" -ForegroundColor Blue
}

if (-not $backend) {
    Write-Host "• Start Backend: cd backend && .\venv\Scripts\activate && python -m uvicorn main:app --reload" -ForegroundColor Blue
}

if (-not $frontend) {
    Write-Host "• Start Frontend: cd frontend && npm run dev" -ForegroundColor Blue
}

if ($mailhogWeb) {
    Write-Host "• Open MailHog: http://localhost:8025" -ForegroundColor Blue
}

if ($backend) {
    Write-Host "• Open API Docs: http://localhost:8000/docs" -ForegroundColor Blue
}

if ($frontend) {
    Write-Host "• Open Frontend: http://localhost:3000" -ForegroundColor Blue
}

Write-Host "`nPress Ctrl+C to exit monitor" -ForegroundColor Gray
