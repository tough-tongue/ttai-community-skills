#!/usr/bin/env bash
# Render every diagrams/*.mmd to PNG with mermaid-cli (mmdc).
# Usage: render_diagrams.sh <diagrams_dir> [width]
# Uses $CHROME_PATH (or an auto-detected Chrome/Chromium) when set; otherwise
# mmdc falls back to its own bundled browser.
set -euo pipefail
dir="$1"; width="${2:-1600}"
chrome="${CHROME_PATH:-}"
if [ -z "$chrome" ]; then
  for c in google-chrome google-chrome-stable chromium chromium-browser \
           "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "/Applications/Chromium.app/Contents/MacOS/Chromium"; do
    if command -v "$c" >/dev/null 2>&1; then chrome="$(command -v "$c")"; break; fi
    if [ -x "$c" ]; then chrome="$c"; break; fi
  done
fi
cfg=()
if [ -n "$chrome" ]; then
  pcfg="$(mktemp)"; trap 'rm -f "$pcfg"' EXIT
  printf '{"executablePath":"%s","args":["--no-sandbox","--disable-gpu","--disable-dev-shm-usage"]}\n' "$chrome" > "$pcfg"
  cfg=(-p "$pcfg")
fi
for f in "$dir"/*.mmd; do
  out="${f%.mmd}.png"
  mmdc ${cfg[@]+"${cfg[@]}"} -i "$f" -o "$out" -w "$width" -s 2 -b white >/dev/null 2>&1 \
    && echo "rendered $out" || { echo "FAILED $f"; exit 1; }
done
