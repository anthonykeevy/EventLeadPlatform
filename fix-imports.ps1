# Fix Backend Import Paths - Converts "from backend.X" to "from X"
param([switch]$DryRun = $false)

Write-Host "Backend Import Path Fix Script" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

$backendPath = Join-Path $PSScriptRoot "backend"
$filesFixed = 0

$pythonFiles = Get-ChildItem -Path $backendPath -Filter "*.py" -Recurse | 
    Where-Object { 
        $_.FullName -notlike "*\tests\*" -and 
        $_.FullName -notlike "*\venv\*" -and
        $_.FullName -notlike "*\__pycache__\*"
    }

Write-Host "Found $($pythonFiles.Count) files to process`n"

foreach ($file in $pythonFiles) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    
    $original = $content
    
    # Apply replacements
    $content = $content -replace 'from backend\.models\.', 'from models.'
    $content = $content -replace 'from backend\.common\.', 'from common.'
    $content = $content -replace 'from backend\.modules\.', 'from modules.'
    $content = $content -replace 'from backend\.services\.', 'from services.'
    $content = $content -replace 'from backend\.middleware\.', 'from middleware.'
    $content = $content -replace 'from backend\.config\.', 'from config.'
    $content = $content -replace 'from backend\.schemas\.', 'from schemas.'
    
    if ($content -ne $original) {
        $relativePath = $file.FullName.Replace($backendPath, "").TrimStart("\")
        
        if ($DryRun) {
            Write-Host "  [DRY RUN] $relativePath" -ForegroundColor Yellow
        } else {
            Set-Content -Path $file.FullName -Value $content -NoNewline
            Write-Host "  Fixed: $relativePath" -ForegroundColor Green
        }
        $filesFixed++
    }
}

Write-Host "`n==============================" -ForegroundColor Cyan
Write-Host "Files fixed: $filesFixed" -ForegroundColor $(if ($filesFixed -gt 0) { "Green" } else { "White" })
if ($DryRun) {
    Write-Host "DRY RUN - No changes made" -ForegroundColor Yellow
}
