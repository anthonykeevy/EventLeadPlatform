# Story 5.5 setup - delegates to generic setup-story.ps1
# Run from: EventLeadPlatform repo root

& "$PSScriptRoot\setup-story.ps1" `
  -Epic 5 `
  -Story "5.5" `
  -Slug "preview-production-governance" `
  -StoryArtifacts @(
    "docs/stories/story-5.5.md",
    "docs/stories/story-context-5.5.xml",
    "docs/stories/STORY-5.5-UAT-TEST-GUIDE.md",
    "docs/stories/STORY-5.5-SINGLE-SESSION-DEV-PROMPT.md"
  ) `
  -WorktreeRoot "C:\wt\elp"
