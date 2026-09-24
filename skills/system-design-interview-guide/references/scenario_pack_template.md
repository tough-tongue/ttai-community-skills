# Scenario Context Pack Template (interviewer-facing)

This is the document an AI interviewer (or a human scenario author) reads to run the mock. It is denser and more directive than the study guide: it tells the interviewer what to answer when asked, when to let a weak answer stand and probe, and how to weight signals.

Header block:

```
# Design <System> — Interview Scenario Context Pack

**Purpose:** Complete reference material for building a voice-based, timed system design
interview scenario (<persona level> persona). Synthesized from <sources>, plus interview-design judgment.

**Difficulty:** <level>. <One sentence: the question's centrepiece and where signal concentrates (a), (b), (c).>

**Similar problems:** <aliases>
```

Then exactly these ten sections, numbered:

## 1. What the System Is
Two or three sentences. What it stores, what it answers, what is out of scope.

## 2. Requirements Clarification — The Question Design Core
- **Canonical Q&A script** table `Candidate should ask | Interviewer answer`. These are the answers the AI gives when asked; keep them short and unambiguous.
- **Requirements the candidate should converge on** — functional / non-functional.
- **Interviewer behavior note(s)** — how to handle the standard trap ("let them state it, then probe latency at scale"); what to do if the candidate skips scoping (play the scoping-trap probe).

## 3. Back-of-the-Envelope Estimation
Exact numbers from the source with the arithmetic chain. If two sources differ, give both variants and name which is ground truth for the scenario. End with **What to grade** — the one or two steps that separate strong from weak.

## 4. API and Data Model (Answer Key)
Signature, parameters, return shape; the stored entities and where each lives.

## 5. High-Level Design (Answer Key)
Subsystem decomposition; Mermaid diagrams in fenced ```mermaid blocks (the pack stays markdown; diagrams render in viewers that support Mermaid); write path and read path as short numbered lists; **Whiteboard-credit checklist**.

## 6. Deep Dives (Where the Signal Lives)
Numbered `### 6.x` subsections mirroring the study guide's Part 5, but written as answer keys: the expected answer core, the refinements that earn extra credit, and the failure modes. Where a trade-off is genuinely contested, preserve both options with the risk named — the rubric grades whether the candidate articulates the trade-off, not which side they pick.

## 7. Wrap-Up Talking Points (Bonus Credit Menu)
The source's follow-ups, one line each, for the last five minutes.

## 8. Interviewer Probe Bank (with hint ladders)
~13 probes. Format is fixed because the conductor script depends on it:

```
**P4. "<probe, in the interviewer's words>"**
- L1: "<nudge>"
- L2: "<direct hint>"
- Expect: <answer core>; <bonus if mentioned>.
```

Tag at least one probe each as (Estimation probe), (Client/ops probe), (Scoping trap, early).

## 9. Rubric Signal Guide (for weighting)
**Strong positive signals** bullets; **Common mistakes / weak signals** bullets. These become the `rubrik` markdown when publishing.

## 10. Suggested Interview Timeline (45-minute voice format)
Table `Time | Phase | Conductor intent`, referencing probe numbers. These rows become `strategy.conductor.messages` when publishing.

## References
Sources as cited in the material; companion packs and which shared theory lives where.
