# workspace-template — Project Overview

## Summary

- project: `workspace-template`
- purpose: define the canonical workspace template for AI-assisted development
- current theme: bootstrap, sync, migration, and boundary safety

## Key References

- local product overview: `./README.md`
- architecture rules: `./ARCHITECTURE.md`
- carried-forward design context: `./CONTEXT.md`
- local contribution rules: `./AGENTS.md`

## Core Constraint

The template may update workspace-managed files, but it must not trample user-managed `custom/` content or local project repos under `projects/`.
