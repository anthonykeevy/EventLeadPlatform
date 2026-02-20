# Terms URL — Blockers and Mitigations

**Purpose:** Document what can go wrong when using external URLs for Terms and how we handle each case.  
**Context:** Story 5.7; Assets → Terms (URL-based)  
**Created:** 2026-02-18  

---

## 1. Summary

When a company adds Terms by URL (e.g. `https://their-site.com/terms.pdf`), several things can prevent successful display or embedding. This document lists blockers and our mitigations.

---

## 2. Embedding Blockers (iframe)

| Blocker | Cause | Mitigation |
|---------|-------|------------|
| **X-Frame-Options: DENY** | Target server blocks all framing | Validate before add; show "Open in new tab" only |
| **X-Frame-Options: SAMEORIGIN** | Target allows framing only from same origin; we are cross-origin | Same as above |
| **CSP frame-ancestors 'none'** | Content Security Policy blocks framing | Same as above |
| **CSP frame-ancestors 'self'** | Same as SAMEORIGIN | Same as above |
| **CSP frame-ancestors [domain list]** | Our domain not in allowed list | Same as above |

**Handled:** Validation endpoint checks headers server-side; we show embeddable/not embeddable. When not embeddable, we always offer "Open in new tab". Production simulation shows info banner for URL terms.

---

## 3. Reachability Blockers

| Blocker | Cause | Mitigation |
|---------|-------|------------|
| **404 Not Found** | URL or path changed | Validation fails; show reason; allow add with warning |
| **403 Forbidden** | Access restricted (auth, IP, region, or host blocks non-allowlisted domains) | Suggest IT add our domain to host's allowlist; or upload PDF |
| **401 Unauthorized** | Login required to view | Same as 403 — may need allowlist; or upload PDF |
| **Timeout** | Slow or unresponsive server | Validation fails with "Could not reach URL" |
| **DNS failure** | Domain doesn't resolve | Same as timeout |
| **Redirect loop** | URL redirects indefinitely | Backend limits redirects (e.g. 5); fails with loop |
| **SSL/certificate error** | Invalid or expired cert on target | Validation fails; HTTPS required |
| **Rate limiting** | Target blocks our validation requests | Validation fails; user can retry later |

**Handled:** Validate endpoint catches these and returns `embeddable: false` with a reason. User can still add URL — it will open in new tab.

---

## 4. Content and Format Blockers

| Blocker | Cause | Mitigation |
|---------|-------|------------|
| **Mixed content** | Our app is HTTPS, URL is HTTP | Reject HTTP URLs at validation and add (HTTPS only) |
| **Wrong Content-Type** | URL returns HTML instead of PDF | Embedding may work; display depends on browser. No strict enforcement today. |
| **Non-PDF** | Terms page is HTML (common for Terms of Service) | iframe can display HTML; works if embeddable |
| **Large file** | PDF > reasonable size | No limit today; browser handles |

**Handled:** HTTPS enforced. Other cases: validation reports embeddability; user can add anyway and use new-tab fallback.

---

## 5. Change-Over-Time Blockers

| Blocker | Cause | Mitigation |
|---------|-------|------------|
| **URL moved/removed** | Company changes site structure | Periodic re-validation; "Re-check" button in UI (future) |
| **Headers changed** | Target adds X-Frame-Options or CSP later | Same as above |
| **Domain expired** | Company lets domain lapse | Validation fails on next check |

**Handled:** PM decision: "Works when tested but may stop working later if their company changes policy." We warn in UI. Re-validation on demand is a future enhancement.

---

## 6. Our Own Constraints

| Blocker | Cause | Mitigation |
|---------|-------|------------|
| **Our CSP** | If our app sets strict CSP | Ensure `frame-src` or `child-src` allows loading external URLs when we embed; or use new-tab only for non-embeddable |
| **CORS** | Validation is server-side (backend fetches URL) | CORS does not apply to server-to-server; some targets may block our backend's User-Agent or IP |
| **Same-origin for blob** | Uploaded PDFs served from our domain | No issue; we control headers |

---

## 7. Recommended UI Copy

- **When validation fails:** Show the `reason` from the API (e.g. "X-Frame-Options: DENY") and the `next_action`.
- **403/401 next_action:** "Ask your IT team or the document host to add our platform's domain to their authorized/allowlist so we can display Terms in a pop-up for form users. Or upload a PDF for full control."
- **When adding non-embeddable URL:** "This URL cannot be embedded. Form users will open it in a new tab."
- **General warning:** "External URLs may stop working if the host changes policy. Validate before adding."
- **CSP / embedding:** "Some sites block embedding. If the preview is blank, use the link below to open in a new tab." (No specific domain names.)

---

## 8. Example URL for Visual Reference

**Goal:** Obtain a real Terms URL from a company that does **not** have blockers (reachable, embeddable, HTTPS, stable) so we can:
- See how the presentation looks when everything works
- Use as a visual/UX reference and test case for the inline display
- Contrast with the PDF view controls (same user-facing behaviour where possible)

**Action:** Research and document one or more example Terms URLs that pass validation. Good candidates: smaller companies with simple hosting (fewer security headers), or terms served from CDN/docs providers that allow embedding.

---

## 9. Future Enhancements

---

*Reference: document-display-and-platform-defaults.md, STORY-5.7-PM-DECISIONS.md*
