# Case File Intake

How to read a negotiation case file and map it onto scenario fields.

## Expected shape

Case files for this pattern (e.g. a classroom design note, an instructor's
adaptation memo) tend to contain some subset of these sections. Look for
them by meaning, not by exact heading text:

1. **Case summary and the twist** — what the negotiation is visibly about,
   and (if present) the hidden compatible interest that makes a win-win
   possible. This is instructor-only material — it never appears verbatim in
   either side's `user_instructions` or `ai_instructions`.
2. **Roles** — who the student plays, who the AI plays, and why that
   assignment was chosen (usually: the AI's role is the more guarded/
   suspicious-sounding one, giving the student a real trust obstacle).
3. **General information** — facts both parties know and would state
   identically. This goes at the top of both instruction blocks, word for
   word.
4. **Each side's private information** — facts only that side knows. The
   student's side goes in `user_instructions`; the AI's side goes in
   `ai_instructions`. Never cross-contaminate.
5. **AI behaviour rules** — persona, opening style, what triggers a reveal,
   concession logic, escalation/walk-away conditions. This is the richest
   section — feed it into the Resistance Pattern and Guarded Disclosure
   Phases in [resistance-and-disclosure.md](resistance-and-disclosure.md).
6. **Tough Tongue AI configuration** — any explicit `max_duration_seconds`,
   conductor timing, silence behavior, or extraction/rubric the case author
   already specified. Prefer these over invented defaults.
7. **Rubric** — evaluation categories and weights for the student.
8. **Extraction variables** (optional) — only wire these up if the case file
   defines them; otherwise default to analysis-only (`enable_extraction:
   false`).
9. **Debrief questions** (optional) — carry into the rubric's report format
   if present; these are for the professor, not the student.
10. **Variants** (optional) — replay ideas (swap seats, change quantities,
    asymmetric power). Note them for later; don't build them unless asked.

## When sources disagree

If you're given more than one document (a build note plus a separate PDF
adaptation, say) and they specify different opening styles, disclosure
rules, or timing, do not blend them silently and do not guess. Ask the user
which document is authoritative, or which specific rule to follow, before
drafting.

## Public vs private — the hard boundary

- `user_instructions` gets: general information + the student's own private
  brief + prep prompts + how-to-succeed + what-to-expect. Nothing from the
  AI's private brief, nothing about the twist.
- `ai_instructions` gets: general information + the AI's own private brief +
  behaviour rules. Nothing about the student's private brief beyond what a
  real counterpart could plausibly assume or have heard as a rumor.
- `user_friendly_description`, `rubrik` visible to the student (check
  `analysis_access`), and any shared context field: never the twist, never
  the solution.
- The rubric text itself is only shown to the student after the session (or
  never, depending on `analysis_access`) — even so, don't use it to coach
  during the session; it's an evaluation document, not a hint sheet.
