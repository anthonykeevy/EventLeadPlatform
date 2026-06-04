"""
Seed EventLead Public Demo Showcase 2026 + eight landing-page demo forms.

Run from backend/ after migrations and with DATABASE_URL configured:

  python scripts/seed_landing_demo_forms.py
  python scripts/seed_landing_demo_forms.py --dry-run
  python scripts/seed_landing_demo_forms.py --refresh-definitions
  python scripts/seed_landing_demo_forms.py --no-publish

Writes manifest: seed_data/landing_demo/manifest.local.json (gitignored via .gitignore if needed)
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from pydantic import ValidationError

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

load_dotenv(BACKEND_ROOT / ".env")

from common.database import SessionLocal  # noqa: E402
from models.log.frontend_event import FrontendEvent  # noqa: F401,E402
from schemas.form_definition import FormDefinition  # noqa: E402
from seed_data.landing_demo.forms import LANDING_DEMO_FORMS  # noqa: E402
from seed_data.landing_demo.runner import (  # noqa: E402
    DEFAULT_USER_ID,
    seed_landing_demo,
    write_manifest,
)


def _validate_definitions() -> None:
    for spec in LANDING_DEMO_FORMS:
        try:
            FormDefinition.model_validate(spec.builder())
        except ValidationError as exc:
            print(f"Definition invalid for {spec.slug}:", file=sys.stderr)
            print(exc, file=sys.stderr)
            raise SystemExit(2) from exc


async def _run(args: argparse.Namespace) -> int:
    _validate_definitions()
    if args.dry_run:
        print("Dry run: all definitions pass FormDefinition validation.")
        for spec in LANDING_DEMO_FORMS:
            print(f"  - {spec.form_name}")
        return 0

    db = SessionLocal()
    try:
        result = await seed_landing_demo(
            db,
            user_id=args.user_id,
            company_name=args.company,
            publish=not args.no_publish,
            update_existing_definitions=args.refresh_definitions,
            skip_if_complete=not args.refresh_definitions,
        )
        db.commit()
        out = BACKEND_ROOT / "seed_data" / "landing_demo" / "manifest.local.json"
        write_manifest(result, out)
        print(json.dumps({"manifest": str(out), "event_created": result.event_created}, indent=2))
        print("\nForms:")
        for row in result.forms:
            status = "created" if row["created"] else "existing"
            print(f"  [{status}] {row['form_name']} (id={row['form_id']})")
            if row.get("public_url"):
                print(f"           {row['public_url']}")
        print(f"\nManifest written to {out}")
        return 0
    except Exception as exc:
        db.rollback()
        print(f"Seed failed: {exc}", file=sys.stderr)
        raise
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed landing-page demo event and forms")
    parser.add_argument("--dry-run", action="store_true", help="Validate definitions only")
    parser.add_argument("--user-id", type=int, default=DEFAULT_USER_ID)
    parser.add_argument("--company", default="Signal Platforms")
    parser.add_argument("--no-publish", action="store_true", help="Create drafts only")
    parser.add_argument(
        "--refresh-definitions",
        action="store_true",
        help="Update existing demo form drafts and re-publish",
    )
    args = parser.parse_args()
    raise SystemExit(asyncio.run(_run(args)))


if __name__ == "__main__":
    main()
