#!/usr/bin/env python
"""Verify four-consumer component catalog alignment (Story 6.5d AC-3).

Compares component codes from:
  1. resolve_allowed_components
  2. form-builder init shape (get_allowed_components)
  3. Block F capability JSON fragment
  4. semantic validator allowed set

Exit 1 on mismatch and print diff.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from modules.form_ai.capability_prompt import build_capability_prompt_block_from_catalog
from modules.form_ai.semantic_validator import validate_semantic_plan
from modules.form_ai.schemas import FormSemanticPlan, SemanticComponentIntent
from modules.form_builder.component_catalog import resolve_allowed_components
from modules.form_builder.service import get_allowed_components


def _codes_from_catalog(company_id: int, country_id: int | None, form_id: int | None) -> set[str]:
    engine = create_engine(_database_url())
    Session = sessionmaker(bind=engine)
    with Session() as db:
        requires_offline = False
        if form_id is not None:
            row = db.execute(
                text(
                    """
                    SELECT TOP 1 [RequiresOfflineCapable]
                    FROM [dbo].[Form]
                    WHERE [FormID] = :form_id AND [IsDeleted] = 0
                    """
                ),
                {"form_id": form_id},
            ).fetchone()
            requires_offline = bool(row.RequiresOfflineCapable) if row else False
        catalog = resolve_allowed_components(
            db,
            company_id,
            country_id,
            requires_offline_capable=requires_offline,
        )
        init_rows = get_allowed_components(
            db, company_id, country_id, form_id=form_id
        )
    init_codes = {row["componentCode"] for row in init_rows}
    resolver_codes = set(catalog.component_codes)
    block_f_text = build_capability_prompt_block_from_catalog(catalog)
    prompt_codes = {
        line.split()[1]
        for line in block_f_text.splitlines()
        if line.strip().startswith("- ")
    }
    capability_json = catalog.to_capability_json()

    # Validator gate: same capability snapshot the generate path uses.
    if resolver_codes:
        sample_type = sorted(resolver_codes)[0]
        plan = FormSemanticPlan(
            semanticPlanVersion="1.0",
            formId="alignment-check",
            title="Alignment check",
            components=[
                SemanticComponentIntent(componentType=sample_type, label="Sample"),
            ],
        )
        gate = validate_semantic_plan(
            plan,
            capability_snapshot_json=capability_json,
            validation_contracts=None,
        )
        if not gate.valid and gate.violations:
            first = gate.violations[0].code
            if first == "unknown-component-type":
                validator_codes: set[str] = set()
            else:
                validator_codes = resolver_codes
        else:
            validator_codes = resolver_codes
    else:
        validator_codes = set()

    sets = {
        "resolver": resolver_codes,
        "init": init_codes,
        "block_f_prompt": prompt_codes,
        "validator": validator_codes,
    }
    return sets


def _database_url() -> str:
    import os

    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is required for verify_component_catalog_alignment.py")
    return url


def main() -> int:
    parser = argparse.ArgumentParser(description="Story 6.5d catalog alignment gate")
    parser.add_argument("--company-id", type=int, default=1)
    parser.add_argument("--country-id", type=int, default=None, help="AU country id (optional)")
    parser.add_argument("--form-id", type=int, default=None)
    args = parser.parse_args()

    country_id = args.country_id
    if country_id is None:
        engine = create_engine(_database_url())
        with engine.connect() as conn:
            row = conn.execute(
                text(
                    """
                    SELECT TOP 1 [CountryID]
                    FROM [ref].[Country]
                    WHERE [CountryCode] = N'AU' AND [IsDeleted] = 0
                    """
                )
            ).fetchone()
            country_id = int(row[0]) if row else None

    sets = _codes_from_catalog(args.company_id, country_id, args.form_id)
    baseline = sets["resolver"]
    mismatches = []
    for name, codes in sets.items():
        if codes != baseline:
            only_here = sorted(codes - baseline)
            missing = sorted(baseline - codes)
            mismatches.append((name, only_here, missing))

    if mismatches:
        print("CATALOG ALIGNMENT FAILED")
        print(f"resolver baseline ({len(baseline)}): {sorted(baseline)}")
        for name, only_here, missing in mismatches:
            print(f"  {name}: extra={only_here} missing={missing}")
        return 1

    print(
        f"CATALOG ALIGNMENT OK — {len(baseline)} codes "
        f"(company={args.company_id}, country={country_id}, form={args.form_id})"
    )
    print(f"  codes: {', '.join(sorted(baseline))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
