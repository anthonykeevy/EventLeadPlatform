# Remove completed Story 5.1 worktrees
# Run from main repo root. If "git worktree remove" fails (e.g. OneDrive path),
# manually delete the folders below, then run: git worktree prune

$WorktreeRoot = if ($env:ELP_WORKTREE_ROOT) { $env:ELP_WORKTREE_ROOT } else { "C:\wt\elp" }

$Completed = @(
    "story-epic5-5.1-background-asset-management",
    "task-5.1-T01-asset-contracts-and-config-foundations",
    "task-5.1-T02-db-migration-asset-metadata",
    "task-5.1-T03-backend-asset-service-and-upload-api",
    "task-5.1-T04-frontend-builder-asset-upload-and-library",
    "task-5.1-T05-shared-resolver-parity",
    "task-5.1-T06-placement-intersection-and-cropping",
    "task-5.1-T07-data-url-guard-and-cleanup",
    "task-5.1-T08-integration-and-uat-polish"
)

foreach ($name in $Completed) {
    $path = Join-Path $WorktreeRoot $name
    if (Test-Path $path) {
        Write-Host "Removing worktree: $path"
        try {
            git worktree remove $path --force 2>&1
            if ($LASTEXITCODE -ne 0) {
                Write-Host "  -> git remove failed. Manually delete: $path"
                Write-Host "  -> Then run: git worktree prune"
            }
        } catch {
            Write-Host "  -> Error: $_"
        }
    }
}

Write-Host ""
Write-Host "If any failed, manually delete folders and run: git worktree prune"
