# Git helper scripts (PowerShell)

These helpers automate the **branch + worktree + PR** setup described in:

- `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

All scripts support `-DryRun` to print commands without executing.

## Scripts

- `scripts/git/new-story.ps1` — create a story branch, push, (optional) create story worktree, (optional) open Draft PR to `master`.
- `scripts/git/new-task.ps1` — create a task branch off a story branch, push, (optional) create task worktree, (optional) open PR into the story branch.

## Examples

Create a story branch and Draft PR (print only):

```powershell
./scripts/git/new-story.ps1 -Epic 3 -Story "3.10" -Slug "grid-layout" -DraftPR -CreateWorktree -DryRun
```

Create a task branch and PR into the story branch:

```powershell
./scripts/git/new-task.ps1 -StoryBranch "story/epic3-3.10-grid-layout" -StoryId "3.10" -TaskId "T03" -Slug "grid-css-rendering" -CreateWorktree -CreatePR -DryRun
```

