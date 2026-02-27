param(
  [Parameter(Mandatory = $true)]
  [string]$StoryId,

  [Parameter(Mandatory = $false)]
  [string]$BackendPath = "backend",

  [Parameter(Mandatory = $false)]
  [string]$FocusedTestCommand = "",

  [Parameter(Mandatory = $false)]
  [string]$BackendGateCommand = "python -m pytest --tb=short",

  [Parameter(Mandatory = $false)]
  [string]$FrontendPath = "frontend",

  [Parameter(Mandatory = $false)]
  [string]$FrontendGateCommand = "",

  [Parameter(Mandatory = $false)]
  [string]$EvidenceFile
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Invoke-CommandCapture {
  param(
    [Parameter(Mandatory = $true)][string]$WorkingDirectory,
    [Parameter(Mandatory = $true)][string]$CommandText
  )

  Push-Location $WorkingDirectory
  try {
    $output = @(Invoke-Expression $CommandText 2>&1)
    $exitCode = $LASTEXITCODE
  } finally {
    Pop-Location
  }

  $esc = [char]27
  $normalizedOutput = @($output | ForEach-Object { ("$_" -replace "$esc\[[0-9;]*[A-Za-z]", "") })
  $summaryLines = @($normalizedOutput | Where-Object { $_ -match "(?i)\d+\s+passed," })
  if ($summaryLines.Count -eq 0) {
    $summaryLines = @($normalizedOutput | Where-Object { $_ -match "(?i)\d+\s+failed," })
  }
  if ($summaryLines.Count -eq 0) {
    $summaryLines = @($normalizedOutput | Where-Object { $_ -match "(?i)\bpassed\b" })
  }
  $hasSummary = $summaryLines.Count -gt 0
  $finalSummary = if ($hasSummary) { "$($summaryLines[-1])" } else { "" }

  [pscustomobject]@{
    Command      = $CommandText
    WorkingDir   = $WorkingDirectory
    ExitCode     = $exitCode
    Output       = $normalizedOutput
    HasSummary   = $hasSummary
    FinalSummary = $finalSummary
    Passed       = (($exitCode -eq 0) -and $hasSummary)
  }
}

function Write-Result {
  param([Parameter(Mandatory = $true)]$Result)
  Write-Host ""
  Write-Host "Command: $($Result.Command)"
  Write-Host "Working dir: $($Result.WorkingDir)"
  Write-Host "Exit code: $($Result.ExitCode)"
  if ($Result.HasSummary) {
    Write-Host "Final summary: $($Result.FinalSummary)"
  } else {
    Write-Host "Final summary: <missing>"
  }
}

$repoRoot = (Get-Location).Path
if ([string]::IsNullOrWhiteSpace($EvidenceFile)) {
  $EvidenceFile = Join-Path $repoRoot "docs/stories/STORY-$StoryId-GATE-EVIDENCE.md"
}

$results = @()

if (-not [string]::IsNullOrWhiteSpace($FocusedTestCommand)) {
  $results += Invoke-CommandCapture -WorkingDirectory (Join-Path $repoRoot $BackendPath) -CommandText $FocusedTestCommand
}

$results += Invoke-CommandCapture -WorkingDirectory (Join-Path $repoRoot $BackendPath) -CommandText $BackendGateCommand

if (-not [string]::IsNullOrWhiteSpace($FrontendGateCommand)) {
  $results += Invoke-CommandCapture -WorkingDirectory (Join-Path $repoRoot $FrontendPath) -CommandText $FrontendGateCommand
}

foreach ($res in $results) { Write-Result -Result $res }

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$md = @()
$md += "# Story $StoryId Gate Evidence"
$md += ""
$md += "- Generated: $timestamp"
$md += "- Repository root: $repoRoot"
$md += ""
$md += "| Command | Working Directory | Exit | Summary detected | Status |"
$md += "|--------|-------------------|------|------------------|--------|"
foreach ($res in $results) {
  $status = if ($res.Passed) { "PASS" } else { "FAIL" }
  $safeCmd = ($res.Command -replace "\|", "\/")
  $safeDir = ($res.WorkingDir -replace "\|", "\/")
  $summaryFlag = if ($res.HasSummary) { "yes" } else { "no" }
  $md += "| $safeCmd | $safeDir | $($res.ExitCode) | $summaryFlag | $status |"
}
$md += ""

foreach ($res in $results) {
  $md += "## $($res.Command)"
  $md += ""
  $md += "- Working dir: $($res.WorkingDir)"
  $md += "- Exit code: $($res.ExitCode)"
  if ($res.HasSummary) {
    $md += "- Final summary: $($res.FinalSummary)"
  } else {
    $md += "- Final summary: <missing>"
  }
  $md += ""
}

Set-Content -Path $EvidenceFile -Value ($md -join [Environment]::NewLine) -Encoding UTF8
Write-Host ""
Write-Host "Evidence written to: $EvidenceFile"

$failed = @($results | Where-Object { $_.Passed -eq $false })
if ($failed.Count -gt 0) {
  Write-Error "Green gate failed (non-zero exit and/or missing final summary)."
  exit 1
}

Write-Host ""
Write-Host "Green gate passed."
