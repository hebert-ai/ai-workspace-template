#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "${ROOT_DIR}/projects"
mkdir -p "${ROOT_DIR}/templates"
mkdir -p "${ROOT_DIR}/scripts"
mkdir -p "${ROOT_DIR}/custom/agents"
mkdir -p "${ROOT_DIR}/custom/scripts"

if [[ ! -d "${ROOT_DIR}/venv" ]]; then
  python3 -m venv "${ROOT_DIR}/venv"
  echo "Created virtual environment at ${ROOT_DIR}/venv"
else
  echo "Virtual environment already exists at ${ROOT_DIR}/venv"
fi

echo "Workspace ready."
echo "Next: review AGENTS.md, WORKSPACE.md, and custom/AGENTS.md"
