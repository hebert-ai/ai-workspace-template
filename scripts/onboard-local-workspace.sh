#!/usr/bin/env bash

set -euo pipefail

TEMPLATE_REPO="hebert-ai/ai-workspace-template"
WORKSPACE_PATH="$PWD"
BACKUP_PATH=""
MIGRATE_FROM=""
WORKSPACE_REPO=""
GITHUB_USER=""
OWNER=""
RUN_SETUP=true
DRY_RUN=false
ASSUME_YES=false
SKIP_CUSTOM=false
SKIP_PROJECTS=false

usage() {
  cat <<'EOF'
Usage:
  Run this script from the directory that should become the workspace root.

  bash scripts/onboard-local-workspace.sh [options]

Options:
  --github-user USER           GitHub username used in the derived repo name.
  --owner OWNER                GitHub owner for the workspace repo. If omitted, the script
                               will prompt using the authenticated user and available orgs.
  --workspace-repo OWNER/REPO  Full repo name override. If omitted, the script derives
                               workspace-<github-user>-<workspace-name>.
  --workspace-path PATH        Workspace path. Default: current directory.
  --backup-path PATH           Backup path override. Default:
                               <parent>/<workspace-name>-backup-<timestamp>
  --migrate-from PATH          Source path to copy custom/ and projects/ from.
                               If omitted and a backup is created, the backup path is used.
  --template-repo OWNER/REPO   Template repo used when creating the workspace repo.
                               Default: hebert-ai/ai-workspace-template
  --skip-setup                 Do not run scripts/setup-workspace.sh in the new workspace.
  --skip-custom                Do not migrate custom/.
  --skip-projects              Do not migrate projects/.
  --yes                        Skip confirmation prompts.
  --dry-run                    Print actions without executing them.
  -h, --help                   Show this help.
EOF
}

log() {
  printf '%s\n' "$*"
}

fail() {
  printf '%s\n' "$*" >&2
  exit 1
}

run_cmd() {
  if [[ "${DRY_RUN}" == true ]]; then
    printf '+'
    printf ' %q' "$@"
    printf '\n'
    return 0
  fi
  "$@"
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "Missing required command: $1"
}

slugify() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/-+/-/g'
}

timestamp_utc() {
  date -u +"%Y%m%d-%H%M%S"
}

current_github_user() {
  gh api user --jq .login
}

list_orgs() {
  gh org list --limit 100
}

repo_exists() {
  gh repo view "$1" >/dev/null 2>&1
}

choose_owner() {
  local personal="$1"
  local orgs
  local choices=()
  local index=1
  local selection
  local value

  choices+=("${personal}")
  while IFS= read -r value; do
    [[ -n "${value}" ]] || continue
    choices+=("${value}")
  done < <(list_orgs)

  log "Choose where to create the workspace repo:"
  for value in "${choices[@]}"; do
    if [[ "${value}" == "${personal}" ]]; then
      printf '  %d) %s (personal)\n' "${index}" "${value}"
    else
      printf '  %d) %s (org)\n' "${index}" "${value}"
    fi
    index=$((index + 1))
  done

  while true; do
    read -r -p "Owner [1-${#choices[@]}]: " selection
    [[ "${selection}" =~ ^[0-9]+$ ]] || { log "Enter a number."; continue; }
    if (( selection >= 1 && selection <= ${#choices[@]} )); then
      printf '%s\n' "${choices[$((selection - 1))]}"
      return 0
    fi
  done
}

confirm() {
  local prompt="$1"
  if [[ "${ASSUME_YES}" == true ]]; then
    return 0
  fi
  read -r -p "${prompt} [y/N]: " reply
  [[ "${reply}" == "y" || "${reply}" == "Y" ]]
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --github-user)
      GITHUB_USER="${2:-}"
      shift 2
      ;;
    --owner)
      OWNER="${2:-}"
      shift 2
      ;;
    --workspace-repo)
      WORKSPACE_REPO="${2:-}"
      shift 2
      ;;
    --workspace-path)
      WORKSPACE_PATH="${2:-}"
      shift 2
      ;;
    --backup-path)
      BACKUP_PATH="${2:-}"
      shift 2
      ;;
    --migrate-from)
      MIGRATE_FROM="${2:-}"
      shift 2
      ;;
    --template-repo)
      TEMPLATE_REPO="${2:-}"
      shift 2
      ;;
    --skip-setup)
      RUN_SETUP=false
      shift
      ;;
    --skip-custom)
      SKIP_CUSTOM=true
      shift
      ;;
    --skip-projects)
      SKIP_PROJECTS=true
      shift
      ;;
    --yes)
      ASSUME_YES=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail "Unknown argument: $1"
      ;;
  esac
done

require_command git
require_command gh
require_command cp
require_command mv
require_command mkdir
require_command bash
require_command date
require_command sed
require_command tr

WORKSPACE_PATH="$(cd "$(dirname "${WORKSPACE_PATH}")" && pwd)/$(basename "${WORKSPACE_PATH}")"
workspace_parent="$(dirname "${WORKSPACE_PATH}")"
workspace_name="$(basename "${WORKSPACE_PATH}")"
workspace_slug="$(slugify "${workspace_name}")"

[[ -n "${workspace_slug}" ]] || fail "Could not derive a valid workspace name from: ${WORKSPACE_PATH}"
[[ "${WORKSPACE_PATH}" != "/" ]] || fail "Refusing to operate on /"
[[ "${WORKSPACE_PATH}" != "${HOME}" ]] || fail "Refusing to operate on \$HOME directly"

if [[ -z "${GITHUB_USER}" ]]; then
  GITHUB_USER="$(current_github_user)"
fi

if [[ -z "${OWNER}" ]]; then
  OWNER="$(choose_owner "${GITHUB_USER}")"
fi

if [[ -z "${WORKSPACE_REPO}" ]]; then
  WORKSPACE_REPO="${OWNER}/workspace-${GITHUB_USER}-${workspace_slug}"
fi

if [[ -z "${BACKUP_PATH}" ]]; then
  BACKUP_PATH="${workspace_parent}/${workspace_name}-backup-$(timestamp_utc)"
fi

[[ "${WORKSPACE_PATH}" != "${BACKUP_PATH}" ]] || fail "--workspace-path and --backup-path must differ"

backup_created=false
if [[ -e "${WORKSPACE_PATH}" ]]; then
  [[ ! -e "${BACKUP_PATH}" ]] || fail "Backup path already exists: ${BACKUP_PATH}"
fi

cat <<EOF
Workspace onboarding plan

Current directory:
  ${PWD}

Workspace path:
  ${WORKSPACE_PATH}

Workspace name:
  ${workspace_name}

GitHub user:
  ${GITHUB_USER}

Workspace repo:
  ${WORKSPACE_REPO}

Template repo:
  ${TEMPLATE_REPO}

Workspace repo visibility:
  private

Backup path:
  ${BACKUP_PATH}

Migration source:
  ${MIGRATE_FROM:-"(will use backup if created)"}
EOF

confirm "Continue?" || fail "Aborted."

if repo_exists "${WORKSPACE_REPO}"; then
  log "Workspace repo already exists on GitHub: ${WORKSPACE_REPO}"
else
  log "Creating private workspace repo from template: ${WORKSPACE_REPO}"
  run_cmd gh repo create "${WORKSPACE_REPO}" --private --template "${TEMPLATE_REPO}"
fi

if [[ -e "${WORKSPACE_PATH}" ]]; then
  log "Backing up existing workspace: ${WORKSPACE_PATH} -> ${BACKUP_PATH}"
  run_cmd mv "${WORKSPACE_PATH}" "${BACKUP_PATH}"
  backup_created=true
fi

if [[ -z "${MIGRATE_FROM}" && "${backup_created}" == true ]]; then
  MIGRATE_FROM="${BACKUP_PATH}"
fi

run_cmd mkdir -p "${workspace_parent}"

log "Cloning workspace repo to: ${WORKSPACE_PATH}"
run_cmd git clone "https://github.com/${WORKSPACE_REPO}.git" "${WORKSPACE_PATH}"

if [[ -n "${MIGRATE_FROM}" ]]; then
  if [[ "${DRY_RUN}" != true ]]; then
    [[ -d "${MIGRATE_FROM}" ]] || fail "Migration source does not exist: ${MIGRATE_FROM}"
  fi

  if [[ "${SKIP_CUSTOM}" == false && ( "${DRY_RUN}" == true || -d "${MIGRATE_FROM}/custom" ) ]]; then
    log "Migrating custom/: ${MIGRATE_FROM}/custom -> ${WORKSPACE_PATH}/custom"
    run_cmd rm -rf "${WORKSPACE_PATH}/custom"
    run_cmd cp -R "${MIGRATE_FROM}/custom" "${WORKSPACE_PATH}/custom"
  fi

  if [[ "${SKIP_PROJECTS}" == false && ( "${DRY_RUN}" == true || -d "${MIGRATE_FROM}/projects" ) ]]; then
    log "Migrating projects/: ${MIGRATE_FROM}/projects -> ${WORKSPACE_PATH}/projects"
    run_cmd rm -rf "${WORKSPACE_PATH}/projects"
    run_cmd cp -R "${MIGRATE_FROM}/projects" "${WORKSPACE_PATH}/projects"
  fi
fi

if [[ "${RUN_SETUP}" == true ]]; then
  log "Running workspace setup"
  run_cmd bash "${WORKSPACE_PATH}/scripts/setup-workspace.sh"
fi

cat <<EOF

Workspace onboarding complete.

Workspace repo:
  ${WORKSPACE_REPO}

Workspace path:
  ${WORKSPACE_PATH}

Backup path:
  ${BACKUP_PATH}

Recommended next steps:
  cd ${WORKSPACE_PATH}
  make check
  git status --short
EOF
