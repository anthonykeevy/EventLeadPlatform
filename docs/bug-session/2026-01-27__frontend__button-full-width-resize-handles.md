### Bug Session — Button Full Width not applying + resize handles broken
- **SessionId**: 2026-01-27__frontend__button-full-width-resize-handles
- **Area**: frontend
- **Status**: Active
- **Created**: 2026-01-27
- **Owner**: Anthony (UAT gate) / Agent (implementation + automation)

#### Problem statement
- **Expected**: Changing Properties panel → Button Settings → Button Width from Auto to Full Width resizes the button edge-to-edge on canvas; resize handles show all handles per `docs/COMPONENT-FRAMEWORK-REFERENCE.md`; resizing affects the button object only (validation object size remains stable).
- **Actual**: Button does not visually resize when switching Auto → Full Width; SmartBorder appears but resize handles show only corner handles; corner handles cannot resize the button; during drag, validation object expands instead of the button.
- **Impact**: Cannot author full-width buttons or resize buttons reliably on canvas; inconsistent with other components.
- **Scope boundaries** (must not change / protected zones): TBD

#### Repro (minimum)
1. Open `http://localhost:3000/forms/46/builder`.
2. Select the submit button component on the canvas.
3. Observe: `buttonWidth` is already `full`, but the button does not stretch; only corner handles appear.

#### Done criteria (machine-verifiable where possible)
- [x] DC1: Switching `buttonWidth` Auto → Full updates button rendered width to fill the component container on canvas.
- [x] DC2: Selected Button shows expected resize handles (N/E/S/W + corners) per `docs/COMPONENT-FRAMEWORK-REFERENCE.md` unless explicitly disabled by capabilities.
- [ ] DC3: Dragging resize handles changes button size (and/or component width) without expanding the validation/help object unexpectedly.
- [ ] DC4: Scripted repro (agent-browser or existing `scripts/test-resize-*.js`) passes for submit button width + handles.

#### Instrumentation plan (baseline first)
- **Frontend evidence** (if applicable): snapshot + screenshot + console + network
- **Backend evidence** (if applicable): diagnostic logs + request correlation
- **Code scope**: git status/diff before and after attempts
- **Automation**: use existing scripts: `scripts/test-frontend.ps1`, `scripts/test-resize-auto-width.js`, `scripts/test-resize-handles.js` (adapt if needed)

#### Baseline evidence (ARTIFACT LINKS)
- Snapshot: `docs/bug-session/artifacts/2026-01-27__frontend__button-full-width-resize-handles/baseline_snapshot.json`
- Selected snapshot: `docs/bug-session/artifacts/2026-01-27__frontend__button-full-width-resize-handles/baseline_selected_snapshot.json`
- Metrics: `docs/bug-session/artifacts/2026-01-27__frontend__button-full-width-resize-handles/baseline_metrics.json`
- Screenshot: `docs/bug-session/artifacts/2026-01-27__frontend__button-full-width-resize-handles/baseline_screenshot.png`
- Console: `docs/bug-session/artifacts/2026-01-27__frontend__button-full-width-resize-handles/baseline_console.txt`
- Network: `docs/bug-session/artifacts/2026-01-27__frontend__button-full-width-resize-handles/baseline_network.txt`
- Backend logs: `docs/bug-session/artifacts/2026-01-27__frontend__button-full-width-resize-handles/baseline_backend_logs.txt`
- Notes: `buttonWidth` is already `full` in props, but DOM button width is ~26px and wrapper ~46px.

#### Working hypotheses (max 3 at a time)
- H1 (confidence 6/10): `buttonWidth` updates in store, but is not applied to the rendered button element on canvas due to style resolution/surface gating or SmartBorder shrink container preventing `width: 100%` from resolving as expected.
- H2 (confidence 7/10): Resize handles are being disabled for submit button by `componentCapabilities`/`componentSurfaceCapabilities` (or wrapper event handling), so only corner handles appear and pointer events are intercepted by a wrapper preventing resizing.
- H3 (confidence 5/10): The resize target ref is attached to the wrong element (validation/help wrapper) for submit button, so drag changes overlay/validation sizing instead of the button element.

#### Attempt ledger (do not repeat failed attempts)
> Each attempt MUST follow the loop: instrument → observe → hypothesize → attempt → verify → record.

---
#### Attempt 01 — Make submit button full width + show edge handles
- **Hypothesis tested**: H1, H2
- **Change summary**:
  - Files: `frontend/src/features/builder/components/SortableComponent.tsx`, `frontend/src/features/builder/components/UniversalFieldShell.tsx`, `frontend/src/features/builder/components/ui/ResizeHandles.tsx`
  - Key change: Treat submit-button `buttonWidth=full` as explicit width + force grid stretch; enable edge handles for submit button.
- **Instrumentation**:
  - Artifacts created:
    - `docs/bug-session/artifacts/2026-01-27__frontend__button-full-width-resize-handles/after_metrics.json`
    - `docs/bug-session/artifacts/2026-01-27__frontend__button-full-width-resize-handles/after_handles.json`
    - `docs/bug-session/artifacts/2026-01-27__frontend__button-full-width-resize-handles/after_snapshot.json`
    - `docs/bug-session/artifacts/2026-01-27__frontend__button-full-width-resize-handles/after_screenshot.png`
    - `docs/bug-session/artifacts/2026-01-27__frontend__button-full-width-resize-handles/after_backend_logs.txt`
- **Verification**:
  - Automated checks run: none (UI-only change; handles verified via agent-browser DOM queries)
  - Result: **Improved** — button now spans component width when `buttonWidth=full`, and handles include N/E/S/W + corners.
- **What we learned**:
  - Submit button grid layout was shrinking items (place-items: start), so `width: 100%` on the button had no effect.
- **Next step**:
  - Validate DC3 with a reliable resize-drag automation or manual UAT; confirm validation object stays fixed while button resizes.

---
