# Architecture

This file describes the structural boundaries of the product.

Related docs:

- `OPERATING_MODEL.md`: how the workflow is intended to work
- `TOOLING_MODEL.md`: how this repo implements that workflow

## Ownership Model

The template system has three ownership zones:

1. Template-managed
   Files and directories the template may create, update, or validate.
2. User-managed
   Local overrides and preferences, primarily under `custom/`.
3. Project-local
   Real projects under `projects/`, often their own repos.

The intended runtime shape is:

- canonical template repo: this product repo
- user workspace repo: a separate repo created from the template and owned by the user
- project repos: independent repos under `projects/<slug>/`

Recommended naming:

- public product name: `AI Workspace Template`
- public repo name: `ai-workspace-template`
- generated workspace name: `AI Workspace`

## Invariants

- template updates may touch template-managed files only
- sync logic must never overwrite `custom/`
- sync logic must never overwrite `projects/`
- project-specific implementation never belongs in the workspace root
- agent read order should remain: root policy, user overrides, project-local rules
- the template contract must be explicit and manifest-defined
- the root workspace is a cross-project planning layer, not a project implementation repo
- user portfolio tracking data must remain user-managed
- project repos must remain decoupled from root workspace migrations
- migration failures should fail conservatively and reviewably

## Expected Template-Managed Surface

- root docs such as `README.md`, `AGENTS.md`, `WORKSPACE.md`, and `SETUP.md`
- root agent adapter files
- `templates/`
- `scripts/`
- ignore rules and setup/bootstrap logic

## Expected User-Managed Surface

- `custom/AGENTS.md`
- `custom/agents/`
- `custom/scripts/`
- `custom/status/`
- optional user docs under `custom/`
- local portfolio tracking, prioritization, and project status files

## Expected Project-Local Surface

- `projects/<slug>/`
- project-local docs
- project-local agent files
- project-local code, assets, and repos

## Sync Contract Rules

- the canonical template payload lives under `template/`; that directory name is part of the product contract
- sync may operate only on manifest-declared template-managed files
- bootstrap may seed user-managed areas, but those seeds do not become sync-managed
- template-internal metadata may exist to support sync, but must not expand the managed surface implicitly
- stale formerly managed files should be reported, not removed automatically
- destructive cleanup, if ever supported, should require an explicit dedicated flow

## User Workspace Model

- users commit the workspace root, excluding ignored local state and `projects/*`, to their own repo
- users restore a workstation by cloning that personal workspace repo and then restoring project repos under `projects/`
- multiple LLM vendors are expected, so agent-specific root files are adapters rather than separate policy systems
- custom agents and vendor-specific local conventions belong under `custom/`, outside the migration path

## Tooling Expectations

- workspace tooling should help users scaffold or clone projects into `projects/`
- workspace tooling should not make assumptions about the internals of project repos
- validation should verify contract integrity and boundary rules
- upgrade flow should be explicit, reviewable, and safe for older workspaces that may lack newer state

## Directory Naming Rationale

- `template/` is singular because it is the canonical payload for one generated workspace
- `templates/` inside the generated workspace is plural because it contains multiple reusable starter and planning documents
- `projects/` is plural because it holds many independent repos
- `custom/` is the user-owned area for overrides and local conventions that must remain outside migration
- `custom/status/` is user-managed because project inventory and priorities are personal workflow data, not template contract
