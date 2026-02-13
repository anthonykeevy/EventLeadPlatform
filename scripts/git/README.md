# Git helper scripts (PowerShell)

These helpers automate the **branch + worktree + PR** setup described in:

- `docs/workflows/AGENTIC-GIT-WORKTREE-WORKFLOW.md`

All scripts support `-DryRun` to print commands without executing.

## Scripts

- `scripts/git/new-story.ps1` — create a story branch, push, (optional) create story worktree, (optional) open Draft PR to `master`.
- `scripts/git/new-task.ps1` — create a task branch off a story branch, push, (optional) create task worktree, (optional) open PR into the story branch.

**After creating the worktree:** Update the task spec (`docs/tasks/<story>/<Txx>-<slug>.md`) Status to `In Progress`, update `STATUS.md`, commit + push, then create the PR. GitHub requires at least one commit to open a PR. See `docs/stories/EPIC-5-WORKFLOW-GUIDE.md` § Task kickoff.

## Examples

## Worktree root (path length on Windows)

By default, the scripts create worktrees under `..\EventLeadPlatform.wt`.

If you hit **Windows path length** issues (common with `node_modules`), use a shorter path outside OneDrive, e.g.:

- One-off per command:

```powershell
./scripts/git/new-task.ps1 ... -CreateWorktree -WorktreeRoot "C:\wt\elp"
```

- Recommended (per machine): set an environment variable so you don’t have to pass `-WorktreeRoot` every time:

```powershell
$env:ELP_WORKTREE_ROOT = "C:\wt\elp"
```

> Note: `ELP_WORKTREE_ROOT` is **local to your machine** and should not be committed to the repo.

Create a story branch and Draft PR (print only):

```powershell
./scripts/git/new-story.ps1 -Epic 3 -Story "3.10" -Slug "grid-layout" -DraftPR -CreateWorktree -DryRun
```

Create a task branch and PR into the story branch:

```powershell
./scripts/git/new-task.ps1 -StoryBranch "story/epic3-3.10-grid-layout" -StoryId "3.10" -TaskId "T03" -Slug "grid-css-rendering" -CreateWorktree -CreatePR -DryRun
```

