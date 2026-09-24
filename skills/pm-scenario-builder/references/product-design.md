# Product Design Cases

"Design/redesign X", "build a product using [hypothetical tech]", "what's
your favorite product [then redesign it]." Tests defining what-to-build —
the PRD-writing muscle.

## Subtypes

| Subtype | Signal | Extra move |
| --- | --- | --- |
| **Improvement** | "Improve ChatGPT / Instagram / Maps" | Ground in the product's actual current state and competitive gaps before segmenting |
| **New / moonshot** | Hypothetical tech ("Google built a Smell Teleportation API") | Clarify the tech's constraints (accuracy, cost, hardware, limits) FIRST — ground sci-fi in specs before segmenting |
| **Creative-brainstorm** | Interviewer explicitly pushes for 10+ ideas ("give me three more") | Keep generating past the first 3; impractical/funny ideas are fine — see Creative Escalation below |
| **Favorite-product** | "What's your favorite product?" | Short passionate intro (niche product, not a mega-hit) → almost always pivots into an Improvement case |

## The approach (candidate should cover this; solution must demonstrate it)

1. **Goals & constraints (2-3 min).** Clarify: what does success look like,
   what timeline (1yr vs 3yr vs 10yr — longer horizon = more license for
   10X), what's already off-limits. For moonshot cases: clarify the tech's
   accuracy/cost/hardware/limitations here, not later.
2. **Customer segments — go broad, then narrow (3-5 min).** Name 3 specific
   segments (never "millennials" — "immigrant families sending food smells
   home" beats "families"). Pick ONE based on market size, frequency of
   need, and willingness to pay. State why the other two lost.
3. **Problem deep dive (5-7 min).** Map the chosen segment's journey
   end-to-end. Find the real pain point (often trust/time, not the obvious
   surface complaint). Close with a "How might we..." statement — this is
   the pivot from problem space to solution space; keep them distinct.
4. **Solution design — variety, not just complexity tiers (7-10 min).**
   Offer 3 named solutions in escalating complexity (Simple → Medium →
   Moonshot), AND vary the delivery medium (don't make all three "an app").
   Name each solution (memorable > generic — "VetChat" beats "diagnostic
   tool"). At least one must be genuinely creative — see Brainstorming
   Techniques below. Never propose a feature that already shipped; if it
   exists, propose expanding/improving it instead.
5. **MVP & metrics (3-5 min).** Pick one solution with a clear rationale
   (speed to market, distribution leverage, technical feasibility).
   Metrics must tie back to the Step-1 goal (adoption goal → adoption
   metrics, not revenue). Use Google's HEART lens (Happiness, Engagement,
   Adoption, Retention, Task success) to pick the metric category.

## Brainstorming techniques (use ≥1 per solution set)

- **Anchor to emerging tech**: AR/VR, GenAI (text/code/multimodal, transfer
  learning), on-device ML, blockchain, API economy, space tech.
- **Analogies / biomimicry**: draw a mechanism from nature or another
  industry (kingfisher beak → bullet train nose; auto industry supplier
  networks → Maps' data suppliers).
- **Cross-industry transplant**: borrow a pattern from an unrelated
  industry and justify the similarity, even loosely.
- **Sci-fi/fiction anchor**: Harry Potter, other fiction — makes futuristic
  ideas concrete and memorable (teleportation ≈ Apparition + Floo Network).
- **SCAMPER**: Substitute / Combine / Adapt / Modify / Put-to-other-use /
  Eliminate / Rearrange — run it against the product's core mechanism.

## Creative escalation (Creative-brainstorm subtype only)

When the interviewer keeps asking for more:

- Don't freeze if told an idea already exists (e.g. "that's basically Uber
  Family") — acknowledge, ask for a moment, pivot to a fresh angle.
- Round 2+ ideas can get progressively more unconventional (drone delivery,
  vending machines, peer-to-peer sharing, programmable matter). This is
  expected and rewarded, not a sign of failure.
- `ai_instructions` persona for this subtype: "intentionally push for 10+
  solutions across the interview; acknowledge existing-feature callouts and
  redirect; accept humor as a valid response when generating many ideas."

## Quality bar for the reference solution

- 3 segments named specifically, 1 chosen with a stated reason.
- A real HMW statement, not skipped.
- 3 named solutions, escalating complexity, varied medium, ≥1 creative.
- MVP choice justified against ≥2 criteria (not just "this is easiest").
- Metrics category matches the Step-1 goal category.

## Example cases

- Improvement: "How would you improve ChatGPT?"
- Moonshot: "OpenAI can now translate animal communication. What would you
  build?", "Design a smell-teleportation product"
- Creative-brainstorm: "Design a car seat product for Uber"
- Favorite-product: "What's your favorite product, and how would you improve
  it?"

## `ai_instructions` persona notes

Standard: "senior PM, 8-10+ years consumer/enterprise, values structured
thinking balanced with creative ideas, pushes with probing 'why' questions,
provides hints only when candidate is stuck." For creative-brainstorm, add
the escalation persona above.
