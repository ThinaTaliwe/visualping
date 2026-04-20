#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is not installed. Install it first (e.g. sudo apt install python3 python3-venv)."
  exit 1
fi

if ! python3 -m venv --help >/dev/null 2>&1; then
  echo "python3-venv is missing. Install with: sudo apt install python3-venv"
  exit 1
fi

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .[dev]

echo "Bootstrap complete."
echo "Activate with: source .venv/bin/activate"
echo "Run app with: uvicorn app.main:app --reload"
