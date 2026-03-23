#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECTS_DIR = ROOT_DIR / "projects"


def slugify(value: str) -> str:
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in value)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")


def main() -> int:
    parser = argparse.ArgumentParser(description="Clone a project repo into projects/<slug>.")
    parser.add_argument("repo_url", help="Git URL to clone")
    parser.add_argument(
        "--slug",
        help="Optional target slug. Defaults to the repo name.",
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

