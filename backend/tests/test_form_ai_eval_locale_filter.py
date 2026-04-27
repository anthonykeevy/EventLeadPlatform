import json
import sys
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from form_ai_eval import run as eval_run  # type: ignore[import-not-found]  # noqa: E402


def test_locale_filter_slices_prompt_set_to_single_locale():
    prompt_set = eval_run.load_prompt_set()
    filtered = eval_run._filter_prompts_by_locale(prompt_set.prompts, "AU")

    assert len(filtered) == 45
    assert {prompt.audience_locale for prompt in filtered} == {"AU"}


def test_locale_filter_empty_match_exits():
    prompt_set = eval_run.load_prompt_set()

    with pytest.raises(SystemExit, match="No prompts matched --locale-filter=ZZ"):
        eval_run._filter_prompts_by_locale(prompt_set.prompts, "ZZ")


def test_locale_filter_run_writes_locale_slice_and_run_id(tmp_path):
    args = eval_run.parse_args(
        [
            "--mock",
            "--variant",
            "rubric-v2-baseline",
            "--locale-filter",
            "AU",
            "--output-root",
            str(tmp_path),
        ]
    )

    metadata = eval_run.run_harness(args)

    run_dir = tmp_path / "rubric-v2-baseline-AU"
    rows = [
        json.loads(line)
        for line in (run_dir / "metrics.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert metadata["run_id"] == "rubric-v2-baseline-AU"
    assert metadata["variant"] == "rubric-v2-baseline-AU"
    assert metadata["locale_filter"] == "AU"
    assert len(rows) == 45
    assert all(row["prompt_id"].split("-")[1] == "au" for row in rows)
