from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import statistics
import sys
import time
from typing import List

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from modules.form_ai.service import generate_form_definition

OUTPUT_PATH = REPO_ROOT / "docs" / "stories" / "STORY-6.2-MODEL-COMPARISON.md"

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

MODELS = [
    "gpt-4o-mini",
    "gpt-4.1-mini",
    "gpt-5-mini",
    "gpt-4.1",
    "gpt-5",
    "gpt-5-pro",
]


@dataclass
class PromptRun:
    model: str
    prompt: str
    status: str
    attempts: int
    retries_used: int
    first_pass_valid: bool
    terminal_reason: str
    latency_ms: int


def _pct(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return (numerator / denominator) * 100.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Story 6.2 cross-model comparison")
    parser.add_argument(
        "--prompt-limit",
        type=int,
        default=10,
        help="Number of prompts to run from the standard set (default: 10).",
    )
    parser.add_argument(
        "--models",
        type=str,
        default=",".join(MODELS),
        help="Comma-separated model IDs. Defaults to Story 6.2 comparison set.",
    )
    args = parser.parse_args()

    selected_models = [m.strip() for m in args.models.split(",") if m.strip()]
    if not selected_models:
        raise ValueError("No models selected for comparison.")

    prompt_limit = max(1, min(len(PROMPTS), int(args.prompt_limit)))
    selected_prompts = PROMPTS[:prompt_limit]

    load_dotenv(REPO_ROOT / "backend" / ".env")
    started_at = datetime.now()
    runs: List[PromptRun] = []

    for model in selected_models:
        print(f"[story-6.2-compare] Running model: {model}")
        for index, prompt in enumerate(selected_prompts, start=1):
            print(f"  - prompt {index}/{len(selected_prompts)}")
            t0 = time.perf_counter()
            result = generate_form_definition(prompt, model_override=model)
            elapsed_ms = int((time.perf_counter() - t0) * 1000)

            first_pass_valid = (
                len(result.trace.attempts) > 0 and result.trace.attempts[0].validation.valid
            )
            runs.append(
                PromptRun(
                    model=model,
                    prompt=prompt,
                    status=result.status,
                    attempts=result.trace.attemptCount,
                    retries_used=result.trace.systemCorrectionAttemptsUsed,
                    first_pass_valid=first_pass_valid,
                    terminal_reason=result.trace.terminalReason,
                    latency_ms=elapsed_ms,
                )
            )

    lines: List[str] = []
    lines.append("# Story 6.2 Model Comparison")
    lines.append("")
    lines.append(f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- Prompt set size: {len(selected_prompts)}")
    lines.append(f"- Models compared: {', '.join(selected_models)}")
    lines.append("")
    lines.append("## Leaderboard")
    lines.append("")
    lines.append(
        "| Model | First-pass validity | Converged <=3 retries | Fail rate | Avg attempts | Avg retries | P95 latency (ms) |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|")

    model_order: List[tuple[str, float, float, float, float]] = []
    for model in selected_models:
        subset = [r for r in runs if r.model == model]
        total = len(subset)
        first_pass = sum(1 for r in subset if r.first_pass_valid)
        converged = sum(
            1 for r in subset if r.status == "completed" and r.retries_used <= 3
        )
        failed = sum(1 for r in subset if r.status != "completed")
        avg_attempts = statistics.mean([r.attempts for r in subset]) if subset else 0.0
        avg_retries = statistics.mean([r.retries_used for r in subset]) if subset else 0.0
        latencies = sorted([r.latency_ms for r in subset])
        p95_idx = max(0, min(len(latencies) - 1, int(round((len(latencies) - 1) * 0.95))))
        p95_latency = latencies[p95_idx] if latencies else 0

        first_pass_rate = _pct(first_pass, total)
        converged_rate = _pct(converged, total)
        fail_rate = _pct(failed, total)
        lines.append(
            f"| {model} | {first_pass_rate:.1f}% | {converged_rate:.1f}% | "
            f"{fail_rate:.1f}% | {avg_attempts:.2f} | {avg_retries:.2f} | {p95_latency} |"
        )
        model_order.append((model, first_pass_rate, converged_rate, fail_rate, avg_attempts))

    model_order.sort(key=lambda x: (-x[2], -x[1], x[3], x[4]))
    lines.append("")
    lines.append("## Ranked Recommendation")
    lines.append("")
    for index, (model, first_pass_rate, converged_rate, fail_rate, avg_attempts) in enumerate(
        model_order, start=1
    ):
        lines.append(
            f"{index}. `{model}` - convergence {converged_rate:.1f}%, "
            f"first-pass {first_pass_rate:.1f}%, fail {fail_rate:.1f}%, avg attempts {avg_attempts:.2f}"
        )

    lines.append("")
    lines.append("## Per-Prompt Results")
    lines.append("")
    lines.append(
        "| Model | Prompt | Status | Attempts | Retries | First-pass valid | Terminal reason | Latency (ms) |"
    )
    lines.append("|---|---|---|---:|---:|---|---|---:|")
    for run in runs:
        prompt_preview = run.prompt[:58] + ("..." if len(run.prompt) > 58 else "")
        lines.append(
            f"| {run.model} | {prompt_preview} | {run.status} | {run.attempts} | "
            f"{run.retries_used} | {'yes' if run.first_pass_valid else 'no'} | "
            f"{run.terminal_reason} | {run.latency_ms} |"
        )

    duration_minutes = (datetime.now() - started_at).total_seconds() / 60.0
    lines.append("")
    lines.append(f"- Total execution time: {duration_minutes:.1f} minutes")

    OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Model comparison written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
