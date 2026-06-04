# Story 6.5e Landing — Single-Session Dev Prompt

You are implementing **Story 6.5e Landing — Customer-Facing Beta Landing Page**.

**Worktree:** `C:\wt\elp\story-epic6-6.5e-landing-page`  
**Branch:** `story/epic6-6.5e-landing-page`  
**PR:** [#117](https://github.com/anthonykeevy/EventLeadPlatform/pull/117) — Draft -> `develop`  
**Base:** `develop`

---

## Mission

Replace the current developer-friendly root page with a customer-facing beta landing page for EventLead.

The page must help a non-technical visitor understand that EventLead is a customer engagement form platform for marketing, events, operations, and agencies. It must encourage account creation, support customer discovery follow-up, and avoid exposing internal development details.

This story is intentionally **not** Form Builder vision work. Image-to-form, billing, Stripe, and production infrastructure are out of scope.

---

## Read First

1. `docs/stories/story-6.5e-landing-page.md`
2. `docs/stories/story-context-6.5e-landing.xml`
3. `docs/LANDING-PAGE-BRIEF.md`
4. `docs/customer-discovery/README.md`
5. `docs/customer-discovery/PROGRAM-STATUS.md`
6. `docs/customer-discovery/feature-resonance-scorecard.md`
7. `docs/customer-discovery/tenancy-sharing-and-dashboards.md`
8. `frontend/src/App.tsx`
9. `frontend/src/features/auth/components/SignupForm.tsx`

---

## Step 0 — Preflight

Run from the worktree root:

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.5e-landing-page" `
  -ExpectedBranch "story/epic6-6.5e-landing-page" `
  -ReportFile "docs/stories/STORY-6.5e-LANDING-PREFLIGHT.md"
```

Confirm:

- Worktree path is correct.
- Branch is `story/epic6-6.5e-landing-page`.
- PR targets `develop`.
- No Alembic migration is needed.

---

## Step 1 — Plan In Chat

Before editing, provide an 8-12 bullet plan covering:

- Component/file shape.
- How `/` will be changed.
- CTA routing.
- SEO/AEO approach.
- Beta trust/footer handling.
- Safe visuals/examples approach.
- Test commands.
- Known follow-up blockers, especially Privacy/Terms if no working links exist.

---

## Step 2 — Implement Landing Page

Preferred implementation:

- Extract the current inline `HomePage` from `frontend/src/App.tsx` into a customer-facing component under `frontend/src/features/marketing/`.
- Keep `App.tsx` routing simple: `/` renders the new landing component.
- Do not alter auth flows unless required for CTA routing.

Required content:

- Trust/status line: `Free Beta from Signal Platforms. Built for marketing, events and customer-engagement teams.`
- One H1. Use brief-aligned language such as `Build customer engagement forms your marketing team can actually use`.
- Clear hero headline/subheadline.
- Primary CTA: `Create an account` -> `/signup`.
- Secondary CTA: `See example forms` -> in-page examples/use-cases section unless safe public examples exist.
- Problem section: the form is only one part of the workflow.
- Capability cards: branded forms, capture anywhere, approval/governance, follow-up/export, teams/workspaces.
- Use-case tiles: event lead capture, demo/test-drive requests, registrations/RSVPs, feedback/NPS, product inquiries, kiosk/reception capture, agency/client campaign forms.
- Differentiation: generic forms collect answers; EventLead focuses on the broader customer engagement workflow.
- FAQ section with crawlable text.
- Final CTA band.
- Beta trust section.
- Footer with Signal Platforms Pty Ltd and Privacy/Terms handling.

Required removals from public root:

- Development Environment Ready.
- Backend API Connected/Not Running.
- Python/Node/SQL Server/Docker/package counts.
- Swagger/API docs link.
- Database Connection Test link.
- MailHog link.
- Local backend start command.
- React/FastAPI/SQL Server architecture footer.

---

## Step 3 — SEO / AEO

Implement the best available option in the current app architecture:

- Set document title for the landing page.
- Add/update meta description if practical.
- Keep exactly one H1.
- Use logical H2s from the brief.
- Add FAQ content in normal DOM text.
- Add JSON-LD for `SoftwareApplication`, `FAQPage`, and/or `Organization` if it can be done cleanly without new dependencies.
- Use useful alt text for any visual/mock UI.

Do not add a new dependency only for metadata unless there is already a local pattern requiring it.

---

## Step 4 — Tests And Checks

Run the fastest targeted checks first, then broaden if risk is high:

```powershell
cd frontend
npm run build
npm run lint
npm run test:run
```

If targeted component/routing tests are added, run them explicitly and record the command.

Record results in:

- `docs/stories/STORY-6.5e-LANDING-GATE-EVIDENCE.md`

---

## Step 5 — Closeout

Before marking Ready for UAT:

1. Fill `STORY-6.5e-LANDING-GATE-EVIDENCE.md`.
2. Fill `STORY-6.5e-LANDING-IMPLEMENTATION-FRICTION-LOG.md` if anything took multiple attempts.
3. Update `docs/stories/story-6.5e-landing-page.md` status and PR number.
4. Confirm `EPIC-6-STATUS.md` and `EPIC-6-WORKFLOW-GUIDE.md` still describe the correct next focus.
5. Mark PR Ready for UAT. Do not merge.

---

## Acceptance Criteria Summary

The implementation is acceptable when:

- Root route is customer-facing.
- CTA to `/signup` works.
- No developer-only diagnostics appear on `/`.
- Beta warning is visible and honest.
- Claims align with customer discovery docs.
- SEO/AEO basics are present.
- Mobile and keyboard use are acceptable.
- Build/lint/test status is recorded.

---

*Story 6.5e Landing SM pack — 2026-06-03.*
