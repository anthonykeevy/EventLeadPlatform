# Backlog: Team Collaboration - Publish Request Chat History

## Context
During Epic 5 (Form Readiness & Review Governance), we implemented a basic publish request workflow. A Company User can send a message when requesting to publish, and a Company Admin can review and approve/reject it. However, the system currently lacks a robust communication loop to track the Admin's response or maintain a history of the conversation for a specific form.

## Requirement
Add an "Advanced (Chat History)" communication feature to the platform under the Team Collaboration Epic. 

## Acceptance Criteria
1. **Database Schema**:
   - Create a `PublishRequestComment` (or similar) table linked to `FormPublishRequest` to allow multiple back-and-forth messages (or at minimum, save the Admin's comment alongside the Requester's message).
2. **Form Details View (Requester)**:
   - When a form is rejected, display a clear alert banner indicating the rejection and showing the Admin's specific rejection reason.
   - Provide a "History" or "Activity" feed showing past publish requests, who made them, and who approved/rejected them along with the associated comments.
3. **Form Review Page (Admin)**:
   - Display the historical thread of publish requests and comments for the form.
   - Allow the Admin to enter a rejection reason or approval comment that gets permanently saved and relayed back to the Requester.
4. **Privacy / Security**:
   - Standard RBAC applies. Only users within the same Tenant/Company who have access to the Event/Form can view the chat history. No special encryption or "hidden" statuses are required beyond standard tenant isolation.