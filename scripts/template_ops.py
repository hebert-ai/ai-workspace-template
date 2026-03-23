#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = PROJECT_DIR / "template"
MANIFEST_FILE = TEMPLATE_DIR / "manifest.json"
INTERNAL_TEMPLATE_FILES = {"manifest.json"}
INSTANCE_STATE_FILE = Path(".workspace-template/state.json")


def load_manifest() -> dict:
    if not MANIFEST_FILE.exists():
        raise FileNotFoundError(f"Template manifest not found: {MANIFEST_FILE}")
    return json.loads(MANIFEST_FILE.read_text())


def should_skip(path: Path) -> bool:
    return "__pycache__" in path.parts or path.suffix == ".pyc"


def normalize_rel_path(path: Path | str) -> str:
    return Path(path).as_posix()


def collect_files(root: Path) -> set[str]:
    return {
        normalize_rel_path(path.relative_to(root))
        for path in root.rglob("*")
        if path.is_file() and not should_skip(path)
    }


def hash_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def hash_file(path: Path) -> str:
    return hash_bytes(path.read_bytes())


def load_instance_state(target_root: Path) -> dict:
    state_path = target_root / INSTANCE_STATE_FILE
    if not state_path.exists():
        return {"version": 1, "managed_files": {}}

    try:
        data = json.loads(state_path.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid instance state file: {state_path}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"Invalid instance state file: {state_path}")

    managed_files = data.get("managed_files", {})
    if not isinstance(managed_files, dict):
        raise ValueError(f"Invalid managed_files in instance state file: {state_path}")

    normalized = {
        normalize_rel_path(rel): digest
        for rel, digest in managed_files.items()
        if isinstance(rel, str) and isinstance(digest, str)
    }
    return {"version": data.get("version", 1), "managed_files": normalized}


def write_instance_state(target_root: Path, state: dict, dry_run: bool) -> None:
    if dry_run:
        return

    state_path = target_root / INSTANCE_STATE_FILE
    state_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "managed_files": dict(sorted(state.get("managed_files", {}).items())),
    }
    state_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def iter_manifest_files(manifest: dict, include_bootstrap_only: bool) -> list[tuple[Path, str]]:
    rel_paths = list(manifest.get("syncable_paths", []))
    if include_bootstrap_only:
        rel_paths.extend(manifest.get("bootstrap_only_paths", []))

    expanded: list[tuple[Path, str]] = []
    for rel in rel_paths:
        source = TEMPLATE_DIR / rel
        if source.is_dir():
            for child in sorted(source.rglob("*")):
                if child.is_file() and not should_skip(child):
                    expanded.append((child, child.relative_to(TEMPLATE_DIR).as_posix()))
        elif source.is_file() and not should_skip(source):
            expanded.append((source, rel))
    return expanded


def validate_manifest_contract(manifest: dict) -> list[str]:
    errors: list[str] = []

    syncable_paths = [normalize_rel_path(path) for path in manifest.get("syncable_paths", [])]
    bootstrap_only_paths = [
        normalize_rel_path(path) for path in manifest.get("bootstrap_only_paths", [])
    ]
    preserve_roots = {normalize_rel_path(path) for path in manifest.get("preserve_roots", [])}

    declared_paths = syncable_paths + bootstrap_only_paths
    duplicate_paths = sorted({path for path in declared_paths if declared_paths.count(path) > 1})
    for path in duplicate_paths:
        errors.append(f"duplicate manifest path: {path}")

    for path in syncable_paths:
        if any(path == root or path.startswith(f"{root}/") for root in preserve_roots):
            errors.append(f"syncable path overlaps preserved root: {path}")

    for root in preserve_roots:
        if root not in {"custom", "projects"}:
            errors.append(f"unexpected preserved root: {root}")

    declared_files = {
        rel
        for _, rel in iter_manifest_files(manifest, include_bootstrap_only=True)
    }
    template_files = collect_files(TEMPLATE_DIR)
    unmanaged_files = sorted(template_files - declared_files - INTERNAL_TEMPLATE_FILES)
    for path in unmanaged_files:
        errors.append(f"template file missing from manifest contract: {path}")

    for path in sorted(declared_files):
        if path in INTERNAL_TEMPLATE_FILES:
            errors.append(f"internal template file should not be manifest-managed: {path}")

    return errors


def copy_file(source: Path, target: Path, dry_run: bool) -> None:
    if dry_run:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def bootstrap(target_root: Path, dry_run: bool, force: bool) -> int:
    target_root = target_root.resolve()
    if target_root.exists() and any(target_root.iterdir()) and not force:
        print(
            f"Target directory is not empty: {target_root}\n"
            "Use --force to bootstrap into a non-empty directory.",
            file=sys.stderr,
        )
        return 1

    manifest = load_manifest()
    syncable_paths = {
        normalize_rel_path(path)
        for path in manifest.get("syncable_paths", [])
    }
    files = iter_manifest_files(manifest, include_bootstrap_only=True)
    state = {"version": 1, "managed_files": {}}
    for source, rel in files:
        target = target_root / rel
        if force and target.exists() and rel.startswith("custom/"):
            print(f"preserve: {target}")
            continue
        action = "overwrite" if target.exists() else "create"
        print(f"{action}: {target}")
        copy_file(source, target, dry_run=dry_run)
        if rel in syncable_paths:
            state["managed_files"][rel] = hash_file(source)

    if not dry_run:
        for rel in ("custom/agents", "custom/scripts", "projects"):
            (target_root / rel).mkdir(parents=True, exist_ok=True)
        write_instance_state(target_root, state, dry_run=False)

    return 0


def sync(target_root: Path, dry_run: bool, force: bool) -> int:
    target_root = target_root.resolve()
    if not target_root.exists():
        print(f"Target directory does not exist: {target_root}", file=sys.stderr)
        return 1

    manifest = load_manifest()
    try:
        state = load_instance_state(target_root)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    syncable_paths = {
        normalize_rel_path(path)
        for path in manifest.get("syncable_paths", [])
    }
    stale_paths = sorted(set(state["managed_files"]) - syncable_paths)
    conflicts = 0
    for source, rel in iter_manifest_files(manifest, include_bootstrap_only=False):
        target = target_root / rel
        source_hash = hash_file(source)

        if not target.exists():
            print(f"create: {target}")
            copy_file(source, target, dry_run=dry_run)
            state["managed_files"][rel] = source_hash
            continue

        target_hash = hash_file(target)
        if target_hash == source_hash:
            print(f"ok: {target}")
            state["managed_files"][rel] = source_hash
            continue

        recorded_hash = state["managed_files"].get(rel)
        if recorded_hash is not None and target_hash == recorded_hash:
            print(f"update: {target}")
            copy_file(source, target, dry_run=dry_run)
            state["managed_files"][rel] = source_hash
            continue

        if force:
            print(f"overwrite: {target}")
            copy_file(source, target, dry_run=dry_run)
            state["managed_files"][rel] = source_hash
        else:
            print(f"conflict: {target}", file=sys.stderr)
            conflicts += 1

    for rel in stale_paths:
        target = target_root / rel
        status = "present" if target.exists() else "missing"
        print(f"stale ({status}): {target}")

    state["managed_files"] = {
        rel: digest
        for rel, digest in state["managed_files"].items()
        if rel in syncable_paths
    }

    if conflicts:
        print(
            f"Found {conflicts} conflicting file(s). Re-run with --force to overwrite.",
            file=sys.stderr,
        )
        return 1

    write_instance_state(target_root, state, dry_run=dry_run)

    return 0


def validate(target_root: Path | None) -> int:
    manifest = load_manifest()
    errors: list[str] = []

    errors.extend(validate_manifest_contract(manifest))

    for rel in manifest.get("syncable_paths", []) + manifest.get("bootstrap_only_paths", []):
        path = TEMPLATE_DIR / rel
        if not path.exists():
            errors.append(f"missing template path: {path}")

    if target_root is not None:
        target_root = target_root.resolve()
        for rel in manifest.get("syncable_paths", []):
            path = target_root / rel
            if not path.exists():
                errors.append(f"missing instance path: {path}")

        state_path = target_root / INSTANCE_STATE_FILE
        if state_path.exists():
            try:
                state = load_instance_state(target_root)
            except ValueError as exc:
                errors.append(str(exc))
            else:
                syncable_paths = {
                    normalize_rel_path(path)
                    for path in manifest.get("syncable_paths", [])
                }
                stale_paths = sorted(set(state["managed_files"]) - syncable_paths)
                for rel in stale_paths:
                    path = target_root / rel
                    status = "present" if path.exists() else "missing"
                    errors.append(f"stale managed path in state ({status}): {path}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"template ok: {TEMPLATE_DIR}")
    if target_root is not None:
        print(f"instance ok: {target_root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Operate on workspace template instances.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap_parser = subparsers.add_parser("bootstrap", help="Create a workspace instance.")
    bootstrap_parser.add_argument("target", help="Path to the workspace instance root.")
    bootstrap_parser.add_argument("--dry-run", action="store_true")
    bootstrap_parser.add_argument("--force", action="store_true")

    sync_parser = subparsers.add_parser("sync", help="Sync template-managed files.")
    sync_parser.add_argument("target", help="Path to the workspace instance root.")
    sync_parser.add_argument("--dry-run", action="store_true")
    sync_parser.add_argument("--force", action="store_true")

    validate_parser = subparsers.add_parser("validate", help="Validate the template and optional instance.")
    validate_parser.add_argument("--target", help="Optional workspace instance root to validate.")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "bootstrap":
        return bootstrap(Path(args.target), dry_run=args.dry_run, force=args.force)
    if args.command == "sync":
        return sync(Path(args.target), dry_run=args.dry_run, force=args.force)
    if args.command == "validate":
        target = Path(args.target) if args.target else None
        return validate(target)

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
