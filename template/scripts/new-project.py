#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT_DIR / "templates" / "project-starter"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return slug


def render_template(template: str, replacements: dict[str, str]) -> str:
    content = template
    for key, value in replacements.items():
        content = content.replace(key, value)
    return content


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

    replacements = {
        "<PROJECT_NAME>": name,
        "<PROJECT_SLUG>": slug,
        "<INITIAL_GOAL>": goal,
    }

    for template_path in sorted(TEMPLATE_DIR.iterdir()):
        if not template_path.is_file():
            continue
        rendered = render_template(template_path.read_text(), replacements)
        (project_dir / template_path.name).write_text(rendered)

    print(f"Created project: {name}")
    print(f"Directory: {project_dir}")
    print(f"Slug: {slug}")
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
