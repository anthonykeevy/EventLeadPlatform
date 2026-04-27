"""Dependency-free statistics helpers for Form AI eval comparisons."""

from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import mean, variance
from typing import Iterable, Literal, Optional

MetricKind = Literal["continuous", "binary"]


@dataclass(frozen=True)
class StatResult:
    status: Literal["ok", "inconclusive"]
    statistic: Optional[float] = None
    p_value: Optional[float] = None
    degrees_of_freedom: Optional[float] = None
    effect_size: Optional[float] = None
    note: str = ""

    @property
    def odds_ratio(self) -> Optional[float]:
        return self.statistic


def _as_floats(values: Iterable[float]) -> list[float]:
    return [float(value) for value in values]


def _student_t_pdf(x_value: float, degrees_of_freedom: float) -> float:
    log_coeff = (
        math.lgamma((degrees_of_freedom + 1.0) / 2.0)
        - math.lgamma(degrees_of_freedom / 2.0)
        - 0.5 * math.log(degrees_of_freedom * math.pi)
    )
    exponent = -((degrees_of_freedom + 1.0) / 2.0) * math.log1p(
        (x_value * x_value) / degrees_of_freedom
    )
    return math.exp(log_coeff + exponent)


def _student_t_two_sided_p(abs_t: float, degrees_of_freedom: float) -> float:
    if abs_t <= 0:
        return 1.0
    if abs_t > 40:
        return 0.0

    intervals = max(200, int(abs_t * 200))
    if intervals % 2:
        intervals += 1
    step = abs_t / intervals
    total = _student_t_pdf(0.0, degrees_of_freedom) + _student_t_pdf(abs_t, degrees_of_freedom)
    for index in range(1, intervals):
        coefficient = 4 if index % 2 else 2
        total += coefficient * _student_t_pdf(index * step, degrees_of_freedom)
    area = total * step / 3.0
    tail = max(0.0, 0.5 - area)
    return min(1.0, 2.0 * tail)


def welch_t_test(baseline_values: Iterable[float], variant_values: Iterable[float]) -> StatResult:
    baseline = _as_floats(baseline_values)
    variant = _as_floats(variant_values)
    if len(baseline) < 2 or len(variant) < 2:
        return StatResult(status="inconclusive", note="Welch t-test requires at least two samples per group.")

    baseline_variance = variance(baseline)
    variant_variance = variance(variant)
    baseline_term = baseline_variance / len(baseline)
    variant_term = variant_variance / len(variant)
    denominator = math.sqrt(baseline_term + variant_term)
    if denominator == 0:
        return StatResult(status="inconclusive", note="Welch t-test undefined for zero combined variance.")

    statistic = (mean(baseline) - mean(variant)) / denominator
    df_denominator = 0.0
    if baseline_term:
        df_denominator += (baseline_term * baseline_term) / (len(baseline) - 1)
    if variant_term:
        df_denominator += (variant_term * variant_term) / (len(variant) - 1)
    if df_denominator == 0:
        return StatResult(status="inconclusive", note="Welch degrees of freedom undefined.")

    degrees_of_freedom = ((baseline_term + variant_term) ** 2) / df_denominator
    p_value = _student_t_two_sided_p(abs(statistic), degrees_of_freedom)
    return StatResult(
        status="ok",
        statistic=statistic,
        p_value=p_value,
        degrees_of_freedom=degrees_of_freedom,
    )


def cohens_d(baseline_values: Iterable[float], variant_values: Iterable[float]) -> StatResult:
    baseline = _as_floats(baseline_values)
    variant = _as_floats(variant_values)
    if len(baseline) < 2 or len(variant) < 2:
        return StatResult(status="inconclusive", note="Cohen's d requires at least two samples per group.")

    baseline_variance = variance(baseline)
    variant_variance = variance(variant)
    pooled_denominator = len(baseline) + len(variant) - 2
    if pooled_denominator <= 0:
        return StatResult(status="inconclusive", note="Cohen's d pooled variance is undefined.")
    pooled_variance = (
        ((len(baseline) - 1) * baseline_variance)
        + ((len(variant) - 1) * variant_variance)
    ) / pooled_denominator
    if pooled_variance <= 0:
        return StatResult(status="inconclusive", note="Cohen's d undefined for zero pooled variance.")

    effect_size = (mean(baseline) - mean(variant)) / math.sqrt(pooled_variance)
    return StatResult(status="ok", effect_size=effect_size)


def _hypergeom_probability(successes_in_baseline: int, baseline_total: int, success_total: int, total: int) -> float:
    return (
        math.comb(success_total, successes_in_baseline)
        * math.comb(total - success_total, baseline_total - successes_in_baseline)
        / math.comb(total, baseline_total)
    )


def fisher_exact(
    *,
    baseline_successes: int,
    baseline_failures: int,
    variant_successes: int,
    variant_failures: int,
) -> StatResult:
    values = [baseline_successes, baseline_failures, variant_successes, variant_failures]
    if any(value < 0 for value in values):
        return StatResult(status="inconclusive", note="Fisher exact counts cannot be negative.")
    total = sum(values)
    if total == 0:
        return StatResult(status="inconclusive", note="Fisher exact requires at least one observation.")

    baseline_total = baseline_successes + baseline_failures
    variant_total = variant_successes + variant_failures
    success_total = baseline_successes + variant_successes
    if baseline_total == 0 or variant_total == 0:
        return StatResult(status="inconclusive", note="Fisher exact requires observations in both groups.")

    observed = _hypergeom_probability(baseline_successes, baseline_total, success_total, total)
    lower = max(0, baseline_total - (total - success_total))
    upper = min(baseline_total, success_total)
    p_value = sum(
        probability
        for probability in (
            _hypergeom_probability(candidate, baseline_total, success_total, total)
            for candidate in range(lower, upper + 1)
        )
        if probability <= observed + 1e-12
    )
    odds_ratio = (
        math.inf
        if baseline_failures == 0 and variant_failures > 0
        else 0.0
        if variant_failures == 0 and baseline_failures > 0
        else (baseline_successes * variant_failures) / (baseline_failures * variant_successes)
        if baseline_failures and variant_successes
        else None
    )
    return StatResult(status="ok", statistic=odds_ratio, p_value=min(1.0, p_value), note="two-sided Fisher exact")


def verdict_for_metric(
    *,
    metric_name: str,
    baseline_values: Iterable[float],
    variant_values: Iterable[float],
    metric_kind: MetricKind,
    category: str,
    alpha: float = 0.05,
    effect_threshold: float = 0.3,
    higher_is_better: bool = True,
) -> dict[str, object]:
    baseline = _as_floats(baseline_values)
    variant = _as_floats(variant_values)
    if metric_kind == "binary":
        result = fisher_exact(
            baseline_successes=sum(1 for value in baseline if bool(value)),
            baseline_failures=sum(1 for value in baseline if not bool(value)),
            variant_successes=sum(1 for value in variant if bool(value)),
            variant_failures=sum(1 for value in variant if not bool(value)),
        )
        effect = None
    else:
        result = welch_t_test(baseline, variant)
        effect_result = cohens_d(baseline, variant)
        effect = effect_result.effect_size if effect_result.status == "ok" else None

    baseline_mean = mean(baseline) if baseline else None
    variant_mean = mean(variant) if variant else None
    delta = None if baseline_mean is None or variant_mean is None else variant_mean - baseline_mean
    if result.status != "ok" or result.p_value is None:
        decision = "inconclusive"
    elif result.p_value >= alpha:
        decision = "inconclusive"
    else:
        improved = (delta or 0.0) > 0 if higher_is_better else (delta or 0.0) < 0
        strong_effect = effect is None or abs(effect) >= effect_threshold
        decision = "win" if improved and strong_effect else "regression" if not improved else "advisory"

    return {
        "metric_name": metric_name,
        "metric_kind": metric_kind,
        "category": category,
        "baseline_mean": baseline_mean,
        "variant_mean": variant_mean,
        "delta": delta,
        "p_value": result.p_value,
        "effect_size": effect,
        "decision": decision,
        "recommended_action": "rerun-at-n15"
        if category == "B" and decision == "inconclusive" and (result.p_value is None or result.p_value >= alpha)
        else "human-review",
        "note": result.note,
    }
