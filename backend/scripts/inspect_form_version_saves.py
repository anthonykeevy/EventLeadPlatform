"""
Inspect recent FormVersion save API requests (safe summary).

Goal:
- Verify the builder is sending a complete Definition payload (globalStyles + component props)
  when saving drafts.
- Provide an agent-friendly summary WITHOUT dumping full request bodies.

Notes:
- Reads from log.ApiRequest (server-side request logging).
- Filters to /api/forms/{id}/versions... endpoints (POST/PUT).
- Does not print response payloads (avoid leaking preview tokens from other endpoints).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import text


backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))


def safe_json_load(raw: Optional[str]) -> Optional[Dict[str, Any]]:
    if not raw:
        return None
    try:
        value = json.loads(raw)
        return value if isinstance(value, dict) else None
    except Exception:
        return None


def as_int(value: Any) -> Optional[int]:
    try:
        if value is None:
            return None
        return int(value)
    except Exception:
        return None


def get_in(d: Dict[str, Any], path: List[str]) -> Any:
    cur: Any = d
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def summarize_global_styles(gs: Any) -> Dict[str, Any]:
    if not isinstance(gs, dict):
        return {"present": False}

    # High-signal subset for Component Framework parity checks
    pick_keys = [
        "primaryColor",
        "baseSpacing",
        "labelFontFamily",
        "labelFontSize",
        "labelFontWeight",
        "labelColor",
        "fontFamily",
        "fontSize",
        "fontWeight",
        "textColor",
        "helpTextFontSize",
        "helpTextColor",
        "inputHeight",
        "inputPaddingX",
        "inputPaddingY",
        "borderWidth",
        "borderRadius",
        "objectRowGapPx",
        "objectColumnGapPx",
        "defaultGridLayout",
        "defaultObjectLayout",
        "defaultLayoutGroups",
    ]

    return {
        "present": True,
        "keyCount": len(gs.keys()),
        "keys": sorted(gs.keys()),
        "selected": {k: gs.get(k) for k in pick_keys if k in gs},
    }


def summarize_component_props(props: Any) -> Dict[str, Any]:
    if not isinstance(props, dict):
        return {"present": False}

    pick_keys = [
        "width",
        "height",
        "textAlign",
        "componentScale",
        "componentScaleAnchor",
        "objectLayout",
        "layoutGroups",
        "rowAlignment",
        "objectSpacing",
        "gridLayout",
        "styleOverrides",
        "labelWidthOverride",
        "inputWidthOverride",
        "helpWidthOverride",
        "labelGapOverride",
        "inputHelpGapOverride",
        "actionWidthOverride",
        "buttonWidth",
        "buttonAlign",
    ]

    return {
        "present": True,
        "keyCount": len(props.keys()),
        "keys": sorted(props.keys()),
        "selected": {k: props.get(k) for k in pick_keys if k in props},
    }


def flatten_components_from_definition(defn: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Pages can be in desktopPages (preferred) or pages (legacy).
    pages = defn.get("desktopPages")
    if not isinstance(pages, list) or not pages:
        pages = defn.get("pages")
    if not isinstance(pages, list):
        return []

    all_components: List[Dict[str, Any]] = []

    def walk(list_items: Any):
        if not isinstance(list_items, list):
            return
        for item in list_items:
            if not isinstance(item, dict):
                continue
            all_components.append(item)
            children = item.get("children")
            if isinstance(children, list) and children:
                walk(children)

    for page in pages:
        if not isinstance(page, dict):
            continue
        comps = page.get("components")
        walk(comps)

    return all_components


def summarize_definition(defn: Any, max_components: int) -> Dict[str, Any]:
    if not isinstance(defn, dict):
        return {"present": False}

    components = flatten_components_from_definition(defn)
    sample = components[: max(0, max_components)]

    sample_summaries: List[Dict[str, Any]] = []
    for c in sample:
        cid = c.get("id")
        ctype = c.get("type")
        props = c.get("props") if isinstance(c.get("props"), dict) else None
        sample_summaries.append(
            {
                "id": cid,
                "type": ctype,
                "props": summarize_component_props(props),
            }
        )

    global_styles = defn.get("globalStyles")

    return {
        "present": True,
        "keys": sorted(defn.keys()),
        "hasDesktopPages": isinstance(defn.get("desktopPages"), list) and len(defn.get("desktopPages") or []) > 0,
        "hasPages": isinstance(defn.get("pages"), list) and len(defn.get("pages") or []) > 0,
        "componentCount": len(components),
        "globalStyles": summarize_global_styles(global_styles),
        "sampleComponents": sample_summaries,
    }


def fetch_recent_version_requests(limit: int, form_id: Optional[int]) -> List[Dict[str, Any]]:
    from common.database import engine

    where = "WHERE Path LIKE :path_filter AND (Method = 'POST' OR Method = 'PUT')"
    params: Dict[str, Any] = {"path_filter": "%/api/forms/%/versions%"}

    if form_id is not None:
        where += " AND Path LIKE :form_filter"
        params["form_filter"] = f"%/api/forms/{form_id}/versions%"

    q = text(
        f"""
        SELECT TOP {limit}
            ApiRequestID,
            Method,
            Path,
            StatusCode,
            DurationMs,
            RequestID,
            UserID,
            CreatedDate,
            RequestPayload
        FROM log.ApiRequest
        {where}
        ORDER BY CreatedDate DESC
        """
    )

    with engine.connect() as conn:
        return [dict(row._mapping) for row in conn.execute(q, params).fetchall()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect recent form version save requests (safe summary).")
    parser.add_argument("--limit", "-l", type=int, default=5, help="How many requests to show (default: 5)")
    parser.add_argument("--form-id", type=int, default=None, help="Optional: filter to a specific FormID")
    parser.add_argument("--max-components", type=int, default=5, help="How many components to summarize per request (default: 5)")
    args = parser.parse_args()

    rows = fetch_recent_version_requests(limit=args.limit, form_id=args.form_id)
    if not rows:
        print("No recent /api/forms/*/versions* POST/PUT requests found in log.ApiRequest.")
        return 0

    print("RECENT FORM VERSION SAVE REQUESTS (SAFE SUMMARY)")
    print("=" * 100)

    for r in rows:
        payload = safe_json_load(r.get("RequestPayload"))
        definition = payload.get("definition") if isinstance(payload, dict) else None
        summary = summarize_definition(definition, max_components=args.max_components)

        print("")
        print(f"[{r.get('CreatedDate')}] {r.get('Method')} {r.get('Path')}")
        print(f"  Status: {r.get('StatusCode')} | DurationMs: {r.get('DurationMs')} | RequestID: {r.get('RequestID')}")
        print(f"  UserID: {r.get('UserID')}")

        if not isinstance(payload, dict):
            print("  Payload: <missing or non-JSON>")
            continue

        print(f"  Payload keys: {sorted(payload.keys())}")
        if "definition" not in payload:
            print("  definition: <MISSING>")
            continue

        if not summary.get("present"):
            print("  definition: <present but not an object>")
            continue

        gs = summary.get("globalStyles") or {}
        print(
            f"  definition keys: {summary.get('keys')}"
        )
        print(
            f"  pages: desktopPages={summary.get('hasDesktopPages')} pages={summary.get('hasPages')} components={summary.get('componentCount')}"
        )
        print(
            f"  globalStyles: present={gs.get('present')} keyCount={gs.get('keyCount')}"
        )

        selected_gs = gs.get("selected") or {}
        if selected_gs:
            print("  globalStyles.selected:")
            for k, v in selected_gs.items():
                # These values are expected to be non-sensitive (fonts, numbers, colors, layout defaults).
                print(f"    - {k}: {v}")

        sample_components = summary.get("sampleComponents") or []
        if sample_components:
            print(f"  sampleComponents (first {len(sample_components)}):")
            for c in sample_components:
                props_summary = c.get("props") or {}
                selected_props = (props_summary.get("selected") or {}) if isinstance(props_summary, dict) else {}
                print(f"    - {c.get('type')} ({c.get('id')}): props.keyCount={props_summary.get('keyCount')}")
                for pk, pv in selected_props.items():
                    # Keep output compact; nested objects (gridLayout/styleOverrides) are shown as "present" by key.
                    if isinstance(pv, dict) and pk == "gridLayout":
                        rows = pv.get("rows")
                        cols = pv.get("columns")
                        row_gap = pv.get("rowGap")
                        col_gap = pv.get("columnGap")
                        assignments = pv.get("cellAssignments") if isinstance(pv.get("cellAssignments"), dict) else {}
                        merged = pv.get("mergedCells") if isinstance(pv.get("mergedCells"), dict) else {}
                        spans = pv.get("objectSpans") if isinstance(pv.get("objectSpans"), dict) else {}
                        row_gaps = pv.get("rowGaps") if isinstance(pv.get("rowGaps"), dict) else {}
                        col_gaps = pv.get("columnGaps") if isinstance(pv.get("columnGaps"), dict) else {}
                        print(
                            f"      - gridLayout: rows={rows} cols={cols} rowGap={row_gap} colGap={col_gap} "
                            f"assignments={len(assignments)} merged={len(merged)} spans={len(spans)} "
                            f"rowGaps={len(row_gaps)} colGaps={len(col_gaps)}"
                        )
                    elif isinstance(pv, dict) and pk == "styleOverrides":
                        keys = sorted(pv.keys())
                        print(f"      - styleOverrides: keyCount={len(keys)} keys={keys[:20]}{'...' if len(keys) > 20 else ''}")
                    elif isinstance(pv, dict) and pk == "objectSpacing":
                        print(f"      - objectSpacing: {pv}")
                    elif isinstance(pv, dict):
                        print(f"      - {pk}: <dict len={len(pv)}>")
                    elif isinstance(pv, list):
                        print(f"      - {pk}: <list len={len(pv)}>")
                    else:
                        print(f"      - {pk}: {pv}")

    print("")
    print("=" * 100)
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

