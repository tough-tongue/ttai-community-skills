---
name: pm-scenario-builder
description: >-
  Turn any PM interview case study (pasted text, URL, or blog/book excerpt)
  into a Tough Tongue AI mock-interview scenario. Classifies the case into one
  of six PM question types (Product Design, Product Strategy, Analytical,
  Execution, Technical, Behavioral), authors a full reference solution
  following that type's approach, and creates the scenario with
  ttai:create_scenario. Use when the user says "turn this case into a
  scenario", "make a PM scenario", "build a PM interview scenario", "PM mock
  interview for...", or pastes a PM case question or case study.
---

# PM Scenario Builder

> Classify → load type file → author the solution → draft the payload →
> confirm → create via MCP → return the practice link.

One case in, one Tough Tongue AI scenario out: an AI interviewer that runs the
case candidate-led, a study guide with a full worked answer, and a weighted
hire/no-hire rubric.

Requires the **Tough Tongue AI (ttai)** MCP server. For general field
semantics, the **toughtongue:scenario-creator** skill's
`references/scenario-fields.md` is the companion reference.

## Workflow

### Step 1 — Ingest

- Pasted case question only → you author a new walkthrough in Step 4.
- Pasted blog/book excerpt with a worked solution → **adapt that solution**,
  don't invent a conflicting one. Preserve the author's specific numbers,
  segment choices, and named features.
- URL → fetch it, extract the case question + any reference solution.

### Step 2 — Classify

Use this table. State the type + subtype to the user before drafting.

| Type | Signals | Subtypes |
| --- | --- | --- |
| **Product Design** | "design X", "improve X", "favorite product", hypothetical tech ("Google built an API that...") | improvement · new/moonshot · creative-brainstorm · favorite-product |
| **Product Strategy** | "3-year strategy", "should X enter Y", pricing, GTM, "as CEO/PM leader..." | general · market-entry · new-opportunity · pricing/GTM |
| **Analytical** | "define success metrics", "estimate...", "what A/B tests..." | metrics · estimation · A/B |
| **Execution** | "X dropped by N%, why?", "should we ship A or B", root-cause, decision-making | RCA · tradeoff |
| **Technical** | "design a [system]", "what happens when you type a URL", coding/algo | system-design · tech-101 · experience |
| **Behavioral** | "tell me about a time", "why this company", "what would you do if" | pitch · fit · STAR · hypothetical |

Hybrid cases (e.g. "How would you improve ChatGPT?" — Design wrapped in
Strategy) → primary type wins the structure; borrow flavor from the other
file (e.g. use Strategy's market-forces analysis inside a Design case).

If the type is genuinely ambiguous, ask the user ONE question rather than
guessing.

### Step 3 — Load references

Always read [references/scenario-payload.md](references/scenario-payload.md).
Then read the matching type file:

| Type | File |
| --- | --- |
| Product Design | [references/product-design.md](references/product-design.md) |
| Product Strategy | [references/product-strategy.md](references/product-strategy.md) |
| Analytical (metrics/estimation/A-B) | [references/analytical.md](references/analytical.md) |
| Execution (RCA/tradeoff) | [references/execution.md](references/execution.md) |
| Technical or Behavioral | [references/other.md](references/other.md) |

### Step 4 — Author the reference solution

Write the full worked solution FIRST, following that type's approach and
quality bar from the reference file. This is the hardest part — it becomes
both the candidate-facing walkthrough and the interviewer's hidden answer key.

Non-negotiable across all types:

- **Frameworks are 50% of a good answer.** The other 50% is real-PM
  judgment, opinions, and — for Design especially — at least one genuinely
  creative (10X) idea. A mechanically framework-following answer with zero
  original thinking is a weak reference solution.
- Ground everything in specifics: named segments (not "millennials"), named
  features (not "a mobile app"), real numbers for estimation/metrics.
- Never propose an already-shipped feature as "new."

### Step 5 — Draft the two instruction fields

Both fields tell the SAME solution at different resolutions. Build
`user_instructions` first (full detail), then compress it into
`ai_instructions` (interviewer's hidden answer key + phase probes).

**`user_instructions` skeleton:**

1. Role + exact case question, verbatim
2. Why this case is hard / the interviewer's mindset (1 short paragraph)
3. Timed approach — the type's steps, each with a "why this matters" and a
   "common mistake"
4. **Full reference solution** — a complete worked answer, not a bullet list
   of topics to cover
5. Tips + what-not-to-do, using ❌ / ✅ pairs
6. Closing line: this is a guide, not the only path — thinking process is
   what's evaluated

**`ai_instructions` skeleton:**

1. Persona: company, seniority, what this interviewer values (2-4 bullets)
2. The `## Interview Approach - CRITICAL` block (copy verbatim from
   [references/scenario-payload.md](references/scenario-payload.md) — candidate-led, never force the framework)
3. `## The Interview Case` — primary question, then `### Expected Solution
   Framework (For Your Reference Only)` and `### Reference Solution (Do Not
   Share Directly)` — the compressed answer key
4. `## Interview Structure` — phases with time ranges, probing questions,
   "context to share ONLY when asked", good-answer traits
5. Opening: greet → present the case verbatim → **open Notepad via the
   Notepad tool** → invite clarifying questions
6. `## Interview Techniques` — when-stuck prompts, probing questions by
   phase, red flags, green flags
7. `## Session Management` — notepad + card usage, end_session timing

RCA/tradeoff cases get one more rule (see references/execution.md): the AI
stays in a data-analyst/stakeholder character and only reveals data for
specific, precise asks — never a proactive info-dump.

### Step 6 — Build the payload and confirm

Assemble `scenario_data` from the defaults in
[references/scenario-payload.md](references/scenario-payload.md), plus:

- `name`: `"PM Interview: {Type} - {Case Name}"` or
  `"{Company} PM Interview: {Case Name}"` when the company is the hook.
- `user_metadata.question_type` set to the classified type;
  `user_metadata.track: "Product Manager"`.
- The two instruction fields and the `rubrik` from Steps 4-5.

Before creating, call `ttai:list_organizations`. If the user belongs to an
organization, ask whether the scenario is personal or for the team, and pass
`org_id` on every call if it is for the team.

Show the user a short summary: classified type + subtype, the case question,
the reference solution's headline answer, the rubric categories and weights,
and public vs. private. Create only after they confirm (or if they already
said "just create it").

### Step 7 — Validate

- [ ] `user_instructions` contains a full worked solution, not just headings
- [ ] `ai_instructions` has the CRITICAL candidate-led block
- [ ] Notepad opening is explicit in the Opening phase
- [ ] `rubrik` has weighted categories summing to 100% + 4 hire tiers
- [ ] No feature is pitched as "new" when the reference solution says it
      already exists
- [ ] At least one idea in the solution is genuinely creative, not just
      the obvious first answer (Design cases especially)
- [ ] `tools_config` / `strategy` / `session_analysis` match
      references/scenario-payload.md (Technical cases: `mermaid` on)

### Step 8 — Create and deliver

1. `ttai:create_scenario` with `scenario_data` (and `org_id` if applicable).
2. Re-fetch with `ttai:get_scenario` and confirm the instructions, rubric,
   and `tools_config` landed as authored.
3. Return the practice link `https://app.toughtongueai.com/run/<id>` and the
   embed link `https://app.toughtongueai.com/embed/<id>`.
4. Offer a test run. If the interviewer drifts (forces the framework,
   info-dumps data in an RCA case, skips the Notepad), fix it with the
   **toughtongue:scenario-refiner** skill.

## Hard rules

- Never create the scenario before the user has seen the Step 6 summary,
  unless they asked you to skip the review.
- Never reproduce large verbatim blocks from a copyrighted book or blog in
  the scenario. Adapt the solution in your own words and keep the source's
  numbers, segment choices, and named features.
- Don't edit an existing scenario with this skill. That's a different job:
  point the user at **toughtongue:scenario-refiner**.

## Key Files

- [references/scenario-payload.md](references/scenario-payload.md) — field
  defaults, tools config, CRITICAL block text, rubrik shape
- [references/product-design.md](references/product-design.md)
- [references/product-strategy.md](references/product-strategy.md)
- [references/analytical.md](references/analytical.md) — metrics ·
  estimation · A/B testing
- [references/execution.md](references/execution.md) — root-cause analysis ·
  tradeoff decisions
- [references/other.md](references/other.md) — technical · behavioral
