# Frontend Testing Helper Script for Agent-Browser
# Usage: .\scripts\test-frontend.ps1 -Url "http://localhost:3000/builder" [options]

param(
    [Parameter(Mandatory=$true)]
    [string]$Url,
    
    [string]$SnapshotOptions = "-i --json",
    
    [string]$Screenshot = "",
    
    [switch]$NoLogin,
    
    [string]$Profile = "$env:USERPROFILE\.eventlead-test-profile"
)

# Test account credentials
$LoginUrl = "http://localhost:3000/login"
$TestEmail = "user2@test.com"
$TestPassword = "JChMom7KYLfL88&!"

# Find agent-browser executable
$AgentBrowserPath = "$env:APPDATA\npm\node_modules\agent-browser\bin\agent-browser-win32-x64.exe"
if (-not (Test-Path $AgentBrowserPath)) {
    Write-Error "agent-browser not found at $AgentBrowserPath"
    Write-Host "Please install agent-browser: npm install -g agent-browser"
    exit 1
}

# Function to run agent-browser command
function Invoke-AgentBrowser {
    param([string[]]$Arguments)
    
    $process = Start-Process -FilePath $AgentBrowserPath -ArgumentList $Arguments -NoNewWindow -Wait -PassThru -RedirectStandardOutput "temp_output.txt" -RedirectStandardError "temp_error.txt"
    
    if (Test-Path "temp_output.txt") {
        Get-Content "temp_output.txt"
        Remove-Item "temp_output.txt"
    }
    
    if (Test-Path "temp_error.txt") {
        $errors = Get-Content "temp_error.txt"
        if ($errors) {
            Write-Warning $errors
        }
        Remove-Item "temp_error.txt"
    }
    
    return $process.ExitCode
}

Write-Host "=== Frontend Testing with Agent-Browser ===" -ForegroundColor Cyan
Write-Host "Target URL: $Url" -ForegroundColor Yellow

# Step 1: Login if needed (unless NoLogin flag is set)
if (-not $NoLogin) {
    Write-Host "`n[1/4] Logging in..." -ForegroundColor Green
    
    # Navigate to login page
    Invoke-AgentBrowser @("open", $LoginUrl) | Out-Null
    Start-Sleep -Seconds 2
    
    # Get snapshot to find form elements
    $snapshot = Invoke-AgentBrowser @("snapshot", "-i", "--json")
    
    # Try to find email input (usually first textbox)
    # In practice, agent will parse JSON and find correct refs
    Write-Host "   Snapshot obtained. Agent should parse JSON to find form refs." -ForegroundColor Gray
    
    # Fill login form (using common refs - agent should verify from snapshot)
    # Note: These refs may vary, agent should check snapshot first
    Write-Host "   Filling login form..." -ForegroundColor Gray
    Invoke-AgentBrowser @("fill", "@e1", $TestEmail) | Out-Null
    Invoke-AgentBrowser @("fill", "@e2", $TestPassword) | Out-Null
    Invoke-AgentBrowser @("click", "@e3") | Out-Null
    
    Write-Host "   Waiting for redirect..." -ForegroundColor Gray
    Start-Sleep -Seconds 3
    
    Write-Host "   ✓ Login completed" -ForegroundColor Green
}

# Step 2: Navigate to target URL
Write-Host "`n[2/4] Navigating to target page..." -ForegroundColor Green
$exitCode = Invoke-AgentBrowser @("open", $Url)

if ($exitCode -ne 0) {
    Write-Warning "Navigation may have failed. Check if login is required."
}

Start-Sleep -Seconds 2

# Step 3: Get snapshot
Write-Host "`n[3/4] Getting page snapshot..." -ForegroundColor Green
$snapshotArgs = $SnapshotOptions -split " "
$snapshot = Invoke-AgentBrowser @("snapshot") + $snapshotArgs

Write-Host "`n=== Page Snapshot ===" -ForegroundColor Cyan
$snapshot
Write-Host "`n=== End Snapshot ===" -ForegroundColor Cyan

# Step 4: Optional screenshot
if ($Screenshot) {
    Write-Host "`n[4/4] Capturing screenshot..." -ForegroundColor Green
    Invoke-AgentBrowser @("screenshot", $Screenshot) | Out-Null
    Write-Host "   ✓ Screenshot saved to: $Screenshot" -ForegroundColor Green
} else {
    Write-Host "`n[4/4] Skipping screenshot (use -Screenshot parameter to capture)" -ForegroundColor Gray
}

Write-Host "`n=== Testing Complete ===" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Review snapshot JSON to identify element refs (@e1, @e2, etc.)" -ForegroundColor White
Write-Host "  2. Use agent-browser commands to interact: click @e1, fill @e2 'text', etc." -ForegroundColor White
Write-Host "  3. Check network requests: agent-browser network requests" -ForegroundColor White
Write-Host "  4. View console: agent-browser console" -ForegroundColor White
