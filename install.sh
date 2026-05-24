#!/usr/bin/env bash
# install.sh — Install claude-evp skill ecosystem
# Usage: curl -fsSL https://raw.githubusercontent.com/cmj-hub/claude-evp/main/install.sh | bash

set -euo pipefail

REPO_URL="https://github.com/cmj-hub/claude-evp"
SKILLS_DIR="${HOME}/.claude/skills"

if ! command -v git >/dev/null 2>&1; then
    echo "ERROR: git is required but not installed." >&2
    exit 1
fi

mkdir -p "$SKILLS_DIR"
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

echo "Installing claude-evp..."
git clone --depth 1 "$REPO_URL" "$TEMP_DIR" >/dev/null 2>&1

echo "  + evp (orchestrator)"
rm -rf "$SKILLS_DIR/evp"
cp -r "$TEMP_DIR/evp" "$SKILLS_DIR/"

for skill_dir in "$TEMP_DIR/skills"/evp-*; do
    if [[ -d "$skill_dir" ]]; then
        skill_name=$(basename "$skill_dir")
        rm -rf "${SKILLS_DIR:?}/$skill_name"
        cp -r "$skill_dir" "$SKILLS_DIR/"
        echo "  + $skill_name"
    fi
done

echo ""
echo "Done. Restart Claude Code to pick up the new skill."
echo ""
echo "Try it:"
echo "  > Write an EVP for <ICP> in <pain>, Tier 3 (solution-aware)"
echo ""
echo "Course:  https://jaymountconsulting.com/learn/courses/evp-generator"
echo "Source:  $REPO_URL"
