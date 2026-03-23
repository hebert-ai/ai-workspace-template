# AI Workspace

This repository is a workspace instance created from the AI Workspace Template. Use it for planning, organizing, and bootstrapping local projects. Do not treat the root as the default place for project implementation.

## How To Use It

1. Clone this repo on a workstation.
2. Run `make setup`.
3. Read `AGENTS.md`, `WORKSPACE.md`, and `custom/AGENTS.md` if you use local overrides.
4. Create a project with `make new-project NAME="Project Name" GOAL="Initial goal"`.
5. Or clone and onboard an existing project with `python3 scripts/clone-project.py <repo-url>`.
6. Keep project-specific work inside `projects/<slug>/`.
7. When you switch into a project directory, use that project’s local agent files as the source of truth.

## What This Workspace Is For

This workspace root is the user’s cross-project management layer for AI-assisted work.

Use it to:

- review the status of multiple projects
- prioritize work across projects
- keep shared agent instructions and reusable templates
- maintain user-specific agent customizations under `custom/`
- bootstrap or clone project repos under `projects/`

Do not use the root as the main place to build a single product. Once work becomes project-specific, move into that project’s own repo under `projects/`.

## Key Files

- `AGENTS.md`: root contributor rules
- `WORKSPACE.md`: operating model and handoff rules
- `custom/`: user-managed overrides and helper files
- `custom/status/`: user-managed project inventory and priority notes
- `custom/status/projects.md`: starter project inventory
- `custom/status/priorities.md`: starter cross-project priorities
- `templates/project-starter/`: starter files for new projects
- `scripts/`: bootstrap, scaffold, and clone commands

Each project starter includes a local `ROADMAP.md` so project-specific milestones and backlog items have one default home.

## Common Commands

- `make setup`: prepare the local workspace
- `make new-project NAME="AirBnb Buddy" GOAL="Plan the MVP"`: scaffold a new project
- `python3 scripts/clone-project.py git@github.com:example/example-repo.git`: clone and onboard an existing project
- `make onboard-project SLUG="existing-project"`: seed missing local project files into an already cloned repo
- `make check`: validate workspace scripts
- `make handoff-project SLUG="airbnb-buddy"`: create `HANDOFF.md` in the project

## Layout Strategy

This workspace instance should contain shared policy, templates, local overrides, and lightweight automation. Real projects should live under `projects/`, and most of them should have their own Git repos.

The recommended model is:

- root: workspace instance created from the template
- `custom/`: user-managed customizations
- `custom/status/`: user-managed portfolio tracking and prioritization
- `projects/<slug>/`: real project directory, often its own repo

The root repo should ignore `projects/*` so local project repos do not pollute workspace updates. Avoid submodules unless you specifically need submodule behavior.

This workspace repo is intended to be the user’s own repo. The canonical template repo remains separate. Template improvements should flow into the workspace through explicit sync/migration, not by treating the user workspace as the template product repo.

## Practical Rule

Use the root to plan and initialize. Use `custom/` for local preferences. Use each project directory to execute.
