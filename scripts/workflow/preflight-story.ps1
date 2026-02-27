param(
  [Parameter(Mandatory = $false)]
  [string]$ExpectedWorktreePath,

  [Parameter(Mandatory = $false)]
  [string]$ExpectedBranch,

  [Parameter(Mandatory = $false)]
  [string]$BackendPath = "backend",

  [Parameter(Mandatory = $false)]
  [string]$ReportFile
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Add-Check {
  param(
    [Parameter(Mandatory = $true)][string]$Name,
    [Parameter(Mandatory = $true)][bool]$Pass,
    [Parameter(Mandatory = $true)][string]$Detail
  )
  $status = if ($Pass) { "PASS" } else { "FAIL" }
  [pscustomobject]@{
    Check  = $Name
    Status = $status
    Detail = $Detail
  }
}

$rows = @()
$cwd = (Get-Location).Path
$branch = (git branch --show-current).Trim()
$statusShort = (git status -sb | Select-Object -First 1).Trim()

$rows += Add-Check -Name "Current directory captured" -Pass $true -Detail $cwd
$rows += Add-Check -Name "Git branch captured" -Pass ([string]::IsNullOrWhiteSpace($branch) -eq $false) -Detail $branch
$rows += Add-Check -Name "Git status captured" -Pass ([string]::IsNullOrWhiteSpace($statusShort) -eq $false) -Detail $statusShort

if ($ExpectedWorktreePath) {
  $dirMatch = ($cwd -ieq $ExpectedWorktreePath)
  $rows += Add-Check -Name "Expected worktree path" -Pass $dirMatch -Detail "expected=$ExpectedWorktreePath ; actual=$cwd"
}

if ($ExpectedBranch) {
  $branchMatch = ($branch -eq $ExpectedBranch)
  $rows += Add-Check -Name "Expected branch" -Pass $branchMatch -Detail "expected=$ExpectedBranch ; actual=$branch"
}

$backendFullPath = Join-Path $cwd $BackendPath
$backendExists = Test-Path $backendFullPath
$rows += Add-Check -Name "Backend path exists" -Pass $backendExists -Detail $backendFullPath

$envDb = $null
$runtimeDb = $null

if ($backendExists) {
  Push-Location $backendFullPath
  try {
    $py = @'
import os
from common.database import DATABASE_URL as DB
print("OS_ENV_DATABASE_URL=" + str(os.getenv("DATABASE_URL")))
print("RUNTIME_DATABASE_URL=" + str(DB))
'@
    $pythonOutput = $py | python - 2>&1
    foreach ($line in $pythonOutput) {
      if ($line -like "OS_ENV_DATABASE_URL=*") { $envDb = $line.Substring("OS_ENV_DATABASE_URL=".Length) }
      if ($line -like "RUNTIME_DATABASE_URL=*") { $runtimeDb = $line.Substring("RUNTIME_DATABASE_URL=".Length) }
    }
    $rows += Add-Check -Name "Python DB preflight executed" -Pass ($LASTEXITCODE -eq 0) -Detail "backend python check"
  } finally {
    Pop-Location
  }

  $rows += Add-Check -Name "Runtime DB resolved" -Pass ([string]::IsNullOrWhiteSpace($runtimeDb) -eq $false) -Detail "$runtimeDb"
  if ([string]::IsNullOrWhiteSpace($envDb) -and ([string]::IsNullOrWhiteSpace($runtimeDb) -eq $false)) {
    $rows += Add-Check -Name "Env/runtime parity signal" -Pass $true -Detail "os.getenv(DATABASE_URL) is empty; runtime fallback is active."
  } else {
    $rows += Add-Check -Name "Env/runtime parity signal" -Pass $true -Detail "os.getenv(DATABASE_URL) and runtime values are both present."
  }
}

Write-Host ""
Write-Host "=== Story Preflight Report ==="
$rows | Format-Table -AutoSize

if ($ReportFile) {
  $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
  $md = @()
  $md += "# Story Preflight Report"
  $md += ""
  $md += "- Timestamp: $timestamp"
  $md += "- Working directory: $cwd"
  $md += "- Branch: $branch"
  $md += ""
  $md += "| Check | Status | Detail |"
  $md += "|------|--------|--------|"
  foreach ($r in $rows) {
    $detail = ($r.Detail -replace "\|", "\/")
    $md += "| $($r.Check) | $($r.Status) | $detail |"
  }
  Set-Content -Path $ReportFile -Value ($md -join [Environment]::NewLine) -Encoding UTF8
  Write-Host ""
  Write-Host "Report written to: $ReportFile"
}

$failed = @($rows | Where-Object { $_.Status -eq "FAIL" })
if ($failed.Count -gt 0) {
  Write-Error "Preflight failed. Resolve failing checks before implementation."
  exit 1
}

Write-Host ""
Write-Host "Preflight passed."
