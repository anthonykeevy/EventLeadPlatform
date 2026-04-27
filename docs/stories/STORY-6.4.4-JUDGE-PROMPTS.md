# Story 6.4.4 Judge Prompts

## Important

Category B judging requires one `judge-package` per eval run.

At the time this doc was created, the only visible live judge package was:

```text
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline\judge-package
```

The H1, H2, H4, and combined live variant run folders were not visible yet. The prompts below include the intended target folders. Only run a judge prompt after that folder exists and contains:

```text
judge-package\rubric_v1.md
judge-package\judge-input-batch.md
judge-package\judge-output-template.json
```

If a folder does not exist yet, do not send that prompt to a judge. First create the live eval run and judge package for that variant.

## Baseline - GPT-5 Mini

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline

JUDGE MODEL:
- GPT-5 mini: set "judge_model" to "gpt5mini" and save output to C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline\judge-package\results\judge-output-gpt5mini.json

Use only these files from the run package:
1. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline\judge-package\rubric_v1.md
2. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline\judge-package\judge-input-batch.md
3. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v1.md.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline\judge-package\results\judge-output-gpt5mini.json

Return only valid JSON.
```

## Baseline - Claude

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline

JUDGE MODEL:
- Claude: set "judge_model" to "claude" and save output to C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline\judge-package\results\judge-output-claude.json

Use only these files from the run package:
1. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline\judge-package\rubric_v1.md
2. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline\judge-package\judge-input-batch.md
3. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v1.md.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline\judge-package\results\judge-output-claude.json

Return only valid JSON.
```

## Baseline - Gemini

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline

JUDGE MODEL:
- Gemini: set "judge_model" to "gemini" and save output to C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline\judge-package\results\judge-output-gemini.json

Use only these files from the run package:
1. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline\judge-package\rubric_v1.md
2. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline\judge-package\judge-input-batch.md
3. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v1.md.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.2-post-cleanup-baseline\judge-package\results\judge-output-gemini.json

Return only valid JSON.
```

## H1 Locale One-Line - GPT-5 Mini

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line

JUDGE MODEL:
- GPT-5 mini: set "judge_model" to "gpt5mini" and save output to C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line\judge-package\results\judge-output-gpt5mini.json

Use only these files from the run package:
1. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line\judge-package\rubric_v1.md
2. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line\judge-package\judge-input-batch.md
3. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v1.md.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line\judge-package\results\judge-output-gpt5mini.json

Return only valid JSON.
```

## H1 Locale One-Line - Claude

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line

JUDGE MODEL:
- Claude: set "judge_model" to "claude" and save output to C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line\judge-package\results\judge-output-claude.json

Use only these files from the run package:
1. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line\judge-package\rubric_v1.md
2. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line\judge-package\judge-input-batch.md
3. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v1.md.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line\judge-package\results\judge-output-claude.json

Return only valid JSON.
```

## H1 Locale One-Line - Gemini

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line

JUDGE MODEL:
- Gemini: set "judge_model" to "gemini" and save output to C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line\judge-package\results\judge-output-gemini.json

Use only these files from the run package:
1. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line\judge-package\rubric_v1.md
2. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line\judge-package\judge-input-batch.md
3. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v1.md.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-locale-one-line\judge-package\results\judge-output-gemini.json

Return only valid JSON.
```

## H2 Consent Decision Table - GPT-5 Mini

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table

JUDGE MODEL:
- GPT-5 mini: set "judge_model" to "gpt5mini" and save output to C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table\judge-package\results\judge-output-gpt5mini.json

Use only these files from the run package:
1. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table\judge-package\rubric_v1.md
2. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table\judge-package\judge-input-batch.md
3. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v1.md.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table\judge-package\results\judge-output-gpt5mini.json

Return only valid JSON.
```

## H2 Consent Decision Table - Claude

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table

JUDGE MODEL:
- Claude: set "judge_model" to "claude" and save output to C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table\judge-package\results\judge-output-claude.json

Use only these files from the run package:
1. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table\judge-package\rubric_v1.md
2. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table\judge-package\judge-input-batch.md
3. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v1.md.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table\judge-package\results\judge-output-claude.json

Return only valid JSON.
```

## H2 Consent Decision Table - Gemini

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table

JUDGE MODEL:
- Gemini: set "judge_model" to "gemini" and save output to C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table\judge-package\results\judge-output-gemini.json

Use only these files from the run package:
1. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table\judge-package\rubric_v1.md
2. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table\judge-package\judge-input-batch.md
3. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v1.md.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h2-consent-decision-table\judge-package\results\judge-output-gemini.json

Return only valid JSON.
```

## H4 Operational Trim - GPT-5 Mini

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim

JUDGE MODEL:
- GPT-5 mini: set "judge_model" to "gpt5mini" and save output to C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim\judge-package\results\judge-output-gpt5mini.json

Use only these files from the run package:
1. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim\judge-package\rubric_v1.md
2. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim\judge-package\judge-input-batch.md
3. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v1.md.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim\judge-package\results\judge-output-gpt5mini.json

Return only valid JSON.
```

## H4 Operational Trim - Claude

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim

JUDGE MODEL:
- Claude: set "judge_model" to "claude" and save output to C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim\judge-package\results\judge-output-claude.json

Use only these files from the run package:
1. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim\judge-package\rubric_v1.md
2. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim\judge-package\judge-input-batch.md
3. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v1.md.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim\judge-package\results\judge-output-claude.json

Return only valid JSON.
```

## H4 Operational Trim - Gemini

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim

JUDGE MODEL:
- Gemini: set "judge_model" to "gemini" and save output to C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim\judge-package\results\judge-output-gemini.json

Use only these files from the run package:
1. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim\judge-package\rubric_v1.md
2. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim\judge-package\judge-input-batch.md
3. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v1.md.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h4-operational-trim\judge-package\results\judge-output-gemini.json

Return only valid JSON.
```

## Combined H1+H2+H4 - GPT-5 Mini

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined

JUDGE MODEL:
- GPT-5 mini: set "judge_model" to "gpt5mini" and save output to C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined\judge-package\results\judge-output-gpt5mini.json

Use only these files from the run package:
1. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined\judge-package\rubric_v1.md
2. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined\judge-package\judge-input-batch.md
3. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v1.md.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined\judge-package\results\judge-output-gpt5mini.json

Return only valid JSON.
```

## Combined H1+H2+H4 - Claude

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined

JUDGE MODEL:
- Claude: set "judge_model" to "claude" and save output to C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined\judge-package\results\judge-output-claude.json

Use only these files from the run package:
1. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined\judge-package\rubric_v1.md
2. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined\judge-package\judge-input-batch.md
3. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v1.md.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined\judge-package\results\judge-output-claude.json

Return only valid JSON.
```

## Combined H1+H2+H4 - Gemini

```text
You are acting as an independent EventLeadPlatform Form AI judge.

You are judging exactly one eval run package:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined

JUDGE MODEL:
- Gemini: set "judge_model" to "gemini" and save output to C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined\judge-package\results\judge-output-gemini.json

Use only these files from the run package:
1. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined\judge-package\rubric_v1.md
2. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined\judge-package\judge-input-batch.md
3. C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined\judge-package\judge-output-template.json

Task:
- Score every row in judge-input-batch.md using rubric_v1.md.
- Return JSON only.
- The JSON must match judge-output-template.json exactly.
- Do not compare against other judges.
- Do not omit rows.
- Do not add markdown, prose, comments, or code fences.
- Use the row IDs exactly as provided.
- Preserve prompt_id, repetition_index, and variant_label exactly from the template/input.
- Scores must be numeric and within the rubric/template range.
- If evidence is weak or unavailable for a metric, score conservatively and use the template rationale fields if present.

Save the JSON output exactly to:
C:\Users\tonyk\OneDrive - Signal Platforms Pty Ltd\Projects\EventLeadPlatform\_bmad-output\eval-runs\story-6.4.4-live-h1-h2-h4-combined\judge-package\results\judge-output-gemini.json

Return only valid JSON.
```
