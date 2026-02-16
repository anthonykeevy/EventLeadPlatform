# Remove completed Story 5.1 and 5.2 worktrees
# Run from main repo root. Close Cursor windows/open folders for these paths first.
# If "git worktree remove" fails (e.g. OneDrive path, permission denied), manually delete
# the folders below, then run: git worktree prune

$WorktreeRoot = if ($env:ELP_WORKTREE_ROOT) { $env:ELP_WORKTREE_ROOT } else { "C:\wt\elp" }

$Completed = @(
    # Story 5.1
    "story-epic5-5.1-background-asset-management",
    "task-5.1-T01-asset-contracts-and-config-foundations",
    "task-5.1-T02-db-migration-asset-metadata",
    "task-5.1-T03-backend-asset-service-and-upload-api",
    "task-5.1-T04-frontend-builder-asset-upload-and-library",
    "task-5.1-T05-shared-resolver-parity",
    "task-5.1-T06-placement-intersection-and-cropping",
    "task-5.1-T07-data-url-guard-and-cleanup",
    "task-5.1-T08-integration-and-uat-polish",
    # Story 5.2
    "story-epic5-5.2-company-form-defaults",
    "task-5.2-T01-database-form-defaults-component-catalog",
    "task-5.2-T02-defaults-api-crud-merge-resolver",
    "task-5.2-T03-form-builder-init-api",
    "task-5.2-T04-dashboard-form-branding-defaults",
    "task-5.2-T05-builder-inherit-override-init-api",
    "task-5.2-T06-resolver-apply-defaults-renderer",
    "task-5.2-T07-builder-defaults-new-form-save-company",
    "task-5.2-T08-integration-uat"
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
