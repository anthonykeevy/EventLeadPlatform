# Start the Understand-Anything dashboard for the current repo.
# Requires: prior /understand scan (.understand-anything/knowledge-graph.json)

$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent $PSScriptRoot
$GraphFile = Join-Path $RepoRoot '.understand-anything\knowledge-graph.json'
$DashboardDir = Join-Path $env:USERPROFILE '.understand-anything\repo\understand-anything-plugin\packages\dashboard'

if (-not (Test-Path $GraphFile)) {
    Write-Host "No knowledge graph found at:" -ForegroundColor Red
    Write-Host "  $GraphFile" -ForegroundColor Yellow
    Write-Host "Run /understand in Cursor first, then retry." -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path $DashboardDir)) {
    Write-Host "Dashboard not installed. See docs/UNDERSTAND-ANYTHING.md" -ForegroundColor Red
    exit 1
}

Write-Host "Starting Understand-Anything dashboard..." -ForegroundColor Green
Write-Host "  GRAPH_DIR = $RepoRoot" -ForegroundColor Cyan
Write-Host "  (Use the tokenized URL printed below — required for access)" -ForegroundColor Cyan

$env:GRAPH_DIR = $RepoRoot
Set-Location $DashboardDir
npx vite --host 127.0.0.1
