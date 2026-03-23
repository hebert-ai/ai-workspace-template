#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "${ROOT_DIR}/projects"
mkdir -p "${ROOT_DIR}/templates"
mkdir -p "${ROOT_DIR}/scripts"
mkdir -p "${ROOT_DIR}/custom/agents"
mkdir -p "${ROOT_DIR}/custom/status"
mkdir -p "${ROOT_DIR}/custom/scripts"

if [[ ! -f "${ROOT_DIR}/custom/status/README.md" ]]; then
  cat > "${ROOT_DIR}/custom/status/README.md" <<'EOF'
# Project Status

Use this directory for user-managed portfolio tracking across projects.

Suggested contents:

- `projects.md` for a project inventory
- `priorities.md` for current focus and ordering
- active work queues
- weekly or milestone status notes
- cross-project blockers and dependencies

This directory is seeded by bootstrap but is not part of template sync. Keep the structure that fits your workflow.
EOF
  echo "Seeded custom/status/README.md"
fi

if [[ ! -f "${ROOT_DIR}/custom/status/projects.md" ]]; then
  cat > "${ROOT_DIR}/custom/status/projects.md" <<'EOF'
# Project Inventory

Use this file to track the projects in this workspace at a glance.

Suggested fields:

| Project | Slug | Repo | Status | Priority | Next Step |
| --- | --- | --- | --- | --- | --- |
| Example Project | `example-project` | `git@github.com:example/example-project.git` | active | high | clarify next milestone |

Notes:

- keep this file user-managed
- add or remove fields to fit your workflow
- treat this as a workspace overview, not a replacement for project-local planning
EOF
  echo "Seeded custom/status/projects.md"
fi

if [[ ! -f "${ROOT_DIR}/custom/status/priorities.md" ]]; then
  cat > "${ROOT_DIR}/custom/status/priorities.md" <<'EOF'
# Priorities

Use this file to track the current order of work across projects.

## Current Focus

- Example Project: clarify the next milestone

## Waiting

- Example Project: waiting on external feedback

## Backlog

- Example Project: evaluate follow-up ideas

Keep this file lightweight. The root workspace should help coordinate across projects, while detailed execution planning stays inside each project repo.
EOF
  echo "Seeded custom/status/priorities.md"
fi

if [[ ! -d "${ROOT_DIR}/venv" ]]; then
  python3 -m venv "${ROOT_DIR}/venv"
  echo "Created virtual environment at ${ROOT_DIR}/venv"
else
  echo "Virtual environment already exists at ${ROOT_DIR}/venv"
fi

echo "Workspace ready."
echo "Next: review AGENTS.md, WORKSPACE.md, and custom/AGENTS.md"
