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

### Builder (form definition authoring)

**Canvas**:
The screen area in the Builder that mimics where the Form will appear — Users drag Components from the Toolbox and place them freely on the Canvas.
_Avoid_: page (without qualifier), artboard alone

**Toolbox**:
The palette of catalog Component types available to add to a Form — compact previews, not the live Form.
_Avoid_: sidebar (implementation detail), component list

**Component**:
A typed instance on the form canvas (catalog type, props, structure) — a grid-based container that holds one or more objects. Identified in `FormDefinition` by component id and `type` (e.g. email, rating).
_Avoid_: field (without type), widget (generic)

**Object**:
One layout/render unit inside a Component — e.g. label, input, validation, action, divider. Objects are positioned by grid layout and rendered through UniversalFieldShell.
_Avoid_: component (the container is the Component), DOM node

**Grid layout**:
The structure that defines how objects are arranged inside a Component — rows, columns, gaps, and cell assignments mapping grid coordinates to object ids. The canonical v3 layout system; not used for Canvas placement.
_Avoid_: object layout (legacy v1 — being removed), canvas layout

**Surface**:
Where a Component is rendered in the Builder framework — one of three: **Toolbox** (palette preview), **Canvas** (authoring WYSIWYG), or **Runtime** (live Form without builder chrome). The same Component definition; behaviour and chrome differ by surface.
_Avoid_: mode (ambiguous), view alone

**Runtime**:
The surface where the Form is shown to respondents — preview or production — with builder-only visuals removed. Same Component definitions as Canvas, rendered through the public Form path.
_Avoid_: canvas, preview alone (preview is a kind of runtime)

**Structure**:
The catalog-defined skeleton of a Component type — which objects exist (label, input, validation, …) and their default layout metadata from the registry. Not user-edited per instance.
_Avoid_: props, grid layout (grid config is props or defaults, not structure)

**Props**:
Per-instance Component settings on the Canvas — values, style overrides, validation, and grid layout overrides. Edited in the properties panel; may inherit from global or company defaults.
_Avoid_: structure (skeleton), definition alone

