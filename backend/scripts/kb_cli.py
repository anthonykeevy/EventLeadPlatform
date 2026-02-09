"""
Knowledge Base CLI (kb schema)

Goal: enable agent-operated capture/retrieval of ideas/aspects/relations/session notes
without creating GitHub delivery work items until an idea is mature.

Usage examples:
  python backend/scripts/kb_cli.py create-aspect --key "process.knowledge-management" --title "Process: Knowledge management"
  python backend/scripts/kb_cli.py create-idea --title "Evaluate Dolt for workflow efficiency" --status rejected --decision-summary "Too large; not worth it"
  python backend/scripts/kb_cli.py link-idea-aspect --idea-id 1 --aspect "process.knowledge-management"
  python backend/scripts/kb_cli.py link-aspects --from "process.knowledge-management" --to "process.git-workflow" --type impacts
  python backend/scripts/kb_cli.py add-session-note --title "Dolt eval pivot" --summary "..." --idea 1 --aspect "process.knowledge-management"
  python backend/scripts/kb_cli.py context-pack --aspect "process.knowledge-management" --pretty
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Ensure imports work when executed from repo root
project_root = Path(__file__).resolve().parent.parent.parent
backend_path = project_root / "backend"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_path))
os.chdir(str(backend_path))

from common.kb_service import KnowledgeBaseService, KbError  # type: ignore[import-not-found]  # noqa: E402


def _print(result, pretty: bool) -> None:
    print(json.dumps(result, indent=2 if pretty else None, ensure_ascii=False, default=str))


def main() -> int:
    parser = argparse.ArgumentParser(description="EventLeadPlatform Knowledge Base CLI (kb schema)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_aspect = sub.add_parser("create-aspect", help="Create an aspect (durable dossier)")
    p_aspect.add_argument("--key", required=True, dest="aspect_key")
    p_aspect.add_argument("--title", required=True)
    p_aspect.add_argument("--summary")
    p_aspect.add_argument("--maturity", default="M0", dest="maturity_code")
    p_aspect.add_argument("--state", default="active", dest="state_code")
    p_aspect.add_argument("--owner")
    p_aspect.add_argument("--created-by", type=int, dest="created_by")
    p_aspect.add_argument("--pretty", action="store_true")

    p_idea = sub.add_parser("create-idea", help="Create an idea (incubation item)")
    p_idea.add_argument("--title", required=True)
    p_idea.add_argument("--problem-statement")
    p_idea.add_argument("--hypothesis")
    p_idea.add_argument("--impact-notes")
    p_idea.add_argument("--risks")
    p_idea.add_argument("--next-step")
    p_idea.add_argument("--decision-summary")
    p_idea.add_argument("--status", default="captured", dest="status_code")
    p_idea.add_argument("--created-by", type=int, dest="created_by")
    p_idea.add_argument("--pretty", action="store_true")

    p_set = sub.add_parser("set-idea-status", help="Update an idea status")
    p_set.add_argument("--idea-id", required=True)
    p_set.add_argument("--status", required=True, dest="status_code")
    p_set.add_argument("--decision-summary")
    p_set.add_argument("--updated-by", type=int, dest="updated_by")
    p_set.add_argument("--pretty", action="store_true")

    p_park = sub.add_parser("park-idea", help="Convenience: set idea status to parked")
    p_park.add_argument("--idea-id", required=True)
    p_park.add_argument("--decision-summary")
    p_park.add_argument("--updated-by", type=int, dest="updated_by")
    p_park.add_argument("--pretty", action="store_true")

    p_approve = sub.add_parser("approve-idea", help="Convenience: set idea status to approved_to_build")
    p_approve.add_argument("--idea-id", required=True)
    p_approve.add_argument("--decision-summary")
    p_approve.add_argument("--updated-by", type=int, dest="updated_by")
    p_approve.add_argument("--pretty", action="store_true")

    p_link_ia = sub.add_parser("link-idea-aspect", help="Link an idea to an aspect")
    p_link_ia.add_argument("--idea-id", required=True)
    p_link_ia.add_argument("--aspect", required=True, dest="aspect_key_or_id")
    p_link_ia.add_argument("--notes")
    p_link_ia.add_argument("--created-by", type=int, dest="created_by")
    p_link_ia.add_argument("--pretty", action="store_true")

    p_link_aa = sub.add_parser("link-aspects", help="Create a typed relationship between two aspects")
    p_link_aa.add_argument("--from", required=True, dest="from_aspect")
    p_link_aa.add_argument("--to", required=True, dest="to_aspect")
    p_link_aa.add_argument("--type", required=True, dest="relation_type_code")
    p_link_aa.add_argument("--notes")
    p_link_aa.add_argument("--created-by", type=int, dest="created_by")
    p_link_aa.add_argument("--no-auto-symmetric", action="store_true")
    p_link_aa.add_argument("--pretty", action="store_true")

    p_note = sub.add_parser("add-session-note", help="Add a session note and link it to ideas/aspects")
    p_note.add_argument("--title", required=True)
    p_note.add_argument("--summary")
    p_note.add_argument("--decisions")
    p_note.add_argument("--source-type", default="cursor_chat")
    p_note.add_argument("--source-ref")
    p_note.add_argument("--idea", action="append", dest="idea_ids")
    p_note.add_argument("--aspect", action="append", dest="aspect_ids_or_keys")
    p_note.add_argument("--created-by", type=int, dest="created_by")
    p_note.add_argument("--pretty", action="store_true")

    p_ctx = sub.add_parser("context-pack", help="Show an aspect context pack (for reliable prompting)")
    p_ctx.add_argument("--aspect", required=True, dest="aspect_key_or_id")
    p_ctx.add_argument("--pretty", action="store_true")

    p_review = sub.add_parser("enqueue-review", help="Enqueue Kaizen review tasks for related aspects")
    p_review.add_argument("--aspect", required=True, dest="aspect_key_or_id")
    p_review.add_argument("--reason", required=True)
    p_review.add_argument("--created-by", type=int, dest="created_by")
    p_review.add_argument("--pretty", action="store_true")

    p_open = sub.add_parser("open-ideas", help="List open ideas and their linked aspects")
    p_open.add_argument(
        "--exclude-status",
        action="append",
        dest="exclude_status_codes",
        help="Exclude ideas with this status code (repeatable). Default: rejected, validated",
    )
    p_open.add_argument("--pretty", action="store_true")

    p_docref = sub.add_parser("add-docref", help="Create (or reuse) a DocRef")
    p_docref.add_argument("--path", required=True, dest="doc_path")
    p_docref.add_argument("--anchor", dest="anchor_id")
    p_docref.add_argument("--snapshot", dest="snapshot_commit_sha")
    p_docref.add_argument("--context-note", dest="context_note")
    p_docref.add_argument("--created-by", type=int, dest="created_by")
    p_docref.add_argument("--pretty", action="store_true")

    p_link_aspect_doc = sub.add_parser("link-aspect-docref", help="Link a DocRef to an aspect")
    p_link_aspect_doc.add_argument("--aspect", required=True, dest="aspect_key_or_id")
    p_link_aspect_doc.add_argument("--docref-id", required=True, dest="doc_ref_id")
    p_link_aspect_doc.add_argument("--notes")
    p_link_aspect_doc.add_argument("--created-by", type=int, dest="created_by")
    p_link_aspect_doc.add_argument("--pretty", action="store_true")

    p_link_idea_doc = sub.add_parser("link-idea-docref", help="Link a DocRef to an idea")
    p_link_idea_doc.add_argument("--idea-id", required=True, dest="idea_id")
    p_link_idea_doc.add_argument("--docref-id", required=True, dest="doc_ref_id")
    p_link_idea_doc.add_argument("--notes")
    p_link_idea_doc.add_argument("--created-by", type=int, dest="created_by")
    p_link_idea_doc.add_argument("--pretty", action="store_true")

    p_idea_pack = sub.add_parser("idea-pack", help="Show a complete idea pack (for recall)")
    p_idea_pack.add_argument("--idea-id", required=True, dest="idea_id")
    p_idea_pack.add_argument("--pretty", action="store_true")

    args = parser.parse_args()
    svc = KnowledgeBaseService()

    try:
        if args.cmd == "create-aspect":
            result = svc.create_aspect(
                aspect_key=args.aspect_key,
                title=args.title,
                summary=args.summary,
                maturity_code=args.maturity_code,
                state_code=args.state_code,
                owner=args.owner,
                created_by=args.created_by,
            )
            _print(result, args.pretty)
            return 0

        if args.cmd == "create-idea":
            result = svc.create_idea(
                title=args.title,
                problem_statement=args.problem_statement,
                hypothesis=args.hypothesis,
                impact_notes=args.impact_notes,
                risks=args.risks,
                next_step=args.next_step,
                decision_summary=args.decision_summary,
                status_code=args.status_code,
                created_by=args.created_by,
            )
            _print(result, args.pretty)
            return 0

        if args.cmd == "set-idea-status":
            result = svc.set_idea_status(
                idea_id=args.idea_id,
                status_code=args.status_code,
                decision_summary=args.decision_summary,
                updated_by=args.updated_by,
            )
            _print(result, args.pretty)
            return 0

        if args.cmd == "park-idea":
            result = svc.set_idea_status(
                idea_id=args.idea_id,
                status_code="parked",
                decision_summary=args.decision_summary,
                updated_by=args.updated_by,
            )
            _print(result, args.pretty)
            return 0

        if args.cmd == "approve-idea":
            result = svc.set_idea_status(
                idea_id=args.idea_id,
                status_code="approved_to_build",
                decision_summary=args.decision_summary,
                updated_by=args.updated_by,
            )
            _print(result, args.pretty)
            return 0

        if args.cmd == "link-idea-aspect":
            result = svc.link_idea_to_aspect(
                idea_id=args.idea_id,
                aspect_key_or_id=args.aspect_key_or_id,
                notes=args.notes,
                created_by=args.created_by,
            )
            _print(result, args.pretty)
            return 0

        if args.cmd == "link-aspects":
            result = svc.link_aspects(
                from_aspect=args.from_aspect,
                to_aspect=args.to_aspect,
                relation_type_code=args.relation_type_code,
                notes=args.notes,
                created_by=args.created_by,
                auto_symmetric=not args.no_auto_symmetric,
            )
            _print(result, args.pretty)
            return 0

        if args.cmd == "add-session-note":
            result = svc.add_session_note(
                title=args.title,
                summary=args.summary,
                decisions=args.decisions,
                source_type=args.source_type,
                source_ref=args.source_ref,
                idea_ids=args.idea_ids,
                aspect_ids_or_keys=args.aspect_ids_or_keys,
                created_by=args.created_by,
            )
            _print(result, args.pretty)
            return 0

        if args.cmd == "context-pack":
            result = svc.get_aspect_context_pack(aspect_key_or_id=args.aspect_key_or_id)
            _print(result, args.pretty)
            return 0

        if args.cmd == "enqueue-review":
            result = svc.enqueue_related_aspect_reviews(
                aspect_key_or_id=args.aspect_key_or_id,
                reason=args.reason,
                created_by=args.created_by,
            )
            _print(result, args.pretty)
            return 0

        if args.cmd == "open-ideas":
            excluded = ["rejected", "validated"]
            for code in args.exclude_status_codes or []:
                c = (code or "").strip()
                if c and c not in excluded:
                    excluded.append(c)
            result = svc.list_open_ideas(exclude_status_codes=tuple(excluded))
            _print(result, args.pretty)
            return 0

        if args.cmd == "add-docref":
            result = svc.create_doc_ref(
                doc_path=args.doc_path,
                anchor_id=args.anchor_id,
                snapshot_commit_sha=args.snapshot_commit_sha,
                context_note=args.context_note,
                created_by=args.created_by,
            )
            _print(result, args.pretty)
            return 0

        if args.cmd == "link-aspect-docref":
            result = svc.link_doc_ref_to_aspect(
                aspect_key_or_id=args.aspect_key_or_id,
                doc_ref_id=args.doc_ref_id,
                notes=args.notes,
                created_by=args.created_by,
            )
            _print(result, args.pretty)
            return 0

        if args.cmd == "link-idea-docref":
            result = svc.link_doc_ref_to_idea(
                idea_id=args.idea_id,
                doc_ref_id=args.doc_ref_id,
                notes=args.notes,
                created_by=args.created_by,
            )
            _print(result, args.pretty)
            return 0

        if args.cmd == "idea-pack":
            result = svc.get_idea_pack(idea_id=args.idea_id)
            _print(result, args.pretty)
            return 0

        raise KbError(f"Unknown command: {args.cmd}")

    except KbError as e:
        _print({"error": str(e), "cmd": args.cmd}, getattr(args, "pretty", False))
        return 1
    except Exception as e:
        _print({"error": f"Unhandled error: {e}", "cmd": args.cmd}, getattr(args, "pretty", False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

