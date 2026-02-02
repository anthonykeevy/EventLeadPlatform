"""
Audit FormVersion definitions for legacy patterns that require frontend migration.

This script answers: "Do we still need migrateComponentToStructure()?"

We scan every dbo.FormVersion.DefinitionJSON and detect patterns that the migration
function historically fixed:
- Legacy component type: 'select' -> should be 'dropdown'
- Divider legacy style mapping: styleOverrides.textBorder* -> dividerBorder*
- Missing structure-era props (objectLayout/layoutGroups/objectSpacing) (informational)

Run:
  python backend/scripts/audit_form_versions_for_structure_migration.py
  python backend/scripts/audit_form_versions_for_structure_migration.py --limit 50
  python backend/scripts/audit_form_versions_for_structure_migration.py --form-id 43
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Tuple

from sqlalchemy import select

# Allow running from repo root or backend/ by ensuring backend is on sys.path
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BACKEND_ROOT = os.path.abspath(os.path.join(_HERE, ".."))
if _BACKEND_ROOT not in sys.path:
    sys.path.insert(0, _BACKEND_ROOT)

from common.database import SessionLocal  # noqa: E402
from models.form_version import FormVersion  # noqa: E402


def _iter_components_from_definition(defn: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    """
    Iterate all components found in likely definition locations.
    Supports both legacy `pages` and newer `desktopPages` layouts.
    """
    pages = defn.get("desktopPages") or defn.get("pages") or []
    if not isinstance(pages, list):
        return []

    def walk_list(items: List[Any]) -> Iterable[Dict[str, Any]]:
        for item in items:
            if not isinstance(item, dict):
                continue
            yield item
            children = item.get("children")
            if isinstance(children, list):
                yield from walk_list(children)

    for page in pages:
        if not isinstance(page, dict):
            continue
        comps = page.get("components") or []
        if isinstance(comps, list):
            yield from walk_list(comps)


@dataclass
class VersionIssues:
    has_legacy_select_type: bool = False
    has_divider_textborder_legacy: bool = False
    missing_object_spacing: int = 0
    has_object_layout_prop: int = 0
    has_layout_groups_prop: int = 0

    total_components: int = 0
    affected_components: int = 0
    affected_examples: List[Tuple[str, str]] = field(default_factory=list)  # (componentId, reason)


def analyze_definition(defn: Dict[str, Any]) -> VersionIssues:
    issues = VersionIssues()

    for c in _iter_components_from_definition(defn):
        issues.total_components += 1
        ctype = str(c.get("type") or "")
        cid = str(c.get("id") or "")
        props = c.get("props") if isinstance(c.get("props"), dict) else {}
        style_overrides = props.get("styleOverrides") if isinstance(props.get("styleOverrides"), dict) else {}

        if ctype == "select":
            issues.has_legacy_select_type = True
            issues.affected_components += 1
            if len(issues.affected_examples) < 10:
                issues.affected_examples.append((cid, "type=select (should be dropdown)"))

        if ctype == "divider":
            has_text_border = bool(style_overrides.get("textBorderColor") or style_overrides.get("textBorderWidth"))
            has_divider_border = bool(style_overrides.get("dividerBorderColor") or style_overrides.get("dividerBorderWidth"))
            if has_text_border and not has_divider_border:
                issues.has_divider_textborder_legacy = True
                issues.affected_components += 1
                if len(issues.affected_examples) < 10:
                    issues.affected_examples.append((cid, "divider styleOverrides.textBorder* (missing dividerBorder*)"))

        # Informational (not necessarily a bug anymore): structure-era props present/missing.
        if props.get("objectLayout") is not None:
            issues.has_object_layout_prop += 1
        if props.get("layoutGroups") is not None:
            issues.has_layout_groups_prop += 1
        if props.get("objectSpacing") is None:
            issues.missing_object_spacing += 1

    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="Limit number of FormVersion rows scanned (0 = no limit)")
    parser.add_argument("--form-id", type=int, default=0, help="Only scan a single FormID")
    args = parser.parse_args()

    with SessionLocal() as db:
        stmt = select(FormVersion).order_by(FormVersion.FormID.desc(), FormVersion.VersionNumber.desc())
        if args.form_id:
            stmt = stmt.where(FormVersion.FormID == args.form_id)
        if args.limit and args.limit > 0:
            stmt = stmt.limit(args.limit)

        rows = list(db.execute(stmt).scalars().all())

    if not rows:
        print("No FormVersion rows found for the given filters.")
        return 0

    total_versions = 0
    versions_needing_migration = 0
    forms_with_issues: Dict[int, int] = {}

    print("====================================================================")
    print("AUDIT: FormVersion definitions for structure migration needs")
    print("====================================================================")

    for v in rows:
        total_versions += 1
        try:
            defn = v.definition or {}
        except Exception:
            defn = {}

        if not isinstance(defn, dict):
            defn = {}

        issues = analyze_definition(defn)
        needs = issues.has_legacy_select_type or issues.has_divider_textborder_legacy

        if needs:
            versions_needing_migration += 1
            forms_with_issues[int(v.FormID)] = forms_with_issues.get(int(v.FormID), 0) + 1

        # Only print per-version detail when something is found (keeps output readable).
        if needs:
            print(f"- FormID={int(v.FormID)} v{int(v.VersionNumber)} status={v.Status} active={bool(v.IsActive)}")
            print(f"  totalComponents={issues.total_components}")
            if issues.has_legacy_select_type:
                print("  - legacySelectType: YES")
            if issues.has_divider_textborder_legacy:
                print("  - dividerTextBorderLegacy: YES")
            if issues.affected_examples:
                print("  examples:")
                for cid, reason in issues.affected_examples:
                    print(f"    - {cid or '<no-id>'}: {reason}")

    print("--------------------------------------------------------------------")
    print(f"Scanned versions: {total_versions}")
    print(f"Versions needing migration: {versions_needing_migration}")
    print(f"Distinct forms with at least one affected version: {len(forms_with_issues)}")

    if forms_with_issues:
        top = sorted(forms_with_issues.items(), key=lambda kv: kv[1], reverse=True)[:10]
        print("Top affected forms (FormID -> affected version count):")
        for form_id, cnt in top:
            print(f"  - {form_id}: {cnt}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

