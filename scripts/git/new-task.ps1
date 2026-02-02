param(
  [Parameter(Mandatory = $true)]
  [string]$StoryBranch,

  [Parameter(Mandatory = $true)]
  [string]$StoryId,

  [Parameter(Mandatory = $true)]
  [string]$TaskId,

  [Parameter(Mandatory = $true)]
  [string]$Slug,

  [string]$Remote = "origin",

  [string]$WorktreeRoot = "..\\EventLeadPlatform.wt",
  [switch]$CreateWorktree,

  [switch]$CreatePR,
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Show-And-Run {
  param(
    [Parameter(Mandatory = $true)][string]$CommandText,
    [Parameter(Mandatory = $true)][scriptblock]$Command
  )

  Write-Host ""
  Write-Host $CommandText

  if ($DryRun) { return }

  & $Command

  if ($LASTEXITCODE -ne 0) {
    throw "Command failed (exit $LASTEXITCODE): $CommandText"
  }
}

$taskBranch = "task/$StoryId/$TaskId-$Slug"
$taskWorktreeName = "task-$StoryId-$TaskId-$Slug" -replace "[/\\\\]", "-"
$taskWorktreePath = Join-Path $WorktreeRoot $taskWorktreeName

Write-Host "Story branch: $StoryBranch"
Write-Host "Task branch:  $taskBranch"
Write-Host "Remote:       $Remote"

Show-And-Run -CommandText "git fetch $Remote" -Command { git fetch $Remote }
Show-And-Run -CommandText "git switch `"$StoryBranch`"" -Command { git switch $StoryBranch }
Show-And-Run -CommandText "git pull $Remote `"$StoryBranch`"" -Command { git pull $Remote $StoryBranch }
Show-And-Run -CommandText "git switch -c `"$taskBranch`"" -Command { git switch -c $taskBranch }
Show-And-Run -CommandText "git push -u $Remote HEAD" -Command { git push -u $Remote HEAD }

if ($CreateWorktree) {
  if (-not $DryRun) {
    New-Item -ItemType Directory -Force -Path $WorktreeRoot | Out-Null
  } else {
    Write-Host ""
    Write-Host "New-Item -ItemType Directory -Force -Path `"$WorktreeRoot`" | Out-Null"
  }

  Show-And-Run -CommandText "git worktree add `"$taskWorktreePath`" `"$taskBranch`"" -Command { git worktree add $taskWorktreePath $taskBranch }
  Write-Host ""
  Write-Host "Task worktree path: $taskWorktreePath"
}

if ($CreatePR) {
  $gh = Get-Command gh -ErrorAction SilentlyContinue
  if (-not $gh) {
    Write-Host ""
    Write-Host "gh not found; skipping PR creation."
    Write-Host "Install GitHub CLI, then run:"
    Write-Host "gh pr create --base `"$StoryBranch`" --head `"$taskBranch`" --title `"${StoryId}: ${TaskId} - ${Slug}`" --body `"Implements ${TaskId} for story ${StoryId}. See docs/tasks/${StoryId}/ for completion + UAT.`""
  } else {
    $title = "$StoryId: $TaskId - $Slug"
    $body = "Implements $TaskId for story $StoryId. See docs/tasks/$StoryId/ for completion + UAT."
    Show-And-Run -CommandText "gh pr create --base `"$StoryBranch`" --head `"$taskBranch`" --title `"$title`" --body `"$body`"" -Command { gh pr create --base $StoryBranch --head $taskBranch --title $title --body $body }
  }
}

Write-Host ""
Write-Host "Done."

