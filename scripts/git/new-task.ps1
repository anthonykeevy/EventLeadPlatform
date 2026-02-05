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

# Optional per-machine override for shorter worktree paths (Windows path length issues).
# Usage:
#   $env:ELP_WORKTREE_ROOT = "C:\wt\elp"
#   scripts/git/new-task.ps1 ... -CreateWorktree
#
# If -WorktreeRoot is explicitly provided, it always wins.
if (-not $PSBoundParameters.ContainsKey("WorktreeRoot")) {
  $envRoot = $env:ELP_WORKTREE_ROOT
  if ($envRoot -and $envRoot.Trim().Length -gt 0) {
    $WorktreeRoot = $envRoot.Trim()
  }
}

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

function Resolve-GhPath {
  $cmd = Get-Command gh -ErrorAction SilentlyContinue
  if ($cmd -and $cmd.Source) { return $cmd.Source }

  $candidates = @()

  if ($env:ProgramFiles) {
    $candidates += (Join-Path $env:ProgramFiles "GitHub CLI\gh.exe")
  }

  $pf86 = [Environment]::GetEnvironmentVariable('ProgramFiles(x86)')
  if ($pf86) {
    $candidates += (Join-Path $pf86 "GitHub CLI\gh.exe")
  }

  if ($env:LOCALAPPDATA) {
    $candidates += (Join-Path $env:LOCALAPPDATA "Programs\GitHub CLI\gh.exe")
  }

  foreach ($p in ($candidates | Select-Object -Unique)) {
    if ($p -and (Test-Path $p)) { return $p }
  }

  return $null
}

$taskBranch = "task/$StoryId/$TaskId-$Slug"
$taskWorktreeName = "task-$StoryId-$TaskId-$Slug" -replace "[/\\\\]", "-"
$taskWorktreePath = Join-Path $WorktreeRoot $taskWorktreeName

Write-Host "Story branch: $StoryBranch"
Write-Host "Task branch:  $taskBranch"
Write-Host "Remote:       $Remote"
Write-Host "Worktree root: $WorktreeRoot"

Show-And-Run -CommandText "git fetch $Remote" -Command { git fetch $Remote }

if ($CreateWorktree) {
  # IMPORTANT: A worktree cannot be created for a branch that is already checked out in the main repo.
  # Create the task branch ref first, then check it out in a worktree.

  # Prefer remote ref if present; fallback to local branch name.
  $baseRef = "$Remote/$StoryBranch"
  & git show-ref --verify --quiet "refs/remotes/$Remote/$StoryBranch" 2>$null
  if ($LASTEXITCODE -ne 0) {
    $baseRef = $StoryBranch
    & git show-ref --verify --quiet "refs/heads/$StoryBranch" 2>$null
    if ($LASTEXITCODE -ne 0) {
      throw "Story branch not found locally or on remote: $StoryBranch"
    }
  }

  $taskBranchExists = $false
  & git show-ref --verify --quiet "refs/heads/$taskBranch" 2>$null
  if ($LASTEXITCODE -eq 0) { $taskBranchExists = $true }

  if (-not $taskBranchExists) {
    Show-And-Run -CommandText "git branch `"$taskBranch`" `"$baseRef`"" -Command { git branch $taskBranch $baseRef }
  } else {
    Write-Host ""
    Write-Host "Local task branch already exists; skipping: $taskBranch"
  }

  Show-And-Run -CommandText "git push -u $Remote `"$taskBranch`"" -Command { git push -u $Remote $taskBranch }

  if (-not $DryRun) {
    New-Item -ItemType Directory -Force -Path $WorktreeRoot | Out-Null
  } else {
    Write-Host ""
    Write-Host "New-Item -ItemType Directory -Force -Path `"$WorktreeRoot`" | Out-Null"
  }

  Show-And-Run -CommandText "git worktree add `"$taskWorktreePath`" `"$taskBranch`"" -Command { git worktree add $taskWorktreePath $taskBranch }
  Write-Host ""
  Write-Host "Task worktree path: $taskWorktreePath"
} else {
  # Non-worktree mode: switch to story branch, branch off it, then work in main repo.
  Show-And-Run -CommandText "git switch `"$StoryBranch`"" -Command { git switch $StoryBranch }
  Show-And-Run -CommandText "git pull $Remote `"$StoryBranch`"" -Command { git pull $Remote $StoryBranch }
  # Idempotency: if the task branch already exists (locally or on remote), re-use it instead of failing.
  $taskBranchLocalExists = $false
  & git show-ref --verify --quiet "refs/heads/$taskBranch" 2>$null
  if ($LASTEXITCODE -eq 0) { $taskBranchLocalExists = $true }

  if ($taskBranchLocalExists) {
    Show-And-Run -CommandText "git switch `"$taskBranch`"" -Command { git switch $taskBranch }
  } else {
    $taskBranchRemoteExists = $false
    & git show-ref --verify --quiet "refs/remotes/$Remote/$taskBranch" 2>$null
    if ($LASTEXITCODE -eq 0) { $taskBranchRemoteExists = $true }

    if ($taskBranchRemoteExists) {
      Show-And-Run -CommandText "git switch --track `"$Remote/$taskBranch`"" -Command { git switch --track "$Remote/$taskBranch" }
    } else {
      Show-And-Run -CommandText "git switch -c `"$taskBranch`"" -Command { git switch -c $taskBranch }
    }
  }
  Show-And-Run -CommandText "git push -u $Remote HEAD" -Command { git push -u $Remote HEAD }
}

if ($CreatePR) {
  $ghPath = Resolve-GhPath
  if (-not $ghPath) {
    Write-Host ""
    Write-Host "gh not found; skipping PR creation."
    Write-Host "Install GitHub CLI, then run:"
    Write-Host "gh pr create --base `"$StoryBranch`" --head `"$taskBranch`" --title `"${StoryId}: ${TaskId} - ${Slug}`" --body `"Implements ${TaskId} for story ${StoryId}. See docs/tasks/${StoryId}/ for completion + UAT.`""
  } else {
    $title = "${StoryId}: $TaskId - $Slug"
    $body = "Implements $TaskId for story $StoryId. See docs/tasks/$StoryId/ for completion + UAT."
    Show-And-Run -CommandText "`"$ghPath`" pr create --base `"$StoryBranch`" --head `"$taskBranch`" --title `"$title`" --body `"$body`"" -Command { & $ghPath pr create --base $StoryBranch --head $taskBranch --title $title --body $body }
  }
}

Write-Host ""
Write-Host "Done."

