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
  [switch]$BootstrapPR,
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

  if ($DryRun) {
    # Ensure DRY RUN doesn't leak a non-zero exit code from previous commands.
    $global:LASTEXITCODE = 0
    return
  }

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

function Invoke-PrBootstrap {
  param(
    [Parameter(Mandatory = $true)][string]$RepoRoot
  )

  $taskBase = "$TaskId-$Slug"
  $taskSpecRelPath = "docs/tasks/$StoryId/$taskBase.md"
  $taskSpecAbsPath = Join-Path $RepoRoot $taskSpecRelPath

  Write-Host ""
  Write-Host "PR bootstrap: updating task spec status -> In Progress (Approved)"
  Write-Host "  File: $taskSpecRelPath"

  if (-not (Test-Path $taskSpecAbsPath)) {
    Write-Host "  Task spec not found; skipping PR bootstrap."
    return
  }

  $content = Get-Content -Raw -Path $taskSpecAbsPath
  $desiredLine = "**Status:** 🔄 In Progress (Approved)"
  $updated = [regex]::Replace($content, "^\*\*Status:\*\*.*$", $desiredLine, [Text.RegularExpressions.RegexOptions]::Multiline)

  if ($updated -eq $content) {
    Write-Host "  Status line already set; skipping bootstrap commit."
    return
  }

  if ($DryRun) {
    Write-Host "  DRY RUN: would update status line and commit+push."
    return
  }

  # Write file (utf8) and commit on the task branch.
  Set-Content -Path $taskSpecAbsPath -Value $updated -Encoding utf8

  Push-Location $RepoRoot
  try {
    & git add -- $taskSpecRelPath
    if ($LASTEXITCODE -ne 0) { throw "git add failed (exit $LASTEXITCODE): $taskSpecRelPath" }

    $msg = "docs(tasks): mark $TaskId in progress (approved)"
    & git commit -m $msg
    if ($LASTEXITCODE -ne 0) { throw "git commit failed (exit $LASTEXITCODE)" }

    & git push
    if ($LASTEXITCODE -ne 0) { throw "git push failed (exit $LASTEXITCODE)" }
  } finally {
    Pop-Location
  }
}

function Normalize-PathForCompare {
  param([Parameter(Mandatory = $true)][string]$Path)

  try {
    return ([IO.Path]::GetFullPath($Path)).TrimEnd('\')
  } catch {
    return $Path.TrimEnd('\')
  }
}

function Get-Worktrees {
  $lines = & git worktree list --porcelain
  if ($LASTEXITCODE -ne 0) {
    throw "git worktree list failed (exit $LASTEXITCODE)"
  }

  $worktrees = @()
  $current = $null

  foreach ($line in $lines) {
    if ($line -like "worktree *") {
      if ($current) { $worktrees += $current }
      $current = [ordered]@{ Path = $line.Substring(9).Trim(); Branch = $null }
      continue
    }

    if ($current -and $line -like "branch *") {
      $current.Branch = $line.Substring(7).Trim()
    }
  }

  if ($current) { $worktrees += $current }
  return $worktrees
}

function Find-WorktreeByPath {
  param([Parameter(Mandatory = $true)][string]$Path)

  $target = Normalize-PathForCompare $Path
  foreach ($wt in (Get-Worktrees)) {
    if ((Normalize-PathForCompare $wt.Path) -ieq $target) { return $wt }
  }

  return $null
}

function Get-CommitDeltaCount {
  param(
    [Parameter(Mandatory = $true)][string]$BaseRef,
    [Parameter(Mandatory = $true)][string]$HeadRef
  )

  $out = & git rev-list --count "$BaseRef..$HeadRef" 2>$null
  if ($LASTEXITCODE -ne 0) { return $null }

  try { return [int]$out } catch { return $null }
}

$taskBranch = "task/$StoryId/$TaskId-$Slug"
$taskWorktreeName = "task-$StoryId-$TaskId-$Slug" -replace "[/\\\\]", "-"
$taskWorktreePath = Join-Path $WorktreeRoot $taskWorktreeName
$prBaseRef = $null

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
  $prBaseRef = $baseRef

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

  if (-not $DryRun) {
    $existingWorktree = Find-WorktreeByPath $taskWorktreePath
    if (-not $existingWorktree -and (Test-Path $taskWorktreePath)) {
      throw "Worktree path already exists but is not registered as a git worktree: $taskWorktreePath"
    }

    if ($existingWorktree) {
      $expectedBranchRef = "refs/heads/$taskBranch"
      if ($existingWorktree.Branch -and $existingWorktree.Branch -eq $expectedBranchRef) {
        Write-Host ""
        Write-Host "Worktree already exists; skipping add: $taskWorktreePath"
      } else {
        throw "Worktree already exists at path but is not for branch ${taskBranch}: $taskWorktreePath"
      }
    } else {
      Show-And-Run -CommandText "git worktree add `"$taskWorktreePath`" `"$taskBranch`"" -Command { git worktree add $taskWorktreePath $taskBranch }
      Write-Host ""
      Write-Host "Task worktree path: $taskWorktreePath"
    }
  } else {
    Show-And-Run -CommandText "git worktree add `"$taskWorktreePath`" `"$taskBranch`"" -Command { git worktree add $taskWorktreePath $taskBranch }
    Write-Host ""
    Write-Host "Task worktree path: $taskWorktreePath"
  }
} else {
  # Non-worktree mode: switch to story branch, branch off it, then work in main repo.
  Show-And-Run -CommandText "git switch `"$StoryBranch`"" -Command { git switch $StoryBranch }
  Show-And-Run -CommandText "git pull $Remote `"$StoryBranch`"" -Command { git pull $Remote $StoryBranch }
  $prBaseRef = $StoryBranch
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

if ($BootstrapPR) {
  if ($CreateWorktree) {
    Invoke-PrBootstrap -RepoRoot $taskWorktreePath
  } else {
    $repoRoot = (& git rev-parse --show-toplevel 2>$null).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $repoRoot) {
      throw "Unable to determine git repo root for bootstrap. Are you running from inside a git repo?"
    }
    Invoke-PrBootstrap -RepoRoot $repoRoot
  }
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

    if ($DryRun) {
      Write-Host ""
      Write-Host "DRY RUN: PR creation requires at least one unique commit on the task branch."
      Write-Host "After your first commit + push, create the PR with:"
      Write-Host "`"$ghPath`" pr create --base `"$StoryBranch`" --head `"$taskBranch`" --title `"$title`" --body `"$body`""
    } else {
      # GitHub cannot create a PR if there are zero commits between base and head.
      # (GraphQL: "No commits between ...")
      if (-not $prBaseRef) { $prBaseRef = "$Remote/$StoryBranch" }
      $deltaCount = Get-CommitDeltaCount -BaseRef $prBaseRef -HeadRef $taskBranch
      if ($deltaCount -eq 0) {
        Write-Host ""
        Write-Host "Skipping PR creation: no commits between $StoryBranch and $taskBranch yet."
        Write-Host "Tip: re-run with -BootstrapPR to create a small doc commit first (safe to re-run)."
        Write-Host "After your first commit + push, re-run this script with -CreateWorktree -CreatePR (safe to re-run)."
        Write-Host "Or create manually:"
        Write-Host "`"$ghPath`" pr create --base `"$StoryBranch`" --head `"$taskBranch`" --title `"$title`" --body `"$body`""
      } else {
        Write-Host ""
        Write-Host "`"$ghPath`" pr create --base `"$StoryBranch`" --head `"$taskBranch`" --title `"$title`" --body `"$body`""

        $output = & $ghPath pr create --base $StoryBranch --head $taskBranch --title $title --body $body 2>&1
        if ($LASTEXITCODE -ne 0) {
          Write-Host ""
          Write-Host "PR creation failed (non-fatal). Output:"
          Write-Host ($output | Out-String)
          Write-Host "You can retry manually with the command above."
        } else {
          Write-Host ($output | Out-String)
        }
      }
    }
  }
}

Write-Host ""
Write-Host "Done."

