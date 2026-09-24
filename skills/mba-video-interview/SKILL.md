---
name: mba-video-interview
description: >-
  Research a named MBA school and create a Tough Tongue AI one-way video essay /
  video interview practice scenario (AI is a recording, not an interviewer).
  Authors timer-safe ai_instructions, applicant-facing user_instructions with
  answer frameworks, AdCom rubrik plus hand-authored processed_rubrik, avatar,
  and analysis wiring. Use when the user says "MBA video essay", "MBA video
  interview practice", "Kellogg/Sloan/Yale/INSEAD video prompts", "create
  video essay for <school>", or provides a school plus format notes.
---

# MBA Video Interview Practice

Build a school-specific **one-way video essay** scenario. The AI is a
recording: card + think timer + answer timer. No conversation, no redo.

Requires the **Tough Tongue AI (ttai)** MCP server. Reference pattern:
Kellogg 2026–27 (5 questions, 30s think practice / 60s answer). Adapt counts
and timing to the school you research. For deeper essay research first, the
**mba-essay-guide** skill produces a source-tagged question bank.

**Read before drafting:**

- [references/timer-and-flow.md](references/timer-and-flow.md) — timer rules
  are non-negotiable. A soft “stay silent” instruction fails on Ocean models.
- [references/user-guide.md](references/user-guide.md) — applicant prep copy
- [references/rubric.md](references/rubric.md) — raw + processed rubric
- [references/template.yml](references/template.yml) — payload skeleton

## Hard rules

1. **Create live.** The output is a scenario created with
   `ttai:create_scenario`, not a file.
2. **Research the school first.** User gives a school (and optional notes).
   Fetch official admissions + recent cycle write-ups. Do not clone Kellogg
   questions onto Sloan/INSEAD/Yale.
3. **Evaluate the applicant**, not the AI. No live-interview rubric
   (active listening, “questions for interviewer,” 25% school knowledge).
4. **Think-time floor is 30 seconds** in `setTimer`, even if the real school
   is 20s. Say so in user-facing copy. The timer tool raises anything under
   30 to 30 and adds a ~10s buffer.
5. **Hand-author `processed_rubrik`** with `rubrik_hash: "user-set"`. Last
   criterion is On-Camera Presence with `requires_video: true`. Weights = 100.
6. **Always set appearance** (voice + `language_code`, plus `avatar_url` if
   the user has an interviewer image), `is_recording: true`, multimodal
   auto-analysis.
7. **`system_instructions_template: "minimal"`** — never `"standard"` (that
   string is treated as a literal custom template and breaks the prompt).

## Workflow

### 1. School + context

Need: school name. Optional: cycle year, official URL, consultant notes,
question count, timing, published vs unpublished prompts.

If the user only says “make an MBA video practice,” ask for the school.

### 2. Research (do this every time)

Fetch, in order:

1. Official “How to apply” / video essay page for the current cycle
2. One recent consultant write-up (Fortuna, Menlo, Clear Admit, P&Q)
3. School values / culture language from the official site (not rankings)

Capture a research brief before writing:

| Fact | Example |
|---|---|
| Format | one-way video essay vs live video interview |
| Question count | 5 unpublished / 3 fixed / 1 open |
| Think / answer | official 20s/60s; practice think ≥ 30s |
| Re-record | none / one retry / unlimited (rare) |
| Prompt style | unpublished mix / locked Q1–Q2 + behavioral |
| Values to score | collaboration, community, “person behind paper” |
| Why-school cap | at most 1 prompt per session unless the school always asks it |

If research conflicts, prefer the official page and note the conflict to the user.

If the school is a **live two-way interview**, stop and say this skill is the
wrong template — use a conversational MBA interview scenario instead.

### 3. Design the session

- Question bank in 3–4 categories (intro/personality, optional Why School,
  behavioral, community/values or school-specific). Mix rule so repeat
  practice is not identical.
- Per-question flow: card → think timer → answer timer → next. No follow-ups.
- Copy the **TIMER WAIT** block from [references/timer-and-flow.md](references/timer-and-flow.md)
  verbatim, then swap school name, question count, and durations.

### 4. Draft fields

Author in this order:

1. `name` — `{School} video prompts` or `{School} video essay`
2. `user_friendly_description` — real vs practice timing
3. `ai_instructions` — FORMAT, TIMER WAIT, bank, mix rule, FLOW, GUARDRAILS
4. `user_instructions` — per [references/user-guide.md](references/user-guide.md)
5. `rubrik` + `processed_rubrik` — per [references/rubric.md](references/rubric.md);
   rename “Kellogg Values” to that school’s values
6. Config from [references/template.yml](references/template.yml)

### 5. Create

1. `ttai:list_organizations` — pass `org_id` only if this is a team scenario
2. Load the `ttai:create_scenario` schema, then call it. Omit `id`.
3. Confirm `processed_rubrik.criteria`: exactly one `requires_video: true`
   (On-Camera Presence), four transcript-only, `rubrik_hash: "user-set"`
4. Return `https://app.toughtongueai.com/run/<id>` and a 4–6 line research
   summary (format, timing, values scored)

If the ttai MCP server is not connected, output the full payload in chat and
tell the user how to connect it.

## Checklist

- [ ] Official format + timing researched; practice think ≥ 30s
- [ ] TIMER WAIT + filler lines (“You can continue thinking.” /
      “Please continue.”) — not “remain silent”
- [ ] Mix rule; Why School at most once unless the school always asks it
- [ ] User guide has STAR / 60s frameworks + story-bank + camera tips
- [ ] Rubric evaluates applicant; values criterion is school-specific
- [ ] Processed prompts are self-contained CONTEXT → WHAT → SCORING → OUTPUT
- [ ] Avatar, recording, multimodal auto-analysis, `evaluation_target`
- [ ] Template is `minimal`; Ocean `medium-stable` unless user says otherwise

## Key Files

| Path | Role |
|---|---|
| [references/timer-and-flow.md](references/timer-and-flow.md) | Timer + FLOW |
| [references/user-guide.md](references/user-guide.md) | Applicant copy |
| [references/rubric.md](references/rubric.md) | Rubrics |
| [references/template.yml](references/template.yml) | Config skeleton |
