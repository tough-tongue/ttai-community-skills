# Authoring Guide — v3 Notepad-Guided Board Interview

## Contents

- The two surfaces (notepad, architecture board, panel rule)
- Palette (the only component names allowed)
- Section-by-section craft: name, user_instructions, ai_instructions, rubrik
- Register and taste rules

The worked example throughout this guide is **Design Facebook Messenger**:
the walk is "A sends 'hi' to B", the load-bearing component is the
**WebSocket Server**, and the disqualifying naive choice is HTTP polling for
real-time delivery. Use it to calibrate the register of any new question.

## The two surfaces (get this exactly right)

- **Notepad** — the interviewer's shared notes. The AGENT controls it
  (`show` / `read` / `append` / `overwrite` / `clear`); the candidate can
  type in it too. Requirements scribing, capacity-math scaffolds, schema
  dictation, and final feedback live here.
- **Architecture board** — the candidate's canvas. The agent can only
  `show` / `read` / `clear` — it cannot draw. The candidate drags typed
  palette components, wires and labels edges, marks tiers distributed. User
  actions stream to the agent as batched `[board]` text events. The board is
  the GROUND TRUTH of the design: if speech and board disagree, the
  interviewer asks about the discrepancy. Never `clear` without explicit
  agreement.
- **Panel rule:** only one surface is on screen at a time; every notepad
  command steals the screen from the board. So: `board show` once at the
  opening (this pins it in the panel's arrow-nav for the whole session),
  work the notepad phases, then hand off to the board and FREEZE the notepad
  during board phases except announced checkpoints (announce → notepad →
  `board show` to return).
- Generic notepad/board command docs are auto-injected into the system prompt
  by the platform — do NOT restate command syntax in ai_instructions. The
  palette is NOT injected — always list the relevant palette names in
  ai_instructions ("Board habits" line).

## Palette (the only component names allowed)

- **Clients**: Web Client, Mobile Client, IoT Device
- **Edge**: CDN, DNS, API Gateway, Load Balancer, Reverse Proxy, WAF
- **Compute**: Service, Serverless Fn, Worker, Cron
- **Storage**: Postgres, MySQL, MongoDB, Cassandra, DynamoDB, Redis,
  Memcached, Elasticsearch, Blob Store, Data Warehouse
- **Messaging**: Kafka, RabbitMQ, SQS, Pub/Sub Topic, WebSocket Server
- **Misc**: Cache, Queue, Rate Limiter, Scheduler, ML Model, Third-party API, Note

Map real-world tech to the nearest palette item and keep the real name in
prose: "Cassandra (HBase at Messenger)". Specialized roles become a renamed
`Service` or `Worker` ("URL Frontier" → Queue + Worker; "Chat Service" →
Service). In ai_instructions list only the subset this question needs,
grouped by category, e.g.:

> Board habits: Steer with palette names: Clients (Web Client, Mobile
> Client), Edge (Load Balancer, CDN), Compute (Service), Storage (Cassandra,
> Redis, Blob Store), Messaging (Kafka, Pub/Sub Topic, WebSocket Server),
> Misc (Third-party API, Note).

## Section-by-section craft

### name / user_friendly_description

- `name`: `System Design: Design <X>` (matches the series).
- `user_friendly_description`: one punchy sentence to the candidate — name
  the system, the board, and the expert interviewer "who watches every move".

### user_instructions — a study guide, not a script

This is what the candidate reads BEFORE the session. Voice: direct, second
person, confident, tradeoff-first. Sentences short. No corporate filler.
Structure (match Messenger's headings):

1. **H1 + framing paragraph** — "Design a … . A 20-minute mock system design
   interview. You drive the pace." State that phases are skippable and that
   thinking is graded, not template-matching.
2. **The two surfaces** — 2 bullets (Notepad, Architecture board) + the
   one-visible-at-a-time arrow note + "If it is not on the board, it is not
   in your design." + "Build incrementally while you talk. Trace one
   <operation> end to end through *your* diagram."
3. **`## Design choices interviewers probe`** — the heart. One `###` per
   design decision (3–7). For each: name the options, say why the naive one
   fails AT SCALE, land on a default, and legitimize variants ("equally
   defensible if you can say why"). Teach the WHY, never just the answer.
   This section is what makes the scenario feel senior — spend the most
   effort here.
4. **`## Reference solution`** — "One complete design you can study, then
   rebuild in your own words. Do not recite it." Subsections:
   - `### Requirements` — bullets; "lock these or take the defaults".
   - `### Capacity` — the 2–4 equations with the method visible
     (DAU × rate × size → per-second), "Rough numbers are fine; the method
     is what gets graded."
   - `### Components to put on the board` — a short "how the graph works"
     paragraph, then an indented ASCII arrow graph in a code fence using
     palette names only, then one bold bullet per component explaining its
     job in 2–3 sentences (what it does, why it exists, what breaks
     without it).
   - `### Walk one <operation>` — numbered steps, 5–8, tracing the single
     core operation through the graph. Then 2–4 bold-prefixed paragraphs for
     the major edge cases (group fan-out, offline, server death…).
   - `### Schema` — code-fenced table list + partition/shard/replication
     bullets.
   - `### Scaling and wrap-up` — what scales how, first metrics, "if time"
     topics.
   - `### Equally defensible variants` — alternate stacks; "What matters is
     that you can argue the tradeoff."

### ai_instructions — the interviewer brain

Order and content (keep Messenger's headings):

1. **Persona line** — senior engineering manager at a top tech company;
   goal: assess ability to design <X>.
2. **`## Interview Approach - CRITICAL`** — candidate-led; reference solution
   is one strong design NOT a requirement; probe reasoning ("why", "what
   breaks at 10x"); accept defended alternatives; ONE question per turn,
   short turns, wait; never recite a script or lecture the answer key.
3. **`## The Interview Case`** — one line: the primary question.
4. **`## Tools`** — notepad = shared interview notes, agent controls, `read`
   before write; board = candidate's canvas, agent observes `[board]`
   events, `read` to re-ground, never `clear` without agreement, board is
   GROUND TRUTH; the **panel rule** paragraph; the **Board habits** palette
   line (question-specific subset).
5. **`## Notepad Usage`** — the opening `overwrite` brief in a code fence,
   question-specific: H1, "Interviewer's shared notes", `## Agenda (20 min)`
   with the 5 phases, empty `## Requirements` and `## Capacity math`
   placeholders. Then the write-trigger bullets: append agreed requirements;
   append settled equations; when stuck on math, append a **scaffold with
   blanks** using this question's real numbers (e.g.
   `100M DAU × 40 msgs/day = ___ msgs/day`) and have them fill it aloud —
   never recite the answer; schema checkpoint dictation.
6. **`## Interview Structure (20 minutes)`** — "Phases can be skipped if the
   candidate wants." Then per phase, with surface tags:
   - **Opening (~30 sec): notepad** — `board show` once (pins arrow-nav),
     then notepad `show` + `overwrite` brief; greet, name the surfaces,
     invite requirements questions; paraphrase, don't recite.
   - **Phase 1 Requirements (quick, never blocking): notepad** — a couple of
     scoping questions; log agreed answers; state the defaults in one line
     if skipped.
   - **Phase 2 Capacity (optional, never blocking): notepad** — guide the
     math aloud, log settled numbers; if skipped, state the headline numbers
     in one line, log, move on.
   - **Handoff** — `board show`, into design.
   - **Phase 3 High-level design (4–5 min): board (notepad frozen)** — they
     build, you coach off `[board]` events; 2–3 one-at-a-time prompts, the
     first always "trace one <operation> on their board".
   - **Phase 4 Deep dives (5–6 min): board, one notepad checkpoint** —
     board `read` first; pick 1–2 areas **based on what they actually
     built**; give 4–6 bold-titled dive options drawn from the design
     decisions; the schema checkpoint is announced → notepad → `board show`
     back.
   - **Phase 5 Scaling + wrap-up (3–4 min)** — which box breaks first at
     10×; mark distributed tiers; wrap-up = board `read`, summarize *their*
     architecture from the graph, append `## Feedback` (2 strengths, 1
     improvement), thank, `end_session`.
7. **`## Hints (when they're stuck)`** — the 3-level ladder, escalate only
   if still stuck, "They still place the pieces":
   1. **Nudge** — a question that names the gap.
   2. **Prescribe** — tell them what to put where (component + edges).
   3. **Sketch** — a fill-in on the notepad
      (`Web Client → Load Balancer → ??? → ??? → …`).
   Give one question-specific example per level.
8. **`## Reference Solution (Do Not Share Directly)`** — the condensed
   answer key: reference graph in one line, how it works, one bullet per
   design decision with the reasoning AND acceptable alternatives, capacity,
   schema, ordering/consistency contract, failure/reliability story. This is
   the interviewer's private crib sheet — denser than user_instructions,
   same facts. End with the "Alternatives … are fine if justified" line.
9. **`## Follow-up Question Bank`** — "Pick one per turn. Do not stack." then
   6–8 short question fragments specific to this system.
10. **`## Important Reminders`** — learning experience not gatekeeping;
    react to board events like glancing at a whiteboard, don't narrate every
    event; `read` both surfaces before any summary or critique; manage time,
    at least one deep dive; `end_session` after wrap-up.

### rubrik — mirrors the phases, weighted

Six sections, weights sum to 100 (Messenger split, reuse unless the question
demands otherwise): Requirements 15% · Capacity 10% · Architecture on the
Board 25% · Technical Deep Dives 30% · Scalability & Additional Topics 15% ·
Board Usage & Communication 5%. Each section = 4–6 yes/no observable
questions ("Did they…"), question-specific — including board-native checks
(labeled edges, distributed marks, traceable flow, no floating components,
built incrementally, revised under challenge).

Then `## Overall Assessment Categories` with **Strong Hire / Hire / Lean
Hire / No Hire** anchors. Make anchors name this question's load-bearing
choice the way Messenger names "Placed WebSocket Server unprompted" and
"Suggested HTTP polling for real-time" — the one component/decision that
separates levels. Close with `## Time Management Guidelines` and
`## Key Technical Points to Assess` (5–6 numbered).

## Register and taste rules

- Interviewer never stacks questions; scenario text never stacks either —
  short sentences, one idea each.
- Numbers always carry their derivation once, then travel as headlines
  ("~46K msgs/sec").
- Every "use X" is followed by why, and by when X breaks.
- Bold is for component names and decision labels, not emphasis spam.
- No exclamation marks, no "amazing/powerful/robust", no hedging filler.
