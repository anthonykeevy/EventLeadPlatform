#!/usr/bin/env bash
set -euo pipefail
# Azure App Service on Linux reads WEBSITES_PORT or PORT when present.
PORT="${WEBSITES_PORT:-${PORT:-8000}}"
exec python -m uvicorn main:app --host "0.0.0.0" --port "${PORT}"
