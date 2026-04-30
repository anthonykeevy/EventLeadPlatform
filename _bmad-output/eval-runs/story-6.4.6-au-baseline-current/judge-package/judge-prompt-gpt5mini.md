You are the GPT-5 mini control judge for Story 6.4.6 AU-only diagnostic baseline.

Use the attached judge package files:
- rubric_v2.md
- shared-context-bundle.json
- judge-input-batch.md
- judge-output-template.json

Score each row against rubric_v2 only. Identify at least one weakness per row before scoring. Inspect shared-context-bundle.json before filling diagnostic conflict fields. Return only valid JSON matching judge-output-template.json.
Set judge_model to "gpt5mini" and judge_model_version to the exact model/version shown in this Cursor session.

Save your output JSON to: `_bmad-output/eval-runs/story-6.4.6-au-baseline-current/judge-package/results/judge-output-gpt5mini.json`. Do not write anywhere else. Create the file if it does not exist.
