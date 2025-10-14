# EventLead Platform - Working Service Monitor
# This script uses curl/Invoke-WebRequest to test actual HTTP connectivity

Clear-Host
Write-Host "EventLead Platform Service Monitor" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host "Last Updated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host ""

# Function to test HTTP connectivity
function Test-HttpService {
    param([string]$URL, [string]$ServiceName)
    
    try {
        $response = Invoke-WebRequest -Uri $URL -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
        Write-Host "$ServiceName: RUNNING (Status: $($response.StatusCode))" -ForegroundColor Green
        Write-Host "   URL: $URL" -ForegroundColor Blue
        return $true
    }
    catch {
        Write-Host "$ServiceName: NOT RUNNING" -ForegroundColor Red
        Write-Host "   URL: $URL" -ForegroundColor Gray
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor DarkRed
        return $false
    }
}

# Function to test MailHog specifically
function Test-MailHog {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8025/api/v2/messages" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
        Write-Host "MailHog Web UI: RUNNING (Status: $($response.StatusCode))" -ForegroundColor Green
        Write-Host "   URL: http://localhost:8025" -ForegroundColor Blue
        return $true
    }
    catch {
        Write-Host "MailHog Web UI: NOT RUNNING" -ForegroundColor Red
        Write-Host "   URL: http://localhost:8025" -ForegroundColor Gray
        return $false
    }
}

# Test Services
Write-Host "Testing Services:" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan

$frontend = Test-HttpService -URL "http://localhost:3000" -ServiceName "Frontend"
$backend = Test-HttpService -URL "http://localhost:8000/api/health" -ServiceName "Backend API"
$mailhog = Test-MailHog

# Summary
Write-Host "`nService Summary:" -ForegroundColor Green
Write-Host "==================" -ForegroundColor Green

$totalServices = 3
$runningServices = 0

if ($frontend) { $runningServices++ }
if ($backend) { $runningServices++ }
if ($mailhog) { $runningServices++ }

$percentage = [math]::Round(($runningServices / $totalServices) * 100)

Write-Host "Services Running: $runningServices/$totalServices ($percentage%)" -ForegroundColor $(if ($percentage -eq 100) { "Green" } elseif ($percentage -ge 50) { "Yellow" } else { "Red" })

# Quick Actions
Write-Host "`nQuick Actions:" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green

if ($frontend) {
    Write-Host "✅ Frontend: http://localhost:3000" -ForegroundColor Green
}
if ($backend) {
    Write-Host "✅ Backend API: http://localhost:8000/docs" -ForegroundColor Green
}
if ($mailhog) {
    Write-Host "✅ MailHog: http://localhost:8025" -ForegroundColor Green
}

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
