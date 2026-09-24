---
name: system-design-interview-builder
description: >
  Turn system design interview material (YouTube transcripts, articles, book
  chapters, notes, URLs) into a complete Tough Tongue AI system design mock
  interview in the two-surface format: an interviewer-controlled notepad plus
  a candidate-owned architecture board. Authors the study guide, interviewer
  brain, hint ladder, and rubric, then creates the scenario with
  ttai:create_scenario. Use when the user says "create a system design
  interview", "turn this into a system design scenario", "new SDI for
  <question>", "board interview for <question>", or feeds interview prep
  material and asks for a scenario.
---

# System Design Interview Builder

Convert raw interview material into a production-quality system design
interview scenario for Tough Tongue AI: a 20-minute, candidate-led mock
interview where the candidate builds their design on a live architecture
board and the AI interviewer scribes requirements and capacity math on a
shared notepad.

Requires the **Tough Tongue AI (ttai)** MCP server.

**Read both reference files before drafting:**

- [references/authoring-guide.md](references/authoring-guide.md) — what makes
  each section good, the palette, the panel rule, the hint ladder.
- [references/template.yml](references/template.yml) — the annotated skeleton
  to fill in. Fixed blocks (tools_config, ai_model_config, etc.) are copied
  verbatim; never improvise them.

For a candidate-facing study guide PDF on the same question, use the
**system-design-interview-guide** skill instead (or first).

## Hard rules

1. **Confirm, then create.** Show the user the Step 4 summary before calling
   `ttai:create_scenario`, unless they asked you to skip the review. If they
   already have a scenario for this question (check with
   `ttai:list_scenarios` using the question name as the search text), offer
   to update it with `ttai:update_scenario` instead of creating a duplicate.
2. **Always two surfaces.** Every interview uses the agent-writable notepad
   plus the candidate-owned architecture board. No mermaid, no whiteboard.
3. **Palette-only components.** Every component named anywhere in the scenario
   must be a palette name (see authoring guide) or a `Note`. If the material
   uses another name (e.g. "ZooKeeper", "HBase"), map it to the nearest
   palette component and mention the real-world name in prose
   ("Cassandra (HBase at Messenger)").
4. **Fill gaps, flag them.** When the material is missing a section (capacity
   math, schema, failure story, variants), derive a sound version from model
   knowledge so the scenario is always complete — then flag it in the final
   report so the user can review exactly what was synthesized.
5. **Adapt, don't copy.** Rewrite source material in your own words. Keep
   the numbers and design decisions; never paste long passages from a book,
   article, or transcript into the scenario.

## Workflow

### Step 1: Ingest the material

Accept anything: pasted transcripts, markdown notes, book-chapter text, URLs
(fetch them), local files. Establish **the question** ("Design X"). Confirm
the title with the user only if genuinely ambiguous.

Then extract from the material, in this order of importance:

1. **The walk** — the single end-to-end trace that proves the design works
   (Messenger: "A sends 'hi' to B"; crawler: "one URL from frontier to
   store"; shortener: "one redirect"). Every scenario is built around one
   traceable operation.
2. **Design decisions** (3–7) — the forks in the road with real tradeoffs
   (protocol choice, SQL vs NoSQL, push vs pull, fan-out on write vs read…).
   These become the probing material. For each: the options, why the naive
   one fails, what a defensible answer sounds like.
3. **Requirements & defaults** — functional + scale numbers the interviewer
   states if the candidate skips scoping.
4. **Capacity math** — the 2–4 headline equations (throughput, storage,
   fleet size). Verify the arithmetic yourself; material often has errors.
5. **Reference architecture** — components (mapped to palette) and edges.
6. **Schema** — tables/keys, partition key, replication.
7. **Failure story** — what dies, what the recovery contract is.
8. **Scaling & wrap-up topics** — what breaks first at 10×, metrics,
   nice-to-have end topics.
9. **Equally defensible variants** — alternate stacks a candidate might
   propose that the interviewer must accept.

Anything not in the material: synthesize (rule 4).

### Step 2: Draft the scenario

Fill `references/template.yml` section by section, following
`references/authoring-guide.md` for craft. Order of drafting that works well:
reference solution first (it grounds everything), then `user_instructions`,
then `ai_instructions`, then the rubric, then the small fields.

### Step 3: Validate

Check every item; fix before creating:

- [ ] The walk is traceable through the reference graph — every hop in the
      numbered walk corresponds to a component + edge in the ASCII graph.
- [ ] Capacity arithmetic is correct and the same numbers appear consistently
      in user_instructions, ai_instructions, and the rubric.
- [ ] Every component name is a palette name; the "Board habits" line in
      ai_instructions lists only the palette entries this question needs.
- [ ] Each design decision appears three times, in different depth:
      taught in user_instructions ("Design choices interviewers probe"),
      condensed in ai_instructions ("Reference Solution — Do Not Share
      Directly"), and assessed in the rubric.
- [ ] ai_instructions contains: candidate-led CRITICAL block, one question
      per turn, the panel rule, the notepad opening brief (question-specific),
      the 5-phase structure with surface assignments and skippable phases,
      the 3-level hint ladder, a follow-up question bank, end_session in
      wrap-up.
- [ ] Notepad scaffolds use fill-in blanks with this question's actual
      equations, not Messenger's.
- [ ] Rubric weights sum to 100%, sections mirror the phases, and the
      Strong/Hire/Lean/No-Hire anchors are specific to this question (name
      the load-bearing component the way Messenger's names "WebSocket Server
      unprompted").
- [ ] Fixed blocks (tools_config, appearance, ai_model_config, strategy,
      session_analysis, memory, access flags) match the template verbatim;
      no `id` on create.
- [ ] Nothing tells the agent to recite; reference solution is marked
      "Do Not Share Directly".

### Step 4: Confirm with the user

Call `ttai:list_organizations`. If the user belongs to an organization, ask
whether the scenario is personal or for the team, and pass `org_id` on every
call if it is for the team.

Then show:

1. A 3–5 line summary of the interview (the walk, the deep dives chosen, the
   headline capacity numbers).
2. **Sourced vs synthesized table** — one row per major section
   (requirements, capacity, architecture, decisions, schema, failure,
   rubric anchors), with "from material" or "synthesized" and a one-line
   note on anything synthesized that deserves review.
3. Public vs. private (`is_public`), and whether they have an interviewer
   avatar image to use.

### Step 5: Create and deliver

1. `ttai:create_scenario` with the filled template as `scenario_data` (and
   `org_id` if applicable).
2. Re-fetch with `ttai:get_scenario` and confirm `tools_config` has
   `notepad`, `architecture_board`, and `end_session` registered and
   everything else off.
3. Return the practice link `https://app.toughtongueai.com/run/<id>` and the
   embed link `https://app.toughtongueai.com/embed/<id>`.
4. Offer a test run. If the interviewer recites the answer key, steals the
   screen from the board, or stacks questions, fix it with the
   **toughtongue:scenario-refiner** skill.
