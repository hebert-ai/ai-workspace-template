# Repository Guidelines

## Purpose

This repository is a workspace instance created from a shared template. Use it for planning, organization, project bootstrap, and shared operating behavior. It is not the place to build or modify a specific product by default.

Read in order before substantial work:

1. `WORKSPACE.md`
2. `custom/AGENTS.md` if it exists and contains user-specific overrides
3. project-local agent files only after entering a project under `projects/`

When work becomes project-specific, switch to that project’s own directory and follow its local agent files such as `CLAUDE.md`, `GEMINI.md`, or `AGENTS.md`.

## Structure & Ownership

- `projects/`: local project directories; ignored by the root workspace repo
- `projects/<project>/`: the place for project-local guidance, code, and execution
- `custom/`: user-managed overrides and helper files that should survive template updates
- `custom/status/`: user-managed project inventory, prioritization, and status notes
- `venv/`: shared virtual environment for workspace-level scripts only
- `WORKSPACE.md`: shared operating rules for all agents
- `templates/`: reusable planning templates
- root `*.md` files: workspace-wide policy, planning, and coordination docs

Keep root-level content generic and reusable. Do not place app source or project-specific implementation notes at the root.

## Working Rules

- Use this directory for portfolio planning, task breakdowns, shared process docs, and templates
- Keep project tracking and prioritization notes under `custom/status/` so they stay user-managed
- Avoid implementing project code from this directory
- Treat each project under `projects/` as the source of truth for its own local conventions
- If a task targets one project, move into that project’s context before making detailed plans or edits
- Put user-specific customizations in `custom/` instead of editing template-managed root files
- Treat `projects/` as local workspace content that is not managed by the root repo

Example: planning a release calendar belongs here; changing `server.js` for one app does not.

## Commands

- `git status --short`: inspect workspace changes
- `find projects -maxdepth 2 -type f -name '*.md' | sort`: review project guidance files
- `sed -n '1,200p' WORKSPACE.md`: review the shared operating model
- `sed -n '1,200p' custom/AGENTS.md`: review user-specific overrides when present
- `python3 scripts/new-project.py "Project Name" "Initial goal"`: scaffold a local project
- `python3 scripts/clone-project.py git@github.com:example/example-repo.git`: clone and onboard an existing project locally
- `python3 scripts/onboard-project.py "project-slug"`: seed missing local project files into an existing project repo
- `python -m venv venv`: recreate the shared local virtual environment

## Style & Validation

Use concise Markdown with clear headings and actionable instructions. Prefer lowercase kebab-case for new doc filenames where practical.

Before submitting changes:

- verify paths and examples are valid
- keep root docs generic and template-managed in scope
- confirm project-specific rules stay inside the relevant project folder
- confirm user-specific preferences live under `custom/`
- confirm portfolio-tracking data remains user-managed under `custom/`

## Commits & Pull Requests

Use imperative commit subjects such as `Add workspace planning guidelines` or `Clarify project handoff rules`.

Pull requests should explain the workspace-level purpose of the change, list affected directories, and note whether any project-specific follow-up is required.
