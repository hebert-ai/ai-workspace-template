# Tooling Model

## Purpose

This file explains how `ai-workspace-template` implements the operating model in concrete files, directories, and scripts.

It answers:

- which files hold which kinds of information
- which commands create or update those files
- which parts are template-managed
- which parts are user-managed
- how agents should interpret the workspace

This is the "how we use this tool" layer.

## Directory Roles

- `template/`: canonical generated workspace payload
- `scripts/`: template-product tooling and validation
- `projects/`: project repos inside a generated workspace
- `custom/`: user-managed overrides and local conventions
- `custom/status/`: cross-project inventory and priorities
- `templates/project-starter/`: project-local starter files
- `templates/project-repo-starter/`: optional GitHub-facing repo stub files

## Managed Surface

Template-managed:

- files declared in `template/manifest.json`
- sync-managed root workspace files
- generated starter and tooling files inside the workspace payload

User-managed:

- everything under `custom/`
- project repos under `projects/`
- project-local changes after scaffolding or onboarding

## Core Commands

### Product Repo Commands

- `python3 scripts/template_ops.py bootstrap <target>`
- `python3 scripts/template_ops.py sync <target>`
- `python3 scripts/template_ops.py validate [--target <path>]`
- `bash scripts/e2e-validate.sh`

### Generated Workspace Commands

- `make setup`
- `make new-project NAME="Project Name" GOAL="Initial goal"`
- `make onboard-project SLUG="project-slug"`
- `make prepare-project-repo SLUG="project-slug"`
- `make handoff-project SLUG="project-slug"`

## Workflow Mapping

The tooling maps to the operating model like this:

- start a new local project:
  `new-project.py`
- bring in an existing repo:
  `clone-project.py` or `onboard-project.py`
- prepare a project repo for GitHub-facing collaboration:
  `prepare-project-repo.py`
- manage cross-project status:
  files under `custom/status/`
- manage project-local roadmap:
  `projects/<slug>/ROADMAP.md`

## Agent Interpretation

Agents should read the workspace in this order:

1. root workspace policy
2. user overrides in `custom/`
3. project-local docs

Agent-specific files are adapters to that order, not alternate policy systems.

## Safety Rules In The Tooling

- sync never manages `custom/` or `projects/`
- onboarding never overwrites existing project files automatically
- project-repo preparation never overwrites existing governance files automatically
- bootstrap-only seeds remain user-managed after creation
- forced bootstrap preserves existing `custom/` content

## Why Two Layers Exist

`OPERATING_MODEL.md` describes the desired behavior independent of implementation.

This file describes the current implementation of that behavior in this repository.

If the tooling changes later, the operating model can remain stable while this file changes to reflect the implementation.
