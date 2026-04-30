"""AU diagnostic context and deterministic checks for Form AI eval runs."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from modules.form_ai import service as form_ai_service


AU_LOCALE_CONTRACT_VERSION = "au-locale-contract-v1"
AU_LOCALE_CONTRACT: Dict[str, Any] = {
    "version": AU_LOCALE_CONTRACT_VERSION,
    "benchmark_market": "AU",
    "facts": {
        "phone_country_code": "+61",
        "date_format": "DD/MM/YYYY",
        "address_shape": "Suburb, State, Postcode",
        "currency": "AUD",
        "privacy_law": "Privacy Act 1988",
        "spam_law": "Spam Act 2003",
        "language": "Australian English",
        "tone": "Practical/plain-English tone",
    },
    "sources": [
        "docs/stories/story-6.4.6.md AC-3",
        "docs/stories/STORY-6.4.6-SINGLE-SESSION-DEV-PROMPT.md Step 2",
        "Existing Form AI locale/prompt assembly reads config.PromptTemplateLocaleBlock when DB context is available.",
    ],
}

CONTRACT_PATH = Path(__file__).with_name("au_locale_contract_v1.json")

SECTION_LABELS = {
    "system_prompt_output_contract": "System Prompt / Output Contract",
    "au_locale_block": "AU Locale Block",
    "brand_posture_block": "Brand Posture Block",
    "component_capability_block": "Component Capability Block",
    "component_property_cheat_sheet": "Component Property Cheat Sheet",
    "consent_legal_guidance": "Consent / Legal Guidance",
    "context_pack_excerpt": "Context Pack Excerpt",
    "runtime_layout_context": "Runtime Layout Context",
    "candidate_prompt_block": "Candidate Prompt Block",
}

SYSTEM_PROMPT_OUTPUT_CONTRACT = (
    "You generate an EventLead semantic form plan for Story 6.3.1.\n"
    "Output a single JSON object only. No markdown or prose.\n"
    "Return FormSemanticPlan only; do not output coordinates, pixel widths, "
    "x/y positions, style blocks, or final DefinitionJSON.\n"
    "Required root keys: semanticPlanVersion, formId, title, components. "
    "Do not add other root keys. Each component uses componentType, label, "
    "placeholder, helpText, section, rowGroup, widthIntent, options, and "
    "validationIntent where applicable."
)


def _hash_content(content: str) -> str:
    return sha256(content.encode("utf-8")).hexdigest()


def _json_text(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, default=str)


def _section(section_id: str, content: str, *, active: bool = True) -> Dict[str, Any]:
    return {
        "section_id": section_id,
        "label": SECTION_LABELS[section_id],
        "active": active,
        "content_hash": _hash_content(content),
        "content": content,
    }


def render_au_contract_text() -> str:
    facts = AU_LOCALE_CONTRACT["facts"]
    return "\n".join(
        [
            f"AU locale contract version: {AU_LOCALE_CONTRACT_VERSION}",
            f"- Phone: {facts['phone_country_code']}",
            f"- Dates: {facts['date_format']}",
            f"- Address: {facts['address_shape']}",
            f"- Currency: {facts['currency']}",
            f"- Privacy: {facts['privacy_law']}",
            f"- Marketing/electronic messages: {facts['spam_law']}",
            f"- Language: {facts['language']}",
            f"- Tone: {facts['tone']}",
        ]
    )


def write_au_contract(path: Path = CONTRACT_PATH) -> None:
    path.write_text(_json_text(AU_LOCALE_CONTRACT) + "\n", encoding="utf-8")


def build_context_sections(
    prompt: Any,
    *,
    db_session: Any = None,
    candidate_prompt_block: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Build stable eval sections from the same helpers used by generation."""

    runtime_context = dict(prompt.runtime_context or {})
    audience_locale = prompt.audience_locale or runtime_context.get("audienceLocale") or "AU"
    brand_posture = runtime_context.get("brandPosture")
    brand_heritage_origin = runtime_context.get("brandHeritageOrigin")
    governance_versions = form_ai_service._resolve_runtime_governance_versions(db_session)
    capability_snapshot = governance_versions.get("componentCapabilitySnapshotJson")
    runtime_context_for_prompt = form_ai_service._filter_runtime_context_to_capability(
        runtime_context,
        capability_snapshot,
    )
    service_locale_block = form_ai_service._assemble_locale_block(
        audience_locale,
        brand_posture,
        db_session,
    )
    context_pack = form_ai_service._trim_context_pack_for_prompt(form_ai_service._load_context_pack())
    capability_block = form_ai_service._build_capability_prompt_block(capability_snapshot)
    runtime_block = form_ai_service._build_runtime_context_block(runtime_context_for_prompt)
    candidate_block = (candidate_prompt_block or "").strip()

    locale_content = (
        f"Service-rendered locale block for audience_locale={audience_locale}:\n"
        f"{service_locale_block}\n\n"
        f"Version-managed AU contract:\n{render_au_contract_text()}"
    )
    component_property_content = (
        "No component property cheat sheet is active in the current prompt state for this baseline."
    )

    return [
        _section("system_prompt_output_contract", SYSTEM_PROMPT_OUTPUT_CONTRACT),
        _section("au_locale_block", locale_content),
        _section(
            "brand_posture_block",
            form_ai_service._render_brand_posture_block(brand_posture, brand_heritage_origin),
        ),
        _section(
            "component_capability_block",
            capability_block or "No DB-backed component capability prompt block was active.",
            active=bool(capability_block),
        ),
        _section("component_property_cheat_sheet", component_property_content, active=False),
        _section("consent_legal_guidance", form_ai_service._active_consent_guidance_block()),
        _section("context_pack_excerpt", context_pack),
        _section(
            "runtime_layout_context",
            runtime_block or "No runtime layout context was supplied.",
            active=bool(runtime_block),
        ),
        _section("candidate_prompt_block", candidate_block, active=bool(candidate_block)),
    ]


def _section_refs(sections: Sequence[Dict[str, Any]]) -> List[Dict[str, str]]:
    return [
        {"section_id": section["section_id"], "content_hash": section["content_hash"]}
        for section in sections
    ]


def build_shared_context_bundle(
    prompts: Iterable[Any],
    *,
    run_id: str,
    benchmark_set_version: str,
    db_session: Any = None,
    candidate_prompt_block: Optional[str] = None,
    experiment_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    prompts_list = list(prompts)
    first_prompt = prompts_list[0] if prompts_list else None
    sections = (
        build_context_sections(
            first_prompt,
            db_session=db_session,
            candidate_prompt_block=candidate_prompt_block,
        )
        if first_prompt
        else []
    )
    return {
        "schema_version": "shared-context-bundle-v1",
        "run_id": run_id,
        "benchmark_set_version": benchmark_set_version,
        "experiment": experiment_metadata,
        "au_locale_contract": AU_LOCALE_CONTRACT,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "sections": sections,
        "cases": {
            prompt.prompt_id: {
                "prompt_id": prompt.prompt_id,
                "audience_locale": prompt.audience_locale,
                "user_prompt": prompt.prompt,
                "expected_au_signals": prompt.expected_signals,
                "prompt_context_section_refs": _section_refs(sections),
            }
            for prompt in prompts_list
        },
    }


CHECK_PATTERNS = [
    {
        "check_id": "foreign_zip",
        "description": "ZIP where Postcode is expected",
        "pattern": re.compile(r"\bZIP(?:\s+code)?\b"),
    },
    {
        "check_id": "foreign_phone_code",
        "description": "+1, +44, or +64 where +61 or neutral AU guidance is expected",
        "pattern": re.compile(r"(?<!\d)(?:\+1|\+44|\+64)(?!\d)"),
    },
    {
        "check_id": "foreign_date_format",
        "description": "MM/DD/YYYY where DD/MM/YYYY is expected",
        "pattern": re.compile(r"\bMM/DD/YYYY\b", re.IGNORECASE),
    },
    {
        "check_id": "nhs_or_nz_region",
        "description": "NHS or NZ-region leakage",
        "pattern": re.compile(r"\b(?:NHS|Auckland|Wellington|Canterbury|Otago)\b", re.IGNORECASE),
    },
]

PRIVACY_PATTERN = re.compile(r"\b(?:GDPR|CCPA)\b", re.IGNORECASE)
AU_PRIVACY_PATTERN = re.compile(r"\b(?:Privacy Act|Spam Act|AU Privacy Act)\b", re.IGNORECASE)


def _is_adversarial(prompt_metadata: Dict[str, Any]) -> bool:
    value = prompt_metadata.get("adversarial") or prompt_metadata.get("source_market_adaptation")
    return bool(value)


def _finding(
    *,
    check_id: str,
    description: str,
    scope: str,
    prompt_id: Optional[str],
    matched_text: str,
    section_id: Optional[str] = None,
    severity: str = "blocking",
) -> Dict[str, Any]:
    return {
        "check_id": check_id,
        "description": description,
        "scope": scope,
        "prompt_id": prompt_id,
        "section_id": section_id,
        "matched_text": matched_text,
        "severity": severity,
    }


def lint_context_sections(
    sections: Sequence[Dict[str, Any]],
    *,
    prompt_id: Optional[str] = None,
    prompt_metadata: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    if _is_adversarial(prompt_metadata or {}):
        return []

    findings: List[Dict[str, Any]] = []
    for section in sections:
        content = str(section.get("content") or "")
        section_id = str(section.get("section_id") or "")
        for check in CHECK_PATTERNS:
            for match in check["pattern"].finditer(content):
                findings.append(
                    _finding(
                        check_id=check["check_id"],
                        description=check["description"],
                        scope="prompt_context",
                        prompt_id=prompt_id,
                        section_id=section_id,
                        matched_text=match.group(0),
                    )
                )
        if PRIVACY_PATTERN.search(content) and not AU_PRIVACY_PATTERN.search(content):
            findings.append(
                _finding(
                    check_id="privacy_law_without_au_anchor",
                    description="GDPR/CCPA-only privacy wording where AU privacy wording is expected",
                    scope="prompt_context",
                    prompt_id=prompt_id,
                    section_id=section_id,
                    matched_text=PRIVACY_PATTERN.search(content).group(0),  # type: ignore[union-attr]
                )
            )
    return findings


def lint_generated_definition(
    definition: Any,
    *,
    prompt_id: str,
    prompt_metadata: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    if _is_adversarial(prompt_metadata or {}):
        return []
    content = json.dumps(definition or {}, sort_keys=True, default=str)
    findings: List[Dict[str, Any]] = []
    for check in CHECK_PATTERNS:
        for match in check["pattern"].finditer(content):
            findings.append(
                _finding(
                    check_id=check["check_id"],
                    description=check["description"],
                    scope="generated_definition",
                    prompt_id=prompt_id,
                    matched_text=match.group(0),
                )
            )
    if PRIVACY_PATTERN.search(content) and not AU_PRIVACY_PATTERN.search(content):
        findings.append(
            _finding(
                check_id="privacy_law_without_au_anchor",
                description="GDPR/CCPA-only privacy wording where AU privacy wording is expected",
                scope="generated_definition",
                prompt_id=prompt_id,
                matched_text=PRIVACY_PATTERN.search(content).group(0),  # type: ignore[union-attr]
            )
        )
    return findings


def _write_markdown(path: Path, title: str, findings: Sequence[Dict[str, Any]]) -> None:
    lines = [f"# {title}", ""]
    if not findings:
        lines.append("No deterministic AU findings.")
    else:
        for finding in findings:
            location = finding.get("section_id") or finding.get("prompt_id") or "run"
            lines.append(
                f"- **{finding['check_id']}** ({finding['severity']}) at `{location}`: "
                f"{finding['description']} matched `{finding['matched_text']}`"
            )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_diagnostic_artifacts(
    run_dir: Path,
    *,
    shared_context_bundle: Dict[str, Any],
    prompt_context_findings: Sequence[Dict[str, Any]],
    rows: Sequence[Dict[str, Any]],
) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    write_au_contract()
    (run_dir / "shared-context-bundle.json").write_text(
        _json_text(shared_context_bundle) + "\n",
        encoding="utf-8",
    )
    prompt_context_payload = {
        "schema_version": "prompt-context-lint-v1",
        "run_id": shared_context_bundle.get("run_id"),
        "finding_count": len(prompt_context_findings),
        "findings": list(prompt_context_findings),
    }
    (run_dir / "prompt-context-lint.json").write_text(
        _json_text(prompt_context_payload) + "\n",
        encoding="utf-8",
    )
    _write_markdown(run_dir / "prompt-context-lint.md", "Prompt Context Lint", prompt_context_findings)

    generated_findings = [
        finding
        for row in rows
        for finding in row.get("deterministic_au_findings", [])
    ]
    deterministic_payload = {
        "schema_version": "au-deterministic-checks-v1",
        "run_id": shared_context_bundle.get("run_id"),
        "au_locale_contract_version": AU_LOCALE_CONTRACT_VERSION,
        "prompt_context_finding_count": len(prompt_context_findings),
        "generated_output_finding_count": len(generated_findings),
        "findings": [*prompt_context_findings, *generated_findings],
    }
    (run_dir / "au-deterministic-checks.json").write_text(
        _json_text(deterministic_payload) + "\n",
        encoding="utf-8",
    )
    _write_markdown(
        run_dir / "au-deterministic-checks.md",
        "AU Deterministic Checks",
        deterministic_payload["findings"],
    )
