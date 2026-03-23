# Scripts

This directory should become the canonical home for template tooling.

Current scripts:

- `bootstrap-instance.sh <target>`: create a workspace instance from `template/`
- `sync-instance.sh <target>`: sync template-managed files only
- `validate-template.sh [--target <path>]`: validate the template payload and optional instance
- `e2e-validate.sh`: run end-to-end validation against a temporary generated workspace
- `onboard-local-workspace.sh`: back up an existing local workspace, create or clone a user workspace repo from the template, migrate `custom/` and `projects/`, and run setup
- `onboard-local-workspace.sh` also runs `make check` by default after setup
- `template_ops.py`: shared implementation used by the shell wrappers

Standalone use:

```bash
mkdir -p /home/ryan/ai
cd /home/ryan/ai
curl -fsSL -o /tmp/onboard-local-workspace.sh \
  https://raw.githubusercontent.com/hebert-ai/ai-workspace-template/main/scripts/onboard-local-workspace.sh
bash /tmp/onboard-local-workspace.sh --github-user ryanhebert --dry-run
bash /tmp/onboard-local-workspace.sh --github-user ryanhebert
```

Behavior rules:

- sync only touches manifest-declared template-managed files
- bootstrap seeds `custom/` and `projects/` defaults but does not treat them as syncable
- the generated workspace includes `custom/status/` as a user-managed home for project inventory and priorities
- `custom/` and `projects/` are preserved during sync
- forced bootstrap preserves existing `custom/` files instead of overwriting user-managed content
- sync records template-applied hashes in `.workspace-template/state.json`
- unchanged files can be updated automatically on later sync runs
- user-diverged files still surface as conflicts unless `--force` is used
- stale previously managed files are reported for review but not removed
- use dry-run or non-force sync first when evaluating changes
