param(
  [Parameter(Mandatory = $true)]
  [string]$StoryId,

  [Parameter(Mandatory = $true)]
  [string]$ToolName,

  [Parameter(Mandatory = $true)]
  [ValidateRange(1, 5)]
  [int]$Rating,

  [Parameter(Mandatory = $true)]
  [string]$Feedback,

  [Parameter(Mandatory = $false)]
  [string]$LogFile = "docs/stories/TOOLING-FEEDBACK-LOG.md"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$repoRoot = (Get-Location).Path
$logPath = Join-Path $repoRoot $LogFile
$safeFeedback = $Feedback -replace "\|", "/"

if (-not (Test-Path $logPath)) {
  $initial = @()
  $initial += "# Tooling Feedback Log"
  $initial += ""
  $initial += "Tracks developer-agent feedback for iterative workflow script improvements."
  $initial += ""
  $initial += "| Timestamp | Story | Tool | Rating (1-5) | Feedback |"
  $initial += "|-----------|-------|------|--------------|----------|"
  Set-Content -Path $logPath -Value ($initial -join [Environment]::NewLine) -Encoding UTF8
}

$line = "| $timestamp | $StoryId | $ToolName | $Rating | $safeFeedback |"
Add-Content -Path $logPath -Value ($line + [Environment]::NewLine) -Encoding UTF8

Write-Host "Feedback appended to: $logPath"
