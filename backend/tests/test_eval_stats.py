import math
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from form_ai_eval import stats  # type: ignore[import-not-found]  # noqa: E402


def test_welch_t_test_detects_known_difference():
    result = stats.welch_t_test([10, 11, 12, 13, 14], [20, 21, 22, 23, 24])

    assert result.status == "ok"
    assert result.statistic < 0
    assert result.p_value is not None and result.p_value < 0.001
    assert result.degrees_of_freedom is not None


def test_cohens_d_direction_and_magnitude():
    result = stats.cohens_d([4, 5, 6], [6, 7, 8])

    assert result.status == "ok"
    assert result.effect_size is not None
    assert math.isclose(result.effect_size, -2.0, rel_tol=0.01)


def test_fisher_exact_detects_binary_regression():
    result = stats.fisher_exact(
        baseline_successes=10,
        baseline_failures=0,
        variant_successes=7,
        variant_failures=3,
    )

    assert result.status == "ok"
    assert result.p_value is not None
    assert 0 < result.p_value < 1
    assert result.odds_ratio == math.inf


def test_tiny_and_zero_variance_samples_are_inconclusive():
    tiny = stats.welch_t_test([1], [2, 3])
    zero_variance = stats.welch_t_test([5, 5, 5], [6, 6, 6])
    effect = stats.cohens_d([5, 5, 5], [5, 5, 5])

    assert tiny.status == "inconclusive"
    assert zero_variance.status == "inconclusive"
    assert effect.status == "inconclusive"


def test_verdict_helper_recommends_auto_rerun_for_inconclusive_category_b():
    verdict = stats.verdict_for_metric(
        metric_name="field_coverage_recall",
        baseline_values=[4.0, 4.2, 3.8],
        variant_values=[4.1, 4.0, 3.9],
        metric_kind="continuous",
        category="B",
    )

    assert verdict["decision"] == "inconclusive"
    assert verdict["recommended_action"] == "rerun-at-n15"


def test_verdict_helper_recommends_auto_rerun_when_p_value_equals_alpha(monkeypatch):
    monkeypatch.setattr(
        stats,
        "welch_t_test",
        lambda baseline_values, variant_values: stats.StatResult(
            status="ok",
            statistic=1.0,
            p_value=0.05,
            degrees_of_freedom=10.0,
            note="forced alpha boundary",
        ),
    )
    monkeypatch.setattr(
        stats,
        "cohens_d",
        lambda baseline_values, variant_values: stats.StatResult(
            status="ok",
            effect_size=0.0,
            note="forced alpha boundary",
        ),
    )

    verdict = stats.verdict_for_metric(
        metric_name="field_coverage_recall",
        baseline_values=[4.0, 4.0],
        variant_values=[4.0, 4.0],
        metric_kind="continuous",
        category="B",
        alpha=0.05,
    )

    assert verdict["decision"] == "inconclusive"
    assert verdict["p_value"] == 0.05
    assert verdict["recommended_action"] == "rerun-at-n15"
