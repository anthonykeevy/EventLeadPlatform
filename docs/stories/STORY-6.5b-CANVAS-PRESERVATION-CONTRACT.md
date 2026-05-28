# Canvas Preservation Contract — Image-to-Form (Story 6.5e-vision)

**Status:** Draft for implementation (Track 1)  
**Applies to:** Image-mode generate and text-mode replace on non-empty canvas  
**Also used by:** Story 6.5f-style (future)

---

## Principle

> **Image provides structure; current canvas provides dimensions.**

The deterministic compiler (Story 6.3.1) already resolves `widthIntent` against **runtime canvas width/grid**. Vision must not infer embed dimensions from screenshot pixel size.

---

## Rules

| # | Rule |
|---|------|
| C1 | When canvas has ≥1 component and user generates from **image**, preserve existing `canvasWidth`, `canvasHeight`, `gridColumns` (and layout mode) in `runtimeContext` sent to `/api/form-ai/generate`. |
| C2 | When canvas is **empty**, use form defaults / builder store defaults — never derive canvas size from image dimensions. |
| C3 | Story 6.4 replace-form warning still applies when canvas non-empty. Image mode adds one line: *"Your current canvas size will be kept so embedded layouts keep fitting."* |
| C4 | Compiled output must not shrink canvas below current settings unless user explicitly changes canvas in builder settings. |
| C5 | `lockedGlobals` in runtime context remain read-only for the LLM (existing sectioned addendum §4). |

---

## UAT proof

1. Set canvas to a non-default width (e.g. narrow embed).
2. Add one field manually.
3. Upload form screenshot → generate.
4. **Pass:** canvas width unchanged in form settings; generated fields compile within same width class policy.

---

## References

- `docs/stories/STORY-6.5-FEASIBILITY-NOTES.md` §2.6  
- `frontend/src/features/builder/components/ai/AIAgentPanel.tsx` — runtime context builder  
- Story 6.4 replace-warning modal

---

*Started Story 6.5e-vision — extend when Track 1 ships.*
