---
name: bug-session
description: Runs a structured scientific-loop debugging session and journals everything in docs/bug-session (instrument → observe → hypothesize → attempt → verify → record). Use for hard bugs, regressions, and “it doesn’t work” investigations.
disable-model-invocation: true
---

# Bug Session (Scientific Loop)

## Purpose
Resolve hard bugs faster by forcing a repeatable loop with strong evidence, automation-first verification, and a no-repeat attempt ledger.

This skill MUST:
- Create a bug session journal file under `docs/bug-session/`
- Capture evidence into `docs/bug-session/artifacts/`
- Iterate using: instrument → observe → hypothesize → attempt → verify → record
- Avoid repeating failed attempts by consulting the ledger before proposing a new fix

## First action: intake (ask only what’s missing)
Ask the user for:
- **Area**: `frontend` | `backend` | `database` | `mixed` | `infra`
- **Short title** (1 line)
- **Expected vs actual**
- **Repro steps** (minimum viable)
- **Where** (URL / route / API endpoint / component)
- **Done criteria** (what “fixed” means)
- **Any constraints** (files that must not change, performance, backwards-compat, etc.)

If any of the above is unknown, ask concise follow-ups. Do not start changing code until baseline evidence is captured.

## Create/Resume the session
### Naming convention (MANDATORY)
- `slug`: kebab-case, 3–10 words (no spaces)
- `session_id`: `YYYY-MM-DD__{area}__{slug}`
- **Journal file**: `docs/bug-session/{session_id}.md`
- **Artifacts folder**: `docs/bug-session/artifacts/{session_id}/`

If `docs/bug-session/` does not exist, create it (and `artifacts/`).
If a matching session already exists (same area+slug), resume it instead of creating a new file.

### Secrets policy
Never write passwords/tokens into the journal. If evidence contains secrets, redact them before saving.

## Journal template (write this immediately)
Create the journal file with:

- Title: `Bug Session — {short title}`
- Session metadata
- Baseline evidence links
- Hypotheses list
- Attempt ledger (empty at start)

Use this exact structure:

### Bug Session — {short title}
- **SessionId**: {session_id}
- **Area**: {area}
- **Status**: Active | Blocked | Resolved
- **Created**: {date}
- **Owner**: Anthony (UAT gate) / Agent (implementation + automation)

#### Problem statement
- **Expected**:
- **Actual**:
- **Impact**:
- **Scope boundaries** (must not change / protected zones):

#### Repro (minimum)
1.
2.
3.

#### Done criteria (machine-verifiable where possible)
- [ ] DC1:
- [ ] DC2:
- [ ] DC3:

#### Instrumentation plan (baseline first)
- **Frontend evidence** (if applicable): snapshot + screenshot + console + network
- **Backend evidence** (if applicable): diagnostic logs + request correlation
- **Code scope**: git status/diff before and after attempts
- **Automation**: find an existing script-based repro; if none exists, create a minimal repro script as part of the session

#### Baseline evidence (ARTIFACT LINKS)
- Snapshot:
- Screenshot:
- Console:
- Network:
- Backend logs:
- Notes:

#### Working hypotheses (max 3 at a time)
- H1 (confidence X/10):
- H2 (confidence X/10):
- H3 (confidence X/10):

#### Attempt ledger (do not repeat failed attempts)
> Each attempt MUST follow the loop: instrument → observe → hypothesize → attempt → verify → record.

---

## Scientific loop (repeat until resolved or blocked)

### 1) Instrument (baseline and per-attempt)
**Rule:** No code change before baseline evidence exists.

Capture evidence into the artifacts folder using PowerShell-safe commands (no `&&`).
Prefer saving full outputs to files and only quoting key excerpts in the journal.

Recommended artifact filenames:
- `baseline_snapshot.json`
- `baseline_screenshot.png`
- `baseline_console.txt`
- `baseline_network.txt`
- `baseline_backend_logs.txt`
- `attempt-XX_snapshot.json`, etc.

#### Frontend evidence capture (preferred tooling)
- Prefer `agent-browser` workflows and/or existing helper scripts in `scripts/`.
- If UI involves builder interactions, search for an existing automation script (examples you may reuse/adapt):
  - `scripts/test-all-resize-handles.js`
  - `scripts/test-resize-handles.js`
  - other `scripts/test-*.js` / `scripts/verify-*.js`

If you need a quick snapshot+screenshot for a URL, you may use:
- `./scripts/test-frontend.ps1 -Url "<url>" -SnapshotOptions "-i --json" -Screenshot "<artifactPath>/baseline.png"`
Then copy the snapshot output into `baseline_snapshot.json` (or capture via redirect if using agent-browser directly).

Also capture:
- console output
- network requests list
- any frontend event logs relevant to the bug (e.g., resize/drag events if present)

#### Backend evidence capture
Run diagnostic logs early:
- `python backend/enhanced_diagnostic_logs.py --limit 20`
Add filters if needed (`--frontend-only`, `--frontend-filter`, `--request-id`, etc.)
Save outputs to artifacts and link them in the journal.

### 2) Observe
Summarize what the evidence shows (numbers, logs, snapshots).
Avoid conclusions; focus on facts.

### 3) Hypothesize
Propose 1–3 hypotheses only, each with:
- Evidence citation (artifact + excerpt)
- Prediction (“If H1 is true, change X will cause Y”)
- A minimal test (the next attempt)

### 4) Attempt (single-variable change)
Pick ONE hypothesis and test it with the smallest viable change.
Before implementing, scan the Attempt Ledger and confirm it’s not a repeat.

For each attempt:
- Keep file touch minimal
- Add temporary instrumentation only if it helps verification (remove or gate it if it becomes permanent noise)
- Record the exact intent in the attempt entry BEFORE making the change

### 5) Verify (automation-first)
After the attempt:
- Re-run the SAME evidence capture that proved the bug existed (so you can compare baseline vs attempt)
- Run the most relevant automated checks for the changed area(s) and report pass/fail
- Decide outcome: **Fixed / Improved / No change / Worse**
- If “Fixed”, prepare a short human UAT checklist for Anthony and wait for UAT results

### 6) Record (append attempt entry)
Append a new section:

#### Attempt XX — {one-line intent}
- **Hypothesis tested**: H#
- **Change summary**:
  - Files:
  - Key change:
- **Instrumentation**:
  - Artifacts created:
- **Verification**:
  - Automated checks run:
  - Result: Fixed / Improved / No change / Worse
- **What we learned**:
- **Next step**:

Update:
- current best hypothesis list
- status (Active/Blocked/Resolved)
- done criteria checkboxes

## Closeout (when resolved)
When Anthony confirms UAT:
- Write a **Root Cause** section (brief, evidence-backed)
- Write a **Fix Summary** section (what changed and why)
- Link final artifacts (“after” evidence)
- Add a **Prevention** section:
  - what automated check could catch this next time
  - what instrumentation/logging proved most valuable

Optionally (only if generally reusable):
- Propose a small update to `docs/AGENT-LOGGING-GUIDE.md` (do NOT bloat it; add only reusable commands/interpretation notes).

