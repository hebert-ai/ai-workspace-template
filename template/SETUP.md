# Workspace Setup

## Purpose

This repository is a portable workspace instance for planning, project bootstrap, and shared coordination. Clone it on any workstation, run the setup script, and keep project-specific implementation inside `projects/<name>/`.

## Quick Start

1. Clone the repository.
2. Run `bash scripts/setup-workspace.sh`.
3. Review `AGENTS.md`, `WORKSPACE.md`, and `custom/AGENTS.md` if you use local overrides.
4. Create a new project with `make new-project NAME="Project Name" GOAL="Initial goal"` or `python3 scripts/new-project.py "Project Name" "Initial goal"`.
5. Or clone and onboard an existing project with `python3 scripts/clone-project.py <repo-url>`.

## What Setup Does

- creates `venv/` if it does not exist
- ensures `projects/`, `templates/`, and `scripts/` are present
- ensures `custom/` subdirectories are present
- seeds `custom/status/` for user-managed portfolio tracking when missing
- seeds starter files for project inventory and priorities under `custom/status/` when missing
- leaves project-specific implementation to project folders
- provides reproducible commands through `Makefile`

## What Not To Commit

- `venv/`
- `.env` files
- logs, caches, and other machine-specific state
- `.workspace-template/` sync state

## Recommended Workflow

- use the root for planning, decisions, and bootstrapping
- keep project inventory and priorities under `custom/status/`
- use `projects/<slug>/` for project-local docs and implementation
- use `custom/` for user-specific overrides and helper files
- use `HANDOFF.md` inside a project when context needs to move cleanly between agents or sessions
