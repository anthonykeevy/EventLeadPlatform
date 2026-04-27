# Story 6.4.4.1-ac10 Judge Prompts

## Important

Use **only** the final aggregate AC-10 judge package below for the story gate:

```text
C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package
```

This is the single 270-row package built from all six completed locale slices:

- `AU` — 45 rows
- `NZ` — 45 rows
- `UK` — 45 rows
- `US` — 45 rows
- `INTL_ONLINE` — 45 rows
- `EU` — 45 rows

Do **not** use the per-locale slice packages for the final AC-10 verdict. They are diagnostics only.

This regenerated v2 package has been verified to contain generated form definitions for all 270 rows (`generated_definition_available = 270 / 270`). Do **not** use the earlier `story-6.4.4.1-ac10-baseline` package; it lacked generated definitions.

Before sending any prompt to a judge, confirm the package contains:

```text
judge-package\rubric_v2.md
judge-package\judge-input-batch.md
judge-package\judge-output-template.json
```

Run exactly three Cursor judge chats total:

- Claude 4.7 primary judge
- Grok 4 primary judge
- GPT-5 mini control judge

## AC-10 Baseline - Claude 4.7

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2

JUDGE MODEL:
- Claude 4.7: set "judge_model" to "claude" and set "judge_model_version" to the exact model/version shown in this Cursor session.

Save output to:
C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\results\judge-output-claude.json

Use only these files from the run package:
1. C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\rubric_v2.md
2. C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\judge-input-batch.md
3. C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v2.md.
- Identify at least one weakness per row before scoring.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Set "rubric_version" to "rubric_v2".
- Set "judge_model" to "claude".
- Set "judge_model_version" to the exact model/version shown in this Cursor session.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\results\judge-output-claude.json

Return only valid JSON.
```

## AC-10 Baseline - Grok 4

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2

JUDGE MODEL:
- Grok 4: set "judge_model" to "grok" and set "judge_model_version" to the exact model/version shown in this Cursor session.

Save output to:
C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\results\judge-output-grok.json

Use only these files from the run package:
1. C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\rubric_v2.md
2. C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\judge-input-batch.md
3. C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v2.md.
- Identify at least one weakness per row before scoring.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Set "rubric_version" to "rubric_v2".
- Set "judge_model" to "grok".
- Set "judge_model_version" to the exact model/version shown in this Cursor session.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\results\judge-output-grok.json

Return only valid JSON.
```

## AC-10 Baseline - GPT-5 Mini

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2

JUDGE MODEL:
- GPT-5 mini: set "judge_model" to "gpt5mini" and set "judge_model_version" to the exact model/version shown in this Cursor session.

Save output to:
C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\results\judge-output-gpt5mini.json

Use only these files from the run package:
1. C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\rubric_v2.md
2. C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\judge-input-batch.md
3. C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v2.md.
- Identify at least one weakness per row before scoring.
- Do not leave template placeholder scores as 0. Score each metric based on the row evidence. A score of 0 means a clear failure for that metric; if all rows receive all-zero scores, re-check your work before saving.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Set "rubric_version" to "rubric_v2".
- Set "judge_model" to "gpt5mini".
- Set "judge_model_version" to the exact model/version shown in this Cursor session.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\results\judge-output-gpt5mini.json

Return only valid JSON.
```

## Output Files

After the three judge chats finish, these files must exist:

```text
C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\results\judge-output-claude.json
C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\results\judge-output-grok.json
C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge\_bmad-output\eval-runs\story-6.4.4.1-ac10-baseline-v2\judge-package\results\judge-output-gpt5mini.json
```

Then ingest with:

```powershell
python -m backend.tests.form_ai_eval.judge_ingest _bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/judge-package
```
