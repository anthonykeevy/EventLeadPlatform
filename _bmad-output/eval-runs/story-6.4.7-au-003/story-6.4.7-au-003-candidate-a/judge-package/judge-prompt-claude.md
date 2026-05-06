You are the Claude 4.7 primary judge for Analyst Form AI prompt experiment.

Use the attached judge package files:
- rubric_v2.md
- shared-context-bundle.json
- judge-input-batch.md
- judge-output-template.json

Score each row against rubric_v2 only. Identify at least one weakness per row before scoring. Inspect shared-context-bundle.json before filling diagnostic conflict fields. Return only valid JSON matching judge-output-template.json.
Set judge_model to "claude" and judge_model_version to the exact model/version shown in this Cursor session.

Save your output JSON to: `_bmad-output/eval-runs/story-6.4.7-au-003/story-6.4.7-au-003-candidate-a/judge-package/results/judge-output-claude.json`. Do not write anywhere else. Create the file if it does not exist.
