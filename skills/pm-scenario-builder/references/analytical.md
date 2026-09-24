# Analytical Cases

Metrics, estimation, and A/B testing. Often follow-ons to a Design/Strategy
case, but write each as a standalone scenario. All three subtypes share one
principle: **the number/metric matters less than the structured process and
stated assumptions.**

## Subtype: Metrics — the GAME framework

Signal: "define success metrics for X", "how would you measure Y."

1. **Goals.** Clarify: new launch or established feature? Primary business
   goal (engagement / creator growth / monetization)? Competitive context?
2. **Actions.** Map user behaviors across ALL stakeholder sides (a feature
   is rarely one-sided — e.g. Reels has creators, viewers, advertisers,
   platform). List behaviors per side.
3. **Metrics.** Go broad FIRST — brainstorm metrics for every side listed
   in step 2, comprehensively, before narrowing. This breadth pass is what
   separates a strong answer from a shallow one.
4. **Evaluate.** Narrow to exactly 3 priority metrics + 1 guardrail metric.
   Justify why each survived the cut. State the trade-offs you're willing
   to accept (e.g. "10% Feed cannibalization is acceptable if it prevents
   losing users to a competitor entirely").

Rules: metrics must drive action — if a metric moving doesn't change a
decision, cut it. Include ≥1 guardrail against an unintended consequence of
the launch. Benchmark at least one metric against an industry-standard
number (DAU/MAU, NRR, etc.) if the case allows it.

## Subtype: Estimation — 5-step structured guess

Signal: "estimate the [market size / storage / revenue] of X."

1. **Clarify requirements** — timeframe (annual vs accumulated), scope
   (global vs US), what's included/excluded.
2. **Break down into components** — pick ONE technique and name it:
   formula-based (price × quantity), segmentation-based (user tiers),
   part-based (base/body/top), or geography-based (US → world via GDP/pop
   ratio). Explain why this breakdown works before computing.
3. **Perform the estimation** — use anchoring (known facts: US pop 300M,
   world pop 8B, US GDP $23T) and proxies (a related, easier-to-estimate
   quantity) for each component, then aggregate. Keep a running number.
4. **Sanity check** — order-of-magnitude check ("does 100 EB feel right for
   a decade-old billion-user video platform?") and a personal-reference
   check where safe.
5. **Communicate uncertainties** — name 2-3 assumptions that could be wrong
   and what you'd validate with more time/data.

Never present a bare final number with no shown work — the process is the
answer.

## Subtype: A/B testing — hypothesis, PICOT, biases

Signal: "what A/B tests would you run on X to increase Y."

1. **Brainstorm 4-5 candidate experiments before picking any** — don't lock
   onto the first idea.
2. **Pick 2-3 and, for each:**
   - **Hypothesis**: null (no difference) vs alternative (specific,
     directional effect).
   - **PICOT**: Population, Intervention (the exact change), Comparison
     (control), Outcome (primary metric, secondary metrics, guardrail
     metric — always all three tiers), Time (long enough to outlast
     novelty/primacy effects, tied to the product's natural cycle).
3. **Name the biases explicitly**: novelty effect (initial curiosity
   inflates results — monitor 4+ weeks), primacy effect (users resist
   change initially — don't kill a good idea on early negative signal),
   interference (treatment/control groups talking to each other),
   statistical significance (p < 0.05 convention, sample-size awareness).

Rules: always propose outcome metrics in three explicit tiers — Primary
(the revenue/growth metric), Secondary (mechanism metric), Guardrail
(what could break). Ground each experiment in a real product mechanism the
company has actually invested in (AR, ML ranking, etc.) rather than a
generic "change the button color."

## Quality bar for the reference solution

- Metrics: broad-then-narrow visibly shown, exactly 3 + 1 guardrail.
- Estimation: named breakdown technique, ≥2 anchors/proxies cited, a sanity
  check performed (not skipped), uncertainties named.
- A/B: ≥2 fully-specified PICOT experiments, all 3 bias types named
  somewhere in the answer.

## Example cases

- Metrics: "Define success metrics for Instagram Reels"
- Estimation: "How much storage does YouTube need per year?", "Estimate
  Google Play Store revenue"
- A/B: "Design an A/B test for a Facebook feature", "How would you test
  Facebook Reactions?"

## `ai_instructions` persona notes

Senior PM with domain expertise matching the case (e.g. ads PM for A/B ads
cases, growth PM for metrics cases). Values rigor over guessed final
answers; pushes on "why that metric/breakdown/experiment specifically."
