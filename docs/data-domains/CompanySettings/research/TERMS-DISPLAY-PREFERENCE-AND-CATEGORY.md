# Terms — Display Preference, Preferred Asset, and Category

**Purpose:** Design for (1) two-path URL validation (pop-up vs new tab), (2) preferred method when multiple Terms assets exist (PDF vs URL), (3) category/label for Terms of Service, Privacy Policy, consent documents.  
**Context:** Story 5.7; Assets → Terms  
**Created:** 2026-02-18  

---

## 1. Research Coverage

From **asset-management-platform-review.md**:
- **TERMS** type: "Terms of Service, Privacy Policy" for consent checkboxes
- **Tags/categories on Asset** listed as a pattern (flexible; weaker structure)
- **Separate TERMS type** vs DOCUMENT with TERMS as category

From **STORY-5.7-PM-DECISIONS.md**:
- "Terms component **automatically uses** the company's terms"
- One default when multiple exist — not explicitly designed

**Gap:** Preferred asset selection and category/label were not fully specified. This document fills that gap.

---

## 2. Two-Path URL Validation (Pop-up vs New Tab)

### Problem
When validation fails (e.g. 403), users are confused: the URL works when they open it in a browser. The failure is because **we** (the platform) cannot load it **for display in a pop-up** (iframe). The host may block our requests or embedding.

### Solution: Two Explicit Paths

| Path | Validate | Add Button | What Form Users Get |
|------|----------|------------|---------------------|
| **Pop-up** | Full check (HTTPS, reachability, embedding headers) | Add URL (pop-up) | Terms in modal/iframe; stays on form |
| **New tab** | Optional (HTTPS only); no embed check | Add URL (new tab) | Link opens in new tab; user leaves form |

### UX Copy
- **Validation error (pop-up failed):** "This URL cannot be displayed in a pop-up because [reason]. Form users would open it in a new tab instead. You can:"
  - **Add URL (new tab)** — add now; form users get a link that opens in a new tab
  - "Once your organisation has added our domain to the host's allowlist, return here and validate again to add as pop-up. Or upload a PDF for full control."
- **Add URL (pop-up):** Only enabled when validation passes. "Form users will see Terms in a pop-up and stay on the form."
- **Add URL (new tab):** Always available (HTTPS). "Form users will open this in a new tab. To switch to pop-up later, validate and re-add or contact support."

### Backend
- `addTermsUrl` accepts `display_mode: "popup" | "new_tab"`
- Store in `Asset.TermsDisplayMode` (nullable; "popup" | "new_tab"; null for PDF or legacy)
- Form runtime: if TermsDisplayMode is "new_tab" or asset is URL and embeddable=false, render as link (target="_blank"); else render iframe

---

## 3. Preferred Method (PDF vs URL)

### Problem
Company has both a PDF and a URL for Terms. Forms use "company Terms" automatically; which one?

### Options

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A. Company default asset** | `Company.DefaultTermsAssetID` or `CompanyTermsDefault` table | Single source of truth; clear | New table or Company column |
| **B. Per-asset "Use as default"** | Checkbox/star on each asset; one can be default | Familiar pattern | Need unique constraint (one default per company) |
| **C. Order/priority** | Sort order; first = default | Simple | Implicit; less obvious |

### Recommended: Option B
- Add `Asset.IsDefaultForCompanyTerms` (BIT) or `CompanyTermsDefault.CompanyID, AssetID` (one row per company)
- UI: "Use as default" star or radio on each Terms asset. Only one can be default.
- Forms Terms component: resolve company's default Terms asset; use that.

---

## 4. Category / Label

### Problem
Company uploads multiple documents: Terms of Service, Privacy Policy, consent form. Need to distinguish and optionally filter.

### Options

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A. TermsCategory ref table** | `ref.TermsCategory`: Terms of Service, Privacy Policy, Consent, Other | Clean; extensible | Migration; form component needs to pick by category |
| **B. DisplayName only** | User sets "Terms of Service" as display name | No schema change | Not structured; hard to filter/query |
| **C. Asset.TermsCategoryCode** | NVARCHAR(20): TERMS_OF_SERVICE, PRIVACY_POLICY, CONSENT, OTHER | Simple | New column |

### Recommended: Option A or C
- **ref.TermsCategory** (Code, Name): TERMS_OF_SERVICE, PRIVACY_POLICY, CONSENT, OTHER
- **Asset.TermsCategoryID** nullable FK
- UI: Dropdown on add/edit: "Terms of Service" | "Privacy Policy" | "Consent document" | "Other"
- Default: TERMS_OF_SERVICE when not specified
- Forms: Default Terms asset used for consent; future story may allow "Privacy Policy" link separately

### Minimal first pass
- Use **DisplayName** to convey category: placeholder "e.g. Terms of Service, Privacy Policy"
- Add category in a follow-up migration when we need structured filtering

---

## 5. Implementation Order

1. **Two-path URL** — UX + `TermsDisplayMode` migration + API changes ✅ Done (migration 046)
2. **Preferred asset** — `CompanyTermsDefault` or `Asset.IsDefaultForCompanyTerms` (next sprint)
3. **Category** — ref.TermsCategory + Asset.TermsCategoryID (when we need filtering)

**Category minimal first pass:** Use DisplayName with placeholder "e.g. Terms of Service, Privacy Policy" until ref.TermsCategory is added.

---

*Reference: TERMS-URL-BLOCKERS-AND-MITIGATIONS.md, asset-management-platform-review.md, STORY-5.7-PM-DECISIONS.md*
