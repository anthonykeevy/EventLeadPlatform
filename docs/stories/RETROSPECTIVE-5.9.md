# Retrospective: Epic 5 - Story 5.9 (Hardening & UAT)

## What Went Well
- **UAT Execution Flow**: The structured UAT Guide proved highly effective in surfacing edge cases that were missed during individual unit testing, particularly around the interactions between Company Defaults and the Form Builder.
- **Problem Resolution Speed**: Complex architectural bugs (e.g., injecting the company terms dynamically into the form definition at render-time without saving it permanently) were diagnosed and resolved quickly while maintaining the integrity of the underlying models.
- **Frontend vs Backend Alignment**: The shared resolver mechanism (ensuring builder parity with the public view) held up very well under scrutiny, confirming the architectural choices made earlier in the Epic.

## What Didn't Go Well
- **Local Asset Storage in Worktrees**: The team encountered significant friction due to Git worktree isolation. Specifically, uploaded test assets (PDFs) were stored locally within one worktree and weren't accessible when a new branch/worktree was created. This caused 404 errors during preview testing until a shared local storage strategy was implemented (`ASSET_STORAGE_LOCAL_DIR`).
- **FileResponse Defaults**: The FastAPI default for `FileResponse` triggered downloads rather than inline browser viewing, which contradicted the UX expectations for viewing Terms of Service. This required an unexpected intervention to manually handle the `content_disposition_type="inline"` based on a query parameter.
- **Missing Communication Loop**: The backend `FormPublishRequest` model was only designed to capture the requester's initial message. We did not originally account for the Admin's response or rejection reason, leading to a gap in the UI on the Form Review page and Form Detail View.

## Lessons Learned
- **Environment Parity**: Always ensure that local development environments (specifically regarding uploaded media/assets) are configured to act predictably across Git branches/worktrees, or clearly document how to use cloud staging blobs early on.
- **Industry Standards vs Assumptions**: The discussion around updating global branding on existing forms highlighted the importance of researching industry standards (HubSpot, Typeform) *before* building complex retroactive update scripts. We saved a lot of engineering effort and risk by confirming our approach matches the safest industry standard.

## Action Items
1. **Backlog - Team Collaboration**: Create a new backlog item for the "Team Collaboration" Epic to implement a complete Chat History/Response Thread for Publish Requests, allowing Admins to provide feedback and Requesters to view it.
2. **Backlog - Global Branding**: Create a feature request backlog item for a "Sync with Company Default" button inside the Form Builder for existing forms, rather than forcing auto-updates.
3. **Architecture Check**: Ensure future endpoints that stream files (PDFs, images) explicitly declare their expected content disposition based on the UX requirements of the frontend calling them.