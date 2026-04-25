# Form AI Eval Judge Workflow

**Status:** Template ready; Dev completes during Story 6.4.3b  
**Audience:** Anthony running Cursor judge chats  
**Scope:** Manual cross-model judging for Form AI eval runs. No model API clients.

---

## 1) Generate Judge Package

Dev fills the exact command after implementation.

```powershell
python -m backend.tests.form_ai_eval.judge_pack `
  --run-dir "_bmad-output/eval-runs/<run-id>"
```

Expected output:

```text
_bmad-output/eval-runs/<run-id>/judge-package/
├── rubric_v1.md
├── judge-input-batch.md
├── judge-output-template.json
└── results/
```

---

## 2) Run Cursor Judge Chats

Run three separate Cursor chats using the same package:

| Output File | Cursor Model | Role |
|-------------|--------------|------|
| `results/judge-output-gpt5mini.json` | GPT-5 mini | Control |
| `results/judge-output-claude.json` | Claude | Cross-model judge #1 |
| `results/judge-output-gemini.json` | Gemini | Cross-model judge #2 |

For each chat:

1. Paste or attach `rubric_v1.md`.
2. Paste or attach `judge-input-batch.md`.
3. Paste or attach `judge-output-template.json`.
4. Ask the model to fill the JSON only, with no prose.
5. Save the returned JSON to the matching `results/` file.

Do not paste secrets. Treat generated names/emails/dates as PII-adjacent.

---

## 3) Ingest Judge Outputs

Dev fills the exact command after implementation.

```powershell
python -m backend.tests.form_ai_eval.judge_ingest `
  --package-dir "_bmad-output/eval-runs/<run-id>/judge-package"
```

Expected behavior:

- validate all judge files,
- reject missing/duplicate/unknown rows,
- reject out-of-range scores,
- compute Claude+Gemini primary means,
- compute GPT-5 mini bias deltas,
- emit ingest summary artifacts,
- update `log.FormAiEvalRun` judge fields when DB is available.

---

## 4) Disagreement Handling

If one judge clearly returns malformed JSON:

1. Re-run that same judge chat once with the same package and a "JSON only" correction instruction.
2. Save the corrected file over the malformed result.
3. Re-run ingest.

If judges disagree semantically but JSON is valid:

- Do not hand-edit scores.
- Keep all outputs.
- Let 6.4.3c diff/statistics surface the disagreement.

---

## 5) What 6.4.3b Does Not Decide

This workflow does not declare prompt winners. It only prepares and ingests judge scores.

Story 6.4.3c adds:

- diff reports,
- Welch/Fisher statistics,
- hypothesis verdict helpers,
- future PR-comment output.
