#!/usr/bin/env bash
# Link every skill in this repo into your local agents' skill folders, so edits
# here take effect immediately in Claude Code, Cursor, Codex, and other agents
# that read ~/.agents/skills. Re-run after adding a skill.
#
# Anything already at a target path (a personal copy, or a link to somewhere
# else) is moved to ~/.skills-backup/<timestamp>/, never deleted.
#
# Usage: scripts/link-local.sh [--dry-run]
# Target folders: $SKILL_DIRS (space-separated) or, by default, whichever of
# ~/.agents/skills ~/.claude/skills ~/.cursor/skills exist.
set -euo pipefail

dry=""
[ "${1:-}" = "--dry-run" ] && dry=1
repo_skills="$(cd "$(dirname "$0")/../skills" && pwd -P)"
backup="$HOME/.skills-backup/$(date +%Y%m%d-%H%M%S)"

dirs=()
for d in ${SKILL_DIRS:-"$HOME/.agents/skills" "$HOME/.claude/skills" "$HOME/.cursor/skills"}; do
  [ -d "$d" ] && dirs+=("$d")
done
[ ${#dirs[@]} -gt 0 ] || { echo "No skill folders found"; exit 1; }

run() { if [ -n "$dry" ]; then echo "  would: $*"; else "$@"; fi; }

for src in "$repo_skills"/*/; do
  name="$(basename "$src")"
  src="${src%/}"
  for d in "${dirs[@]}"; do
    target="$d/$name"
    if [ -L "$target" ] && [ "$(cd "$target" 2>/dev/null && pwd -P)" = "$src" ]; then
      echo "ok      $target"
      continue
    fi
    if [ -L "$target" ] || [ -e "$target" ]; then
      label="$(basename "$(dirname "$d")")"
      echo "backup  $target -> $backup/$label/$name"
      run mkdir -p "$backup/$label"
      run mv "$target" "$backup/$label/$name"
    fi
    echo "link    $target -> $src"
    run ln -s "$src" "$target"
  done
done
