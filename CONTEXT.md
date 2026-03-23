# Context

## Why This Project Exists

The workspace root was shaped into a portable instance created from a shared template. The next step is to turn that implicit design into an explicit template product that can be versioned and improved safely.

## Decisions Carried Forward

- the root workspace should be a workspace instance, not a live portfolio registry
- `projects/` should be local to the workspace instance and ignored by the root repo
- real projects should live inside `projects/<slug>/` and usually have their own repos
- user-specific differences should live under `custom/`
- migration should operate only on template-managed files
- sync tooling must preserve both `custom/` and `projects/`

## Practical Implications

- root docs should stay generic and reusable
- project tracking should not be hard-coded into the template
- agent files should share one read order and one ownership model
- the template repo needs its own docs and scripts because it is now a product

## Immediate Next Step

Define the first version of the sync contract:

- which files are template-managed
- how changes are applied
- how conflicts are surfaced
- how user divergence is handled
