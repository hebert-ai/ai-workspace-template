# Contributing

## Scope

This repository is the product repo for `ai-workspace-template`.

Contributions should improve:

- the template contract
- generated workspace docs and starter files
- bootstrap, sync, validation, and onboarding tooling
- release safety and regression coverage

Do not treat this repo as a workspace instance for day-to-day project work.

## Before You Change Anything

Read:

- `README.md`
- `ARCHITECTURE.md`
- `MIGRATIONS.md`
- `ROADMAP.md`
- `AGENTS.md`

## Working Rules

- preserve the boundary between template-managed files, user-managed `custom/`, and project-local `projects/`
- never design tooling that overwrites `custom/` or `projects/`
- prefer explicit, reviewable behavior over convenience automation
- keep generated workspace behavior conservative and understandable
- update docs when changing product behavior

## Validation

Before opening a pull request, run:

```bash
python3 scripts/template_ops.py validate
bash scripts/e2e-validate.sh
```

If you change generated workspace scripts, also run the relevant generated workspace checks in a temp workspace when practical.

## Pull Requests

Pull requests should:

- explain the product-level purpose of the change
- note any changes to the template contract
- call out migration or compatibility impact explicitly
- keep unrelated refactors out of the same change

## Design Preference

When there is a tradeoff, prefer:

- safety over automation
- clarity over cleverness
- conservative migration behavior over aggressive synchronization
