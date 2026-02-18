# Story 5.7 — UX/Design Consultation Feedback

**For:** Product Manager (decision-maker)  
**From:** UX Expert (Sally), UX Designer (Sally), Business Analyst (Mary)  
**Context:** 3 remaining open questions from STORY-5.7-PM-DECISIONS.md  
**Created:** 2026-02-17  
**Status:** PM decided — see STORY-5.7-PM-DECISIONS.md "Resolved (Final PM Decisions)"  

---

## Purpose

Consultation feedback to support PM decisions on the three open items before implementation.

---

## Question 1: Mobile/Responsive for Company Settings

**Context:** Company Settings has a sidebar nav (Company Details | Form Approval Workflow | Form Branding | Assets). Desktop layout: fixed left nav (w-52), main content. PM deferred; suggested options: accordion on small screens, or stacked cards.

### Sally (UX Expert / UX Designer)

**Recommendation: Collapsible hamburger + bottom sheet or full-screen overlay on mobile**

- **Problem:** A 4–6 item sidebar doesn't translate well to small screens. Tabs can work but hide the "hub" feeling; accordion risks long scroll; stacked cards can feel scattered.
- **Preferred pattern:** 
  - **Tablet (≥768px):** Keep sidebar — it works. Possibly collapse to icons-only with labels on hover/expand.
  - **Mobile (<768px):** **Hamburger menu** in the header that opens a **full-width bottom sheet or slide-over panel** with the nav items. User taps a section → content loads in main area → sheet closes (or stays open for quick switching). This preserves "hub" and avoids endless scroll.
- **Alternative:** **Horizontal scroll tabs** (e.g. Company Details | Workflow | Branding | Assets) — compact, familiar, one tap to switch. Best if sections are relatively shallow.
- **Avoid:** Pure accordion for 4+ sections — users lose context of where they are. Stacked cards only if each section is very short.

**Summary:** Hamburger + slide-over/bottom sheet for mobile; horizontal tabs as a simpler fallback.

---

### Mary (Business Analyst)

**Recommendation: Align with existing platform patterns**

- **Requirement:** Company Settings must be usable on mobile/tablet. Audience: Company Admins — often desk-based but may access on phone (e.g. urgent billing update).
- **Data point:** Form Branding page (accordion-style sections within content) — if that pattern exists, reuse for consistency.
- **Specification:** 
  - **Breakpoint:** Define mobile as &lt;640px (Tailwind `sm`); tablet 640–1024px.
  - **Mobile:** Nav becomes **horizontal scroll tabs** at top of content, or **hamburger → slide-over**. Content area uses existing form patterns (stacked, full width).
  - **Acceptance:** No horizontal scroll of page on 320px viewport; all nav items reachable; no "pinch to zoom" required for form inputs.

**Summary:** Reuse platform patterns; define breakpoints; ensure nav is reachable and content readable on 320px.

---

### PM Decision Support

| Option | Pros | Cons |
|--------|------|------|
| **Hamburger + slide-over** | Clean, preserves hub feel, familiar | Slightly more dev effort |
| **Horizontal scroll tabs** | Simple, common, quick to build | Can feel cramped with 4+ items |
| **Accordion** | Minimal change | Poor for 4+ sections; context loss |
| **Stacked cards** | Visual, scannable | Long scroll; not true navigation |

**Suggested decision:** Hamburger + slide-over for mobile (&lt;768px); keep sidebar for tablet and desktop. Horizontal tabs as fallback if scope is tight.

---

## Question 2: ABR Search — Popup vs Inline

**Context:** Company Details page will have ABR search (AU only). Currently in OnboardingStep2 it's inline — a teal box with SmartCompanySearch. PM favours popup for neatness.

### Sally (UX Expert / UX Designer)

**Recommendation: Popup/modal — with caveats**

- **Why popup works:**
  - Company Details has many fields: display name, legal name, ABN, billing address, contact, etc. ABR search is a **distinct sub-task** ("find my company in the register"). A popup keeps the main form clean and focused.
  - User mental model: "I'm filling company details" vs "I'm searching a register" — the popup creates a clear boundary.
  - Less scrolling; less cognitive load when returning to the form with pre-filled data.
  
- **Caveats:**
  - **Discoverability:** Ensure a clear primary CTA — e.g. "Search Australian Business Register" button that opens the popup. Don't hide it.
  - **Flow:** After selection, popup closes and form populates. Show a brief success message ("Company details filled from ABR") so the user knows what happened.
  - **Escape hatch:** "Enter manually" link inside the popup and/or on the main form. Some users will skip search.
  - **Accessibility:** Modal must be keyboard-trappable, focus returns to trigger on close, and screen readers announce the dialog.

- **When inline is better:** If Company Details is very short (e.g. 4–5 fields total), inline might suffice. Given billing address, contact, etc., the form is long — popup wins.

**Summary:** Popup recommended. Ensure discoverability, clear success feedback, and manual-entry fallback.

---

### Mary (Business Analyst)

**Recommendation: Popup — supports requirement traceability**

- **Requirement:** "ABR search in popup for cleaner Company Details screen" (PM).
- **Use case:** AU company admin opens Company Details → chooses "Search ABR" → popup opens → searches by ABN/ACN/name → selects company → popup closes → form auto-fills.
- **Edge cases to document:**
  1. User opens popup, searches, finds nothing → can dismiss and enter manually.
  2. User opens popup, selects company → popup closes → user can override any auto-filled field.
  3. Non-AU users: no ABR; popup/button not shown; manual entry only.
- **Acceptance:** Popup is reachable from Company Details; on selection, form updates; user can always fall back to manual entry.

**Summary:** Popup aligns with PM preference and keeps form manageable. Document edge cases for implementation.

---

### PM Decision Support

| Option | Pros | Cons |
|--------|------|------|
| **Popup/modal** | Clean form; clear sub-task; PM preference | Must ensure discoverability; a11y |
| **Inline** | No modal; current Onboarding pattern | Longer form; more scroll; cognitive load |

**Suggested decision:** **Popup.** Add "Search Australian Business Register" button; on click, open modal with SmartCompanySearch; on selection, close and populate form. Include "Enter manually" in modal and on form.

---

## Question 3: Image Swap Alignment — Technical Rules for Safe Swap

**Context:** Company changes logo; wants to replace image A with image B across all forms. PM: same dimensions confirmed. Need to specify: aspect ratio, MIME type, or other attributes?

### Sally (UX Expert / UX Designer)

**Recommendation: Focus on user expectations, not just tech**

- **User story:** "I uploaded a new logo. I want it to replace the old one everywhere it's used."
- **User expectation:** The new image appears in the same spots, same size/frame. They don't think in pixels or aspect ratio — they think "swap logo."
- **UX implications:**
  - **Same dimensions:** Safest — layout won't break. Recommend this as the default.
  - **Same aspect ratio, different size:** Often acceptable (e.g. 500×200 → 1000×400). Renderer typically scales. Lower risk if we use `object-fit: contain` or similar.
  - **Different aspect ratio:** Risk of stretch/squash. We should **warn** the user: "New image has different proportions. Some forms may look different. Preview before applying."
  - **MIME type:** PNG vs JPG vs WebP — usually irrelevant for layout. Transparency (PNG) vs not (JPG) can matter for overlays. Recommend: allow swap across MIME types; if new image lacks transparency and old had it, show a warning.
  
- **Suggested UI:** 
  - Swap wizard: "Replace [Old Logo] with [New Image]"
  - Pre-swap: Show list of forms affected.
  - Validation: If dimensions mismatch, show warning with option to "Apply anyway" or "Cancel."
  - Success: "Replaced in 5 forms."

**Summary:** Same dimensions = auto-allow. Different aspect ratio = warn, allow with confirmation. MIME/transparency = warn if going from transparent to opaque. Prioritise user control and clear feedback.

---

### Mary (Business Analyst)

**Recommendation: Define swap rules as unambiguous requirements**

- **Business rule (proposed):**
  - **BR-1:** Swap is allowed when `WidthPx` and `HeightPx` match (exact). No warning.
  - **BR-2:** Swap is allowed when aspect ratio matches (Width/Height ratio within tolerance, e.g. 1%). Show info: "Aspect ratio preserved; image may scale slightly."
  - **BR-3:** Swap when aspect ratio differs: **block** with message "New image has different proportions. Use same dimensions to avoid layout changes," OR **allow with strong warning** and require explicit confirmation. PM to choose.
  - **BR-4:** MIME type: No restriction. PNG↔JPG↔WebP all allowed. If old had alpha (PNG) and new does not (JPG): warn "Background may show where transparency was used."
  - **BR-5:** Placement/crop: Current DefinitionJSON stores `placement`, `imageSize` (cover/contain/etc). Swap updates `asset` ref only; placement is unchanged. New image is rendered into the same frame — so aspect ratio matters for visual fit.

- **Traceability:** Image swap supports use case "Company rebrand — update logo across all forms." Alignment rules prevent layout breakage and set user expectations.

**Summary:** Same dimensions = silent allow. Same aspect ratio = allow with info. Different aspect ratio = block or allow with strong confirmation (PM choice). MIME: allow; warn on transparency loss.

---

### PM Decision Support

| Rule | Behaviour | Rationale |
|------|-----------|-----------|
| **Same dimensions (W×H)** | Allow, no warning | Safest; pixel-perfect replacement |
| **Same aspect ratio** | Allow, info toast | "Image may scale slightly" — usually fine |
| **Different aspect ratio** | Block, or allow with confirmation | Risk of stretch; user must opt in |
| **MIME type** | No restriction | Layout unaffected by format |
| **Transparency (PNG→JPG)** | Warn | "Background may show where transparent" |

**Suggested decision:** 
- Allow swap when dimensions **or** aspect ratio match.
- If aspect ratio differs: **block** with message "Use an image with the same dimensions (or aspect ratio) to avoid layout changes."
- If swapping from PNG (transparent) to JPG (opaque): show warning; allow.

---

## Summary for PM

| # | Question | Consensus | PM Action |
|---|----------|------------|-----------|
| 1 | Mobile/responsive | Hamburger + slide-over for mobile; sidebar for tablet+ | Approve or choose alternative (e.g. horizontal tabs) |
| 2 | ABR popup vs inline | **Popup** — clean, discoverable, with manual fallback | Approve popup |
| 3 | Image swap alignment | Same dims = allow; same ratio = allow + info; different ratio = block (or confirm); warn on transparency loss | Approve rules; decide block vs warn for different ratio |

---

*Consultation feedback — use to finalise STORY-5.7-PM-DECISIONS.md*
