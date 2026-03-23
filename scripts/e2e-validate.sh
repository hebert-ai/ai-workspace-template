#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE_DIR="$(mktemp -d /tmp/ai-workspace-template-e2e.XXXXXX)"
SAMPLE_REPO_DIR="$(mktemp -d /tmp/ai-workspace-template-sample.XXXXXX)"

cleanup() {
  rm -rf "${WORKSPACE_DIR}" "${SAMPLE_REPO_DIR}"
}
trap cleanup EXIT

assert_file() {
  local path="$1"
  if [[ ! -f "${path}" ]]; then
    echo "missing expected file: ${path}" >&2
    exit 1
  fi
}

assert_contains() {
  local path="$1"
  local expected="$2"
  if ! grep -Fq "${expected}" "${path}"; then
    echo "expected content not found in ${path}: ${expected}" >&2
    exit 1
  fi
}

echo "[1/7] Validate template contract"
python3 "${ROOT_DIR}/scripts/template_ops.py" validate

echo "[2/7] Bootstrap temp workspace and validate instance"
python3 "${ROOT_DIR}/scripts/template_ops.py" bootstrap "${WORKSPACE_DIR}" >/dev/null
python3 "${ROOT_DIR}/scripts/template_ops.py" validate --target "${WORKSPACE_DIR}" >/dev/null

echo "[3/7] Run generated workspace checks"
make -C "${WORKSPACE_DIR}" check >/dev/null

echo "[4/7] Scaffold a fresh project"
python3 "${WORKSPACE_DIR}/scripts/new-project.py" "Fresh Project" "Ship initial plan" >/dev/null
assert_file "${WORKSPACE_DIR}/projects/fresh-project/PROJECT.md"
assert_contains "${WORKSPACE_DIR}/projects/fresh-project/PROJECT.md" "Ship initial plan"

echo "[5/7] Clone and onboard an existing repo"
git init -b main "${SAMPLE_REPO_DIR}" >/dev/null
printf '# Sample Repo\n' > "${SAMPLE_REPO_DIR}/README.md"
printf '# Existing Agent Rules\n' > "${SAMPLE_REPO_DIR}/AGENTS.md"
git -C "${SAMPLE_REPO_DIR}" add . >/dev/null
git -C "${SAMPLE_REPO_DIR}" -c user.name='Test User' -c user.email='test@example.com' commit -m 'init' >/dev/null

python3 "${WORKSPACE_DIR}/scripts/clone-project.py" "${SAMPLE_REPO_DIR}" --slug sample-repo --name "Sample Repo" --goal "Adopt workspace conventions" >/dev/null
assert_file "${WORKSPACE_DIR}/projects/sample-repo/PROJECT.md"
assert_contains "${WORKSPACE_DIR}/projects/sample-repo/AGENTS.md" "# Existing Agent Rules"
assert_contains "${WORKSPACE_DIR}/projects/sample-repo/PROJECT.md" "Adopt workspace conventions"

echo "[6/7] Verify setup restores missing status starter files"
rm -f \
  "${WORKSPACE_DIR}/custom/status/README.md" \
  "${WORKSPACE_DIR}/custom/status/projects.md" \
  "${WORKSPACE_DIR}/custom/status/priorities.md"
bash "${WORKSPACE_DIR}/scripts/setup-workspace.sh" >/dev/null
assert_file "${WORKSPACE_DIR}/custom/status/README.md"
assert_file "${WORKSPACE_DIR}/custom/status/projects.md"
assert_file "${WORKSPACE_DIR}/custom/status/priorities.md"

echo "[7/7] Verify legacy-safe validation and custom preservation on forced bootstrap"
printf 'user-owned\n' > "${WORKSPACE_DIR}/custom/AGENTS.md"
rm -f "${WORKSPACE_DIR}/custom/status/projects.md" "${WORKSPACE_DIR}/custom/status/priorities.md"
python3 "${ROOT_DIR}/scripts/template_ops.py" validate --target "${WORKSPACE_DIR}" >/dev/null
python3 "${ROOT_DIR}/scripts/template_ops.py" bootstrap "${WORKSPACE_DIR}" --force >/dev/null
assert_contains "${WORKSPACE_DIR}/custom/AGENTS.md" "user-owned"

echo "e2e validation passed"
