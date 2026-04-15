"""
Push a DefinitionJSON file into the latest DRAFT FormVersion for a form (e.g. 403).

Use after form-ai first-shot (or any) CLI so the Form Builder loads the same draft from
the API when you open /forms/{id}/builder — no need to paste JSON by hand.

Requires DB access (DATABASE_URL / backend .env). Bypasses HTTP; still enforces
access_guard + schema validation like PUT /api/forms/{form_id}/versions/{version_number}.

Usage (PowerShell, from repo backend/):

  python scripts/push_form_draft_definition.py `
    --form-id 403 `
    --definition path/to/definition.json `
    --user-id 1 `
    --comment "REG-CONF iter 4 first-shot"

If multiple drafts exist, the highest VersionNumber with Status=DRAFT is updated.
Override with --version-number N.

  # Pick user id that has EDIT on the form (often your admin test user).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import desc, select

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

load_dotenv(REPO_ROOT / "backend" / ".env")

from common.database import SessionLocal  # noqa: E402
from models.form_version import FormVersion  # noqa: E402
from models.log.frontend_event import FrontendEvent  # noqa: F401,E402
from modules.forms.version_service import FormVersionService  # noqa: E402
from schemas.form_definition import FormDefinition  # noqa: E402


def _resolve_draft_version_number(db, form_id: int) -> int:
    stmt = (
        select(FormVersion.VersionNumber)
        .where(FormVersion.FormID == form_id, FormVersion.Status == "DRAFT")
        .order_by(desc(FormVersion.VersionNumber))
        .limit(1)
    )
    row = db.execute(stmt).scalar_one_or_none()
    if row is None:
        raise SystemExit(
            f"No DRAFT FormVersion found for FormID={form_id}. "
            "Create or open a draft in the builder first, or pass --version-number."
        )
    return int(row)


async def _run(
    form_id: int,
    definition_path: Path,
    user_id: int,
    version_number: int | None,
    comment: str | None,
) -> None:
    raw = definition_path.read_text(encoding="utf-8")
    definition = json.loads(raw)
    if not isinstance(definition, dict):
        raise SystemExit("Definition file must be a JSON object")

    try:
        FormDefinition.model_validate(definition)
    except ValidationError as exc:
        print("Definition failed schema validation (FormDefinition):", file=sys.stderr)
        print(exc, file=sys.stderr)
        raise SystemExit(2) from exc

    db = SessionLocal()
    try:
        vn = version_number if version_number is not None else _resolve_draft_version_number(db, form_id)
        if version_number is None:
            print(f"Using latest DRAFT: FormID={form_id} VersionNumber={vn}", flush=True)

        service = FormVersionService(db)
        await service.update_version(
            form_id=form_id,
            version_number=vn,
            user_id=user_id,
            definition=definition,
            comment=comment,
        )
        db.commit()
        print(f"Updated FormVersion FormID={form_id} version={vn} OK", flush=True)
    except HTTPException as exc:
        db.rollback()
        print(f"HTTP {exc.status_code}: {exc.detail}", file=sys.stderr)
        raise SystemExit(3) from exc
    except ValueError as exc:
        db.rollback()
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(3) from exc
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Push DefinitionJSON into a form draft version")
    parser.add_argument("--form-id", type=int, default=403, help="Form.FormID (default 403)")
    parser.add_argument("--definition", type=Path, required=True, help="Path to DefinitionJSON file")
    parser.add_argument("--user-id", type=int, required=True, help="UserID with EDIT on the form")
    parser.add_argument(
        "--version-number",
        type=int,
        default=None,
        help="Optional; default = latest DRAFT version number",
    )
    parser.add_argument(
        "--comment",
        type=str,
        default=None,
        help="Optional FormVersion.VersionComment",
    )
    args = parser.parse_args()

    if not args.definition.is_file():
        raise SystemExit(f"Not a file: {args.definition}")

    asyncio.run(
        _run(
            form_id=args.form_id,
            definition_path=args.definition,
            user_id=args.user_id,
            version_number=args.version_number,
            comment=args.comment,
        )
    )


if __name__ == "__main__":
    main()
