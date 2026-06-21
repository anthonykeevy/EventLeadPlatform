# EventLeadPlatform

B2B platform for capturing respondent data at events and other touchpoints via branded forms, with company-scoped ownership, approval workflows, and publication to public links.

## Language

### Capture

**Submission**:
A completed capture of answers submitted through a published form link, persisted as one record with its form version and link context.
_Avoid_: Lead (customer/marketing language only), response, entry

### Forms

**Form**:
The respondent-facing web page opened via a PublicLink — the rendered experience built from a FormVersion definition.
_Avoid_: form record, template (without qualifier)

**Form header**:
The durable owning record for a form — name, company, parent Event, lifecycle and approval status, dashboard metrics, and form availability settings. Not the rendered page.
_Avoid_: Form (reserved for the respondent-facing page), form entity

**FormVersion**:
A numbered snapshot of a form's design (fields, layout, logic) stored as definition JSON.
_Avoid_: draft (without version number), schema alone

**Builder**:
The authoring environment where a User edits a FormVersion definition — fields, layout, and logic — before publish. Not the form header and not the respondent-facing Form.
_Avoid_: editor (without qualifier), form designer alone

**Approval**:
A governance decision that authorizes a form header to go live — required for some Companies or roles before Publish.
_Avoid_: publish (when you mean only the authorization step), sign-off alone

**Publish**:
The go-live action that makes a Form accept real Submissions — activates the PRODUCTION PublicLink and the active FormVersion on the form header.
_Avoid_: deploy, go live (without qualifier), approval

**PublicLink**:
A tokenized URL that opens a Form. Preview links render the latest version number; production links render the active FormVersion.
_Avoid_: public URL, token, share link

### Tenancy

**Company**:
The customer organization using EventLead — the tenant that owns form headers, events, and submission visibility. Parent/subsidiary links are still Companies, not a separate concept.
_Avoid_: account, organization, tenant

**Event**:
A Company-scoped container that groups related form headers for management and attribution — e.g. "Public website", "Launch event". A form header always belongs to exactly one Event. An Event may have an optional start/end window; not all Events do.
_Avoid_: calendar invite alone, session, campaign

**Form availability**:
The window during which a Form accepts Submissions. Set manually on the form header, scheduled to a fixed date, or tied to the parent Event's end when that Event has dates.
_Avoid_: expiry (without qualifier), unpublish mode (implementation label)

### People & access

**User**:
A person with a platform login (email, profile, authentication). Exists independently of any single Company.
_Avoid_: account, member (without company qualifier)

**Company membership**:
A User's relationship to a Company — including role (e.g. Company Admin, Company User, Company Viewer) and membership status. Permissions are evaluated in this context, not from the User alone.
_Avoid_: user role (ambiguous — prefer the full membership role name)
