# Document Display & Platform Default Assets

**Purpose:** Address document/terms display in the frontend, link vs upload, CORS, and platform default assets for new customers.  
**Context:** Story 5.7; asset types IMAGE, DOCUMENT, TERMS  
**Created:** 2026-02-17  

---

## 1. Browser Document Viewing — What Works Out of the Box

### 1.1 PDF

| Aspect | Details |
|--------|---------|
| **Native support** | Chrome, Edge, Safari, Firefox, Opera — all support inline PDF display (2024) |
| **Mobile** | Limited: Android browsers, Chrome/Firefox for Android generally do **not** support inline PDF viewing |
| **Detection** | `navigator.pdfViewerEnabled` (boolean) — check at runtime |
| **Display method** | `<iframe src="url.pdf">` or `<object>` or `<embed>` — no JavaScript required |

**Complexity:** **Low** for PDF on desktop. For mobile, fall back to "Open in new tab" or download link.

```html
<!-- Simple PDF embed (same-origin URL) -->
<iframe src="/api/assets/123/url" width="100%" height="600px" loading="lazy"></iframe>
```

### 1.2 Word, Excel, PowerPoint

| Aspect | Details |
|--------|---------|
| **Native support** | **None** — browsers do not render .docx, .xlsx, .pptx natively |
| **Options** | (a) Convert to PDF server-side, (b) Use Microsoft Office Web Viewer or Google Drive Viewer (external URLs), (c) Use ViewerJS or similar client-side library |

**Complexity:** **Medium to high** for Office files. **Recommendation:** For Terms, restrict to **PDF only** — universal support, no conversion.

---

## 2. Link vs Document for Terms — Options

### 2.1 Option A: Link Only (External URL)

| Pros | Cons |
|------|------|
| No upload/storage | Customer may change/remove link without our knowledge |
| No CORS if opened in new tab | Cannot embed inline — only `target="_blank"` |
| Simple to implement | Customer hosts document; we don't control availability |

**Display:** `<a href="https://customer-site.com/terms.pdf" target="_blank">Terms of Service</a>` — opens in new tab. **No CORS** for navigation.

### 2.2 Option B: Document Only (Uploaded Asset)

| Pros | Cons |
|------|------|
| We host, control availability | Requires storage, asset management |
| Same-origin → no CORS for embed | Conversion needed if non-PDF |
| Versioning, audit trail possible | Slightly more complex setup |

**Display:** `<iframe src="/api/assets/{id}/url">` — we serve from our domain. **No CORS** (same origin).

### 2.3 Option C: Both (Recommended)

Allow **either**:
- **Link:** Customer provides URL → open in new tab for "View terms"
- **Document:** Customer uploads PDF → we host, can embed or open in new tab

**Consent checkbox:** In both cases, user sees "I have read and agree to the [Terms of Service]" — link/document opens in new tab for reading. GDPR: consent must be separate, specific, unambiguous; linking to the document satisfies "informed" if the document is readable.

**Display complexity:**
- **Link:** Zero — just `target="_blank"`. User leaves our page to read.
- **Document (our URL):** Low — `<iframe>` or new-tab link. Same origin, no CORS.

---

## 3. CORS and Embedding — When It Matters

| Scenario | CORS Issue? | Notes |
|----------|-------------|-------|
| **Link opens in new tab** (`<a target="_blank">`) | No | Full navigation; user leaves our page |
| **iframe src = our URL** (e.g. `/api/assets/123`) | No | Same origin |
| **iframe src = external URL** (e.g. customer's site) | Often yes | Target site may send `X-Frame-Options: DENY` or `SAMEORIGIN`; we cannot control that |

**Conclusion:**  
- If we **host the document** (uploaded asset), we control headers → **no CORS/embed issues**.  
- If customer provides **link only**, embedding depends on the target server's headers. We can **validate** before allowing embed.  
- **Best of both:** Support both; validate external URLs; embed when possible, fall back to new-tab when not.

---

## 4. Validating External URLs for iframe Embedding

When a customer provides a Terms URL, we can **validate** whether it can be embedded before we allow iframe display. Validation must be **server-side** — the browser's same-origin policy prevents JavaScript from reading cross-origin response headers.

### 4.1 Headers That Block Embedding

| Header | Value | Effect |
|--------|-------|--------|
| **X-Frame-Options** | `DENY` | Cannot embed anywhere |
| **X-Frame-Options** | `SAMEORIGIN` | Only same-origin can embed; we're cross-origin → cannot embed |
| **Content-Security-Policy** | `frame-ancestors 'none'` | Cannot embed anywhere |
| **Content-Security-Policy** | `frame-ancestors 'self'` | Only same-origin can embed → cannot embed |
| **Content-Security-Policy** | `frame-ancestors https://app.eventlead.com` | We can embed if our domain matches |

### 4.2 Validation Flow (Backend)

1. **When customer saves a Terms URL**, backend performs a `HEAD` or `GET` request (with redirect following, limit 5).
2. **Inspect response headers** of the final URL:
   - `X-Frame-Options`
   - `Content-Security-Policy` (parse `frame-ancestors` directive)
3. **Determine embeddability:**

   | Condition | Embeddable? |
   |-----------|-------------|
   | X-Frame-Options: DENY | No |
   | X-Frame-Options: SAMEORIGIN | No (we're cross-origin) |
   | CSP frame-ancestors 'none' | No |
   | CSP frame-ancestors 'self' | No |
   | CSP frame-ancestors includes our domain | Yes |
   | No restrictive headers | Yes (default is allow) |

4. **Optional:** Verify `Content-Type: application/pdf` if we want to enforce PDF-only for Terms.
5. **Store result:** `termsUrl`, `termsUrlEmbeddable` (boolean), `termsUrlValidatedAt` (timestamp).

### 4.3 Implementation Sketch

```python
# backend: validate_terms_url(url: str) -> EmbeddabilityResult
def validate_terms_url(url: str) -> EmbeddabilityResult:
    try:
        resp = requests.head(url, allow_redirects=True, timeout=10)
        xfo = resp.headers.get("X-Frame-Options", "").upper()
        csp = resp.headers.get("Content-Security-Policy", "")

        if xfo == "DENY":
            return EmbeddabilityResult(embeddable=False, reason="X-Frame-Options: DENY")
        if xfo == "SAMEORIGIN":
            return EmbeddabilityResult(embeddable=False, reason="X-Frame-Options: SAMEORIGIN (cross-origin)")

        # Parse frame-ancestors from CSP
        if "frame-ancestors" in csp.lower():
            if "'none'" in csp.lower() or '"none"' in csp.lower():
                return EmbeddabilityResult(embeddable=False, reason="CSP frame-ancestors 'none'")
            if "'self'" in csp.lower() or '"self"' in csp.lower():
                return EmbeddabilityResult(embeddable=False, reason="CSP frame-ancestors 'self'")
            # If our domain is listed, embeddable=True

        return EmbeddabilityResult(embeddable=True)
    except Exception as e:
        return EmbeddabilityResult(embeddable=False, reason=f"Validation failed: {e}")
```

### 4.4 Caveats

| Caveat | Mitigation |
|--------|------------|
| **Headers can change** | Re-validate periodically or on-demand; cache result with TTL (e.g. 24h); allow "revalidate" button in UI |
| **Different for bots** | Use a realistic User-Agent; some CDNs treat head requests differently |
| **Redirects** | Follow redirects; check final response headers |
| **HTTPS only** | Reject `http://` URLs for Terms (security) |
| **Private/internal URLs** | May return 401/403 — treat as not embeddable; suggest upload instead |

### 4.5 UX Flow

1. Customer enters Terms URL → click "Validate" or auto-validate on blur/save.
2. Backend runs validation → returns `{ embeddable: true|false, reason?: string }`.
3. **If embeddable:** Store URL; frontend uses `<iframe src="url">` for "View terms".
4. **If not embeddable:** Show message: "This URL cannot be embedded (reason). You can: (a) Upload the document instead, or (b) Use a link that opens in a new tab." — store URL with `embeddable=false`; frontend uses new-tab only.
5. **Revalidate:** Offer "Re-check" button — headers may have changed.

---

## 5. Recommended UX for Terms Display

| Source | Display behaviour |
|--------|-------------------|
| **Uploaded asset (PDF)** | "View terms" — embed in modal or new tab; we control headers |
| **External link (embeddable)** | "View terms" — embed in modal via `<iframe src="url">` |
| **External link (not embeddable)** | "View terms" — open in new tab only |
| **Mobile** | Prefer new-tab over embed (mobile PDF embed is flaky) |

**Implementation:** Consent component stores `assetRef`, or `termsUrl` + `termsUrlEmbeddable`. When `termsUrlEmbeddable=true`, use iframe; when false, use new-tab link only.

---

## 6. Platform Default Assets for New Customers

### 6.1 Requirement

- **Default images:** A few platform-provided images available to new customers (e.g. placeholders, generic backgrounds)
- **Default Terms:** Platform Terms of Service that companies can use if they don't have their own
- **Acceptance flow:** Companies must **acknowledge/accept** platform terms before they can use them for their forms

### 6.2 Data Model

| Concept | Implementation |
|---------|----------------|
| **Platform vs company assets** | Asset with `CompanyID = NULL` (or dedicated "Platform" company) = platform assets |
| **Default images** | Platform assets with AssetType=IMAGE; seeded in migration or seed script |
| **Default Terms** | Platform asset with AssetType=TERMS; one canonical "Platform Terms of Service" |
| **Company acceptance** | New table: `CompanyPlatformTermsAcceptance` — CompanyID, AcceptedAt, AcceptedBy, TermsAssetID/Version |

### 6.3 CompanyPlatformTermsAcceptance (Proposed)

```sql
-- Company must accept platform terms before using them
CREATE TABLE [dbo].[CompanyPlatformTermsAcceptance] (
    CompanyPlatformTermsAcceptanceID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CompanyID BIGINT NOT NULL,
    TermsAssetID BIGINT NOT NULL,           -- Asset ID of accepted Terms (versioned)
    AcceptedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    AcceptedBy BIGINT NULL,                 -- UserID (Company Admin)
    IPAddress NVARCHAR(50) NULL,
    CONSTRAINT UQ_CompanyPlatformTermsAcceptance UNIQUE (CompanyID),
    CONSTRAINT FK_CompanyPlatformTermsAcceptance_Company FOREIGN KEY (CompanyID) REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_CompanyPlatformTermsAcceptance_Asset FOREIGN KEY (TermsAssetID) REFERENCES [dbo].[Asset](AssetID)
);
```

**Alternative:** Single row per company; when platform terms are updated, require re-acceptance (new TermsAssetID) — then UQ would be (CompanyID, TermsAssetID) or we'd invalidate and require new acceptance.

**Simpler MVP:** One acceptance per company; we track "last accepted Terms version". When we publish new platform terms, we notify companies and require re-acceptance before continued use.

### 6.4 Flow

1. **New company** signs up → no acceptance yet.
2. **Company Admin** goes to Company Settings → Assets (or similar).
3. **"Use platform default Terms"** — if not yet accepted, show platform terms + "I have read and agree to use these terms for my forms" checkbox.
4. On accept → insert `CompanyPlatformTermsAcceptance`; company can now select "Platform default" as Terms for consent components.
5. **Default images** — no acceptance needed; they're just optional assets. New companies see them in the asset picker (filter: CompanyID IS NULL OR CompanyID = current).

### 6.5 Asset Picker Logic

```text
List assets: (CompanyID = current_company) OR (CompanyID IS NULL AND AssetType IN (IMAGE, TERMS))
```

- Company sees their own assets + platform defaults.
- For Terms: if company has no custom Terms, offer "Use platform default" — gate on acceptance.

---

## 7. Summary & Recommendations

| Topic | Recommendation |
|-------|----------------|
| **Document display** | PDF only for Terms; browser native support on desktop. Use `<iframe>` or new-tab; avoid Office formats. |
| **Terms: Link vs document** | Support **both** — link opens in new tab; document we host, same origin, no CORS. |
| **CORS / Embed** | Validate external URLs server-side (X-Frame-Options, CSP frame-ancestors). Embed when embeddable; new-tab fallback when not. |
| **Platform default images** | Asset with CompanyID=NULL; seed a few images; show in picker for all companies. |
| **Platform default Terms** | One platform Terms asset; `CompanyPlatformTermsAcceptance` table; require acceptance before "use platform default". |
| **Complexity** | Low for PDF + new tab; low for same-origin embed; medium only if we add Office format support (not recommended for Terms). |

---

*Last Updated: 2026-02-17*
