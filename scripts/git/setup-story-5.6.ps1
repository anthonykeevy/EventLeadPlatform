# Story 5.6 setup - delegates to generic setup-story.ps1
# Run from: EventLeadPlatform repo root

& "$PSScriptRoot\setup-story.ps1" `
  -Epic 5 `
  -Story "5.6" `
  -Slug "publish-request-workflow" `
  -StoryArtifacts @(
    "docs/stories/story-5.6.md",
    "docs/stories/story-context-5.6.xml",
    "docs/stories/STORY-5.6-UAT-TEST-GUIDE.md",
    "docs/stories/STORY-5.6-SINGLE-SESSION-DEV-PROMPT.md"
  ) `
  -WorktreeRoot "C:\wt\elp"
