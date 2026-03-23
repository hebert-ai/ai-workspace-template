# Onboarding

## Goal

Create a personal AI workspace repo from `ai-workspace-template` without confusing the template product repo with the user’s long-lived workspace repo.

## Recommended Model

- canonical template repo: `ai-workspace-template`
- personal workspace repo: for example `ai-workspace` or `<team>-workspace`
- project repos: independent repos under `projects/<slug>/`

## Initial Setup

1. Clone or copy the generated workspace payload into a new personal repo.
2. Initialize that workspace as the user’s own Git repo.
3. Run the workspace setup commands.
4. Review the root guidance files and the user-managed `custom/` area.
5. Start creating or cloning project repos under `projects/`.

## Recommended Automated Setup

If you already have an older local workspace and want a safer migration path, use the product utility from the directory that should become the workspace root:

```bash
mkdir -p /home/ryan/ai
cd /home/ryan/ai
curl -fsSL -o /tmp/onboard-local-workspace.sh \
  https://raw.githubusercontent.com/hebert-ai/ai-workspace-template/main/scripts/onboard-local-workspace.sh
bash /tmp/onboard-local-workspace.sh --github-user ryanhebert --dry-run
bash /tmp/onboard-local-workspace.sh --github-user ryanhebert
```

That flow can:

- derive the workspace name from the current directory
- list the authenticated user and available GitHub orgs for owner selection
- create a private GitHub workspace repo from the template if needed
- back up an existing local workspace
- clone the new workspace repo
- migrate `custom/` and `projects/`
- run the generated workspace setup script
- run `make check` automatically unless explicitly skipped

For the example above:

- current directory: `/home/ryan/ai`
- derived workspace name: `ai`
- derived repo name: `workspace-ryanhebert-ai`
- if you select `hebert-ai` as the owner, the resulting repo becomes:
  `hebert-ai/workspace-ryanhebert-ai`

## One Simple Way To Do It

From the template product repo:

```bash
mkdir -p ~/ai-workspace
cp -R template/. ~/ai-workspace/
cd ~/ai-workspace
git init
git add .
git commit -m "Initialize AI workspace"
bash scripts/setup-workspace.sh
```

That manual flow is still valid, but the scripted onboarding path is preferred once you want a repeatable migration utility.

Then review:

- `README.md`
- `AGENTS.md`
- `WORKSPACE.md`
- `custom/AGENTS.md`
- `custom/status/README.md`

## What To Customize First

- `custom/AGENTS.md` for user-specific workflow rules
- `custom/agents/` for custom agents and vendor-specific adapter files
- `custom/scripts/` for personal helper scripts
- `custom/status/` for project inventory, priorities, and blockers

## What Not To Customize First

- do not put personal workflow data into template-managed root docs
- do not treat `projects/` as part of the root workspace repo
- do not store product implementation at the root unless it is truly cross-project workspace logic

## Daily Use

- use the root workspace to review status and prioritize
- use `make new-project NAME="Project Name" GOAL="Initial goal"` to scaffold a project workspace
- use `python3 scripts/clone-project.py <repo-url>` to bring an existing repo into `projects/`
- switch into `projects/<slug>/` when the work becomes project-specific

## Updating From The Template

The user workspace repo is separate from the canonical template repo.

Recommended flow:

1. pull or fetch changes in `ai-workspace-template`
2. review what changed in the canonical template
3. run sync from the template repo against the personal workspace repo, for example:

```bash
python3 scripts/template_ops.py sync ~/ai-workspace --dry-run
python3 scripts/template_ops.py sync ~/ai-workspace
```

4. inspect `create`, `update`, `conflict`, and `stale` output carefully
5. use `--force` only when the user intends to overwrite divergence

## Notes For Public Users

- this system is intentionally repo-first and conservative
- `custom/` and `projects/` are outside the migration path
- multiple LLM vendors are expected; the root policy model stays shared even when client-specific adapters differ
