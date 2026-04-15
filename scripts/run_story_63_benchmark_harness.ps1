# Story 6.3: run all 10 benchmark cases (mocked LLM) in one pytest session.
# Optional: install pytest-xdist (pip install pytest-xdist) then use -n auto for parallel workers.
# For live OpenAI smoke tests across all prompts, use a separate integration script — this harness stays fast and deterministic.

$ErrorActionPreference = "Stop"
$backend = Join-Path $PSScriptRoot ".." "backend"
Set-Location $backend

$parallel = $args -contains "-Parallel"
if ($parallel) {
    python -m pytest tests/test_story_63_benchmark_harness.py -v --tb=short -n auto
} else {
    python -m pytest tests/test_story_63_benchmark_harness.py -v --tb=short
}
exit $LASTEXITCODE
