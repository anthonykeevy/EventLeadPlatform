"""
Pytest plugin: per-test timing logger.

Writes a line for each test at START and FINISH with wall-clock timestamps,
duration, and outcome. Output goes to a timestamped file under backend/test-logs/.

Activate via pytest.ini (addopts = -p tests.pytest_test_timing) or
command-line: pytest -p tests.pytest_test_timing

The log file is created fresh per session. Previous logs are preserved
(timestamped filenames prevent overwrite).
"""

import os
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest


LOG_DIR = Path(__file__).resolve().parent.parent / "test-logs"
_session_log_path: Path | None = None
_test_starts: dict[str, float] = {}


def _log(line: str) -> None:
    if _session_log_path is None:
        return
    with open(_session_log_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


# ── Session hooks ──────────────────────────────────────────────

def pytest_configure(config: pytest.Config) -> None:
    global _session_log_path
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    # Keep filename timestamps in UTC to match in-file log timestamps.
    stamp_utc = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")
    _session_log_path = LOG_DIR / f"test-timing-{stamp_utc}.log"


def pytest_sessionstart(session: pytest.Session) -> None:
    _log(f"SESSION_START | {_ts()} | pytest {pytest.__version__}")
    _log(f"{'-' * 100}")


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    _log(f"{'-' * 100}")
    _log(f"SESSION_END   | {_ts()} | exit_status={exitstatus}")

    _log("")
    _log("SUMMARY (slowest 20 tests):")
    _log(f"{'-' * 100}")

    # _test_starts entries that were never finished are potential hangs
    hung: list[str] = []

    for nodeid, start in _test_starts.items():
        # If still present, it means pytest_runtest_logreport never fired
        # with phase="call" for this test — possible hang.
        elapsed = time.monotonic() - start
        hung.append(f"  {elapsed:8.3f}s  {nodeid}")

    if hung:
        _log("  Potential hangs (started but never reached call-phase FINISH):")
        for entry in hung:
            _log(entry)
        _log(f"{'-' * 100}")

    # Ensure no stale state survives beyond this session.
    _test_starts.clear()

    if _session_log_path and _session_log_path.exists():
        # Parse durations from log lines for summary
        durations: list[tuple[str, float]] = []
        with open(_session_log_path, "r", encoding="utf-8") as f:
            for raw in f:
                if "FINISH" in raw and "duration=" in raw:
                    parts = raw.strip().split(" | ")
                    if len(parts) >= 4:
                        nodeid_part = parts[2].strip()
                        dur_part = [p for p in parts if p.strip().startswith("duration=")]
                        if dur_part:
                            try:
                                dur = float(dur_part[0].strip().split("=")[1].rstrip("s"))
                                durations.append((nodeid_part, dur))
                            except (ValueError, IndexError):
                                pass

        durations.sort(key=lambda x: x[1], reverse=True)
        for nodeid, dur in durations[:20]:
            _log(f"  {dur:8.3f}s  {nodeid}")

        total = sum(d for _, d in durations)
        _log(f"{'-' * 100}")
        _log(f"  Total test time: {total:.3f}s across {len(durations)} tests")


# ── Per-test hooks ─────────────────────────────────────────────

def pytest_runtest_logstart(nodeid: str, location: tuple) -> None:
    _test_starts[nodeid] = time.monotonic()
    _log(f"START         | {_ts()} | {nodeid}")


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    if report.when != "call":
        # Only log the main test phase, not setup/teardown
        if report.when == "setup" and report.failed:
            _test_starts.pop(report.nodeid, None)
            _log(f"SETUP_FAIL    | {_ts()} | {report.nodeid} | duration={report.duration:.3f}s | {_short_repr(report)}")
        elif report.when == "setup" and report.skipped:
            _test_starts.pop(report.nodeid, None)
            _log(f"SETUP_SKIP    | {_ts()} | {report.nodeid} | duration={report.duration:.3f}s")
        elif report.when == "setup" and report.passed:
            # Move tracking anchor to call-phase start. This avoids treating
            # setup-complete tests as hangs if call-phase reporting is disrupted.
            _test_starts[report.nodeid] = time.monotonic()
        elif report.when == "teardown":
            # Defensive cleanup: teardown reports can arrive even when call-phase
            # timing was not finalized due to upstream errors.
            _test_starts.pop(report.nodeid, None)
            if report.failed:
                _log(f"TEARDOWN_FAIL | {_ts()} | {report.nodeid} | duration={report.duration:.3f}s | {_short_repr(report)}")
        return

    start = _test_starts.pop(report.nodeid, None)
    wall = time.monotonic() - start if start is not None else report.duration

    outcome = report.outcome.upper()  # "passed", "failed", "skipped"
    _log(f"FINISH        | {_ts()} | {report.nodeid} | duration={wall:.3f}s | {outcome}")

    if report.failed:
        longrepr = _short_repr(report)
        if longrepr:
            _log(f"  FAILURE: {longrepr}")


def _short_repr(report: pytest.TestReport) -> str:
    """Extract a one-line failure summary."""
    if report.longrepr is None:
        return ""
    text = str(report.longrepr)
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if lines:
        return lines[-1][:200]
    return ""
