# Customizations

Use `custom/` for user-specific workspace behavior that should survive template updates.

Recommended subdirectories:

- `custom/AGENTS.md`: user-specific workflow rules that extend the root policy
- `custom/agents/`: extra agent/client-specific files
- `custom/scripts/`: personal helper scripts
- `custom/status/`: project inventory, priorities, and portfolio notes
- `custom/docs/`: personal notes or local operating docs

Rules:

- do not edit root template-managed files for personal preferences unless you are intentionally changing the shared workspace behavior
- keep custom agents and vendor-specific client conventions here so they remain outside the migration path
- keep portfolio tracking data here rather than in template-managed root files
- do not store project-specific implementation notes here unless they are explicitly personal cross-project notes
- do not store secrets here unless you also exclude them from version control
