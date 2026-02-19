# Story 5.7 setup - delegates to generic setup-story.ps1
# Run from: EventLeadPlatform repo root
#
# IMPORTANT: Commit the Story 5.7 docs and PM decisions to the main repo first,
# so the CompanySettings research docs exist for the worktree. Then run this script.

& "$PSScriptRoot\setup-story.ps1" `
  -Epic 5 `
  -Story "5.7" `
  -Slug "company-settings-hub" `
  -StoryArtifacts @(
    "docs/stories/story-5.7.md",
    "docs/stories/story-context-5.7.xml",
    "docs/stories/STORY-5.7-UAT-TEST-GUIDE.md",
    "docs/stories/STORY-5.7-SINGLE-SESSION-DEV-PROMPT.md",
    "docs/data-domains/CompanySettings/research/STORY-5.7-PM-DECISIONS.md",
    "docs/data-domains/CompanySettings/research/STORY-5.7-CONSULTATION-FEEDBACK.md",
    "docs/data-domains/CompanySettings/research/data-model-analysis.md"
  ) `
  -WorktreeRoot "C:\wt\elp"
