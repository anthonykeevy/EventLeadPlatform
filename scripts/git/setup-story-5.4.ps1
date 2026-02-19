# Story 5.4 setup - delegates to generic setup-story.ps1
# Run from: EventLeadPlatform repo root

& "$PSScriptRoot\setup-story.ps1" `
  -Epic 5 `
  -Story "5.4" `
  -Slug "shared-resolver-parity" `
  -StoryArtifacts @(
    "docs/stories/story-5.4.md",
    "docs/stories/story-context-5.4.xml",
    "docs/stories/STORY-5.4-UAT-TEST-GUIDE.md",
    "docs/stories/STORY-5.4-SINGLE-SESSION-DEV-PROMPT.md"
  ) `
  -WorktreeRoot "C:\wt\elp"
