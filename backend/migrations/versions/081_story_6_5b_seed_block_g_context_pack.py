"""Story 6.5b: Seed Block G FEW_SHOT variant from STORY-6.2-AI-CONTEXT-PACK.md (R6 fix).

Revision ID: 081
Revises: 080
Create Date: 2026-05-20

This is the migration that closes Risk **R6** (`context-pack-load-failed` on
the deployed Test environment). It seeds Block G (`FEW_SHOT`) variant
`DEFAULT` with the *post-trim* content of
`docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` so that
`backend/modules/form_ai/service.py::_load_context_pack` can be deleted in
the same story (Step 5 of the dev prompt). Once this migration runs, the
Azure deploy package no longer needs the on-disk markdown file at
`/home/site/wwwroot/docs/stories/...`.

Trim semantics:
  Equivalent to backend/modules/form_ai/service.py::_trim_context_pack_for_prompt
  with `_prompt_shrink_candidate_enabled('h4')` -> True (production
  default for `FORM_AI_EVAL_PROMPT_SHRINK_MODE` is `h2-h4`):
    1. Find marker `\\n## Operational Notes`.
    2. Slice up to that index.
    3. .rstrip() the result to drop trailing whitespace/newlines.

The trim is applied *at seed time* rather than at render time. Rationale:
  * Trim is deterministic (single hard-coded marker; no inputs).
  * Storing the post-trim content avoids a runtime trim cost on every
    request and removes the need for the renderer to know about
    `_trim_context_pack_for_prompt` semantics.
  * If a future story (e.g. 6.5c) decides that the eval-only `baseline`
    or `h4` shrink modes are no longer needed, the trimmed content is
    already what production has been sending; nothing changes.

The fingerprint for the trimmed content (sha256, computed at base
commit cb339ed against the on-disk file): 06e09b59be6d3a7aba592fb045eb4
5bee35144e92e0d98a8440b185ab285f853 (6,355 chars). Tests in
`test_story_6_5b_equivalence.py` re-compute this from the live
file in the worktree and assert it matches the seeded variant.

After this migration runs:
  * The on-disk file `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` is kept
    in the repo as documentation reference only (with a banner added in
    Story 6.5b Step 9). It is NOT read at runtime by Form AI.
"""

from alembic import op
from sqlalchemy import text


revision = "081"
down_revision = "080"
branch_labels = None
depends_on = None


# ---------------------------------------------------------------------------
# BLOCK_G_DEFAULT_TRIMMED
# Computed from `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` at base commit
# `cb339ed` by:
#   content = path.read_text(encoding='utf-8')
#   marker = '\n## Operational Notes'
#   idx = content.find(marker)
#   trimmed = content[:idx].rstrip()
# Length: 6,355 chars.
# SHA-256: 06e09b59be6d3a7aba592fb045eb45bee35144e92e0d98a8440b185ab285f853
# DO NOT hand-edit this string. Re-derive via the same recipe and update
# the fingerprint comment if the source markdown is intentionally rev'd.
# ---------------------------------------------------------------------------

BLOCK_G_DEFAULT_TRIMMED = '# STORY-6.2 AI Context Pack\n\n**Context Pack Version:** 1.3  \n**Last Updated:** 2026-04-02  \n**Owner:** SM Agent\n\n---\n\n## Purpose\n\nProvide a consistent instruction bundle for the LLM so generated `DefinitionJSON` matches EventLead product behavior, component rules, and validation constraints.\n\n---\n\n## Product Usage Context\n\n1. Users describe a form in natural language.\n2. AI generates an initial single-page form definition draft.\n3. System validates draft via Story 6.1 validator.\n4. If invalid, system sends structured correction instructions and retries.\n5. If valid, draft loads into Builder canvas for human refinement.\n6. Final save/publish remains in existing manual workflows.\n\n---\n\n## Component Catalog (MVP Set)\n\nAllowed component types for Story 6.2 MVP generation:\n- `text`\n- `first-name`\n- `email`\n- `phone`\n- `url`\n- `number`\n- `date`\n- `dropdown`\n- `checkbox`\n- `radio`\n- `textarea`\n- `address`\n- `rating`\n- `file-upload`\n- `terms`\n- `header`\n- `paragraph`\n- `divider`\n- `submit-button`\n\nComponent-specific notes for expanded set:\n- `url`: use `validation.url: true`; optional `urlPrefix` and `urlPattern` can be included.\n- `rating`: include `ratingMax` (typically 5 or 10) and `ratingStyle` (`stars` | `numbers` | `emoji`).\n- `paragraph`: display-only content block (prefer `text`, fallback `label` for legacy compatibility).\n- `file-upload`: **available** (Story 6.2.2). Use `allowMultiple` / `maxFiles` only when multiple files in one control are required; answers store **public attachment UUIDs** only (never paths). Generation must respect max size and `accept` / `acceptedFileTypes` hints.\n\nFor each component:\n- Must include stable `id`.\n- Must include `type`.\n- Must include `position` (`x`, `y`) for render placement.\n- Should include width/height style hints where relevant.\n\nDisallowed in this story:\n- Payment component logic (Story 6.7).\n- Multi-page generation orchestration.\n\n---\n\n## Layout and Canvas Rules\n\n1. Single-page only.\n2. Components must stay within canvas boundaries.\n3. Components must not overlap.\n4. Prefer top-to-bottom **reading order** with reasonable spacing (rows still read top \u2192 bottom).\n5. Keep layout simple and editable by humans after load.\n6. **Multi-column rows (encouraged on wide canvases):** You **may and should** place **two related short inputs on the same horizontal row** when the user lists them as separate fields \u2014 same `position.y`, different `position.x`, each with roughly **half** the main form width (minus a **gap** of about **56\u201396px** between fields). Typical pairs: **First name | Last name**, **Phone | Email**. Keep **full-width rows** for `textarea`, `address`, and other tall/wide controls. This uses horizontal space, **saves vertical space**, and helps keep **`submit-button` clearly below** `textarea` so collision validation passes. On narrow canvases or when the user asks for one column, a single stack is fine.\n7. **`textarea` + `submit-button` (bottom of form):** The builder reserves a **validation / error message band** under controls. Do **not** rely on a minimal `style.height` (~140px) for comments when a submit sits below \u2014 use **`style.height` \u2265 180\u2013240px** (prefer **200+**). Place **`submit-button` last** with **`position.y` \u2265 `textarea.y + textarea.style.height + 48\u201372px`**. If corrections still report collisions between submit and textarea, **increase that gap** and/or **textarea height** before changing column layout.\n\n---\n\n## Strict Output Contract (JSON Only)\n\nLLM output requirements:\n1. Return valid JSON object only.\n2. Do not include markdown, prose, comments, or code fences.\n3. Root must be a DefinitionJSON-compatible object.\n4. Maintain deterministic key/value structure where practical.\n\n---\n\n## Validator Feedback to Correction Mapping\n\nWhen validator returns errors:\n1. `schemaErrors`:\n   - fix missing/incorrect required fields and types.\n2. `boundaryViolations`:\n   - reposition or resize affected components inside canvas.\n3. `collisions`:\n   - re-space components to remove overlap while preserving intent.\n4. Re-submit corrected JSON for validation until:\n   - `valid=true`, or\n   - max retries reached.\n\nCorrection priorities:\n1. Schema correctness\n2. Boundary correctness\n3. Collision removal\n4. Visual readability improvements\n\n---\n\n## Example A (Valid Generation)\n\n```json\n{\n  "schemaVersion": "1.0",\n  "formId": "gen-contact-form",\n  "canvasSettings": { "width": 500, "height": 700, "gridSize": 8 },\n  "pages": [\n    {\n      "id": "page-1",\n      "title": "Contact Form",\n      "components": [\n        { "id": "h1", "type": "header", "props": { "text": "Contact Us" }, "position": { "x": 20, "y": 20 }, "style": { "width": 460, "height": 48 } },\n        { "id": "name", "type": "text", "props": { "label": "Full Name" }, "position": { "x": 20, "y": 90 }, "style": { "width": 460, "height": 72 } },\n        { "id": "email", "type": "email", "props": { "label": "Email" }, "position": { "x": 20, "y": 180 }, "style": { "width": 460, "height": 72 } },\n        { "id": "submit", "type": "submit-button", "props": { "label": "Submit" }, "position": { "x": 20, "y": 280 }, "style": { "width": 180, "height": 56 } }\n      ]\n    }\n  ]\n}\n```\n\n---\n\n## Example B (Invalid -> Corrected)\n\n### Invalid Candidate (collision + boundary)\n\n```json\n{\n  "schemaVersion": "1.0",\n  "formId": "gen-invalid",\n  "canvasSettings": { "width": 500, "height": 400, "gridSize": 8 },\n  "pages": [\n    {\n      "id": "page-1",\n      "title": "Broken Layout",\n      "components": [\n        { "id": "a", "type": "text", "props": { "label": "A" }, "position": { "x": -10, "y": 20 }, "style": { "width": 300, "height": 72 } },\n        { "id": "b", "type": "email", "props": { "label": "B" }, "position": { "x": 100, "y": 40 }, "style": { "width": 320, "height": 72 } }\n      ]\n    }\n  ]\n}\n```\n\n### Corrected Candidate\n\n```json\n{\n  "schemaVersion": "1.0",\n  "formId": "gen-invalid",\n  "canvasSettings": { "width": 500, "height": 400, "gridSize": 8 },\n  "pages": [\n    {\n      "id": "page-1",\n      "title": "Broken Layout",\n      "components": [\n        { "id": "a", "type": "text", "props": { "label": "A" }, "position": { "x": 20, "y": 20 }, "style": { "width": 460, "height": 72 } },\n        { "id": "b", "type": "email", "props": { "label": "B" }, "position": { "x": 20, "y": 110 }, "style": { "width": 460, "height": 72 } }\n      ]\n    }\n  ]\n}\n```\n\n---'


def upgrade() -> None:
    connection = op.get_bind()

    section_id = connection.execute(
        text(
            """
            SELECT TOP 1 ps.[PromptSectionID]
            FROM [config].[PromptSection] ps
            INNER JOIN [config].[PromptAssemblyRegistryVersion] prv
                ON prv.[PromptAssemblyRegistryVersionID] = ps.[PromptAssemblyRegistryVersionID]
            INNER JOIN [config].[PromptAssemblyRegistry] pr
                ON pr.[PromptAssemblyRegistryID] = prv.[PromptAssemblyRegistryID]
            WHERE pr.[Code] = N'FORM_AI_V1'
              AND prv.[IsActive] = 1
              AND prv.[IsDeleted] = 0
              AND ps.[SectionCode] = N'G'
              AND ps.[IsDeleted] = 0
            """
        )
    ).scalar_one_or_none()

    if section_id is None:
        raise RuntimeError(
            "Story 6.5b migration 081 cannot resolve PromptSectionID for "
            "registry='FORM_AI_V1', section='G'. Migrations 078 and 079 "
            "must run first."
        )

    existing = connection.execute(
        text(
            """
            SELECT TOP 1 [PromptSectionVariantID]
            FROM [config].[PromptSectionVariant]
            WHERE [PromptSectionID] = :section_id
              AND [VariantCode] = N'DEFAULT'
              AND [IsDeleted] = 0
            """
        ),
        {"section_id": int(section_id)},
    ).scalar_one_or_none()

    if existing is not None:
        # Idempotent: variant already seeded by a prior run.
        return

    connection.execute(
        text(
            """
            INSERT INTO [config].[PromptSectionVariant]
            (
                [PromptSectionID],
                [VariantCode],
                [DisplayName],
                [Description],
                [IsDefault],
                [PromptSnippet],
                [VariantVersion],
                [IsLockedForEdits],
                [ActivatedUtc],
                [ChangeReason],
                [CreatedUtc],
                [IsDeleted]
            )
            VALUES
            (
                :section_id,
                N'DEFAULT',
                N'Few-shot context pack (R6 fix)',
                N'Story 6.2 AI context pack content (post-trim per _trim_context_pack_for_prompt h4 mode). Migrated from on-disk file STORY-6.2-AI-CONTEXT-PACK.md by Story 6.5b. Closes R6 - context-pack-load-failed in deployed Test environment.',
                1,
                :snippet,
                1,
                0,
                GETUTCDATE(),
                N'Initial migration of Block G from on-disk markdown file to registry (Story 6.5b - R6 fix migration).',
                GETUTCDATE(),
                0
            )
            """
        ),
        {"section_id": int(section_id), "snippet": BLOCK_G_DEFAULT_TRIMMED},
    )


def downgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
        DECLARE @SectionID BIGINT = (
            SELECT TOP 1 ps.[PromptSectionID]
            FROM [config].[PromptSection] ps
            INNER JOIN [config].[PromptAssemblyRegistryVersion] prv
                ON prv.[PromptAssemblyRegistryVersionID] = ps.[PromptAssemblyRegistryVersionID]
            INNER JOIN [config].[PromptAssemblyRegistry] pr
                ON pr.[PromptAssemblyRegistryID] = prv.[PromptAssemblyRegistryID]
            WHERE pr.[Code] = N'FORM_AI_V1'
              AND prv.[IsActive] = 1
              AND prv.[IsDeleted] = 0
              AND ps.[SectionCode] = N'G'
              AND ps.[IsDeleted] = 0
        );

        IF @SectionID IS NULL RETURN;

        DELETE FROM [config].[PromptSectionVariant]
        WHERE [PromptSectionID] = @SectionID
          AND [VariantCode] = N'DEFAULT';
        """
    )
