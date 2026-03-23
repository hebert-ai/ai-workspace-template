#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from project_scaffold import scaffold_project_files, slugify


ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECTS_DIR = ROOT_DIR / "projects"


def infer_name(project_dir: Path, slug: str, explicit_name: str | None) -> str:
    if explicit_name:
        return explicit_name
    if project_dir.name:
        return project_dir.name
    return slug


def onboard_project(slug: str, name: str | None, goal: str) -> int:
    project_dir = PROJECTS_DIR / slug
    if not project_dir.exists():
        print(f"Project directory does not exist: {project_dir}", file=sys.stderr)
        return 1
    if not project_dir.is_dir():
        print(f"Project path is not a directory: {project_dir}", file=sys.stderr)
        return 1

    project_name = infer_name(project_dir, slug=slug, explicit_name=name)
    created, skipped = scaffold_project_files(project_dir, name=project_name, slug=slug, goal=goal)

    print(f"Onboarded project: {project_name}")
    print(f"Directory: {project_dir}")
    print(f"Created files: {len(created)}")
    print(f"Skipped existing files: {len(skipped)}")

    if created:
        print("Created:")
        for path in created:
            print(f"- {path.name}")

    if skipped:
        print("Skipped:")
        for path in skipped:
            print(f"- {path.name}")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Seed missing workspace project files into an existing projects/<slug> repo."
    )
    parser.add_argument("slug", help="Project slug under projects/")
    parser.add_argument(
        "--name",
        help="Optional project display name. Defaults to the directory name.",
    )
    parser.add_argument(
        "--goal",
        default="Document the initial project goal.",
        help="Initial goal to seed into newly created project files.",
    )
    args = parser.parse_args()

    slug = slugify(args.slug)
    if not slug:
        print("Could not determine a valid project slug.", file=sys.stderr)
        return 1

    return onboard_project(slug=slug, name=args.name, goal=args.goal)


if __name__ == "__main__":
    raise SystemExit(main())
