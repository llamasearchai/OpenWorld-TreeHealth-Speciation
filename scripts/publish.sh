#!/usr/bin/env bash
set -euo pipefail

BRANCH="feat/repo-polish-and-agents"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "Not a git repository. Aborting." >&2
  exit 1
fi

current_branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$current_branch" != "$BRANCH" ]; then
  echo "Switching to $BRANCH" && git checkout "$BRANCH"
fi

echo "Pushing branch $BRANCH to origin..."
git push -u origin "$BRANCH"

if command -v gh >/dev/null 2>&1; then
  echo "Creating pull request via GitHub CLI..."
  gh pr create --fill --base main --title "Release 0.2.1: polish + OpenAI Agents" \
    --body "Prepares v0.2.1 with agents integration, security, logging, docs CI/Pages, plugin hardening, and branding."
  echo "Pull request created. Review and merge it in the browser."
else
  echo "GitHub CLI not found. Please open a PR for $BRANCH to main using the GitHub UI."
fi

echo "After merge, tag and push to trigger the Release workflow:"
echo "  make tag VERSION=0.2.1 && git push origin v0.2.1"

echo "Optionally set repo topics (tags) for discoverability (requires gh):"
echo "  gh repo edit --add-topic forestry --add-topic lidar --add-topic point-cloud --add-topic canopy-height-model --add-topic machine-learning --add-topic gis --add-topic fastapi --add-topic datasette --add-topic plugins --add-topic provenance --add-topic openai --add-topic agents"

echo "If not already enabled, set GitHub Pages to use GitHub Actions in repository Settings → Pages."

