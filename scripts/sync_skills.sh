#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

install_skill() {
  local skill_name="$1"
  local src="$repo_root/skills/$skill_name/SKILL.md"

  if [[ ! -f "$src" ]]; then
    echo "missing source skill: $src" >&2
    exit 1
  fi

  local targets=(
    "$HOME/.codex/skills/$skill_name/SKILL.md"
    "$HOME/.hermes/skills/productivity/$skill_name/SKILL.md"
    "$HOME/.hermes/profiles/ds/skills/productivity/$skill_name/SKILL.md"
  )

  for target in "${targets[@]}"; do
    mkdir -p "$(dirname "$target")"
    cp "$src" "$target"
    echo "synced $skill_name -> $target"
  done
}

install_skill "daily-manager"
install_skill "personal-feishu-interface"
install_skill "calendar-sync"

# Hermes rebuilds this snapshot on demand; clearing it prevents stale skill text.
rm -f "$HOME/.hermes/profiles/ds/.skills_prompt_snapshot.json"

echo "done"
