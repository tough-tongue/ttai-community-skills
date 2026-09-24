#!/usr/bin/env python3
"""Print one chapter of the Alex Xu text dump.

The Xu file is plain text (despite the .pdf name). Each chapter title appears twice:
once in the table of contents and once as the chapter heading. We take the second
occurrence and stop at the next chapter heading.

Usage: extract_xu_chapter.py <xu_file> "<part of chapter title>"
       extract_xu_chapter.py <xu_file> --list
"""
import re, sys

path, key = sys.argv[1], sys.argv[2]
lines = open(path, encoding="utf-8", errors="replace").read().replace("\r", "").split("\n")
heads = [(i, l) for i, l in enumerate(lines) if re.match(r"^CHAPTER \d+:", l)]

if key == "--list":
    seen = set()
    for i, l in heads:
        n = l.split(":")[0]
        if n not in seen:
            seen.add(n); print(l.strip())
    sys.exit()

matches = [(i, l) for i, l in heads if key.upper() in l.upper()]
if len(matches) < 2:
    sys.exit(f"chapter containing '{key}' not found twice (TOC + body); use --list")
start = matches[1][0]
chap = lines[start].split(":")[0]
later = [i for i, _ in heads if i > start and not lines[i].startswith(chap + ":")]
end = later[0] if later else len(lines)
print("\n".join(lines[start:end]))
