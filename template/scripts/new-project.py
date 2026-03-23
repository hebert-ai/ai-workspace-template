#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from project_scaffold import scaffold_project_files, slugify

ROOT_DIR = Path(__file__).resolve().parent.parent


def create_project(name: str, goal: str) -> int:
    slug = slugify(name)
    if not slug:
        print("Could not derive a valid project slug from project name.", file=sys.stderr)
        return 1

    project_dir = ROOT_DIR / "projects" / slug
    if project_dir.exists():
        print(f"Project directory already exists: {project_dir}", file=sys.stderr)
        return 1

    project_dir.mkdir(parents=True)
    created, skipped = scaffold_project_files(project_dir, name=name, slug=slug, goal=goal)

    print(f"Created project: {name}")
    print(f"Directory: {project_dir}")
    print(f"Slug: {slug}")
    print(f"Scaffolded files: {len(created)}")
    if skipped:
        print(f"Skipped existing files: {len(skipped)}")
    print(f"Next: review {project_dir / 'PROJECT.md'} and refine the local agent files.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a new project folder from the shared workspace templates."
    )
    parser.add_argument("name", help='Project name, for example "AirBnb Buddy"')
    parser.add_argument(
        "goal",
        nargs="?",
        default="Define initial project goal.",
        help="Initial goal to seed into the project files.",
    )
    args = parser.parse_args()
    return create_project(args.name, args.goal)


if __name__ == "__main__":
    raise SystemExit(main())
