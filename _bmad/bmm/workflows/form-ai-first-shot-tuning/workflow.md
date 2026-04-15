# Form AI first-shot tuning — entry

**Workflow ID:** `form-ai-first-shot-tuning`  
**Config:** [workflow.yaml](./workflow.yaml)

## How to run (BMAD)

1. Load `{project-root}/_bmad/core/tasks/workflow.xml` as the workflow engine.  
2. Pass this folder’s **`workflow.yaml`** as the workflow config.  
3. Follow **`instructions.md`** in order.  
4. Use **`experiment-review-template.md`** to create `docs/experiments/form-ai-first-shot/{{experiment_id}}-review.md`.
5. For panel-driven sectioned runs, use `docs/experiments/form-ai-first-shot/SECTIONED-PROMPT-ARCHITECTURE-v1.md`.

## Human + agent roles

- **Agent:** Maintain indicator registry, enforce one change per iteration, fill expected vs actual, suggest splits/new indicators.  
- **Human:** Approve **block checkpoint** after every 5 iterations before the next block.

## Persona

For domain-heavy decisions, use **`_bmad/bmm/agents/form-builder-master.md`** (menu **[FS]** runs this workflow).
