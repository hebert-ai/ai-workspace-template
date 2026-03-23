# Migrations

## Goal

Allow a workspace instance created from the template to receive template updates without losing user-specific customizations or local project repos.

The expected deployment model is:

- this repo remains the canonical template product
- each user keeps a separate personal workspace repo created from the template
- updates flow from the canonical template into the user workspace through explicit sync

## Rules

- only template-managed files are eligible for sync
- `custom/` is always preserved
- `projects/` is always preserved
- sync should be explicit and reviewable
- destructive updates should require confirmation
- older workspaces that are missing newer state should remain safe, even if that means more conflicts and manual review

## First Sync Contract

The initial sync implementation should likely handle only:

- root Markdown guidance files
- root agent adapter files
- `scripts/`
- `templates/`
- ignore/setup files
- bootstrap-only seeds for `custom/` and `projects/`

It should not attempt to merge arbitrary user edits automatically. The first implementation uses `template/manifest.json` as the sync contract.

## Current Behavior

- sync creates missing template-managed files
- sync auto-updates files that still match the last recorded template-applied hash
- sync reports conflicts for user-diverged files unless `--force` is used
- sync records per-file template state in `.workspace-template/state.json`
- sync reports stale formerly-managed files that are no longer in the current manifest
- dry-run is supported for bootstrap and sync

## Current Upgrade Flow

1. update or clone the canonical template source
2. review template changes
3. run sync against the user workspace repo
4. inspect `create`, `update`, `conflict`, and `stale` output
5. use `--force` only when the user intends to overwrite local divergence

## Open Questions

- Should users have an allowlist/denylist for template updates?
- Should state include a manifest or template version identifier in addition to per-file hashes?
- Should stale files eventually support an explicit prune command or confirmation flow?
