# AI Workspace Overview

This directory is a shared workspace for managing multiple projects at a high level. Its purpose is planning, coordination, documentation, and shared resources across projects.

Read `WORKSPACE.md` for the operating model and `custom/AGENTS.md` for local overrides when present.

## Scope

Use this directory for:

- cross-project planning
- shared process documentation
- reusable templates or notes
- organization of project folders under `projects/`

Do not treat this directory as the default place to build or edit a specific application. Project implementation should happen from the relevant project directory.

## Workspace Structure

- `projects/`: contains project-specific folders
- `projects/<project>/`: each project’s own docs, agent instructions, and specialized context
- `custom/`: user-managed overrides and helper files
- `venv/`: shared virtual environment for workspace-level utilities
- `WORKSPACE.md`: shared rules for how all agents should operate here
- `templates/`: reusable planning templates
- root Markdown files: workspace-wide guidance only

## Project Boundaries

Each project should maintain its own agent files and operating rules. When switching from high-level planning to project execution:

1. move into the target project directory
2. read that project’s local guidance files
3. keep implementation decisions and project-specific notes there
