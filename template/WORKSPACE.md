# Workspace Operating Model

## Purpose

This directory is a workspace instance created from the shared template. Use it for planning, organization, reusable documentation, project bootstrap, and cross-project decisions.

This is not the default place for project implementation, but it is the correct place to initiate new projects and create their starting structure under `projects/`.

## Read Order

Before doing meaningful work from this directory:

1. read `AGENTS.md`
2. read this file
3. read `custom/AGENTS.md` if present
4. read any relevant project-local docs only if the task clearly targets that project

## What Belongs Here

- roadmap planning
- project intake and prioritization
- user-maintained portfolio status tracking across projects
- creation of new project folders and starter agent files
- cloning and onboarding existing project repos into `projects/`
- shared templates and checklists
- user-specific overrides under `custom/`
- lightweight scripts that bootstrap or scaffold the workspace

## What Does Not Belong Here

- feature implementation for a single project
- project-specific bug fixing
- app-local architecture notes that only matter inside one repo
- project build artifacts or assets

## Handoff Rule

If a task becomes specific to one project, move into `projects/<project>/` and use that project’s local guidance files as the source of truth.

Example:

- root: define release sequencing across projects
- root: create `projects/<project>/` and its starter docs
- project folder: change a route, schema, scene, component, or test

## New Project Bootstrap Rule

When asked to start a new project from the root workspace:

1. create `projects/<project-slug>/`
2. create the project’s local agent files from `templates/project-starter/`
3. fill in the project name, directory, and initial goal
4. ensure the new project files reference shared root guidance such as `../../WORKSPACE.md`
5. prefer `make new-project` or `python3 scripts/new-project.py` over manual scaffolding

Suggested slug format: lowercase kebab-case, for example `AirBnb Buddy` -> `airbnb-buddy`.

## Existing Project Onboarding Rule

When asked to bring an existing repo into the workspace:

1. clone the repo into `projects/<project-slug>/`
2. seed missing local project files from `templates/project-starter/`
3. never overwrite existing project files automatically during onboarding
4. prefer `python3 scripts/clone-project.py <repo-url>` or `make onboard-project SLUG="<project-slug>"` over manual copying

## GitHub Preparation Rule

When a project repo should be prepared for GitHub publication or more formal collaboration:

1. use `make prepare-project-repo SLUG="<project-slug>"` or `python3 scripts/prepare-project-repo.py "<project-slug>"`
2. create missing governance stubs such as `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, and optional CI workflow files
3. never overwrite existing repo-governance files automatically
4. keep this separate from ordinary project scaffolding and onboarding

## Default Project Workflow Rule

For consistency across projects created or managed from this workspace:

1. track project-local roadmap work in `projects/<slug>/ROADMAP.md`
2. track cross-project status and prioritization in `custom/status/`
3. commit locally at coherent task boundaries
4. push to GitHub when work should be backed up, reviewed, shared, or continued elsewhere

This workspace should reduce decision fatigue by keeping those defaults consistent unless a specific project has a strong reason to differ.

## Customization Rules

- keep root docs generic and template-managed
- put user-specific customizations under `custom/`
- put user-maintained project inventory and prioritization data under `custom/status/`
- do not edit root template-managed files for personal preferences unless you intend to own divergence
- never store project-specific implementation notes at the root
- never let migration or sync tooling overwrite `custom/` or `projects/`
- use project-local `HANDOFF.md` files when transferring execution context

## Repo Layout Recommendation

The preferred model is:

- root repo: workspace instance with template-managed files
- `custom/`: user-managed overrides and helper files
- `custom/status/`: user-managed project inventory and status tracking
- `projects/<slug>/`: project-local directory, often its own Git repo

This keeps template updates, user overrides, and project implementation cleanly separated.

## Agent Alignment

Gemini, Codex, OpenCode, Grok, and Claude should all follow the same read order: root policy first, `custom/` overrides second, project-local rules last. Agent-specific files should act as adapters to this policy, not alternate sources of truth.
