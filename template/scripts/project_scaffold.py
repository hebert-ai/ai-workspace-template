from __future__ import annotations

import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECT_TEMPLATE_DIR = ROOT_DIR / "templates" / "project-starter"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return slug


def render_template(template: str, replacements: dict[str, str]) -> str:
    content = template
    for key, value in replacements.items():
        content = content.replace(key, value)
    return content


def scaffold_project_files(project_dir: Path, name: str, slug: str, goal: str) -> tuple[list[Path], list[Path]]:
    replacements = {
        "<PROJECT_NAME>": name,
        "<PROJECT_SLUG>": slug,
        "<INITIAL_GOAL>": goal,
    }

    created: list[Path] = []
    skipped: list[Path] = []
    for template_path in sorted(PROJECT_TEMPLATE_DIR.iterdir()):
        if not template_path.is_file():
            continue

        target = project_dir / template_path.name
        if target.exists():
            skipped.append(target)
            continue

        rendered = render_template(template_path.read_text(), replacements)
        target.write_text(rendered)
        created.append(target)

    return created, skipped
