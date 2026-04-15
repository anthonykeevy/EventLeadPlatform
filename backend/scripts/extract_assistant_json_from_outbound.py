"""Parse OpenAI outbound RequestPayload and print component boxes for collision debugging."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.database import engine  # noqa: E402
from modules.form_ai.service import (  # noqa: E402
    _collect_visual_collisions,
    _flatten_collision_visual_components,
)


def _find_inner_json(messages: str) -> dict | None:
    # Last assistant message often contains raw DefinitionJSON
    try:
        outer = json.loads(messages)
    except json.JSONDecodeError:
        return None
    if isinstance(outer, dict) and "input" in outer:
        blocks = outer["input"]
    elif isinstance(outer, list):
        blocks = outer
    else:
        return None
    for block in reversed(blocks if isinstance(blocks, list) else []):
        if not isinstance(block, dict):
            continue
        if block.get("role") != "assistant":
            continue
        for part in block.get("content") or []:
            if not isinstance(part, dict):
                continue
            txt = part.get("text") or ""
            if '"pages"' in txt and '"schemaVersion"' in txt:
                try:
                    return json.loads(txt)
                except json.JSONDecodeError:
                    m = re.search(r"\{[\s\S]*\}", txt)
                    if m:
                        return json.loads(m.group(0))
    return None


def main() -> None:
    inbound = "903afb9d-36c5-40ab-a6f2-feaa8ad34596"
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
            SELECT ApiRequestID, RequestPayload
            FROM log.ApiRequest
            WHERE RequestID LIKE :pat AND Path LIKE '/outbound/openai%'
            ORDER BY ApiRequestID ASC
            """
            ),
            {"pat": inbound + "%"},
        ).fetchall()

    print(f"outbound rows: {len(rows)}")
    rt = {
        "canvas": {"width": 1920, "height": 980},
        "componentFootprints": [
            {"componentType": "textarea", "width": 720, "height": 209},
            {"componentType": "first-name", "width": 560, "height": 110},
            {"componentType": "text", "width": 560, "height": 110},
        ],
    }

    for aid, payload in rows:
        if not payload:
            continue
        print("\n" + "=" * 80)
        print("ApiRequestID", aid)
        inner = _find_inner_json(payload)
        if not inner:
            print("(could not parse assistant JSON)")
            continue
        pages = inner.get("pages")
        if not isinstance(pages, list) or not pages:
            continue
        comps = pages[0].get("components")
        if not isinstance(comps, list):
            continue
        for c in comps:
            if not isinstance(c, dict):
                continue
            cid = c.get("id")
            st = c.get("style") if isinstance(c.get("style"), dict) else {}
            pr = c.get("props") if isinstance(c.get("props"), dict) else {}
            pos = c.get("position") if isinstance(c.get("position"), dict) else {}
            print(
                f"  {cid} type={c.get('type')} x={pos.get('x')} y={pos.get('y')} "
                f"style.w={st.get('width')} style.h={st.get('height')} props.w={pr.get('width')}"
            )
        _, flat = _flatten_collision_visual_components(inner, rt)
        print("\n  collision boxes (form_ai visual):")
        for f in flat:
            print(
                f"    {f['id']}: x={f['x']:.0f} y={f['y']:.0f} w={f['width']:.0f} h={f['height']:.0f}"
            )
        for label, ctx in (
            ("no runtime_context", None),
            ("sample runtime_context (textarea/first-name/text footprints)", rt),
        ):
            cols = _collect_visual_collisions(inner, ctx)
            print(f"\n  _collect_visual_collisions ({label}): {len(cols)}")
            for v in cols:
                print(
                    f"    {v.componentAId} / {v.componentBId} area={v.overlapArea:.1f}"
                )


if __name__ == "__main__":
    main()
