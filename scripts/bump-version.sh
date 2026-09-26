#!/usr/bin/env bash
# Bump the plugin version in every manifest at once, so Claude Code and Cowork
# users are offered the update.
#
# Usage: scripts/bump-version.sh [patch|minor|major|X.Y.Z]   (default: patch)
set -euo pipefail
cd "$(dirname "$0")/.."

python3 - "${1:-patch}" <<'EOF'
import json, re, sys

files = ["plugin.json", ".claude-plugin/plugin.json"]
current = {f: json.load(open(f))["version"] for f in files}
if len(set(current.values())) != 1:
    sys.exit(f"Manifest versions disagree, fix by hand first: {current}")

old = next(iter(current.values()))
major, minor, patch = map(int, old.split("."))
arg = sys.argv[1]
if arg == "patch":
    new = f"{major}.{minor}.{patch + 1}"
elif arg == "minor":
    new = f"{major}.{minor + 1}.0"
elif arg == "major":
    new = f"{major + 1}.0.0"
elif re.fullmatch(r"\d+\.\d+\.\d+", arg):
    new = arg
else:
    sys.exit("Usage: scripts/bump-version.sh [patch|minor|major|X.Y.Z]")

for f in files:
    text = open(f).read()
    text = re.sub(r'("version"\s*:\s*")[^"]+(")', rf"\g<1>{new}\g<2>", text, count=1)
    open(f, "w").write(text)
print(f"{old} -> {new}")
EOF
