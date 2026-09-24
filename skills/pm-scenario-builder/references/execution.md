# Execution Cases

Two distinct flavors that both test "can you drive a decision with
incomplete information under a deadline":

| Subtype | Signal | Core skill |
| --- | --- | --- |
| **RCA** | "Metric X dropped by N% — why?" | MECE elimination + data-gathering discipline |
| **Tradeoff** | "Ship A or B?", "Feature X or Y with the same eng team?" | Decision-making with explicit criteria, not just gut |

## Subtype: RCA — MECE elimination + hidden root cause

The AI is NOT a neutral narrator here — it plays an **in-character
data-holder** (data analyst / eng lead / support lead) who only reveals
facts when asked precisely. This is the one subtype where `ai_instructions`
structure differs meaningfully from the others.

### Authoring the case

1. Pick a metric drop with a **real, specific root cause** — not "user
   experience got worse" (too vague to be discoverable) but something
   concrete: a backend bug, a pricing change, a competitor launch, a policy
   change, a seasonal confound. Numbers matter: state the drop precisely
   (e.g. "cancellation rate up from 8% to 14% over 3 weeks").
2. Build a **MECE hypothesis tree** covering all plausible buckets:
   typically Internal/Product (bug, feature change, pricing) ×
   External/Market (competitor, seasonality, regulation) × Data artifact
   (tracking bug, mislabeled event). The reference solution eliminates
   branches one at a time using data, not guesses.
3. Write the **root cause as a hidden section** —
   `## The Actual Root Cause (Reference Solution - Do Not Share)` — the AI
   must never reveal this directly, only through data responses to precise
   questions.
4. Write a **data-reveal catalog**, organized by investigation category
   (e.g. Initial Clarifications, Segment Breakdown, Driver/Supply-Side,
   Rider/Demand-Side, Technical Investigation, Competitive Landscape, Time
   Patterns). Each entry: the specific question that unlocks it → the exact
   data/number to reveal. Vague questions get a push-back, not an answer:
   *"Could you be more specific? What exact data would help you?"*

### `ai_instructions` additions specific to RCA

```markdown
## Persona
You are a {data analyst / eng lead} at {Company} with access to internal dashboards. You answer ONLY what is asked, precisely. You do not volunteer the root cause or unprompted context.

## Response Rules
- Vague question ("what's going on?") → push back: ask what specific data would help.
- Precise question ("what's the cancellation rate by driver tenure?") → reveal exactly that data point, formatted clearly.
- Never proactively suggest the next question to ask.
- Never confirm or deny a hypothesis directly - only supply the data that would let the candidate confirm it themselves.
```

### Quality bar

- MECE tree has ≥2 top-level branches, each with ≥2 sub-branches.
- Root cause is specific and singular (not "it's complicated").
- Data-reveal catalog has ≥5 entries across ≥3 categories.
- At least one plausible-but-wrong branch exists that data should rule out
  (tests whether the candidate follows evidence over first instinct).

## Subtype: Tradeoff — criteria-driven decision

Signal: "Ship feature A or B with the same team", "cut scope or delay
launch", "prioritize retention or new-user growth this quarter."

### Approach

1. **Clarify the real constraint** — what's actually fixed (deadline? eng
   headcount? budget?) and what's the deciding stakeholder's priority this
   period.
2. **Name explicit decision criteria** (3-4): typically impact on the
   primary goal metric, effort/cost, risk, strategic fit/optionality.
3. **Score each option against every criterion** — even briefly — before
   concluding. Don't jump straight to a gut pick.
4. **Recommend one option with a stated reason tied to the criteria**, and
   name the biggest risk of that choice plus a mitigation.
5. **State what would change the decision** — a threshold or new piece of
   information that would flip the recommendation. This shows the decision
   isn't dogmatic.

### Quality bar

- ≥3 named criteria, applied to both/all options (not just the winner).
- A clear recommendation — "it depends" without a final pick fails this
  case.
- Reversal condition stated explicitly.

## Example cases

- RCA: "Lyft ride cancellations are up 15%. Why?", "Lyft ETAs got worse this
  week. Find the root cause."
- Tradeoff: "Should Facebook ship video events?", "Spotify can build only one
  of two features this quarter. Which one?", "Should Netflix launch an ad
  tier?"

## `ai_instructions` persona notes

RCA: in-character data-holder (see above) — this overrides the usual
"warm interviewer" tone during the investigation phase; return to warm
interviewer tone only for the wrap-up/reflection.
Tradeoff: standard senior-PM persona, pushes on "what would change your
mind?" as the signature probing question.
