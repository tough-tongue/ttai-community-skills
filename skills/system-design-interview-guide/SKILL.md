---
name: system-design-interview-guide
description: Build system design interview materials for a named problem (e.g. "Design Twitter Search", "Design a Rate Limiter", "Design Uber") from source books such as Alex Xu's System Design Interview and Grokking the System Design Interview, filling gaps with web research. Produces (1) a student-facing study guide — problem, why it is asked, real-world use, requirements, worked estimation, API/data model, architecture diagrams, deep dives, trade-off tables, practice questions with hint ladders, self-assessment checklist, glossary — rendered to a styled PDF, and (2) an interviewer-facing scenario context pack usable as input to a Tough Tongue AI (or similar) mock-interview scenario. Use this skill whenever the user asks for a reading guide, study material, context pack, scenario pack, interview prep doc, or "make a PDF like the last one" for any system design topic, mentions Xu/Grokking chapters, or wants to turn a system design chapter into an AI interview scenario — even if they don't say "guide" or "PDF".
---

# System Design Interview Guide

Turn one system design interview problem into two artefacts from the same research:

| Artefact | Audience | Format |
|---|---|---|
| **Study guide** | Candidates preparing for the question | Markdown → styled A4 PDF (~20–25 pages) |
| **Scenario context pack** | The AI interviewer / scenario author | Markdown (10 fixed sections); optionally published to Tough Tongue AI via `ttai:create_scenario` |

The work runs in two phases with an explicit checkpoint between them. Phase 1 ends with a draft the user reviews in chat. Phase 2 (PDF build, scenario publishing) starts only after the user says "go ahead" or equivalent. Skipping the checkpoint wastes minutes of rendering on a draft the user wanted changed.

## Phase 0 — Establish inputs (30 seconds, no tools unless needed)

Collect from the conversation, and ask only for what is missing:

1. **Topic** — the problem name. If ambiguous (e.g. "Twitter" could mean the feed, search, or ID service), ask.
2. **Sources** — the book chapters, PDFs, or notes the user has supplied (attached files, the project folder, or pasted text). Ask for them if none are provided; this skill works from material the user owns, not from memory of the books. Read `references/sources.md` for how to extract each file type and which chapter usually covers which topic. Use both books when both cover the topic; say which is primary.
3. **Which artefacts** — default to both. If the user only wants one, produce one.
4. **Scenario parameters** (only if publishing to Tough Tongue AI): persona name/level, number of suggestions/k, latency bar, scale numbers — else take them from the source.

Don't ask about things that are inferable; a sensible default stated in the draft is better than a question.

## Phase 1 — Research and draft

### 1.1 Extract the sources

Run the extraction scripts rather than reading ZIP/text by hand:

```bash
bash scripts/extract_source.sh <path/to/grokking_chapter.pdf> work/grok.txt
python3 scripts/extract_xu_chapter.py <path/to/xu_book.txt> "SEARCH AUTOCOMPLETE" > work/xu.txt
```

Read the extracted text fully. Note every number (QPS, storage, server counts), every named component, every follow-up the book raises, and any place the two books disagree. Disagreements go into the guide as explicit callouts — students get asked about them.

### 1.2 Identify gaps and research them

The books are thin in predictable places: API detail, data model, freshness/deletion pipelines, what happens after the "wrap-up" list. Check `references/gap_checklist.md` for the standard gap list per topic family. For each gap:

- Fill from general knowledge if it is textbook material (inverted indexes, consistent hashing, geohash).
- **Web-search** when the gap needs a real-world figure or a specific system (e.g. the published latency bar, Snowflake bit layout, how a named company actually did it). Prefer engineering blogs and papers; paraphrase, never quote at length; keep the source in the References section.
- Mark every section that goes beyond the books with **☆** and explain the mark once in the "How to use" intro. Readers must be able to tell canonical material from supplementation.

### 1.3 Write the study guide

Follow `references/study_guide_template.md` exactly for section order and content expectations — it is the contract that makes guides in the family look alike. Key rules:

- **Candidate voice.** "You should ask…", "interviewers listen for…". Interviewer probes become practice questions with H1/H2 hints and a covered answer; rubric rows become a two-column strong/weak self-assessment checklist; the timeline column says what the interviewer is listening for.
- **Source fidelity.** Preserve the books' exact numbers and the chain of arithmetic; show intermediate results in tables. Never "round to make it nicer".
- **Diagrams as Mermaid** in `diagrams/*.mmd`, referenced from the markdown as `![caption](diagrams/name.png)`. Always include: the main architecture, the write/build path if it differs from the read path, and one illustration of the core data structure or the central trade-off (a trie with cached lists, word- vs. document-sharding, a geohash grid). See `references/diagram_conventions.md` for the styling that renders well on A4.
- **Cross-reference the family.** Canonical homes for shared theory: fan-out and celebrity hot-keys → Newsfeed; TweetID/Snowflake sharding → Twitter; spatial indexing → Yelp; scatter-gather top-k → Yelp/Uber/Twitter Search. Cite the sibling guide rather than re-deriving.

Save to `<slug>/<slug>.md` in the working directory.

### 1.4 Write the scenario context pack

Follow `references/scenario_pack_template.md` (10 sections: what the system is; requirements Q&A script; estimation; API & data model; high-level design; deep dives; wrap-up; probe bank ~13 entries with L1/L2 hints; rubric signal guide; 45-minute timeline). It shares research with the study guide but keeps the interviewer voice ("let them state it, then probe…"). Save alongside as `<slug>_scenario_pack.md`.

### 1.5 Checkpoint

Share both markdown files with the user along with a short summary: primary source, what was supplemented (☆) and from where, any source discrepancies found, and the defaults you chose. Then stop and wait. Do not build the PDF yet.

## Phase 2 — Build (after the user's go-ahead)

Apply any edits requested, then:

```bash
bash scripts/render_diagrams.sh <slug>/diagrams
python3 scripts/build_pdf.py <slug>/<slug>.md \
    --title "Designing Twitter Search" \
    --subtitle "The inverted index, from sizing to sharding to recovery" \
    --meta "Difficulty=Medium" --meta "Primary source=Grokking, 'Designing Twitter Search'" \
    --meta "Cross-references=Xu Ch. 5, Ch. 7" --meta "Prepared for=Tough Tongue AI practice scenarios" \
    --out outputs/Designing_Twitter_Search.pdf
```

Build requirements: `pandoc`, `pdfinfo`/`pdftoppm` (poppler), Python Pillow, Google Chrome or Chromium, and `mmdc` (`npm i -g @mermaid-js/mermaid-cli`). Both scripts find Chrome automatically; set `CHROME_PATH` if it lives somewhere unusual.

`build_pdf.py` runs pandoc (TOC, cover), strips pandoc's title header, renders with headless Chrome, and writes a contact sheet next to the PDF. **View the contact sheet** before presenting: look for near-empty pages, diagrams pushed to their own page, tables split awkwardly. Fix by adjusting the markdown (move a paragraph, shrink a diagram width) and rebuild — do not hand-edit the HTML. Then share the PDF and the markdown source together.

### Publishing a scenario (only if asked)

If the user wants the scenario on Tough Tongue AI, load the `ttai:create_scenario` tool schema and read `references/tough_tongue_mapping.md` for how the pack's sections map to `ai_instructions`, `strategy.conductor.messages`, `rubrik`, `session_analysis.extraction_vars` and `pdf_context`. Confirm the organisational context (personal vs. an organization from `ttai:list_organizations`) before creating.

## Quality bar

Before the checkpoint, run through `references/quality_checklist.md`. The common failures: estimation without intermediate steps; probes copied verbatim instead of reframed; diagrams that only show the read path; supplementation not marked with ☆; a discrepancy between sources noticed in extraction but not surfaced in the guide.

## Files

- `references/sources.md` — how the source files are packaged and which chapter covers what
- `references/study_guide_template.md` — section-by-section contract for the study guide
- `references/scenario_pack_template.md` — the 10-section interviewer pack
- `references/gap_checklist.md` — what the books usually omit, by topic family
- `references/diagram_conventions.md` — Mermaid styling that renders cleanly on A4
- `references/tough_tongue_mapping.md` — pack → `create_scenario` field mapping
- `references/quality_checklist.md` — pre-checkpoint review
- `scripts/extract_source.sh`, `scripts/extract_xu_chapter.py`, `scripts/render_diagrams.sh`, `scripts/build_pdf.py`
- `assets/style.css`, `assets/cover_template.html`
