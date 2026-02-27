param(
  [Parameter(Mandatory = $true)]
  [int]$Epic,

  [Parameter(Mandatory = $true)]
  [string]$Story,

  [Parameter(Mandatory = $true)]
  [string]$Slug,

  [string]$BaseBranch = "master",
  [string]$Remote = "origin",

  [string]$WorktreeRoot = "..\\EventLeadPlatform.wt",
  [switch]$CreateWorktree,

  [switch]$DraftPR,
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Optional per-machine override for shorter worktree paths (Windows path length issues).
# Usage:
#   $env:ELP_WORKTREE_ROOT = "C:\wt\elp"
#   scripts/git/new-story.ps1 ... -CreateWorktree
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

$storyBranch = "story/epic$Epic-$Story-$Slug"
$storyWorktreeName = ($storyBranch -replace "[/\\\\]", "-")
$storyWorktreePath = Join-Path $WorktreeRoot $storyWorktreeName

Write-Host "Story branch: $storyBranch"
Write-Host "Base branch:  $BaseBranch"
Write-Host "Remote:       $Remote"
Write-Host "Worktree root: $WorktreeRoot"

Show-And-Run -CommandText "git fetch $Remote" -Command { git fetch $Remote }
Show-And-Run -CommandText "git switch $BaseBranch" -Command { git switch $BaseBranch }
Show-And-Run -CommandText "git pull $Remote $BaseBranch" -Command { git pull $Remote $BaseBranch }

if ($CreateWorktree) {
  # IMPORTANT: A worktree cannot be created for a branch that is already checked out in the main repo.
  # When using worktrees, we keep the main repo on the base branch and check out the story branch in the worktree.

  # Create branch ref without checking it out in the main repo.
  $branchExists = $false
  & git show-ref --verify --quiet "refs/heads/$storyBranch" 2>$null
  if ($LASTEXITCODE -eq 0) { $branchExists = $true }

  if (-not $branchExists) {
    Show-And-Run -CommandText "git branch `"$storyBranch`"" -Command { git branch $storyBranch }
  } else {
    Write-Host ""
    Write-Host "Local branch already exists; skipping: $storyBranch"
  }

  Show-And-Run -CommandText "git push -u $Remote `"$storyBranch`"" -Command { git push -u $Remote $storyBranch }

  if (-not $DryRun) {
    New-Item -ItemType Directory -Force -Path $WorktreeRoot | Out-Null
  } else {
    Write-Host ""
    Write-Host "New-Item -ItemType Directory -Force -Path `"$WorktreeRoot`" | Out-Null"
  }

  Show-And-Run -CommandText "git worktree add `"$storyWorktreePath`" `"$storyBranch`"" -Command { git worktree add $storyWorktreePath $storyBranch }

  Write-Host ""
  Write-Host "Story worktree path: $storyWorktreePath"
} else {
  # Non-worktree mode: check out the branch in the main repo.
  Show-And-Run -CommandText "git switch -c `"$storyBranch`"" -Command { git switch -c $storyBranch }
  Show-And-Run -CommandText "git push -u $Remote HEAD" -Command { git push -u $Remote HEAD }
}

if ($DraftPR) {
  if (-not $DryRun) {
    # GitHub cannot create a PR when there are zero commits between base and head.
    # Auto-bootstrap with an empty commit so Draft PR creation does not fail.
    $aheadRaw = (& git rev-list --count "$BaseBranch..$storyBranch").Trim()
    $aheadCount = 0
    if (-not [int]::TryParse($aheadRaw, [ref]$aheadCount)) {
      throw "Could not parse ahead-count for $BaseBranch..$storyBranch (raw: '$aheadRaw')"
    }

    if ($aheadCount -eq 0) {
      Write-Host ""
      Write-Host "No commits between $BaseBranch and $storyBranch. Creating bootstrap commit."
      $bootstrapMsg = "chore(epic${Epic}): bootstrap $Story draft PR"

      if ($CreateWorktree) {
        Show-And-Run -CommandText "git -C `"$storyWorktreePath`" commit --allow-empty -m `"$bootstrapMsg`"" -Command { git -C $storyWorktreePath commit --allow-empty -m $bootstrapMsg }
        Show-And-Run -CommandText "git -C `"$storyWorktreePath`" push -u $Remote `"$storyBranch`"" -Command { git -C $storyWorktreePath push -u $Remote $storyBranch }
      } else {
        Show-And-Run -CommandText "git commit --allow-empty -m `"$bootstrapMsg`"" -Command { git commit --allow-empty -m $bootstrapMsg }
        Show-And-Run -CommandText "git push -u $Remote `"$storyBranch`"" -Command { git push -u $Remote $storyBranch }
      }
    }
  }

  $ghPath = Resolve-GhPath
  if (-not $ghPath) {
    Write-Host ""
    Write-Host "gh not found; skipping PR creation."
    Write-Host "Install GitHub CLI, then run:"
    Write-Host "gh pr create --draft --base `"$BaseBranch`" --head `"$storyBranch`" --title `"epic${Epic}: Story $Story - $Slug`" --body `"Draft story PR. Task PRs merge into this branch.`""
  } else {
    $title = "epic${Epic}: Story $Story - $Slug"
    $body = "Draft story PR. Task PRs merge into this branch."
    Show-And-Run -CommandText "`"$ghPath`" pr create --draft --base `"$BaseBranch`" --head `"$storyBranch`" --title `"$title`" --body `"$body`"" -Command { & $ghPath pr create --draft --base $BaseBranch --head $storyBranch --title $title --body $body }
  }
}

Write-Host ""
Write-Host "Done."

