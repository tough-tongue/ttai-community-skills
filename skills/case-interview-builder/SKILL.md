---
name: case-interview-builder
description: >
  Turn a consulting case (casebook PDF page range, case doc, or pasted text)
  into an interviewer-led Tough Tongue AI mock case interview with a
  polished exhibit deck: builds the deck with the Gamma MCP connector, pauses
  for the user's published Google Slides embed link, then creates the
  scenario with slide-cued interview flow, hidden answer keys, a
  phase-by-phase study guide, and a weighted rubric. Use when the user says "turn this
  case into a case interview", "build a consulting case scenario", "mock case
  interview for Case N", "interviewer-led case with exhibits", or hands over a
  casebook case to practice.
---

# Case Interview Builder

Turn one consulting case into: (1) a Gamma exhibit deck, (2) a Google Slides embed supplied by the user, (3) a Tough Tongue AI interviewer-led scenario wired to those slides. Requires the Gamma and Tough Tongue AI (ttai) MCP servers.

## Step 1 — Extract the case

Read the source (PDF page range, project doc, or pasted text) and separate the material into four buckets. Never invent numbers; every figure must come verbatim from the source.

1. **Case prompt** — read aloud by the interviewer at the start.
2. **Clarifying information** — revealed ONLY piece-by-piece when the candidate asks; never volunteered.
3. **Parts/phases** — most interviewer-led cases have: structure → 1-2 quantitative parts (each tied to an exhibit) → recommendation. Note which exhibit each part uses and the time budget per part.
4. **Answer keys and bonus insights** — expected numbers (with acceptable rounding), the intended solution path, extra-credit insights (e.g., inefficiencies in the data, cost-of-capital questions). These go in ai_instructions, the rubric, and the user_instructions study guide — NEVER on the slides.

If an exhibit's underlying values are genuinely unrecoverable from the source (chart series with no printed values, and no answer-key math that pins them down), do NOT invent numbers — generate that slide as a titled placeholder and tell the user to paste a screenshot of the original exhibit during the Google Slides conversion.

## Step 2 — Generate the exhibit deck with Gamma (the deck IS the experience)

The slides are the wow factor of the interview: the candidate watches the interviewer pull up each exhibit at the right dramatic moment, and a polished, visual deck is what makes the session feel like a real interview rather than a phone call. Invest here.

**Deck design principles — apply all of them:**
- **Generous slide count.** Never ship the bare minimum. A typical case deck is 5–8 slides: a title/welcome slide, the case prompt slide, ONE slide per exhibit (never two exhibits on one slide), and optional neutral transition slides between parts. More distinct slides = more moments where the interviewer visibly advances the deck, which is a core part of the experience.
- **Transition/divider slides** (optional but encouraged): a near-empty slide with just a part title (e.g., "Part 2 — Your recommendation") gives the interviewer something to flip to during non-exhibit phases. Rule: a divider must be exactly as neutral as the interviewer's own spoken transition — it must never telegraph a structure, insight, or number the candidate is supposed to produce. When in doubt, leave it out.
- **Charts over tables, wherever the data is a series.** If the source exhibit is a chart, recreate it as a real chart and describe the form explicitly to Gamma (e.g., "two side-by-side vertical bar charts, Year on x-axis, GW on y-axis, scale 0–8"; "pie chart with these four segments and percentage labels"). If the source is a table but one column is a comparable series (market shares by city, profit by segment), STRONGLY prefer rendering it as a labeled bar chart — candidates read patterns off charts the way they would in a real interview, and it looks dramatically better on screen. Keep any footnotes from the original.
- **Recreate visual exhibits visually.** Maps, timelines, process diagrams: reproduce the information as a designed visual (chart, annotated list, two-column comparison) rather than collapsing it into plain text — but only encode facts that are verbatim in the source or provably derivable from the answer key (e.g., a with/without-competitor split whose averages reproduce the key's figures exactly). Anything else → titled placeholder + tell the user to paste a screenshot of the original at conversion time.
- **Tables stay tables** when the source is a financial statement or line-item table — render them clean, aligned, and large, with footnotes intact.

Call `Gamma:generate` with:
- `textMode: "preserve"` and `cardSplit: "inputTextBreaks"` with `---` separators — this guarantees one slide per section with numbers untouched.
- Slide 1: case intro (title, case type/industry tags, the case prompt, the key question in a callout). Then the exhibit and divider slides in the order the interview presents them.
- `imageOptions: {"source": "noImages"}` — exhibits must be clean; no decorative AI images.
- `additionalInstructions`: state that this is a case-interview exhibit deck, candidates do math from it, keep every number exactly as given, make charts large and legible with clearly labeled axes and data labels, and give the deck a consistent, polished, professional look.
- Answer keys, solution steps, and interviewer guidance must NOT appear anywhere in the deck.

Poll `Gamma:get_generation_status`, then share the gammaUrl. Ask the user to eyeball every exhibit slide in the Gamma editor before converting — chart rendering is the one thing worth a manual check — and remind them that content tweaks happen in the Gamma editor (the MCP tools cannot edit an existing gamma).

## Step 3 — Ask the user for the Google Slides embed link

Gamma embeds are not used directly. Ask the user to:
1. Export/convert the Gamma deck to Google Slides (or recreate it there), pasting screenshots into any placeholder exhibit slides.
2. Publish it (File → Share → Publish to web).
3. Send back the published link.

PAUSE the workflow until the link arrives. When it does, use the `/pubembed` (or `/embed`) form of the published URL — not the plain `/pub` page — as the value for `tool_settings.embedUrl`.

## Step 4 — Create the scenario

Use the **toughtongue:scenario-creator** skill's field reference for schemas, then author with these case-interview-specific settings. Call `ttai:list_organizations` first and pass `org_id` if the scenario is for a team. Create with `ttai:create_scenario`.

### Config (deviations from generic defaults — all deliberate)
- `ai_model_config`: `{"provider": "Ocean", "model": "medium-stable"}` — native voice, stable for long multi-part sessions.
- `is_recording: false` — do NOT switch on auto-recording for case interviews.
- `session_analysis`: `is_auto_analysis: true`, `is_auto_submit: false`, `enable_extraction: true` with extraction_vars for each key quantitative answer (include the correct value in the description) plus the final recommendation as text.
- `appearance`: ask the user for an avatar URL (or reuse their standard one) and set `avatar_url`; `language_code` per locale.
- `tools_config`:
  - `google_slides`: `should_register: true`, `add_to_system_prompt: false`, `tool_settings: {"embedUrl": "<published embed URL>"}` — slide guidance lives in ai_instructions, not the tool prompt. Because of this, the ONLY thing that makes the agent call the tool is the text in ai_instructions — which is why the slide-cue bullets in INTERVIEW FLOW below are mandatory, not stylistic.
  - `end_session`: `should_register: true`, `add_to_system_prompt: true`, `disconnectDelaySeconds: 5`.
  - `browser`: `should_register: false`.
- `strategy`: `skip_auto_start: false` (interviewer speaks first), `system_instructions_template: "minimal"`, `silence: {"silence_threshold": 30000, "end_session": false, "force_agent_to_speak": true}` (candidates need thinking time — 30s, nudge, never disconnect), `max_duration_seconds` ≈ case length + 25%, conductor messages at T-5min ("show slide #N and ask for the final recommendation now" — name the recommendation slide so the deck moves even when the conductor forces the jump; `end_turn: false`) and at T ("close warmly, use end_session", `end_turn: true`).

### ai_instructions structure (## sections, in this order)
1. **ROLE** — top-tier-firm case interviewer; professional, warm but measured; one question per turn then stop; never lectures.
2. **SLIDE DECK NAVIGATION** — list every slide number and its content, dividers included. The deck is a centerpiece of the experience: the interviewer navigates it ACTIVELY — advance to each slide at the moment its part begins, make the reveal a moment ("Let me pull up Exhibit A — you should see it on slide 3"), flip to divider slides during transitions so the screen always matches the conversation, and return to an earlier exhibit if the candidate asks to revisit it. NEVER show an exhibit slide before its part; gate especially hard when an exhibit's data or footnotes reveal figures an earlier part asks the candidate to estimate. Fallback: name the slide number and read the exhibit data aloud if the tool is unavailable.
3. **CASE PROMPT** — verbatim, read aloud with the prompt slide showing. The section opens with the action bullet `- Show slide #1` (or `#2` when slide 1 is a title/welcome slide) BEFORE the prompt text.
4. **CLARIFYING INFORMATION** — bulleted; header states "reveal ONLY the piece the candidate asks about — never volunteer all of it".
5. **PROBING (applies to every part)** — the interview is a dialogue: probe the WHY behind at least one answer per part INCLUDING correct/strong ones, in the interviewer's own words reacting to what the candidate actually said; probe strong answers one level deeper, probe weak answers with a question that lets the candidate find the gap themselves; ONE probe at a time, max 2 per part, then move on to protect time. Keep example probes short and natural — they may be spoken nearly verbatim.
6. **INTERVIEW FLOW** — one `###` per part with: time budget, **the slide-cue action bullets (see the convention below — these are the first lines of every part)**, the exact transition line to say, the exhibit data restated in text (so the agent can discuss it), an ANSWER KEY block marked "do not reveal; guide with questions if stuck" including accepted roundings, named traps, and bonus-credit insights, the wrong-answer protocol (ask them to walk through their calculation aloud — never correct directly), and ONE anchored probe (e.g., "So what does this mean for the client?" after the math lands; a single push-back on the recommendation drawn from the candidate's own analysis, never a second one). Honor case-specific quirks from the source (e.g., "do not allow time to write the recommendation", "push pace on market sizing — no correct answer").
7. **BEHAVIOR RULES** — one question per turn, never stack; wait quietly when the candidate asks for a minute (minus any case-specific exception); never reveal answer-key numbers unless produced by the candidate or the interview is ending; after two failed nudges give the figure and move on; stay in character, no mid-case coaching; unknown facts → "the team doesn't have that data, make a reasonable assumption".
8. **ENDING** — thank the candidate, say feedback follows in the session report, call end_session; conductor wrap-up overrides position in the flow.

### Slide-cue convention (mandatory in every `### Part` block)

The agent only advances the deck reliably when the cue is an explicit, unhedged ACTION LINE placed before anything it is told to say. A cue inside a part heading ("### Part 2 … Show Slide 2 now.") reads as a title; a cue after the Say line makes the agent announce the slide before it has been told to show it; a hedged cue ("Return to Slide 1 or keep Slide 3 up") gives it permission to do nothing. All three forms were found in earlier scenarios and all three failed in live sessions. Write every part like this:

```
### Part 2 — Capacity math (~7-8 min)
- Show slide #2
- Say: "The team has pulled together projections… I'm showing you Exhibit A on slide 2. How much additional capacity…"
```

Rules:
- **Bullet first, speech second.** Every `### Part` block (framework parts and brainstorm parts included) begins with one or more bullets of the exact form `- Show slide #N` or `- Keep slide #N up`, before the first `Say:` / `Transition:` / `Ask:` line. The heading may still mention the exhibit, but the bullet is what drives the tool call.
- **One bullet per reveal, at its trigger.** A part that reveals two slides gets two bullets, the later one stating its trigger from the case: `- Show slide #5` then `- Once the candidate has computed the station count, show slide #6`. Never collapse two reveals into one sentence.
- **No-exhibit parts still get a bullet** so the screen state is explicit: `- Keep slide #1 up (no exhibit in this part)`. Do not write only what NOT to show.
- **The recommendation part gets one definite slide** — the recommendation divider if the deck has one, otherwise `- Show slide #1`. Never write "or keep slide N up".
- **Slide numbers must exist in SLIDE DECK NAVIGATION.** Cross-check every bullet against the list before creating the scenario.
- The T-5min conductor message names the same recommendation slide (see Config above).

### user_instructions — a full study guide, not a pre-brief

`user_instructions` renders as rich markdown on the run page. This is a mock-interview PREPARATION tool: the candidate should be able to read user_instructions alone and know how to attack every phase — including the reference answers. Do not withhold the answer key here; the candidate chooses whether to study before or review after. Use headings, bold, and bullets; avoid tables.

Structure it as:
1. **`## Your role`** — candidate in an interviewer-led case; exhibits appear on embedded slides when each phase begins, don't read ahead; pen and paper; time budget.
2. **`## The case at a glance`** — client, situation, the question(s) asked, and key context worth asking about (goals, constraints, entry costs).
3. **One `## Phase N — <name>` section per phase** (with its time budget and exhibit/slide reference), each containing bullets for:
   - **What happens** — the ask in that phase.
   - **How to approach** — the method that works, stated concretely ("convert everything to $/kWh: running hours = 24 × 365 × load factor × lifetime...", "size top-down: population → male share → % paying → frequency → price"), plus any facts the candidate must ask for.
   - **Reference answer** — the casebook's expected numbers, structures, or buckets, verbatim from the answer key, with intermediate steps and bold final figures.
   - **Watch out** — the traps by name (e.g., "monthly rent — annualize it", "highest % margin is bait — demand is flat"), the bonus-credit insights, and what the interviewer will probe for in that phase.
4. **`## General tips`** — clarifying info is revealed only when asked; a "why?" probe on a correct answer tests depth, not error; and the rubric's category weights so the candidate knows how they're scored.

### rubrik
First line: "Evaluate the CANDIDATE (the human user) — not the AI interviewer." Weighted categories summing to 100%, tuned to the case (typical: Structure & Problem Solving 25%, Quantitative Accuracy 30% — include the exact answer-key numbers so the report can show candidate-vs-key, Business Judgment & Insight 20%, Communication 15%, Recommendation & Risks 10%). End with a Report Format section: overall score /10 with a hire band, per-category scores each with one observed example, exact math vs answer key, top 2 strengths, top 3 improvement areas with practice suggestions.

## Step 5 — Verify and deliver

1. Re-fetch with `ttai:get_scenario`; confirm embedUrl, `is_recording: false`, conductor times, and that answer-key numbers in ai_instructions, rubric, and user_instructions match the source case exactly.
2. Slide-cue check: scan ai_instructions and confirm every `### Part` block (and the CASE PROMPT section) has a `- Show slide #` / `- Keep slide #` bullet before its first spoken line, no "or keep" / "Return to Slide" phrasing remains, and every slide number in a bullet appears in SLIDE DECK NAVIGATION. Fix with `ttai:update_scenario` before delivering.
3. Return the practice link `https://app.toughtongueai.com/run/<id>` and embed link `https://app.toughtongueai.com/embed/<id>`.
4. Offer a test session and refinement from the transcript via the **toughtongue:scenario-refiner** skill. In the transcript, the `google_slides` call must land BEFORE the interviewer's "you should see it on slide N" line at each part transition — that is the acceptance test for navigation.

## Verification checklist
- [ ] Every number on the slides and in ai_instructions matches the source case verbatim
- [ ] No answer keys or interviewer guidance on the slides
- [ ] Deck is generous and visual: 5–8 slides, one exhibit per slide, series data rendered as charts (not tables), visual exhibits recreated visually or placeholdered — never silently flattened to text
- [ ] Divider slides (if any) are as neutral as a spoken transition — no leaked structure, insights, or numbers
- [ ] Slide gating: each exhibit slide is shown only when its part begins (and never before a part that estimates its figures); ai_instructions directs ACTIVE navigation, dividers included, so the screen always matches the conversation
- [ ] Slide cues: every `### Part` block and the CASE PROMPT open with `- Show slide #N` / `- Keep slide #N up` bullets BEFORE the first Say line; one bullet per reveal with its trigger; no-exhibit parts have an explicit Keep bullet; recommendation part names one definite slide (no "or keep"); T-5min conductor message names that slide
- [ ] PROBING section present (probe correct answers too; max 2 per part; one push-back on the recommendation)
- [ ] Clarifying info marked reveal-on-request only
- [ ] user_instructions is a full phase-by-phase study guide: role → case at a glance → per-phase (what happens / how to approach / reference answer / watch out) → general tips with rubric weights — rich markdown, bullets not tables
- [ ] `is_recording: false`, `is_auto_submit: false`, google_slides `embedUrl` set with `add_to_system_prompt: false`
- [ ] Rubric evaluates the CANDIDATE, weights sum to 100%, includes answer-key numbers
- [ ] Extraction vars capture each key number and the final recommendation