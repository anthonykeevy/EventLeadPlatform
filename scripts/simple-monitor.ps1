# EventLead Platform - Simple Service Monitor
# This script monitors all services and shows their status

Clear-Host
Write-Host "EventLead Platform Service Monitor" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host "Last Updated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host ""

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
        Write-Host "$ServiceName (port $Port): RUNNING" -ForegroundColor Green
        if ($URL) {
            Write-Host "   URL: $URL" -ForegroundColor Blue
        }
        return $true
    } else {
        Write-Host "$ServiceName (port $Port): NOT RUNNING" -ForegroundColor Red
        return $false
    }
}

# Check MailHog
Write-Host "MailHog Email Service:" -ForegroundColor Cyan
$mailhogSMTP = Get-ServiceStatus -Port 1025 -ServiceName "MailHog SMTP"
$mailhogWeb = Get-ServiceStatus -Port 8025 -ServiceName "MailHog Web UI" -URL "http://localhost:8025"

# Check Backend
Write-Host "`nBackend API Service:" -ForegroundColor Cyan
$backend = Get-ServiceStatus -Port 8000 -ServiceName "Backend API" -URL "http://localhost:8000"

# Check Frontend
Write-Host "`nFrontend Service:" -ForegroundColor Cyan
$frontend = Get-ServiceStatus -Port 3000 -ServiceName "Frontend" -URL "http://localhost:3000"

# Summary
Write-Host "`nService Summary:" -ForegroundColor Green
Write-Host "==================" -ForegroundColor Green

$totalServices = 3
$runningServices = 0

if ($mailhogWeb) { $runningServices++ }
if ($backend) { $runningServices++ }
if ($frontend) { $runningServices++ }

$percentage = [math]::Round(($runningServices / $totalServices) * 100)

Write-Host "Services Running: $runningServices/$totalServices ($percentage%)" -ForegroundColor $(if ($percentage -eq 100) { "Green" } elseif ($percentage -ge 50) { "Yellow" } else { "Red" })

# Quick Actions
Write-Host "`nQuick Actions:" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green

if (-not $mailhogWeb) {
    Write-Host "Start MailHog: docker-compose up mailhog -d" -ForegroundColor Blue
}

if (-not $backend) {
    Write-Host "Start Backend: cd backend; .\venv\Scripts\activate; python -m uvicorn main:app --reload" -ForegroundColor Blue
}

if (-not $frontend) {
    Write-Host "Start Frontend: cd frontend; npm run dev" -ForegroundColor Blue
}

if ($mailhogWeb) {
    Write-Host "Open MailHog: http://localhost:8025" -ForegroundColor Blue
}

if ($backend) {
    Write-Host "Open API Docs: http://localhost:8000/docs" -ForegroundColor Blue
}

if ($frontend) {
    Write-Host "Open Frontend: http://localhost:3000" -ForegroundColor Blue
}

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
