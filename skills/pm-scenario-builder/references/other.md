# Technical & Behavioral Cases

Two lighter-weight types, each with one dominant sub-pattern in the existing
collection.

## Technical

Signal: "design a [system]", "what happens when you type a URL and hit
enter", "explain [tech concept] to a 10-year-old", "walk me through your
most technical project."

### Subtypes

| Subtype | Signal | Approach |
| --- | --- | --- |
| **System design** | "How would [system] work at a high level?" | PM-level, not engineer-level: components + data flow + key tradeoffs (latency vs consistency, cost vs scale), NOT implementation code |
| **Tech-101 / explain-like** | "Explain APIs / ML / blockchain to a non-technical exec" | Analogy-first, then 1 layer of real mechanism, then why it matters for product decisions |
| **Experience-based technical** | "Tell me about the most technical project you've led" | STAR structure (see Behavioral) but probe for genuine technical depth — can they go 2 levels deeper when pushed? |

### Approach for system design (the deepest subtype)

1. Clarify scale (users, QPS, data volume) and the ONE primary constraint
   the interviewer cares about (usually latency, consistency, or cost).
2. Sketch major components and data flow at a PM level of abstraction —
   client → API → service → datastore, plus 1-2 supporting systems
   (cache, queue, CDN) where they clearly matter.
3. Call out exactly one real tradeoff explicitly (e.g. "we could cache
   aggressively for speed but risk staleness — acceptable here because...").
4. Tie every technical choice back to a product/user outcome — this is
   what separates a PM's system-design answer from an engineer's.

Turn `tools_config.tools.mermaid.should_register` **on** for this subtype
only — the candidate should be able to sketch the architecture. Everything
else in `references/scenario-payload.md` stays default.

### Quality bar

- Scale/constraint clarified before designing.
- ≥3 components named with data flow between them.
- ≥1 tradeoff named explicitly with a reasoned choice.
- Every technical point connects back to a product outcome.

### Coaching-format variant

A technical scenario can also be structured as Phase 1 (Learning) → Phase 2
(Practice) rather than a single worked case. If the user's source material is
a single concrete system-design question, prefer the single-case shape
(matching the other five types) unless they explicitly ask for a
coaching/learning format.

## Behavioral

Signal: "tell me about a time you...", "why do you want to work here?",
"what would you do if [hypothetical interpersonal/team situation]?"

### Four question categories (cover all, weight per the case)

1. **Pitch** — "tell me about yourself" — keep the reference answer to
   30-60 seconds: current role → 1-2 relevant achievements → why this
   move.
2. **Fit** — "why this company/role" — company-specific: name 2-3 real
   things about the company (product, mission, recent news) the candidate
   should reference, not generic flattery.
3. **Experience-based (STAR/PAR)** — the bulk of interview time (∼25-30 of
   35-40 min). For EACH sample question, write a full STAR reference
   answer:
   - **Situation**: specific context, not vague ("At my last company" →
     name the product/team/timeframe).
   - **Task**: the candidate's specific responsibility, not the team's.
   - **Action**: 3-4 concrete steps THE CANDIDATE took (not "we decided").
   - **Result**: quantified outcome + a reflection/lesson.
4. **Hypothetical** — "what would you do if a stakeholder disagreed with
   your roadmap?" — reference answer should show a repeatable
   decision-process (listen → find the shared goal → data or compromise →
   escalate only as last resort), not just "I'd talk to them."

### Company-specific emphasis (bake into persona + question mix)

- Amazon → frame around named Leadership Principles (Customer Obsession,
  Ownership, Dive Deep, etc.) — pick 3-4 relevant to the role.
- Google → competency-based (structured thinking, "Googleyness",
  leadership without authority).
- Meta → heavier hypothetical/scenario mix, fast-paced follow-ups.
- Startup → cultural fit + scrappiness/ambiguity-tolerance emphasis.

### Quality bar

- Pitch capped at ≤5 min combined with Fit in the interview structure.
- ≥3 full STAR reference answers with quantified results.
- ≥1 hypothetical with a named repeatable process, not a one-liner.
- Fit answer references real, specific company facts.

### Example cases

"Tell me about a time you disagreed with your manager", "Why this company?",
and a Leadership-Principles-anchored variant for Amazon ("Tell me about a
time you showed Customer Obsession").

## `ai_instructions` persona notes

Technical: senior PM or EM-turned-PM who can go deep but frames everything
in product terms — never lets the conversation become a pure engineering
interview. Behavioral: hiring manager or bar-raiser persona, listens for
specificity and ownership language ("I decided" vs "we decided") as a
signal, and gently redirects vague answers ("Can you walk me through the
specific steps you took?").
