---
name: debug-report
description: Creates a structured debug report using backend diagnostic logs and the frontend snapshot workflow. Use for UAT failures, regressions, and “it doesn’t work” issues.
disable-model-invocation: true
---

# Debug Report (EventLeadPlatform)

## When to use
- UAT failed
- UI behavior unexpected (builder drag/resize/render issues)
- API error / auth issue / 4xx/5xx
- “Works locally but not in flow”

## Inputs (ask only if missing)
- Symptom (expected vs actual)
- Where (URL / page / feature)
- Repro steps
- Any IDs (request ID, user, company, form, version) if available

## Workflow (agent-owned)
1. **Classify scope**: frontend / backend / db / mixed.
2. **Collect evidence (never output secrets/credentials):**
   - **Backend logs (start here):**
     - `python backend/enhanced_diagnostic_logs.py --limit 20`
     - If relevant, add filters like:
       - `--frontend-only`
       - `--frontend-filter "<keyword>"`
       - `--request-id "<id>"`
   - **Frontend evidence (if UI involved):**
     - `./scripts/test-frontend.ps1 -Url "<url>" -SnapshotOptions "-i --json"`
     - Optional: `-Screenshot "<file>.png"`
     - Note: this script handles login using stored test creds; do NOT print creds in output.
   - **Change scope (if code changes exist):**
     - `git status`
     - `git diff`
3. **Analyze**:
   - Provide top 1–3 hypotheses, each tied to evidence.
   - Identify the smallest viable fix.
4. **Verify**:
   - Run the most relevant automated checks for the touched area(s) and summarize pass/fail.
   - Re-run the evidence step(s) that originally showed the failure to confirm it’s fixed.
5. **Output** using the template below.

## Output template
Use exactly this structure:

```markdown
## Debug Report
- **Issue**:
- **Scope**: frontend / backend / db / mixed
- **Repro steps**:
- **Expected**:
- **Actual**:
- **Evidence**
  - **Backend diagnostic logs**: (commands run + key excerpts)
  - **Frontend snapshot / console / network**: (commands run + key excerpts or filenames)
  - **Change scope**: (files changed)
- **Hypothesis**:
- **Fix (minimal)**:
- **Verification (automated)**:
- **What remains for human UAT**:
```

