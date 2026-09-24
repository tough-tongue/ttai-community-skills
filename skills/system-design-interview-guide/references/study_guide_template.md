# Study Guide Template (candidate-facing)

Use this section order. Headings are `#` for Parts and `##`/`###` inside. The build script gives every `#` heading a TOC entry and starts "Part 1" on a fresh page; everything else flows. Target 20–25 A4 pages.

Voice: second person, addressed to the candidate. Interviewer intent is always phrased as *what they are listening for*, never as instructions to the interviewer.

Mark any section or paragraph that goes beyond the source books with **☆** in its heading (or an inline "☆ note").

---

## `# How to Use This Guide`

- One paragraph: what problem, who it is for, which sources (name primary vs. secondary), what ☆ means.
- **Suggested reading path** — numbered, 5 steps, tells them to attempt estimation before reading it.
- **Difficulty** line + one sentence naming the 2–3 places where interview signal concentrates.
- If a sibling guide shares the skeleton (Yelp ↔ Twitter Search, Uber ↔ Yelp), say so here.

## `# Part 1 — The Problem`

- `## 1.1 What <system> is` — plain-language description; alternative names the question is asked under; what the product does for users.
- `## 1.2 ☆ Where this shows up in practice` — 3–5 real products/companies that run this system and the business reason it matters (why latency / freshness / correctness is worth engineering). Web-search if unsure; keep to one paragraph or a short list.
- `## 1.3 Why it is a good interview question` — 3–5 bullets on what it tests (a dominant data structure, opposite-shaped read/write paths, a forced trade-off, a non-trivial recovery story…).

## `# Part 2 — Requirements Clarification`

- `## 2.1 Questions to ask, and typical answers` — table `You should ask | Typical interviewer answer`. Include the scale numbers, the semantics questions, and at least one question the books leave open (freshness, history depth) with a note that asking it is a strong signal.
- `## 2.2 Requirements you should converge on` — **Functional** bullets, **Non-functional** bullets. Tie each non-functional to the design consequence it forces ("100 ms → in memory").
- A blockquote **Interview note** about the standard trap (e.g. "use Elasticsearch" / "SQL LIKE") and how to present it as a strawman.

## `# Part 3 — Back-of-the-Envelope Estimation`

- Lead with the *key insight* if there is one (keystroke multiplier, postings duplication, ×15).
- Tables with columns `Quantity | Calculation | Result`, bold results. Preserve the books' exact numbers; when the two books use different assumptions, give both as Variant A / Variant B and say which the scenario uses.
- Cross-reference callouts where a book's simplification diverges from reality (5-byte vs. 8-byte Snowflake IDs) in a blockquote.
- `## 3.x What to do with the numbers` / `What interviewers are listening for` — the conclusions the numbers license ("fits in memory", "tier hot/cold").

## `# Part 4 — High-Level Design`

- `## 4.1 API` — endpoint or function signature in a code block, parameter table, response example. If the book omits it, write one and mark ☆.
- `## 4.2 ☆ Data model` — table `Data | Shape | Where it lives`. Include a tiny worked example (three rows / three tweets / three nodes) that later sections can refer back to.
- `## 4.3 The strawman` (if the book has one) — show it, say why it breaks, name the replacement.
- `## 4.4 Decomposition` — the 2–3 subsystems and how their shapes differ.
- Diagram(s): main architecture; build/write pipeline if separate. Each followed by a **Components** list, one line per box: what it does and which deep-dive covers it.
- `## ☆ Life of a <request>` — numbered walkthrough of one read and (if different) one write, touching every component in order. This is the section students report as most useful; do not skip it.
- `## Whiteboard checklist` — 5–6 bullets of what the drawn diagram must show.

## `# Part 5 — Deep Dives`

Open with "Interviewers typically choose three; X, Y and Z are the most common." Then one `##` per deep dive, ordered by interview weight. Expect 5–8. Each should:

- state the problem in one sentence;
- give the naive answer and why it fails (with numbers where possible);
- give the book's answer, then any refinements;
- end with a comparison table when there are ≥2 competing schemes (sharding options, update strategies);
- include one diagram if the concept is spatial/structural (a trie, sharding comparison, geohash cells).

Always cover, where applicable: the core data structure and its complexity; the update/freshness pipeline; sharding/partitioning; deletion/content removal; persistence and recovery; caching and client behaviour; replication/failover; ranking.

## `# Part 6 — Trade-off Summary ☆`

Table `Decision | Chosen | Alternative | Why`, 6–9 rows, one per major design choice. This is the page students photograph.

## `# Part 7 — Extensions and Wrap-up Topics`

The books' actual follow-ups plus 2–3 sensible additions. One bullet each: the extension, why it is harder, a direction. Preface with "you are expected to know these exist and sketch a direction, not design them".

## `# Part 8 — Practice Questions`

12–14 questions reframed from the interviewer probe bank. Format:

```
**Q3. <probe as the interviewer would say it>**
- H1: <nudge>
- H2: <nearly the answer>        (omit H2, or both, for easy ones)
- *Answer:* <expected answer core in 1–3 sentences>
```

Include: one estimation probe, one "execute this query/request" probe, one failure/recovery probe, one deletion/policy probe, one early scoping trap ("just start building X"), one "your <component> is the bottleneck" probe, one stretch/real-time probe.

## `# Part 9 — Self-Assessment Checklist`

Two-column table `Strong signals | Weak signals / common mistakes`, each cell prefixed with ☐, rows paired so the weak signal is the failure mode of the strong one. 9–11 rows.

## `# Part 10 — Suggested 45-Minute Timeline`

Table `Time | Phase | What the interviewer is listening for`, 8 rows, referencing question numbers from Part 8.

## `# Glossary ☆`

10–14 terms, table `Term | Meaning`. Include the data-structure terms, the pattern names (scatter-gather, fan-out), and any book-specific coinages.

## `# References and Further Reading`

Primary chapter(s); sibling guides; Xu chapters used as building blocks; the book's own citations (engineering blogs, papers); anything web-searched for ☆ material.
