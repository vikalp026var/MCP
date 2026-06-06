#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Avoid --project so Connect uses fastmcp from .venv directly (no uv needed)
exec .venv/bin/fastmcp dev inspector main.py --no-reload
