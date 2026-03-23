# Release Checklist

## Product Fit

- confirm the product description still matches the intended workspace model
- confirm the template is still repo-first, conservative, and migration-safe
- confirm `custom/` and `projects/` remain outside the sync path

## Naming

- confirm the public product name is `AI Workspace Template`
- confirm the public repo name is `ai-workspace-template`
- confirm directory names remain consistent across docs and scripts:
  `template/`, `templates/`, `projects/`, `custom/`, `custom/status/`

## Docs

- review `README.md` for a clear public-facing opening
- review `ARCHITECTURE.md` for ownership boundaries and invariants
- review `MIGRATIONS.md` for current sync behavior and upgrade flow
- review `ONBOARDING.md` for a realistic user setup path
- review generated workspace docs under `template/`

## Template Contract

- verify `template/manifest.json` matches the actual template payload
- confirm bootstrap-only seeds stay outside sync management
- confirm no template-managed path overlaps `custom/` or `projects/`

## Tooling

- run `python3 scripts/template_ops.py validate`
- run `python3 scripts/template_ops.py bootstrap /tmp/ai-workspace-template-release-check --dry-run`
- run a real bootstrap to a temp directory and verify the generated workspace shape
- run `python3 scripts/template_ops.py sync <temp-workspace> --dry-run`
- verify stateful sync behavior still works for unchanged files
- verify user-diverged files still produce conflicts
- verify stale managed paths are reported but not removed

## Generated Workspace Review

- confirm the generated workspace includes `custom/status/`
- confirm the generated workspace ignores `.workspace-template/`
- confirm `projects/.gitkeep` is preserved
- confirm root docs clearly tell the user to move into `projects/<slug>/` for project-specific work
- confirm multiple LLM client adapter files remain aligned with one shared policy model

## Public Release Hygiene

- confirm example commands and paths are valid
- confirm there are no org-internal assumptions left in public-facing docs
- confirm there are no secrets, machine-local paths, or private repo references in the template payload
- confirm the repo is ready for a clean initial tag or release
