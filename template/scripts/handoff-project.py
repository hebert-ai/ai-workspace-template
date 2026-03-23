#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_FILE = ROOT_DIR / "templates" / "project-handoff.md"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a handoff note for a project.")
    parser.add_argument("slug", help="Project slug")
    args = parser.parse_args()

    project_dir = ROOT_DIR / "projects" / args.slug
    if not project_dir.exists():
        print(f"Project directory does not exist: {project_dir}", file=sys.stderr)
        return 1

    handoff_file = project_dir / "HANDOFF.md"
    template = TEMPLATE_FILE.read_text()
    content = (
        template.replace("Name:", f"Name: {args.slug}")
        .replace("Slug:", f"Slug: {args.slug}")
        .replace("Directory:", f"Directory: projects/{args.slug}")
        .replace("Repo URL:", "Repo URL:")
    )
    handoff_file.write_text(content)
    print(f"Wrote handoff note: {handoff_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
