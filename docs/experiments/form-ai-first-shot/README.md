# Form AI first-shot experiments

- **Review dossiers:** Copy `_bmad/bmm/workflows/form-ai-first-shot-tuning/experiment-review-template.md` to `{{experiment_id}}-review.md` in this folder (see workflow `default_output_file`).
- **Machine-readable log:** Set `--changelog-jsonl` on `form_ai_first_shot_tune.py` to append rows (scores, addendum fingerprint).
- **After each iteration (human-in-the-loop):** Run `form_ai_first_shot_tune.py` with `--save-definition` to an artifact path, then from EventLead `backend/`: `python scripts/push_form_draft_definition.py --form-id 403 --definition <that.json> --user-id <EDIT user> --comment "..."`. That updates the **latest DRAFT** `FormVersion.DefinitionJSON` for form **403** so `/forms/403/builder` loads the same layout as the scored run (hard refresh). Wait for human visual confirmation before the next iteration.
- **Best-run JSON on disk (optional):** After each block, you can still save the winning draft with `--save-definition artifacts/<experiment-id>-block<N>-best.json` for dossier / diff. **`collisionCount`** in logs is **DefinitionJSON / server** geometry (see `docs/FORM-403-COLLISION-TRUTH-VS-LLM-FEEDBACK.md` §9), not SmartBorder.
- **Run workflow:** Load `_bmad/core/tasks/workflow.xml` with `_bmad/bmm/workflows/form-ai-first-shot-tuning/workflow.yaml`, or open the **Form Builder Master** agent (`_bmad/bmm/agents/form-builder-master.md`) and choose **[FS]**.

Adjust `eventlead_backend_root` in `workflow.yaml` if your EventLead clone is not at `../EventLeadPlatform/backend` relative to this story worktree.
