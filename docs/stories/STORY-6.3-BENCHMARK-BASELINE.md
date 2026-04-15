# Story 6.3 — Benchmark quality baseline

**Purpose:** Record automated (mocked CI) and optional live-model results for the 10 benchmarks defined in `STORY-6.2-BENCHMARK-FORMS.md`.

| Benchmark | Title (short) | Automated result | Notes (dimensions / failures) |
|-----------|----------------|------------------|-------------------------------|
| 1 | Party RSVP | **Pass** | Harness: schema + type set + single page (`test_story_63_benchmark_harness.py` bm01) |
| 2 | Contact + address | **Pass** | bm02 |
| 3 | Event registration | **Pass** | bm03 |
| 4 | Job application | **Pass** | bm04 — `file-upload`, `url`, `terms` |
| 5 | Customer feedback | **Pass** | bm05 — dual `rating` |
| 6 | Merchandise order | **Pass** | bm06 — large `checkbox` option set |
| 7 | Newsletter minimal | **Pass** | bm07 — `paragraph` |
| 8 | Pre-order date/time | **Pass** | bm08 — `date` date + time modes |
| 9 | Support ticket | **Pass** | bm09 — dual `dropdown`, `file-upload` |
| 10 | Sales lead | **Pass** | bm10 — `rating`, `terms` |

**Run metadata**

| Field | Value |
|-------|--------|
| Git commit | `db51bb53e1a797c283274bb4d4566294a54fc337` (parent at doc fill; amend after Story 6.3 merge commit if policy requires exact SHA) |
| Date (UTC) | 2026-03-31 |
| Model / mode | `mocked-ci` |

**Scoring rubric reference:** See `STORY-6.2-BENCHMARK-FORMS.md` (Field Completeness, Layout Quality, Schema Validity, Prompt Fidelity, Visual Polish). Automated harness prioritizes **schema + structural** checks; human rubric optional post-UAT.

## Live UAT closeout note

- Automated mocked baseline remained green.
- Human UAT did not achieve satisfactory layout quality for story acceptance.
- Story 6.3 is closed as learning capture; see `STORY-6.3-CLOSEOUT-REPORT.md`.
