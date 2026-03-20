from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import List, Tuple

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from modules.form_ai.service import CONTEXT_PACK_PATH, generate_form_definition

UAT_RESULTS_PATH = REPO_ROOT / "docs" / "stories" / "STORY-6.2-UAT-RESULTS.md"

PROMPTS = [
    "Build a contact form with full name, email, phone, and submit button.",
    "Create an event registration form with attendee name, email, company, and dietary preference dropdown.",
    "Generate a lead capture form for webinar signup with first name, last name, email, and consent checkbox.",
    "Create a support request form with subject, category dropdown, detailed message textarea, and contact email.",
    "Build a job application starter form with full name, email, phone, and available start date.",
    "Create a product demo request form with company name, role, email, phone, and submit button.",
    "Generate a feedback form with header, rating radio options, comments textarea, and submit button.",
    "Create a newsletter signup form with email, optional first name, consent checkbox, and submit button.",
    "Build a venue booking inquiry form with contact details, event date, expected attendee number, and notes.",
    "Generate an onboarding questionnaire with header, name, email, phone, preferred contact method, and submit.",
]


@dataclass
class PromptResult:
    prompt: str
    status: str
    first_attempt_valid: bool
    attempts: int
    retries_used: int
    terminal_reason: str
    usability_proxy: int
    manual_effort: str


def _manual_effort_label(status: str, retries_used: int) -> str:
    if status != "completed":
        return "high"
    if retries_used == 0:
        return "low"
    if retries_used == 1:
        return "med"
    return "high"


def _usability_proxy(status: str, attempts: int) -> int:
    if status != "completed":
        return 2
    if attempts == 1:
        return 5
    if attempts == 2:
        return 4
    if attempts == 3:
        return 3
    return 2


def _tighten_context_pack(cycle: int) -> str:
    marker = f"## Cycle {cycle} Quality Addendum"
    rule_block = (
        f"\n{marker}\n\n"
        "1. Keep exactly one page in `pages`.\n"
        "2. Prefer y-spacing >= 80 between stacked controls to reduce collisions.\n"
        "3. Keep x >= 20 and widths <= canvas width - 40.\n"
        "4. Always include `theme`, `canvasSettings`, and `schemaVersion`.\n"
    )
    current = CONTEXT_PACK_PATH.read_text(encoding="utf-8")
    if marker in current:
        return "addendum already present"
    CONTEXT_PACK_PATH.write_text(current + rule_block, encoding="utf-8")
    return "context pack tightened"


def run_cycle(cycle_number: int) -> Tuple[List[PromptResult], dict]:
    rows: List[PromptResult] = []
    for prompt in PROMPTS:
        response = generate_form_definition(prompt)
        first_attempt_valid = (
            bool(response.trace.attempts)
            and response.trace.attempts[0].validation.valid
        )
        attempts = response.trace.attemptCount
        retries_used = response.trace.systemCorrectionAttemptsUsed
        status = response.status
        usability_proxy = _usability_proxy(status=status, attempts=attempts)
        effort = _manual_effort_label(status=status, retries_used=retries_used)
        rows.append(
            PromptResult(
                prompt=prompt,
                status=status,
                first_attempt_valid=first_attempt_valid,
                attempts=attempts,
                retries_used=retries_used,
                terminal_reason=response.trace.terminalReason,
                usability_proxy=usability_proxy,
                manual_effort=effort,
            )
        )

    total = len(rows)
    first_pass = sum(1 for r in rows if r.first_attempt_valid)
    converged = sum(1 for r in rows if r.status == "completed")
    usable = sum(1 for r in rows if r.usability_proxy >= 4)
    low_or_med = sum(1 for r in rows if r.manual_effort in ("low", "med"))

    metrics = {
        "cycle": cycle_number,
        "structural_validity_rate": first_pass / total,
        "retry_convergence_rate": converged / total,
        "usability_rate": usable / total,
        "manual_effort_rate": low_or_med / total,
    }
    return rows, metrics


def format_percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def main() -> None:
    load_dotenv(REPO_ROOT / "backend" / ".env")
    cycle_sections: List[str] = []
    metrics_history: List[dict] = []
    consecutive_passes = 0

    for cycle in range(1, 4):
        rows, metrics = run_cycle(cycle)
        metrics_history.append(metrics)

        passed = (
            metrics["retry_convergence_rate"] >= 0.8
            and metrics["usability_rate"] >= 0.7
            and metrics["manual_effort_rate"] >= 0.8
        )
        consecutive_passes = consecutive_passes + 1 if passed else 0

        table_lines = [
            "| Prompt | Status | First-pass valid | Attempts | Retries | Usability proxy | Manual effort |",
            "|---|---|---|---:|---:|---:|---|",
        ]
        for row in rows:
            table_lines.append(
                "| "
                + f"{row.prompt[:58]}... | {row.status} | "
                + f"{'yes' if row.first_attempt_valid else 'no'} | {row.attempts} | "
                + f"{row.retries_used} | {row.usability_proxy}/5 | {row.manual_effort} |"
            )

        cycle_notes = [
            f"- Structural validity rate: {format_percent(metrics['structural_validity_rate'])}",
            f"- Retry convergence rate (<=3): {format_percent(metrics['retry_convergence_rate'])}",
            f"- Human usability proxy (>=4/5): {format_percent(metrics['usability_rate'])}",
            f"- Manual correction effort low/med: {format_percent(metrics['manual_effort_rate'])}",
        ]

        adjustment = "none"
        if not passed and cycle < 3:
            adjustment = _tighten_context_pack(cycle)
            cycle_notes.append(f"- Context-pack update: {adjustment}")
        else:
            cycle_notes.append("- Context-pack update: none")

        cycle_sections.append(
            f"## Cycle {cycle}\n\n"
            + "\n".join(cycle_notes)
            + "\n\n"
            + "\n".join(table_lines)
            + "\n"
        )

        if consecutive_passes >= 2:
            break

    final_status = (
        "accepted (two consecutive passing cycles)"
        if consecutive_passes >= 2
        else "max cycles reached; manual follow-up recommended"
    )
    summary = [
        "# Story 6.2 UAT Results",
        "",
        "## Prompt Quality Evaluation Loop",
        f"- Prompt set size: {len(PROMPTS)}",
        f"- Cycles executed: {len(metrics_history)}",
        f"- Outcome: {final_status}",
        "",
        "### Cycle Metrics Overview",
        "",
        "| Cycle | Structural validity | Retry convergence | Usability proxy >=4/5 | Manual effort low/med |",
        "|---:|---:|---:|---:|---:|",
    ]
    for metric in metrics_history:
        summary.append(
            "| "
            + f"{metric['cycle']} | "
            + f"{format_percent(metric['structural_validity_rate'])} | "
            + f"{format_percent(metric['retry_convergence_rate'])} | "
            + f"{format_percent(metric['usability_rate'])} | "
            + f"{format_percent(metric['manual_effort_rate'])} |"
        )

    content = "\n".join(summary) + "\n\n" + "\n\n".join(cycle_sections).strip() + "\n"
    UAT_RESULTS_PATH.write_text(content, encoding="utf-8")
    print(content)


if __name__ == "__main__":
    main()
