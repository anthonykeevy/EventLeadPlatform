#!/usr/bin/env bash
set -euo pipefail
# Azure App Service on Linux reads WEBSITES_PORT or PORT when present.
PORT="${WEBSITES_PORT:-${PORT:-8000}}"
# Invoke the bundled antenv Python directly so we do NOT rely on Oryx auto-activating
# the venv (which only happens when SCM_DO_BUILD_DURING_DEPLOYMENT rebuilds it). The
# CI workflow always packages backend/antenv into the deploy, so /home/site/wwwroot/antenv
# is the deterministic interpreter for both Oryx-built and Oryx-skipped deploys.
exec antenv/bin/python -m uvicorn main:app --host "0.0.0.0" --port "${PORT}"
