---
name: case-interview-study-guide
description: >
  Turn a case-interview practice case (from a Kindle workbook, PDF casebook,
  or pasted text) into a detailed, phase-by-phase Word study guide: original
  notes and reference answers, plus any exhibit or graph recreated as a real
  chart. Use when the user asks for a study guide, notes, or write-up of a
  specific casebook case ("make notes on Case 4", "do the same for Case 7",
  "turn this case into a study guide").
---

# Case interview study guide builder

## Trigger

The user asks for a study guide, notes, or write-up of a specific case from a case-interview
workbook or casebook ("Can you make notes on Case 4", "do the same for Case 7", "turn this
case into a study guide"). Very often the source is a Kindle book open in the browser, where
text can't be selected or copied — but the same approach applies to a PDF casebook or pasted
case text.

This produces a **study aid with original analysis**, not a copy of the book. Never screenshot
the case pages into a PDF/doc as-is and call it done — that reproduces copyrighted material
wholesale. The deliverable is notes: your own "how to approach it" reasoning, the reference
answer restated and paraphrased, watch-outs, and (new) a properly rendered chart for any
exhibit — built from the facts and numbers in the case (data/figures aren't copyrightable;
the book's prose expression is what you must not reproduce).

If a user instead asks to screenshot/export a case wholesale as a PDF for reading — with no
request for notes/analysis — that's a copyright problem, not this skill: decline and offer this
study-guide treatment instead (see the docx skill's general copyright guidance).

## Steps

### 1. Locate the case

If the source is Kindle (read.amazon.com in the browser):
- Open the Table of Contents (icon in the top toolbar) and click the named case (e.g.
  "Practice Case #4 – GDS Systems") to jump straight to it — don't page through from the start.
- **Page-turning quirk**: a single click on the right-arrow nav control often does nothing (it
  just "wakes" the reader chrome). Use `double_click` on the arrow to reliably advance one page.
  Screenshot after every page turn — Kindle renders text as canvas/images, so `get_page_text`
  returns nothing useful; you must read pages visually.
- Read every page of the case start to finish (prompt → framework → each question → each
  "sample answer" page → conclusion) until the next case's title page appears, confirming the
  boundary. Don't stop early — the sample-answer and conclusion pages carry the reference
  answers and are the most valuable part of the case for this deliverable.
- For any chart/exhibit, `zoom` into the region to read axis labels, series values, and legend
  precisely — don't guess numbers. If the chart's own answer/explanation page clarifies an
  ambiguous reading (e.g. what a growth-rate column refers to), use that to confirm your
  transcription before building the recreated chart.

If the source is a PDF, use the **pdf** skill to extract text/tables directly instead of
screenshotting. If the user pastes the case text directly, skip extraction entirely.

### 2. Extract into buckets, verbatim on facts, never on prose

As you read, capture into: (a) the case prompt, (b) the sample framework, (c) each numbered
question, (d) each exhibit's exact data, (e) each reference/sample answer with its full
calculation steps, (f) the conclusion/recommendation. Numbers, figures, and data points are
facts — copy them exactly. Do not copy the book's sentences verbatim; you will rewrite the
explanatory prose yourself in step 4.

### 3. Recreate any exhibit as a real chart, not just a table

When a case includes a graph/chart exhibit (not just a data table), the visual shape is often
part of what the candidate is meant to interpret — preserve that.

1. Load the **dataviz** skill for the categorical palette and chart rules before writing any
   plotting code.
2. Build the chart with matplotlib (`Agg` backend), matching the source's chart type (stacked
   bar, line, etc.) and using the *exact* figures you transcribed. Use the dataviz reference
   palette's fixed categorical hue order (light-surface hexes: slot1 `#2a78d6` blue, slot2
   `#eb6834` orange, slot3 `#1baf7a` aqua, slot4 `#eda100` yellow, slot5 `#e87ba4` magenta —
   assign colors to series by identity, never by rank/position). Direct-label each segment/point
   with its value, add a legend, light gridlines, and a clear title ("Exhibit N — <name>").
   This is your own rendition of the underlying data, which is what makes it fair to recreate.
3. Save as PNG at 200 dpi, `Read` it back to eyeball for label collisions/overflow before
   embedding.
4. Embed via `ImageRun` in the docx (see step 5) sized to roughly page width, followed
   immediately by a compact exact-figures table (italic caption: "Exact figures, if you want to
   work from numbers rather than eyeballing the bars") — the reader needs both the visual
   pattern and precise numbers to actually solve the case.
5. If a case's exhibit is only a table in the source (no chart), a recreated table is enough —
   don't manufacture a chart that wasn't there.

### 4. Write the guide — this is the part to be diligent about

Load the **docx** skill, then build with the `docx` (npm) library. Structure, in order:

1. **Title block**: "Case Interview Study Guide" + "Practice Case #N — <name>", and an italic
   source line: *Source: <book title> (Practice Case #N, "<difficulty>" difficulty) — this guide
   is my own study notes and analysis built from that case, not a reproduction of the book's
   pages.*
2. **How to use this guide** — one short paragraph: read "Case at a glance" cold, build your own
   framework before looking, work each phase's math before checking the reference answer.
3. **Case at a glance** — client, situation/trigger, the ask, and difficulty with *why* (what
   skills this case actually drills).
4. **Suggested framework** — the case's bucketed structure with sub-questions as nested bullets,
   plus one sentence naming the throughline skill being tested.
5. **One section per phase/question**, named for its actual content (not "Question 1"), each with:
   - The prompt, paraphrased in your own words (short quotes under 15 words are fine).
   - Chart/table if this phase has an exhibit (per step 3).
   - **How to approach it** — the method, stated concretely and originally (your own
     explanation of the technique, not a restatement of the book's).
   - **Reference answer** — the book's numbers and conclusion, paraphrased into clean bullets
     with the arithmetic shown.
   - **Watch out** — 1–2 concrete traps specific to this phase (the mistake a candidate
     actually makes, and why it's wrong) — this is original commentary, add value beyond the book.
   - Occasionally **Extra angle worth adding** when there's a genuine value-add insight (e.g.
     tying a later phase's brainstorm back to an earlier exhibit's finding).
6. **Pulling it together — recommendation** — a synthesized closing recommendation that ties
   every phase back together, not a copy of the book's conclusion paragraph.
7. **General tips for this case** — what the difficulty rating implies about the bar, plus a
   suggested timing budget per phase if the user is using this for timed practice.
8. Closing italic disclaimer line matching the title block's spirit.

Use US Letter page size (12240×15840 DXA), a `bullets` numbering config (never literal `•`
characters), and small helper functions (`h1`, `h3`, `bullet`, `hr`) to keep the script
readable — see the docx skill for the `docx`-library gotchas (table dual widths, `ImageRun`
needs `type:`, no `\n`, etc).

### 5. Verify before sending

Render to PDF and page images, then `Read` every page image back:

```bash
python3 <docx-skill-dir>/scripts/office/soffice.py --headless --convert-to pdf out.docx
pdftoppm -jpeg -r 100 out.pdf page
```

Check: every number matches what you transcribed from the source; the chart (if any) renders
without collisions; headings and bullets render correctly; no stray placeholder text. Fix and
rebuild before delivering — don't send unseen output.

### 6. Deliver

Send the `.docx` to the user with a one-sentence caption naming the case and what's inside (not a
full recap — the user can open it). If this is part of a series ("do Case 3 too"), keep the
same structure and quality bar for consistency, and note once if a particular case has no
exhibit to recreate (nothing to add there, don't manufacture one).

## Verification checklist

- [ ] No page of the source was screenshotted into the deliverable — only extracted facts/numbers feed original prose
- [ ] Every number in the guide matches the source exactly (spot-check against your extraction notes)
- [ ] Any chart exhibit is a freshly rendered chart (dataviz palette, direct labels, legend) plus an exact-figures table, not a screenshot
- [ ] Every phase has How to approach it / Reference answer / Watch out, in the guide's own words
- [ ] Guide closes with a synthesized recommendation and general/timing tips
- [ ] Rendered to PDF and visually checked page-by-page before sending
- [ ] Delivered to the user with a one-line caption