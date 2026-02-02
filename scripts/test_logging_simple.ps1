# Simple Logging Test Script
# Tests that logging events are being captured and sent to backend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Component Framework - Logging Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if backend diagnostic script exists
$diagnosticScript = "backend\enhanced_diagnostic_logs.py"
if (-not (Test-Path $diagnosticScript)) {
    Write-Host "ERROR: Diagnostic script not found at $diagnosticScript" -ForegroundColor Red
    exit 1
}

Write-Host "Step 1: Checking for recent frontend logs..." -ForegroundColor Yellow
Write-Host ""

# Test 1: History events
Write-Host "Testing history events (history.push, history.undo, history.redo)..." -ForegroundColor Green
python $diagnosticScript --frontend-only --frontend-filter "history" --limit 5
Write-Host ""

# Test 2: Resize phase events
Write-Host "Testing resize phase events (resize.phase.transition)..." -ForegroundColor Green
python $diagnosticScript --frontend-only --frontend-filter "resize.phase" --limit 5
Write-Host ""

# Test 3: Object layout events
Write-Host "Testing object layout events (objectlayout.*)..." -ForegroundColor Green
python $diagnosticScript --frontend-only --frontend-filter "objectlayout" --limit 5
Write-Host ""

# Test 4: Text length events
Write-Host "Testing text length events (canvas.textlength.calculated)..." -ForegroundColor Green
python $diagnosticScript --frontend-only --frontend-filter "textlength" --limit 5
Write-Host ""

# Test 5: Width resize events
Write-Host "Testing width resize events (resize.width.calculated)..." -ForegroundColor Green
python $diagnosticScript --frontend-only --frontend-filter "resize.width" --limit 5
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "NOTE: If no logs appear, ensure:" -ForegroundColor Yellow
Write-Host "  1. Frontend is running with VITE_ENABLE_DEV_LOGS=true" -ForegroundColor Yellow
Write-Host "  2. VITE_LOG_SEND_TO_BACKEND=true is set" -ForegroundColor Yellow
Write-Host "  3. User has performed actions in the builder" -ForegroundColor Yellow
Write-Host "  4. Backend API endpoint /api/v1/logs/frontend is accessible" -ForegroundColor Yellow
Write-Host ""
