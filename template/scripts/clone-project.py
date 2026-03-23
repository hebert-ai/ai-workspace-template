#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from project_scaffold import scaffold_project_files, slugify


ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECTS_DIR = ROOT_DIR / "projects"


def main() -> int:
    parser = argparse.ArgumentParser(description="Clone a project repo into projects/<slug>.")
    parser.add_argument("repo_url", help="Git URL to clone")
    parser.add_argument(
        "--slug",
        help="Optional target slug. Defaults to the repo name.",
    )
    parser.add_argument(
        "--name",
        help="Optional project display name for generated local project files.",
    )
    parser.add_argument(
        "--goal",
        default="Document the initial project goal.",
        help="Initial goal to seed into newly created local project files.",
    )
    parser.add_argument(
        "--no-onboard",
        action="store_true",
        help="Clone only. Do not seed missing workspace project files into the repo.",
    )
    args = parser.parse_args()

    default_name = Path(args.repo_url.rstrip("/")).name
    if default_name.endswith(".git"):
        default_name = default_name[:-4]
    slug = slugify(args.slug or default_name)
    if not slug:
        print("Could not determine a valid project slug.", file=sys.stderr)
        return 1

    target_dir = PROJECTS_DIR / slug
    if target_dir.exists():
        print(f"Project directory already exists: {target_dir}", file=sys.stderr)
        return 1

    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", args.repo_url, str(target_dir)], check=True)
    print(f"Cloned {args.repo_url} -> {target_dir}")

    if args.no_onboard:
        return 0

    project_name = args.name or default_name.replace("-", " ").replace("_", " ").strip() or slug
    created, skipped = scaffold_project_files(target_dir, name=project_name, slug=slug, goal=args.goal)
    print(f"Onboarded local project files for: {project_name}")
    print(f"Created files: {len(created)}")
    print(f"Skipped existing files: {len(skipped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
