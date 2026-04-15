"""
Deterministic scoring for first-shot (single model response) form-AI experiments.

Separates:
  * layout_score — from validator counts (collisions, boundaries, schema).
  * goal_score — heuristic coverage of the user's natural-language request.

Goal checks are keyword-gated: only requirements that appear in the user prompt
are scored, so the same scorer works across prompts.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Tuple


def flatten_components(definition: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Depth-first list of component dicts from the first page (and nested children)."""
    pages = definition.get("pages")
    if not isinstance(pages, list) or not pages:
        return []
    page = pages[0]
    components = page.get("components")
    if not isinstance(components, list):
        return []

    out: List[Dict[str, Any]] = []

    def walk(items: List[Any]) -> None:
        for item in items:
            if isinstance(item, dict):
                out.append(item)
                ch = item.get("children")
                if isinstance(ch, list):
                    walk(ch)

    walk(components)
    return out


def _label_lower(component: Dict[str, Any]) -> str:
    props = component.get("props") if isinstance(component.get("props"), dict) else {}
    for key in ("label", "text", "placeholder"):
        v = props.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip().lower()
    return ""


def _option_labels(component: Dict[str, Any]) -> List[str]:
    props = component.get("props") if isinstance(component.get("props"), dict) else {}
    raw = props.get("options")
    if not isinstance(raw, list):
        return []
    labels: List[str] = []
    for opt in raw:
        if isinstance(opt, dict):
            lab = opt.get("label")
            if isinstance(lab, str):
                labels.append(lab.lower())
    return labels


def score_layout(
    collision_count: int,
    boundary_count: int,
    schema_error_count: int,
) -> float:
    """
    0–100; lower is better for error counts. Same scale across runs for comparison.
    """
    raw = (
        100.0
        - 5.0 * float(max(0, collision_count))
        - 8.0 * float(max(0, boundary_count))
        - 15.0 * float(max(0, schema_error_count))
    )
    return max(0.0, min(100.0, raw))


def score_goal_coverage(
    definition: Dict[str, Any],
    user_prompt: str,
) -> Tuple[float, List[Dict[str, Any]]]:
    """
    Returns (score 0–100, checklist rows for logging).

    Each applicable requirement (derived from phrases in the prompt) contributes
    equally to the score.
    """
    prompt_l = user_prompt.lower()
    flat = flatten_components(definition)
    types = [str(c.get("type", "")).lower() for c in flat]
    labels = [_label_lower(c) for c in flat]

    def has_type(*names: str) -> bool:
        return any(t in types for t in names)

    checks: List[Dict[str, Any]] = []
    applicable: List[Tuple[str, Callable[[], bool]]] = []

    if "first name" in prompt_l:
        applicable.append(
            (
                "first_name",
                lambda: has_type("first-name")
                or (has_type("text") and any("first" in lab for lab in labels)),
            )
        )
    if "last name" in prompt_l:
        applicable.append(
            (
                "last_name",
                lambda: has_type("text") and any("last" in lab for lab in labels),
            )
        )
    if "email" in prompt_l:
        applicable.append(("email_field", lambda: has_type("email")))
    if "phone" in prompt_l:
        applicable.append(("phone_field", lambda: has_type("phone")))
    if "company" in prompt_l:
        applicable.append(
            (
                "company_field",
                lambda: has_type("text") and any("company" in lab for lab in labels),
            )
        )
    if "job title" in prompt_l or ("job" in prompt_l and "title" in prompt_l):
        applicable.append(
            (
                "job_title",
                lambda: has_type("text")
                and any(("job" in lab or "title" in lab) for lab in labels),
            )
        )
    if "country" in prompt_l and ("dropdown" in prompt_l or "select" in prompt_l):
        def country_dropdown() -> bool:
            for c in flat:
                t = str(c.get("type", "")).lower()
                if t not in ("dropdown", "select"):
                    continue
                opts = _option_labels(c)
                if len(opts) < 2:
                    continue
                joined = " ".join(opts)
                if "australia" in joined and ("united" in joined or "kingdom" in joined or "canada" in joined):
                    return True
            return False

        applicable.append(("country_dropdown_options", country_dropdown))

    if "register" in prompt_l or "submit" in prompt_l:
        def submit_register() -> bool:
            for c in flat:
                if str(c.get("type", "")).lower() != "submit-button":
                    continue
                lab = _label_lower(c)
                if "register" in lab:
                    return True
            return False

        applicable.append(("submit_register_label", submit_register))

    if not applicable:
        return 100.0, [
            {
                "id": "_note",
                "ok": True,
                "detail": "No goal keywords matched; goal score neutral at 100.",
            }
        ]

    passed = 0
    for cid, fn in applicable:
        ok = False
        try:
            ok = bool(fn())
        except Exception:
            ok = False
        checks.append({"id": cid, "ok": ok, "detail": None})
        if ok:
            passed += 1

    frac = passed / len(applicable)
    return 100.0 * frac, checks


def combined_score(layout: float, goal: float, *, layout_weight: float = 0.5) -> float:
    w = max(0.0, min(1.0, layout_weight))
    return w * layout + (1.0 - w) * goal


def addendum_fingerprint(text: str) -> str:
    """Short stable hash for changelog rows (avoid storing full text twice)."""
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
