# Roadmap

## Purpose

This file is the product-level roadmap for `ai-workspace-template`.

Use it to track:

- the current baseline
- the next highest-value improvements
- open product decisions
- explicitly deferred ideas

This is not the user workspace backlog. It is the roadmap for the template product itself.

## Current Baseline

The current product already provides:

- a canonical template payload under `template/`
- explicit ownership boundaries between template-managed files, user-managed `custom/`, and project-local `projects/`
- manifest-driven bootstrap, sync, and validation tooling
- conservative sync behavior with per-file state tracking
- stale managed path reporting
- generated workspace commands for:
  - creating a new project
  - cloning and onboarding an existing project repo
  - seeding project-local agent files without overwriting existing files
- starter user-managed portfolio tracking under `custom/status/`
- product-repo end-to-end validation via `scripts/e2e-validate.sh`

## Next Priorities

### 1. Improve Upgrade Ergonomics

Goal:
Make template updates easier to understand and safer to review without widening the migration surface.

Candidates:

- add clearer sync summaries at the end of runs
- distinguish review-only warnings from blocking failures more cleanly
- add a template version identifier alongside per-file hashes
- document the recommended upgrade flow with concrete examples for common cases

### 2. Add Explicit Stale-File Cleanup Flow

Goal:
Keep stale managed paths reviewable but give users a safe way to clean them up deliberately.

Candidates:

- add a dedicated prune command for stale managed state and stale files
- require explicit confirmation or a dedicated flag
- never piggyback destructive cleanup onto normal sync

### 3. Strengthen Automated Validation

Goal:
Keep regressions visible before release.

Candidates:

- expand `scripts/e2e-validate.sh` with more edge cases
- test conflict behavior more explicitly
- test sync update behavior against older recorded hashes
- add tests that exercise the core LLM client adapters and verify they load the intended root, custom, and project-local guidance consistently
- verify agent-adapter behavior stays aligned across supported clients rather than drifting silently
- consider a CI workflow once the repo is pushed publicly

### 4. Tighten Public Onboarding

Goal:
Reduce ambiguity for first-time external users.

Candidates:

- decide whether the preferred user flow is:
  - copy `template/` into a new repo
  - use GitHub template-repo behavior
  - run a dedicated bootstrap command
- document the recommended GitHub setup path after first publish
- add a public quickstart that assumes no prior context

### 5. Standardize Project Workflow Conventions

Goal:
Reduce decision fatigue by giving every generated project the same default structure for roadmap tracking, local commits, and GitHub pushes.

Candidates:

- keep project-local roadmap tracking in `projects/<slug>/ROADMAP.md`
- keep cross-project prioritization in `custom/status/`
- document default commit and push timing clearly in starter files
- add optional helper tooling later if the documented workflow proves stable

## Open Product Decisions

- Should sync state include an explicit template version in addition to file hashes?
- Should users get an allowlist or denylist for selected template-managed files?
- Should stale cleanup operate on files, state entries, or both?
- Should the project eventually provide a one-command personal-workspace bootstrap flow?
- Should project onboarding ever attempt structured merge behavior for existing local project docs, or remain create-only for missing files?

## Deferred Ideas

- richer project inventory templates under `custom/status/`
- optional CI configuration for generated workspaces
- optional GitHub issue or project templates for the product repo
- additional vendor-specific agent adapters if there is clear demand
- richer reporting or JSON output from sync tooling

## Release Milestones

### First Public Push

Success criteria:

- docs are public-facing and consistent
- ownership boundaries are explicit
- bootstrap/sync/validation behavior is conservative and tested
- onboarding covers both new projects and existing repos
- roadmap and release checklist exist in the repo

### First Public Release

Success criteria:

- users can create a personal workspace repo with minimal ambiguity
- upgrade flow is documented and tested
- known limitations are documented rather than implied

## Updating This File

- keep it concise
- prefer product decisions and priorities over brainstorming
- move completed items into released docs or release notes instead of letting this become a changelog
