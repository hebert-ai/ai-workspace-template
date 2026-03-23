# Repository Guidelines

## Purpose

This project defines the canonical AI workspace template used to create portable workspace instances. It is a product repo for the template itself, not a place to run day-to-day project work.

Read `../../WORKSPACE.md` first for the current workspace-instance model, then use this file as the local guide for template development.

## Product Boundaries

- this repo owns template-managed root files, starter templates, and migration/sync tooling
- it does not own user customizations under `custom/`
- it does not own live project repos under `projects/`

Changes here must preserve the separation between:

- template-managed files
- user-managed overrides
- project-local repos

## Local Structure

- `README.md`: product overview for the template repo
- `ARCHITECTURE.md`: ownership boundaries and design rules
- `CONTEXT.md`: working context carried forward from initial design
- `MIGRATIONS.md`: sync and update strategy
- `scripts/`: template bootstrap, sync, and validation tooling

## Working Rules

- optimize for safe workspace upgrades, not one-off local convenience
- never design sync logic that overwrites `custom/` or `projects/`
- keep generated workspace behavior simple and explicit
- prefer updating docs and invariants before adding automation
- when changing root template behavior, update the corresponding docs in this project

## Immediate Priorities

- define template-managed vs user-managed file ownership
- build bootstrap and sync tooling for workspace instances
- keep the root workspace and this project aligned while the template is still evolving
