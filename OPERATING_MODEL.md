# Operating Model

## Purpose

This file defines the tool-agnostic way of working that `ai-workspace-template` is designed to support.

It answers:

- how work is organized
- where planning lives
- how project repos relate to the workspace root
- when to commit locally
- when to push to GitHub
- how roadmap and execution items should be tracked

This is the "how we work" layer.

## Core Model

The operating model has three levels:

1. Workspace level
   Cross-project planning, prioritization, intake, and shared operating rules.
2. Project level
   Project-specific roadmap, implementation, and repo-local decisions.
3. GitHub/public collaboration level
   The point where a project repo needs governance files, remote collaboration, and repo-hosted workflows.

## Source Of Truth Rules

- workspace root: cross-project coordination
- `custom/status/`: user-managed cross-project inventory and prioritization
- `projects/<slug>/ROADMAP.md`: project-local roadmap and backlog
- `projects/<slug>/PROJECT.md`: project definition and current direction
- project repo issues and pull requests: execution and review artifacts once GitHub collaboration matters

The workspace should not become a duplicate of project-local planning, and project repos should not absorb cross-project portfolio tracking.

## Default Workflow

### Starting Work

- create a new project under `projects/<slug>/` when the work is new
- clone and onboard an existing repo under `projects/<slug>/` when the work already exists elsewhere
- move into the project directory when the work becomes project-specific

### Tracking Work

- track cross-project priorities in `custom/status/`
- track project-local milestones and backlog in `projects/<slug>/ROADMAP.md`
- track project purpose and current direction in `projects/<slug>/PROJECT.md`

### Local Commits

Make a local commit when:

- one focused change is coherent and reviewable
- a task or bug fix reaches a natural checkpoint
- you are switching context
- you are about to hand work to another person or agent

Prefer:

- small, focused commits
- imperative commit subjects
- relevant validation before committing when practical

### GitHub Pushes

Push when:

- the work should be backed up remotely
- another person or machine needs to pick it up
- a pull request or review is needed
- the project is moving from local-only work to shared collaboration

Do not treat every local commit as an automatic push requirement. Pushes should reflect collaboration, backup, or publication needs.

## GitHub Collaboration Layer

Preparing a project for GitHub is a separate step from ordinary project creation.

That step should:

- add or confirm repo-governance files
- prepare CI stubs if useful
- avoid overwriting existing governance choices

This keeps the default project workflow lightweight while still giving a consistent path to more formal collaboration.

## Decision Fatigue Reduction

The point of this model is consistency.

Users should not have to decide from scratch:

- where roadmap items go
- when to commit
- when to push
- where GitHub-facing repo files come from

The default answers should already exist unless a project has a strong reason to differ.
