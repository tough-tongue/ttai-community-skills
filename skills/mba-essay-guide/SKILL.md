---
name: mba-essay-guide
description: Research an MBA program's application essays (written prompts, video essays, optional and reapplicant essays) across the school's own site and blog, admissions officers on record, applicant-reported question banks, and the major admissions consultants (Aringo, Stacy Blackman, mbaMission, Vantage Point, Leland, Menlo, Clear Admit, Accepted, Personal MBA Coach, Sam Weeks, Stratus), then produce a single tiered, source-tagged markdown guide. Use this whenever the user names a business school and asks for an essay guide, essay research, video essay questions, "what does the adcom look for", "make a guide like the Kellogg one", or anything about MBA application essays for a specific school, even if they do not say "guide" or "skill".
---

# MBA Essay Guide

Turn "give me a guide for [School]'s essays" into a reader-friendly markdown guide that a first-time applicant can follow top to bottom, with every claim tagged by how much it can be trusted.

The reference output is `assets/example-kellogg-video-essay-guide.md`. Read it once before starting so you know what "done" looks like. The template it follows is in `references/guide-template.md`.

## Inputs

The user gives you a school name, and optionally:
- **Scope**: full essay component (default), or a single component such as "video essay only" or "the optional essay"
- **Cycle**: default is the current application cycle. Say which cycle you are researching in the guide header.
- **Audience**: default is an applicant. If the user says it is for building a practice scenario or a coaching rubric, keep the rubric section but expand it.

If the school has no video essay, the guide simply has no video section. Do not invent one.

## Why the tiering matters

Consultant blogs are abundant but they recycle each other and are sometimes a cycle out of date. A reader cannot tell which claims come from the school and which are inference. The whole value of this guide is that it separates the two. Every factual line carries one tag:

| Tag | Meaning |
|---|---|
| [Official] | The school's own website, application portal text, or admissions blog |
| [Adcom] | A named admissions officer on record (interview, podcast, conference Q&A) |
| [Reported] | Applicants recounting what they were actually asked (GMAT Club, Reddit, Clear Admit LiveWire, consultant client reports) |
| [Consultant] | Guidance from an admissions consulting firm |

When two tiers disagree (a prep-time figure, question count, word limit), show both and say which is more recent. Never silently pick one.

## Workflow

### Step 1: Confirm the school and check for format changes

Run one broad search first: `[School] MBA essay questions [current cycle]`. Read three or four results and answer:
- What is the exact current written prompt set and word limits?
- Is there a video essay, and did the format change this cycle (question count, timing, deadline)?
- Did the school restructure the application this year?

If the format changed, treat every source dated before the change as historical and label it that way. Format changes are the single most common way these guides go wrong.

### Step 2: Exhaustive source sweep

Work through `references/source-checklist.md` in order. It lists every source family with URL patterns, search queries, and what to extract from each. Do not skip tiers because the consultant coverage "feels complete"; the official blog and the applicant-reported lists are what make the guide better than the consultants.

Minimum bar before writing:
- The school's official How to Apply page (current cycle) and at least two posts from the school's admissions blog or news site about essays or video essays, including older posts that explain the design
- At least one admissions officer on record
- At least one applicant-reported question compilation (GMAT Club is usually the best; check dates)
- At least six consultant sources, including Aringo, Stacy Blackman, mbaMission and Vantage Point if they cover the school

Fetch full pages rather than relying on search snippets. Snippets miss the question lists and the caveats.

### Step 3: Reconcile

Before writing, build a scratch table of every factual claim (question count, prep seconds, answer seconds, deadline offset, retake policy, word limits, who reviews, order of review) with the source and date for each. Flag disagreements. These become the "Open questions and caveats" section, which readers value more than false certainty.

Deduplicate question banks across sources. Keep the applicant-reported list intact as its own block; merge consultant lists into a separate block and remove anything already in the reported list. Attribute each consultant prompt with a short code (VP, L, A, SW) as the example does.

### Step 4: Write the guide

Follow `references/guide-template.md` section by section. The section order is fixed so that guides for different schools read the same way. Rules:

- Lead with a format-at-a-glance table. Readers want the mechanics first.
- Put the school's own words about *why* the component exists in its own section. Paraphrase; keep any direct quote under 15 words.
- The question bank is layered: Official, Reported, Consultant, then a pattern-summary table that collapses everything into 6 to 8 buckets with a prep priority.
- Every prep tip is attributed. A tip with no source is your opinion; either find a source or cut it.
- End with a source library grouped by tier, with URLs and dates, so the reader can go deeper.
- Include a 10-point self-assessment rubric derived from the "what is measured" table.

### Step 5: Quality pass

Read the draft as a nervous applicant with 96 hours to record. Check:
- Could they act on Section 1 alone if they read nothing else? (They should be able to.)
- Is every disagreement between sources surfaced rather than hidden?
- Are dates on every consultant source, so staleness is visible?
- Is the question bank free of duplicates across tiers?
- Does the file open with the tag legend?

Save as `[school-slug]-essay-guide.md` (or `-video-essay-guide.md` if the scope is video only) in the working directory, or wherever the user asks, and share it.

## Style rules for the guide

- Plain, direct sentences. No em dashes or double hyphens anywhere in the guide; use commas, colons, or a new sentence.
- No emojis.
- Tables for anything with more than three parallel items. Bullets for lists of prompts. Prose for reasoning.
- Paraphrase sources. Direct quotes are rare, under 15 words, and never more than one per source.
- Name the school's people (deans, directors) when they are on record; it is what makes the [Adcom] tier credible.
- Do not pad. A section with nothing to say is deleted, not filled.

## Common failure modes

- **Trusting the first consultant page.** Several firms publish essay analyses in June and never update them; the school may change the format in July. Always check the school page last, so it wins.
- **Mixing tiers in one list.** A prompt from a consultant's "practice list" is not a reported question. Keep them apart.
- **Missing the historical design.** Schools often explained the component years ago and stopped. Search the school's blog with `site:` style terms and year ranges, and look for archived FAQ text on consultant sites (Aringo archives these).
- **Round timing.** If the user asks right after a round deadline, note that fresh applicant reports will appear in the following one to two weeks and say so in caveats.
