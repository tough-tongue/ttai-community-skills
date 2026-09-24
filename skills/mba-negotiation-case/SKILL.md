---
name: mba-negotiation-case
description: >
  Turn a two-party negotiation case file (public facts + each side's private
  brief, optionally a hidden compatible-interest twist) into a Tough Tongue
  AI negotiation scenario. The AI plays a guarded counterpart with a resistance
  and phased-disclosure pattern; the student plays the other side. Use when
  the user provides an MBA-style negotiation case, a case study PDF/note, or
  says "turn this case into a negotiation scenario", "Ugli Orange style
  scenario", or "two-party negotiation exercise".
---

# MBA Negotiation Case

Turn a two-party negotiation case file into a Tough Tongue AI scenario where the
AI plays a guarded counterpart and the student has to work for every
disclosure. Intake → draft student brief → draft counterpart brief with
resistance/disclosure → configure model & strategy → rubric → produce →
validate.

Requires the **Tough Tongue AI (ttai)** MCP server. The worked example
throughout is the classic Ugli Orange case; see
[references/resistance-and-disclosure.md](references/resistance-and-disclosure.md).

## Workflow

### Step 1: Intake the case file

Read [references/case-file-intake.md](references/case-file-intake.md). Extract:

- The two roles, and which one the student plays vs which the AI plays
- Public facts identical to both sides
- Each side's private brief (constraints, budget, what they assume about
  the other side)
- An optional hidden compatible-interest twist (the "win-win" the student is
  meant to discover)
- Stated timing (prep time, conversation length)
- Any rubric or extraction variables the case file already defines

If two source documents disagree (a design note and a separate brief, say),
ask the user which is authoritative — do not guess or blend silently.

### Step 2: Ask only what the case file doesn't answer

Always check org context: call `ttai:list_organizations`, and if the user
belongs to an organization, ask whether the scenario is personal or for the
team (pass `org_id` on every call if so).

Ask only if unclear from the case file:

- Which role the student plays.

### Step 3: Draft `user_instructions` (student brief)

Structure, in order:

1. General information — public facts, word-for-word identical to what the
   AI instructions state.
2. Your private brief — this role's constraints, budget, what they've heard
   about the other side. Never the twist, never the other side's private
   facts.
3. Prepare before the session — 3-5 self-reflection prompts (what outcome do
   you need, what will you share vs protect, what are you assuming, what
   happens if this fails).
4. How to succeed — stay inside your authority, don't invent facts, stay
   calm under guardedness, what a useful agreement specifies.
5. What to expect — who opens, how guarded the counterpart is, duration.

### Step 4: Draft `ai_instructions` (counterpart brief)

Read [references/resistance-and-disclosure.md](references/resistance-and-disclosure.md)
first — it has the reusable Resistance Pattern and Guarded Disclosure Phases
this step applies.

Structure, in order:

1. Role/identity + tone (precise/formal/guarded — or whatever the case calls
   for; ground it in a real motive, not villainy).
2. General information — same public facts as the student brief, verbatim.
3. Private brief — true need/constraint, what they assume about the student,
   why they initiated the conversation (or didn't).
4. Opening — a bare greeting only, directive form ("Thank them for coming.
   Keep it to a short greeting. Then STOP and wait."). Never script a
   strategic question or frame the negotiation in the opening — let the
   student drive from turn one.
5. Resistance pattern (from the reference file, filled in for this case).
6. Guarded disclosure phases (from the reference file, filled in for this
   case) — including the pivotal-reveal rule.
7. Concession & stance — how the counterpart reacts to specific proposals
   (splits, joint bids, moral arguments).
8. Escalation & walk-away — what ends the session early (accusations,
   ultimatums, bad-faith moves) → `end_session`.
9. Closing — what a valid agreement must specify; never invent a third
   party's acceptance (e.g. a seller saying yes).
10. Limits — no invented facts, no false ceilings, never break character or
    reveal this is an exercise.

### Step 5: Model & technical defaults

- `ai_model_config`: Ocean `medium` by default (text, two-party case
  negotiation). Only switch to Landmass `cascade-01` if the user explicitly
  wants a live voice call.
- `appearance.voice` (only relevant if voice is used): male counterpart →
  `Puck`, female counterpart → `Aoede`.
- `strategy`:
  - `skip_auto_start: false` (the counterpart opens with the bare greeting
    from Step 4.4, which lives in `ai_instructions`)
  - `silence`: tuned to keep pressure on without advancing any disclosure
    phase or hinting at the pivotal reveal
  - `conductor`: one optional safety-valve nudge partway through (only if
    the case defines one, to prevent a total wash-out) plus a wrap-up
    message near the end asking for a final summary or acknowledged impasse
    — never instruct the agent to invent agreement
  - `max_duration_seconds`: from the case's stated conversation length
- `tools_config.tools.end_session`: `should_register: true`,
  `add_to_system_prompt: true`
- `session_analysis`: `is_auto_analysis: true`, `is_auto_submit: true`,
  `enable_extraction: false` by default (analysis-only) — only turn on
  extraction if the case file defines explicit extraction variables
- `analysis_access: "always"` (top-level field) so students see their report

### Step 6: Rubric

Always evaluates the student — never the AI counterpart. Default weighted
shape, adapt names/weights to the case's actual teaching objective:

- Interest/issue discovery
- Information sharing / reciprocity
- Assumption testing
- Agreement quality
- Process & trust

Weights sum to 100. Include a report-format block (overall score, per-category
evidence, strengths, improvements) and, if useful, professor debrief
questions.

### Step 7: Create the scenario

1. Show the user a short summary before creating: roles, the pivotal reveal
   and what unlocks it, duration, rubric categories and weights.
2. `ttai:create_scenario` with the drafted fields as `scenario_data` (and
   `org_id` if applicable). Never put the instructor-only design note, the
   twist, or either side's private facts into `user_friendly_description` or
   the other side's instructions.
3. Re-fetch with `ttai:get_scenario` and spot-check that the student's
   `user_instructions` contain nothing from the counterpart's private brief.
4. Return the practice link `https://app.toughtongueai.com/run/<id>`.

### Step 8: Validate

On top of the **toughtongue:scenario-creator** skill's universal checklist:

- [ ] Public facts are identical, word-for-word, on both sides
- [ ] Neither side's private brief or the twist leaks into the other side's
      text
- [ ] The case's one pivotal reveal never originates from the agent — only
      ever from the student's own words, at any phase or under any pressure
- [ ] Opening is a bare greeting, not a scripted strategy line or leading
      question
- [ ] Silence-fill never advances a disclosure phase or hints at the reveal
- [ ] `end_session` enabled; rubric evaluates the student; weights sum to 100

## Related skills

- **toughtongue:scenario-creator** — general Tough Tongue AI scenario
  creation via MCP; its `references/sales-roleplay.md` is the source of the
  Resistance Pattern / Discovery Process this skill adapts.
- **toughtongue:scenario-refiner** — use after a session reveals the
  counterpart is too easy, too stubborn, or leaking the reveal early.
