#!/usr/bin/env bash
# Extract readable text from a source file regardless of how it is packaged.
# Handles: ZIP archives of page text (Grokking "PDFs"), plain text files with a .pdf
# extension (the Xu book), and real PDFs (via pdftotext).
# Usage: extract_source.sh <input> <output.txt>
set -euo pipefail
in="$1"; out="$2"
kind=$(file -b "$in")
case "$kind" in
  *"Zip archive"*)
    tmp=$(mktemp -d)
    unzip -q "$in" -d "$tmp"
    # Page files are 1.txt, 2.txt ... — concatenate in numeric order, strip CRs
    for f in $(ls "$tmp"/*.txt | sed 's#.*/##' | sort -n); do
      printf '\n===== page %s =====\n' "${f%.txt}"
      cat "$tmp/$f"
    done | tr -d '\r' > "$out"
    rm -rf "$tmp";;
  *"PDF document"*)
    pdftotext -layout "$in" "$out";;
  *)
    tr -d '\r' < "$in" > "$out";;
esac
echo "wrote $out ($(wc -l < "$out") lines)"
