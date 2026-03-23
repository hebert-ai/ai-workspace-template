# Repository Guidelines

## Purpose

This directory contains one project inside the shared AI workspace. Project-specific planning and implementation happen here, while shared workspace policy lives at `../../AGENTS.md` and `../../WORKSPACE.md`.

Read `../../WORKSPACE.md` and `../../custom/AGENTS.md` when present, then use this file as the local project guide.

## Local Structure

- local agent files such as `CLAUDE.md`, `GEMINI.md`, and related adapters
- project plans, notes, and implementation files as the project grows

Keep project-specific decisions in this directory unless they affect multiple projects.

## Working Rules

- prefer keeping implementation, notes, and assets local to this project
- inherit shared workspace policy from the root rather than duplicating it
- keep project decisions local unless they require a workspace-level template change

## Default Workflow

- track project-local roadmap items in `./ROADMAP.md`
- use `../../custom/status/projects.md` and `../../custom/status/priorities.md` only for cross-project visibility and ordering
- make a local Git commit when a focused change is coherent, reviewable, and leaves the project in a better state than before
- prefer committing at natural checkpoints such as:
  - after finishing one task or bug fix
  - before switching to a different task
  - before handing work to another person or agent
- push to GitHub when the work should be backed up remotely, shared, reviewed, or picked up from another machine
- do not wait for a huge batch of unrelated changes before committing
- do not push broken or half-explained work unless the push is explicitly a draft checkpoint and is labeled that way

## Local Git Rules

- keep commit subjects imperative and specific
- prefer small, focused commits over large mixed commits
- if the project has tests or checks, run the relevant ones before committing when practical
- if a change affects roadmap direction, update `./ROADMAP.md` or `./PROJECT.md` in the same commit

## Project Setup

- Project name: `<PROJECT_NAME>`
- Directory: `projects/<PROJECT_SLUG>`
- Initial goal: `<INITIAL_GOAL>`
