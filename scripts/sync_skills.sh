#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Sync a whole skill directory (SKILL.md + any bundled scripts) to every
# installed agent skill location. Repo skills/ stays the single source of truth.
install_skill() {
  local skill_name="$1"
  local src_dir="$repo_root/skills/$skill_name"

  if [[ ! -f "$src_dir/SKILL.md" ]]; then
    echo "missing source skill: $src_dir/SKILL.md" >&2
    exit 1
  fi

  local targets=(
    "$HOME/.codex/skills/$skill_name"
    "$HOME/.hermes/skills/productivity/$skill_name"
    "$HOME/.hermes/profiles/ds/skills/productivity/$skill_name"
    "$HOME/.workbuddy/skills/$skill_name"
  )

  for target in "${targets[@]}"; do
    mkdir -p "$target"
    # top-level files only (SKILL.md + bundled scripts); skip __pycache__/.DS_Store
    find "$src_dir" -maxdepth 1 -type f ! -name ".*" -exec cp {} "$target"/ \;
    echo "synced $skill_name -> $target"
  done
}

install_skill "daily-manager"
install_skill "personal-feishu-interface"
install_skill "calendar-sync"
install_skill "zju-mail"

# Hermes rebuilds this snapshot on demand; clearing it prevents stale skill text.
rm -f "$HOME/.hermes/profiles/ds/.skills_prompt_snapshot.json"

echo "done"
