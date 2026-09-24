---
name: slides-scenario-builder
description: >
  Build or convert a Tough Tongue AI scenario around an embedded Google Slides
  deck: generate the deck with the Gamma connector, pause for the user's
  published Google Slides embed link, then wire the scenario with a slide map
  the agent can navigate. Use whenever the user wants a slide-driven or
  slide-specific scenario, says "use slides instead of cards", "the card is not
  interesting", "create slides for this scenario", "embed this deck", or hands
  over a Google Slides /pubembed link for a scenario — even if they don't say
  "skill" or name the two-step process.
---

# Slides Scenario Builder

Turn a Tough Tongue AI scenario into a slide-driven session in two steps:

1. **Generate the deck** with the Gamma MCP connector and share it.
2. **PAUSE** — ask the user for the published Google Slides embed link
   (they export the Gamma deck to Google Slides and publish it), then wire
   the scenario: `google_slides` tool + a SLIDE MAP in `ai_instructions`.

Requires the **Gamma** and **Tough Tongue AI (ttai)** MCP servers. This skill
covers only the slide integration; for scenario-type authoring rules (persona,
rubric, MCQs, model table) defer to the **toughtongue:scenario-creator** skill
and its `references/scenario-fields.md`.

## Step 0 — Establish context

- `ttai:list_organizations`; pass `org_id` on every call if the scenario is
  for a team.
- **New scenario or conversion?** Most requests convert an existing card-based
  scenario ("slides instead of cards"). For a conversion, `ttai:get_scenario`
  first and reuse its content — the deck teaches the same material; slides
  replace `card_tool` moments, they don't change the curriculum unless asked.
- Note the source of truth for facts (project files, reading chapters, an
  existing scenario's instructions). Slides must not invent numbers, quotes,
  or scripts that aren't in the source.

## Step 1 — Plan the deck before generating

Write the full slide-by-slide content yourself, separated by `---`. The deck
generator must not decide slide boundaries — your authored sections become the
slide map, so you need to control count and order exactly.

- Typical teaching deck: **8–14 slides**. Title → framework/overview → one
  slide per teaching beat → wrap-up/takeaways.
- **Situation slides replace situation cards**: one large in-character quote
  plus one line of context, nothing else. The agent reads the quote aloud in
  character when the slide shows.
- Contrast material (do/don't, use/never, selling/educating) as two-column
  slides; weighted or staged material as a flow with the numbers under each
  step; real examples with real figures as stat callouts.
- Everything factual comes verbatim from the source. Quotes in other scripts
  (e.g. Devanagari) are preserved verbatim.

## Step 2 — Generate with Gamma

Call `Gamma:generate` with:

- `textMode: "preserve"` and `cardSplit: "inputTextBreaks"` — guarantees one
  slide per `---` section, content untouched. (`numCards` is ignored in this
  mode; slide count = section count.)
- `sharingOptions: {"externalAccess": "view"}` — set at generation time so the
  embed works for anyone.
- `cardOptions: {"dimensions": "16x9"}`.
- `imageOptions.source`: `"pictographic"` for training decks (clean icon-style
  drawings) or `"noImages"` when slides carry data the learner must read.
- `additionalInstructions`: say the deck renders inside a **small embedded
  frame** (large readable text, minimal decoration), that every fact and
  quote must stay exactly as written, and name the layout per slide
  (table on slide N, two-column contrast on slide M, quote-block situation
  slides…).
- A theme if the user has a house style — reuse the same theme across a
  scenario family so decks look like a set.

Poll `Gamma:get_generation_status` (typically 45–120 seconds; sleep between
polls). Share the `gammaUrl` and tell the user content tweaks happen in the
Gamma editor — the MCP tools cannot edit an existing gamma. If they change the
slide count or order there, the slide map must be updated to match.

## Step 3 — PAUSE: ask for the Google Slides embed link

Ask the user to:

1. Export the Gamma deck to Google Slides (Gamma export → PPTX → import, or
   their own conversion flow).
2. **File → Share → Publish to web** in Google Slides.
3. Send back the published link.

Wait for it. Two rules when it arrives:

- Use the **`/pubembed`** form of the URL (accepted directly by
  `tool_settings.embedUrl` — no transformation needed). A plain `/pub` link:
  change the suffix to `/pubembed`.
- **Fetch the link and check the page title** matches the deck before wiring
  it — this catches wrong-deck paste and confirms the export carried the same
  slides, so the slide map still lines up.

Optional interim: wire `https://gamma.app/embed/<gamma_id>` immediately so the
scenario is testable before the Google link arrives, then swap when it does.
Ask the user which they prefer; don't block testing on the export.

## Step 4 — Create or update the scenario

For a **new** scenario, author the full payload per
**toughtongue:scenario-creator** (Steps 5–7 there), then add the pieces below.
For a **conversion**, use `ttai:update_scenario` and change only what the
slide integration needs — plus anything the user explicitly asked for (model
change, rubric). Always set `save_as_version` with a short label (e.g.
`"v1 — card-based"`) so the prior configuration is archived.

**`tools_config`** — pass every tool key explicitly with `should_register` and
`add_to_system_prompt` (the platform expects the full set on update):

- `google_slides`: `should_register: true`, and
  `tool_settings: {"embedUrl": "<the /pubembed link>"}`.
  `add_to_system_prompt: true` for coach/teaching scenarios (short generic
  guidance helps); `false` when the ai_instructions slide section is
  exhaustive (case-interview style).
- `card`, `image_generation`, `slide_generation`, `whiteboard`: **off** — one
  visual tool per scenario. The deck replaces the cards.
- Keep `mcq`, `emoji_reaction`, `memory_search`, `end_session` as the
  scenario type prescribes.

**`ai_instructions`** — add a SLIDE MAP section and wire the flow to it:

```
## SLIDE MAP — google_slides (navigate FIRST, then talk)
The deck has exactly <N> slides. Use google_slides with command show and the
slideNumber. Call it once, right when you reach that slide. Track the current
slide yourself — every session starts fresh at slide one regardless of
memory. Never read a slide verbatim; use it as the anchor and ask the trainee
about it. Situation slides are a moment — read the quote aloud in character,
then ask what the trainee would do.

- Slide 1 — <one-line summary of what is on it>
- Slide 2 — <…>
...
```

- One line per slide, in deck order, summarizing what's on it — including
  the key figures — so the agent can teach from the summary without reading
  the slide.
- In the session-flow sections, cue navigation explicitly per step:
  "Show slide 5." before the teaching/asking for that beat. Never leave the
  agent to infer when to advance.
- State the tool contract once: never show a slide before its moment; honor
  "go back" / "repeat" requests by revisiting the slide after the current
  answer completes.

**`user_instructions` / `user_friendly_description`** — mention the deck
("<Coach name> walks you through N slides…") so learners expect a screen, not just a
voice.

## Step 5 — Verify and deliver

1. Re-fetch with `ttai:get_scenario`: confirm `embedUrl`, that `card` (and
   other visual tools) are off, and the slide count in the SLIDE MAP matches
   the deck.
2. Return the practice link `https://app.toughtongueai.com/run/<id>`, the
   deck link, and 2–3 sentences on what changed.
3. Suggest one test run to check the embed renders inside the slide frame —
   layout fixes happen in the deck editor, not the scenario.

## Pitfalls

- **Slide-map drift** is the failure mode of this whole pattern. Any edit
  that adds, removes, or reorders slides (in Gamma or in Google Slides)
  silently breaks every `slideNumber` cue. After any deck edit, re-confirm
  the count and update the map.
- **`preserve` mode or bust.** Letting Gamma restructure content (`generate`
  / `condense` textMode, or `cardSplit: auto`) means you no longer know
  what's on slide N — the map becomes a guess.
- Don't leave `card` registered alongside `google_slides` — the agent will
  split attention between two visual surfaces.
- The embed link must be the **published** (`/pubembed`) URL; a normal
  `docs.google.com/presentation/d/<id>/edit` link will not render for
  learners.
- Don't put teaching content only on the slides. The agent cannot see the
  deck — the SLIDE MAP summary is all it knows. If a figure matters, it goes
  in the map or the knowledge section, not just on the slide.
