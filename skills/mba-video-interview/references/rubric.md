# Rubric + processed rubric

Evaluate **the applicant**. Composure over polish. Do not require Why School
on every question — only when that prompt actually appeared.

Do not copy a live Kellogg interview rubric (school knowledge 25%,
questions-for-interviewer, active listening).

## Default weights (must sum to 100)

| # | Topic | Weight | `requires_video` |
|---|---|---|---|
| 1 | Person Behind the Paper | 25 | false |
| 2 | Think-on-Your-Feet Communication | 20 | false |
| 3 | Story Quality and Specificity | 20 | false |
| 4 | {School} Values in Action | 20 | false |
| 5 | On-Camera Presence | 15 | **true** (last) |

Rename #4 to the school’s own language (Sloan: principled leadership /
hands-on; Yale: community & impact; INSEAD: international / diversity).
Put official value words in CONTEXT and WHAT TO EVALUATE.

## Hard caps (put in raw `rubrik` and in each processed prompt)

- Scripted / memorized delivery, or intro = resume recap → Person Behind the Paper **cap 4**
- Cut off mid-sentence / no landing → Think-on-Your-Feet **cap 6** (a recovered stumble is **not** a ding)
- Vague “we did a project” with no personal action → Story **cap 5**
- Generic “collaborative culture” with no evidence → Values **cap 5**
- Frozen, note-reading, chaotic background → Presence **cap 5**
- No recording → Presence score 0, `score_str` `"N/A: no recording"`
- Fewer than 3 of N answered → incomplete; unanswered = 0; never invent content

## Raw `rubrik`

Use the Kellogg-style bands (Excellent 9–10 / Good 7–8 / Needs 5–6 / Poor 0–4)
for each of the five topics. End with Gating, Report Tone (name the clip,
e.g. “Q3 conflict story”), and Next Steps: exactly three drills — story bank,
60s timing, camera. No “be more confident.”

## `processed_rubrik`

```yaml
processed_rubrik:
  rubrik_hash: "user-set"
  criteria: []  # 5 entries
  report_instructions: |
    Use admissions-committee-facing language, not classroom-exam language. In strengths and
    weaknesses, name the specific question clip (e.g. "Q3 conflict story") rather than
    abstract traits. Keep detailed_feedback to 2-3 lines per criterion.
  next_steps_instructions: |
    Recommend exactly three drills: (1) a story-bank exercise — write 4-5 fresh STAR stories
    covering leadership, conflict, risk, and community impact that are NOT in the applicant's
    written essays; (2) a 60-second timing drill — practice out loud with a visible timer
    until answers land with 5-10 seconds to spare; (3) a camera drill — record a 60-second
    answer and review eye line, energy, and background. Do not give generic "be more
    confident" advice.
```

Each `prompt` is a **standalone panelist brief**. The judge sees only this
prompt + transcript (and video if `requires_video`). Structure:

```
CONTEXT: {School} MBA video essay practice ({cycle}) — {N} prompts, ~{THINK}s think,
up to {ANSWER}s one-take, no re-record. Score the APPLICANT only. {criterion-specific facts}

WHAT TO EVALUATE:
- observable checks for this criterion only

SCORING:
- 9-10 / 7-8 / 5-6 / 0-4 (or 4-6 / 0-3 for presence)
- zero case: If no questions were answered: score 0, note "no responses to evaluate".
- hard caps from the table above

OUTPUT: score (0-10), score_str, note citing the specific question or visual moment
```

Values criterion extra rules:

- Judge Why School **only if** that question is in the transcript
- Do not penalize a personality/curveball answer for missing professor names
- If neither values nor Why School was asked: score 5 (neutral) and say so

On-Camera Presence: stumble + breath/smile/recovery is a **plus**. If no
recording: 0 + `"N/A: no recording"`.

## Do not

- Leave `processed_rubrik` to auto-compile (coin flip on `requires_video`)
- Fall back to the platform's generic compiled rubric (Communication / Problem-Solving / Domain)
- Set all five `requires_video: true`
