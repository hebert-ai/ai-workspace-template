# AI Workspace Template

AI Workspace Template is a conservative, repo-first system for running an AI-assisted project workspace across many repos.

It gives a user one root workspace repo for planning, prioritization, shared agent guidance, templates, and workspace tooling, while keeping real project repos isolated under `projects/`.

This project is the canonical template product for that workspace model.

## Why This Exists

Most multi-project AI workflows need one place to:

- track project status across many repos
- prioritize work across projects
- keep shared instructions for multiple LLM clients
- preserve personal workspace conventions across machines
- bootstrap new projects without turning the workspace root into a product repo

This template is designed around that split:

- root workspace repo for coordination
- `projects/` for real project repos
- `custom/` for user-owned agents, scripts, and status tracking
- explicit sync for template-managed files only

## Quick Summary

- Publish this repo as the canonical template source.
- Each user creates their own separate workspace repo from it.
- That user workspace repo becomes their persistent AI management workspace.
- Each real project lives under `projects/<slug>/` as its own repo.
- Template updates are applied through explicit sync, never by overwriting `custom/` or `projects/`.

## Product Model

This repo is the product repo for the template itself, not the day-to-day workspace a user operates from.

The intended deployment model is:

- this repo defines the canonical workspace contract
- each user maintains their own separate workspace repo created from that contract
- that user workspace repo contains the root planning layer, shared agent guidance, templates, and workspace tooling
- each real project lives under `projects/<slug>/` as its own repo
- users can move to a new workstation by cloning their personal workspace repo and then restoring or recloning project repos under `projects/`

If this project is published, the recommended public repo name is `ai-workspace-template`. A generated user workspace can then use a simpler repo name such as `ai-workspace` or `<team>-workspace`.

## Getting Started

1. Review [OPERATING_MODEL.md](OPERATING_MODEL.md) for the tool-agnostic working model.
2. Review [TOOLING_MODEL.md](TOOLING_MODEL.md) for how this repository implements that model.
3. Review [ARCHITECTURE.md](ARCHITECTURE.md) for the ownership model and sync boundaries.
4. Follow [ONBOARDING.md](ONBOARDING.md) to create a personal workspace repo from this template.
5. Use the generated workspace’s `make setup`, `make new-project`, and `python3 scripts/clone-project.py` commands to start using it.
6. Review [ROADMAP.md](ROADMAP.md) for future improvements and open product decisions.
7. Before publishing a release, run through [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md).

## Repository Files

- [LICENSE](LICENSE): repository license
- [CONTRIBUTING.md](CONTRIBUTING.md): contribution and validation expectations
- [SECURITY.md](SECURITY.md): vulnerability reporting guidance
- [.github/workflows/validate.yml](.github/workflows/validate.yml): CI validation workflow

## What This Repo Owns

- template-managed root files
- starter templates for new projects
- agent adapter defaults
- bootstrap, validation, and future sync tooling

## What This Repo Does Not Own

- user-specific overrides in `custom/`
- live project repos under `projects/`
- user-managed portfolio tracking data under `custom/`
- workstation-local state such as `venv/`, logs, caches, sync state, or secrets

## Current Product Direction

The workspace model is:

- root: workspace instance created from the template
- `custom/`: user-managed overrides that must survive template updates
- `custom/status/`: user-managed project inventory, priorities, and portfolio notes
- `custom/agents/`: user-managed custom agents, client adapters, and vendor-specific files
- `projects/<slug>/`: real project directories, usually their own repos

The workspace root is the user’s cross-project management layer for AI-assisted work. It is where they review status across projects, prioritize work, keep shared operating rules, and bootstrap new projects. It is not the default place for product implementation.

Sync and migration apply only to the explicit template contract. They must never overwrite `custom/` or `projects/`.

## Operating Decisions

- The user’s personal workspace repo is separate from this canonical template repo.
- The canonical template payload lives under `template/`, and that directory name is part of the contract.
- The root workspace repo ignores `projects/*` but preserves `projects/.gitkeep`.
- User-specific workflow data, project inventory, and custom agents live under `custom/`.
- Agent adapters for different LLM vendors should all resolve to one shared policy model:
  root policy -> user overrides -> project-local rules.
- Project creation tooling may scaffold local docs and directories or clone an existing project repo, but it must not treat project repos as template-managed content.
- Update flow should stay explicit and reviewable: users pull changes from the canonical template source, then apply them to their workspace repo through the manifest-defined sync contract.
- Failure behavior should stay conservative: missing or invalid state, stale managed paths, and user divergence should surface clearly instead of being auto-merged away.

## Naming Decisions

- Product name: `AI Workspace Template`
- Recommended public repo name: `ai-workspace-template`
- Generated user workspace concept: `AI Workspace`
- Internal payload directory: `template/`
- User project area: `projects/`
- User-owned override area: `custom/`
- User-owned project inventory area: `custom/status/`
- Reusable workspace starters and docs: `templates/`

These names are intentionally plain. They optimize for immediate comprehension over clever branding.

## Near-Term Work

- keep the template contract explicit and minimal
- improve upgrade ergonomics without expanding the migration surface
- preserve clean separation between template-managed files, user-managed files, and project repos
