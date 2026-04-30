"""Analyst experiment orchestrator for Form AI eval runs.

The config is JSON-shaped YAML, matching the prompt files, so the backend test
environment does not need a YAML dependency.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

TESTS_DIR = Path(__file__).resolve().parents[1]
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from form_ai_eval import diff, judge_pack, run as eval_run  # type: ignore[import-not-found]  # noqa: E402


class ExperimentConfigError(RuntimeError):
    """Raised when an Analyst experiment config cannot be executed."""


def _utc_now_text() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _read_json_config(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ExperimentConfigError(
            f"{path} must be JSON-shaped YAML for dependency-free loading: {exc}"
        ) from exc
    if not isinstance(payload, dict):
        raise ExperimentConfigError("Experiment config must be a JSON object")
    return payload


def _resolve_path(value: Any, *, config_dir: Path, default: Optional[Path] = None) -> Path:
    if value in (None, ""):
        if default is None:
            raise ExperimentConfigError("Missing required path value")
        return default
    path = Path(str(value))
    if not path.is_absolute():
        candidate = config_dir / path
        path = candidate if candidate.exists() else path
    return path


def _resolve_run_dir(value: str, *, output_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute() or path.exists():
        return path
    return output_root / value


def _candidate_addendum(candidate: Dict[str, Any], *, config_dir: Path) -> str:
    inline = (
        candidate.get("system_prompt_addendum")
        or candidate.get("prompt_context_text")
        or candidate.get("candidate_prompt_text")
    )
    file_value = (
        candidate.get("system_prompt_addendum_file")
        or candidate.get("prompt_context_file")
        or candidate.get("candidate_prompt_file")
    )
    if inline and file_value:
        raise ExperimentConfigError(
            f"{candidate.get('label', '<candidate>')}: use inline text or file, not both"
        )
    if file_value:
        path = _resolve_path(file_value, config_dir=config_dir)
        return path.read_text(encoding="utf-8").strip()
    return str(inline or "").strip()


def _validate_config(config: Dict[str, Any]) -> None:
    required = {"experiment_id", "baseline_run_id", "improvement_goal", "candidates"}
    missing = sorted(required - set(config))
    if missing:
        raise ExperimentConfigError(f"Experiment config missing required fields: {missing}")
    candidates = config.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise ExperimentConfigError("Experiment config must include at least one candidate")
    if len(candidates) > 3:
        raise ExperimentConfigError("Analyst experiments support at most three candidates")
    seen_labels: set[str] = set()
    for index, candidate in enumerate(candidates, start=1):
        if not isinstance(candidate, dict):
            raise ExperimentConfigError(f"Candidate {index} must be an object")
        label = str(candidate.get("label") or "").strip()
        if not label:
            raise ExperimentConfigError(f"Candidate {index} missing label")
        if label in seen_labels:
            raise ExperimentConfigError(f"Duplicate candidate label: {label}")
        seen_labels.add(label)


def _resolve_prompt_ids(config: Dict[str, Any], prompts_path: Path) -> List[str]:
    explicit = [str(value) for value in (config.get("prompt_ids") or [])]
    if explicit:
        return explicit
    scenario_slice = str(config.get("scenario_slice") or "all").strip().lower()
    if scenario_slice in {"all", "au-all"}:
        return []
    prompt_set = eval_run.load_prompt_set(prompts_path)
    if scenario_slice in {"neutral", "au-neutral"}:
        return [prompt.prompt_id for prompt in prompt_set.prompts if prompt.variant == "neutral"]
    if scenario_slice in {"ambiguous", "au-ambiguous"}:
        return [prompt.prompt_id for prompt in prompt_set.prompts if prompt.variant == "ambiguous"]
    if scenario_slice in {"adversarial", "au-adversarial"}:
        return [prompt.prompt_id for prompt in prompt_set.prompts if prompt.variant == "adversarial"]
    raise ExperimentConfigError(
        "Unknown scenario_slice. Supported values: all, au-all, au-neutral, "
        "au-ambiguous, au-adversarial"
    )


def _tracking_payload(
    *,
    config: Dict[str, Any],
    experiment_dir: Path,
    candidate_summaries: List[Dict[str, Any]],
) -> Dict[str, Any]:
    return {
        "schema_version": "form-ai-eval-analyst-tracking-row-v1",
        "generated_at_utc": _utc_now_text(),
        "experiment_id": config["experiment_id"],
        "baseline_run_id": config["baseline_run_id"],
        "improvement_goal": config["improvement_goal"],
        "target_metrics": list(config.get("target_metrics") or []),
        "scenario_slice": config.get("scenario_slice") or "explicit-prompt-ids",
        "selected_prompt_ids": list(config.get("resolved_prompt_ids") or []),
        "candidate_count": len(candidate_summaries),
        "candidate_runs": candidate_summaries,
        "evidence_folder": str(experiment_dir),
        "suggested_tracking_status": "Pending judge sessions and candidate comparison review",
    }


def _write_tracking_markdown(path: Path, payload: Dict[str, Any]) -> None:
    lines = [
        "# Analyst Experiment Tracking Payload",
        "",
        f"- Experiment: `{payload['experiment_id']}`",
        f"- Baseline: `{payload['baseline_run_id']}`",
        f"- Goal: {payload['improvement_goal']}",
        f"- Target metrics: `{', '.join(payload['target_metrics'])}`",
        f"- Status: {payload['suggested_tracking_status']}",
        "",
        "## Candidate Runs",
        "",
    ]
    for candidate in payload["candidate_runs"]:
        lines.append(
            f"- `{candidate['candidate_label']}`: run `{candidate['run_id']}`, "
            f"judge package `{candidate['judge_package_dir']}`"
        )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def run_experiment(config_path: Path) -> Dict[str, Any]:
    config_path = Path(config_path)
    config = _read_json_config(config_path)
    _validate_config(config)
    config_dir = config_path.parent

    experiment_id = str(config["experiment_id"]).strip()
    output_root = _resolve_path(
        config.get("output_root"),
        config_dir=config_dir,
        default=eval_run.DEFAULT_OUTPUT_ROOT,
    )
    experiment_dir = output_root / experiment_id
    baseline_run = _resolve_run_dir(str(config["baseline_run_id"]), output_root=output_root)
    prompts_path = _resolve_path(
        config.get("prompts_path"),
        config_dir=config_dir,
        default=eval_run.DEFAULT_AU_PROMPTS_PATH,
    )
    prompt_ids = _resolve_prompt_ids(config, prompts_path)
    config["resolved_prompt_ids"] = prompt_ids
    target_metrics = [str(value) for value in (config.get("target_metrics") or [])]
    mock = bool(config.get("mock", False))
    allow_au_context_conflicts = bool(config.get("allow_au_context_conflicts", False))
    repetitions = int(config.get("repetitions", 1))
    concurrency = int(config.get("concurrency", eval_run.MAX_CONCURRENCY))
    max_cost_usd = config.get("max_cost_usd")

    experiment_dir.mkdir(parents=True, exist_ok=True)
    candidate_summaries: List[Dict[str, Any]] = []
    for candidate in config["candidates"]:
        label = str(candidate["label"]).strip()
        run_id = str(candidate.get("run_id") or label).strip()
        addendum = _candidate_addendum(candidate, config_dir=config_dir)
        changed_section_id = str(candidate.get("changed_section_id") or "candidate_prompt_block")
        experiment_metadata = {
            "experiment_id": experiment_id,
            "baseline_run_id": str(config["baseline_run_id"]),
            "improvement_goal": str(config["improvement_goal"]),
            "target_metrics": target_metrics,
            "scenario_slice": config.get("scenario_slice") or "explicit-prompt-ids",
            "selected_prompt_ids": prompt_ids,
            "candidate_label": label,
            "candidate_hypothesis": str(candidate.get("hypothesis") or ""),
            "changed_section_id": changed_section_id,
            "expected_metric_movement": candidate.get("expected_metric_movement"),
            "known_risk_metrics": list(candidate.get("known_risk_metrics") or []),
            "eval_only": True,
            "system_prompt_addendum_hash": _hash_text(addendum) if addendum else None,
        }

        argv = [
            "--prompts-path",
            str(prompts_path),
            "--variant",
            experiment_id,
            "--hypothesis-code",
            str(config["improvement_goal"]),
            "--variant-label",
            label,
            "--run-id",
            run_id,
            "--output-root",
            str(experiment_dir),
            "--repetitions",
            str(repetitions),
            "--concurrency",
            str(concurrency),
            "--system-prompt-addendum",
            addendum,
        ]
        if max_cost_usd is not None:
            argv.extend(["--max-cost-usd", str(max_cost_usd)])
        if mock:
            argv.append("--mock")
        if allow_au_context_conflicts:
            argv.append("--allow-au-context-conflicts")
        for prompt_id in prompt_ids:
            argv.extend(["--prompt-id", prompt_id])

        args = eval_run.parse_args(argv)
        args.experiment_metadata = experiment_metadata
        metadata = eval_run.run_harness(args)
        candidate_run_dir = experiment_dir / run_id
        package_dir = judge_pack.write_judge_package(
            candidate_run_dir,
            prompts_path=prompts_path,
        )

        diff_dir: Optional[Path] = None
        if baseline_run.exists():
            diff_dir = experiment_dir / "diffs" / label
            diff.compare_runs(baseline_run, candidate_run_dir, diff_dir)

        candidate_summaries.append(
            {
                "candidate_label": label,
                "run_id": metadata["run_id"],
                "run_dir": str(candidate_run_dir),
                "judge_package_dir": str(package_dir),
                "judge_input_batch": str(package_dir / "judge-input-batch.md"),
                "diff_dir": str(diff_dir) if diff_dir is not None else None,
                "status": metadata["status"],
                "completed_count": metadata["completed_count"],
                "system_prompt_addendum_hash": experiment_metadata["system_prompt_addendum_hash"],
            }
        )

    tracking = _tracking_payload(
        config=config,
        experiment_dir=experiment_dir,
        candidate_summaries=candidate_summaries,
    )
    summary = {
        "schema_version": "form-ai-eval-analyst-experiment-summary-v1",
        "generated_at_utc": _utc_now_text(),
        "config_path": str(config_path),
        "experiment_dir": str(experiment_dir),
        "baseline_run_dir": str(baseline_run),
        "candidate_runs": candidate_summaries,
        "tracking_payload": tracking,
    }
    (experiment_dir / "experiment-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    (experiment_dir / "tracking-row-payload.json").write_text(
        json.dumps(tracking, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    _write_tracking_markdown(experiment_dir / "tracking-row-payload.md", tracking)
    return summary


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run an Analyst Form AI eval experiment.")
    parser.add_argument("config", type=Path)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    summary = run_experiment(args.config)
    print(json.dumps(summary, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
