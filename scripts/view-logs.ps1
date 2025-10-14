# EventLead Platform - Log Viewer
# This script shows logs for different services

param(
    [string]$Service = "all",
    [int]$Lines = 20
)

Write-Host "EventLead Platform Log Viewer" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Green
Write-Host ""

function Show-MailHogLogs {
    param([int]$LogLines)
    
    Write-Host "MailHog Container Logs:" -ForegroundColor Cyan
    Write-Host "======================" -ForegroundColor Cyan
    try {
        docker logs --tail $LogLines eventlead-mailhog
    }
    catch {
        Write-Host "Could not retrieve MailHog logs. Container may not be running." -ForegroundColor Red
    }
    Write-Host ""
}

function Show-DockerLogs {
    param([int]$LogLines)
    
    Write-Host "All Docker Container Logs:" -ForegroundColor Cyan
    Write-Host "=========================" -ForegroundColor Cyan
    try {
        docker-compose logs --tail $LogLines
    }
    catch {
        Write-Host "Could not retrieve Docker Compose logs." -ForegroundColor Red
    }
    Write-Host ""
}

function Show-ContainerList {
    Write-Host "Running Containers:" -ForegroundColor Cyan
    Write-Host "==================" -ForegroundColor Cyan
    try {
        docker ps
    }
    catch {
        Write-Host "Could not list containers." -ForegroundColor Red
    }
    Write-Host ""
}

# Main logic
switch ($Service.ToLower()) {
    "mailhog" {
        Show-MailHogLogs -LogLines $Lines
    }
    "docker" {
        Show-DockerLogs -LogLines $Lines
    }
    "containers" {
        Show-ContainerList
    }
    "all" {
        Show-ContainerList
        Show-MailHogLogs -LogLines $Lines
    }
    default {
        Write-Host "Usage: .\scripts\view-logs.ps1 [-Service <mailhog|docker|containers|all>] [-Lines <number>]" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Examples:" -ForegroundColor Green
        Write-Host "  .\scripts\view-logs.ps1 -Service mailhog -Lines 10" -ForegroundColor Blue
        Write-Host "  .\scripts\view-logs.ps1 -Service docker -Lines 20" -ForegroundColor Blue
        Write-Host "  .\scripts\view-logs.ps1 -Service containers" -ForegroundColor Blue
        Write-Host "  .\scripts\view-logs.ps1 -Service all" -ForegroundColor Blue
    }
}

Write-Host "Note: Backend and Frontend logs are shown in their respective terminal windows." -ForegroundColor Gray
