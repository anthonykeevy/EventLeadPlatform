<#
.SYNOPSIS
  Unblock new-story.ps1 and ensure story artifacts are in the worktree.
  Fixes trailing whitespace (avoids git stash warnings), handles conflicting files, creates worktree, copies artifacts, commits, and creates draft PR.

.DESCRIPTION
  Run from EventLeadPlatform repo root. Use for Story 5.4+ when:
  - Local changes block git pull (modified Epic docs, untracked story files from previous work)
  - New story branch must have at least one commit for Draft PR (GitHub rejects empty PRs)

.PARAMETER Epic
  Epic number (e.g. 5)

.PARAMETER Story
  Story ID (e.g. "5.4")

.PARAMETER Slug
  Branch slug (e.g. "shared-resolver-parity")

.PARAMETER StoryArtifacts
  Array of relative paths (from repo root) to copy into worktree after creation.
  E.g. @("docs/stories/story-5.4.md", "docs/stories/STORY-5.4-SINGLE-SESSION-DEV-PROMPT.md")

.PARAMETER FilesToStash
  Files to stash before pull. Default: EPIC-5-STATUS.md, EPIC-5-WORKFLOW-GUIDE.md

.PARAMETER FilesToRemove
  Untracked/conflicting files to remove before pull (master has merged versions).
  Default: Story 5.3 artifacts that conflict with merged master.

.PARAMETER WorktreeRoot
  Worktree root path. Default from $env:ELP_WORKTREE_ROOT or "C:\wt\elp"

.EXAMPLE
  # Story 5.4 (or use setup-story-5.4.ps1)
  ./scripts/git/setup-story.ps1 -Epic 5 -Story "5.4" -Slug "shared-resolver-parity" -StoryArtifacts @(
    "docs/stories/story-5.4.md",
    "docs/stories/story-context-5.4.xml",
    "docs/stories/STORY-5.4-UAT-TEST-GUIDE.md",
    "docs/stories/STORY-5.4-SINGLE-SESSION-DEV-PROMPT.md"
  )

.EXAMPLE
  # Story 5.5 - create setup-story-5.5.ps1 that calls this with 5.5 params
  ./scripts/git/setup-story.ps1 -Epic 5 -Story "5.5" -Slug "preview-production-governance" -StoryArtifacts @(
    "docs/stories/story-5.5.md",
    "docs/stories/story-context-5.5.xml",
    "docs/stories/STORY-5.5-SINGLE-SESSION-DEV-PROMPT.md"
  )
#>

param(
  [Parameter(Mandatory = $true)]
  [int]$Epic,

  [Parameter(Mandatory = $true)]
  [string]$Story,

  [Parameter(Mandatory = $true)]
  [string]$Slug,

  [Parameter(Mandatory = $true)]
  [string[]]$StoryArtifacts,

  [string[]]$FilesToStash = @(
    "docs/stories/EPIC-5-STATUS.md",
    "docs/stories/EPIC-5-WORKFLOW-GUIDE.md"
  ),

  [string[]]$FilesToRemove = @(
    "docs/stories/STORY-5.3-SINGLE-SESSION-DEV-PROMPT.md",
    "docs/stories/STORY-5.3-UAT-TEST-GUIDE.md",
    "docs/stories/story-5.3.md",
    "docs/stories/story-context-5.3.xml"
  ),

  [string]$WorktreeRoot = $null
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if (-not $WorktreeRoot) {
  $WorktreeRoot = if ($env:ELP_WORKTREE_ROOT -and $env:ELP_WORKTREE_ROOT.Trim()) {
    $env:ELP_WORKTREE_ROOT.Trim()
  } else {
    "C:\wt\elp"
  }
}

$repoRoot = $PSScriptRoot | Split-Path | Split-Path
$storyBranch = "story/epic$Epic-$Story-$Slug"
$storyWorktreeName = $storyBranch -replace "[/\\]", "-"
$worktreePath = Join-Path $WorktreeRoot $storyWorktreeName

function Fix-TrailingWhitespace {
  param([string[]]$Paths)
  foreach ($p in $Paths) {
    $fullPath = Join-Path $repoRoot $p
    if (-not (Test-Path $fullPath)) { continue }
    $content = Get-Content $fullPath -Raw
    if (-not $content) { continue }
    $fixed = $content -replace '[ \t]+\r?\n', "`n" -replace '[ \t]+\r?$', ''
    if ($content -ne $fixed) {
      [System.IO.File]::WriteAllText($fullPath, $fixed)
      Write-Host "   Fixed trailing whitespace: $p" -ForegroundColor Gray
    }
  }
}

function Invoke-GitStash {
  param([string]$Message, [string[]]$Paths)
  if (-not $Paths -or $Paths.Count -eq 0) {
    Write-Host "   No paths to stash" -ForegroundColor Gray
    return
  }
  # Run git stash; redirect stderr to avoid PowerShell throwing on trailing-whitespace warning
  $prevErr = $ErrorActionPreference
  $ErrorActionPreference = 'SilentlyContinue'
  try {
    $null = & git stash push -m $Message -- $Paths 2>&1
    $list = git stash list
    if ($list -match $Message) {
      Write-Host "   Stashed successfully" -ForegroundColor Gray
    }
  } finally {
    $ErrorActionPreference = $prevErr
  }
}

Set-Location $repoRoot

Write-Host "1. Fixing trailing whitespace in files to stash..." -ForegroundColor Cyan
$filesExist = $FilesToStash | Where-Object { Test-Path (Join-Path $repoRoot $_) }
if ($filesExist) {
  Fix-TrailingWhitespace -Paths $FilesToStash
} else {
  Write-Host "   (No files to fix)" -ForegroundColor Gray
}

Write-Host "2. Stashing modified files..." -ForegroundColor Cyan
$toStash = $FilesToStash | Where-Object { Test-Path (Join-Path $repoRoot $_) }
if ($toStash) {
  Invoke-GitStash -Message "pre-story-$Story-setup" -Paths $toStash
} else {
  Write-Host "   (Nothing to stash)" -ForegroundColor Gray
}

Write-Host "3. Removing conflicting local files (master has merged versions)..." -ForegroundColor Cyan
foreach ($f in $FilesToRemove) {
  $fullPath = Join-Path $repoRoot $f
  if (Test-Path $fullPath) {
    Remove-Item $fullPath -Force
    Write-Host "   Removed $f"
  }
}

Write-Host "4. Pulling latest master..." -ForegroundColor Cyan
git pull origin master

Write-Host "5. Running new-story.ps1 (no DraftPR - we add commits first)..." -ForegroundColor Cyan
& "$PSScriptRoot\new-story.ps1" -Epic $Epic -Story $Story -Slug $Slug -CreateWorktree -WorktreeRoot $WorktreeRoot

if (-not (Test-Path $worktreePath)) {
  Write-Host "ERROR: Worktree not found at $worktreePath" -ForegroundColor Red
  exit 1
}

Write-Host "6. Copying story artifacts into worktree..." -ForegroundColor Cyan
foreach ($f in $StoryArtifacts) {
  $src = Join-Path $repoRoot $f
  $dst = Join-Path $worktreePath $f
  $dstDir = Split-Path $dst
  if (-not (Test-Path $dstDir)) {
    New-Item -ItemType Directory -Path $dstDir -Force | Out-Null
  }
  if (Test-Path $src) {
    Copy-Item $src $dst -Force
    Write-Host "   Copied $f"
  } else {
    Write-Host "   SKIP: $f not found in main repo" -ForegroundColor Yellow
  }
}

Write-Host "7. Committing story artifacts in worktree..." -ForegroundColor Cyan
Push-Location $worktreePath
$artifactPaths = $StoryArtifacts | Where-Object { Test-Path (Join-Path $worktreePath $_) }
if ($artifactPaths) {
  git add $artifactPaths
  $commitMsg = "docs($Story): add Story $Story artifacts and single-session Dev prompt"
  $commitResult = git commit -m $commitMsg 2>&1
  if ($LASTEXITCODE -eq 0) {
    git push origin $storyBranch
    Write-Host "`n8. Creating draft PR..." -ForegroundColor Cyan
    $prTitle = "epic${Epic}: Story $Story - $Slug"
    gh pr create --draft --base master --head $storyBranch --title $prTitle --body "Draft story PR. Single-session Dev implementation."
  } else {
    Write-Host "   (No new commit - files may already be committed)" -ForegroundColor Yellow
  }
}
Pop-Location

Write-Host "`nDone. Open worktree in Cursor: $worktreePath" -ForegroundColor Green
Write-Host "`nOptionally restore stashed Epic docs in main repo: git stash pop" -ForegroundColor Gray
