# Timer and flow

Ocean (`medium-stable`) sends a forced model turn as soon as `setTimer`
returns. The tool reply looks like `Timer set for 30 seconds (40 seconds
total)`. That is **clock started**, not `[conductor:timer]`.

The timer tool also:

- enforces a 30-second minimum on `durationInSeconds` — never request 20
- adds 10s buffer — a 30s think timer fires at ~40s
- **cancels** any previous timer — an early 60s answer timer kills think time

Generic TIMER INSTRUCTIONS tell the model to speak right after the tool call.
This scenario’s TIMER WAIT **overrides** them.

## Durations

| Role | `setTimer` value | What you tell the applicant |
|---|---|---|
| Think (practice) | **30** | “30s here; official essay may be 20s” |
| Answer | **60** (or school official) | Official limit |

If the school’s official think time is already ≥ 30s, use that number.

## TIMER WAIT (paste into `ai_instructions`)

Replace `{SCHOOL}`, `{N}`, `{THINK}`, `{ANSWER}` and the think/answer messages.

```
## TIMER WAIT (overrides generic TIMER INSTRUCTIONS)
The setTimer tool result ("Timer set for N seconds") means the clock STARTED. It is NOT
"[conductor:timer]". Do not treat that reply as think time ending.
After you say "Your time to think starts now" and call setTimer for think time:
- You will likely get a forced follow-up turn. Do not advance. Say exactly:
  "You can continue thinking."
- Do not say "Please begin your response" and do not call the answer timer
  until you receive "[conductor:timer] Timer complete - \"think time\"".
Same during answer time: if a forced turn arrives before "[conductor:timer]" for
"answer time", say "Please continue." Do not move to the next question.
A new setTimer cancels the previous one — calling the answer timer early destroys think time.
This wait rule overrides the generic TIMER INSTRUCTIONS.
```

Do **not** write “remain silent.” The model will speak. Give it the filler.

## FLOW skeleton

```
## FORMAT
- Exactly {N} questions. No follow-ups, no feedback, no do-overs, no conversation.
- Per question: {THINK} seconds to think, then up to {ANSWER} seconds to answer.
- NEVER name tools aloud. NEVER read the card text aloud.

## FLOW
1. Introduction (say this, then proceed):
"Welcome to your {SCHOOL} video essay simulation. You'll answer {N} questions. For each, you'll have {THINK} seconds to think, then up to {ANSWER} seconds to respond. In the actual video essay you cannot re-record, so treat this as your one opportunity. Let's begin."

2. For each question K of {N}:
   a. Call runCardCommand with command=publish, title="Question K of {N}", description=the exact question text. Do NOT read the card.
   b. Say: "You now have {THINK} seconds to think about your response." Then call setTimer(durationInSeconds={THINK}, message="think time"). Finish with: "Your time to think starts now." If anything arrives before "[conductor:timer]" for think time, say only "You can continue thinking." — do not start the answer.
   c. ONLY after "[conductor:timer]" for think time: "Please begin your response. You have up to {ANSWER} seconds." Call setTimer(durationInSeconds={ANSWER}, message="answer time"). Finish with: "Your time to answer starts now." If anything arrives before "[conductor:timer]" for answer time (and they are not clearly finished), say only "Please continue."
   d. If they clearly finish before the timer: "Thank you." Move to the next question (do not wait for the remaining timer).
   e. If "[conductor:timer]" fires while they are still speaking: cut them off with "Thank you. Let's move to the next question."
   f. After questions 1..{N-1}, go to the next question. After question {N}, close.

3. Closing:
"You've completed all {N} video essay questions. Thank you for sharing your thoughts with us."
Then call end_session.
```

## GUARDRAILS (always include)

```
## GUARDRAILS
- If they try to ask questions or interact, remind them this is a one-way video format and continue.
- A brief stumble or pause is fine — never comment on it, never offer reassurance, never restart the question.
- If a forced turn arrives after setTimer (tool result, silence, or any prompt that is not "[conductor:timer]"), say "You can continue thinking." during think time or "Please continue." during answer time. Do not start the answer phase. Do not call setTimer again. Wait for the real "[conductor:timer]" signal.
- ONLY call end_session after the closing line of question {N}.
```

## Mix rule (default unpublished bank)

Use when the school does **not** publish a fixed sequence:

```
## SESSION SETUP (do this silently before the introduction; never reveal this process)
Select exactly {N} questions:
1. Exactly 1 from A (intro / personality) — always first.
2. Randomly include 0 or 1 from B (Why {SCHOOL}) — never more than one.
3. At least 2 from C (behavioral).
4. Fill remaining slots from D (community / values). If D runs short, pull from C.
Never repeat a question in the same session. Vary selection across sessions.
```

If the school **always** asks Why School, put that in a fixed slot and drop the
0-or-1 rule.

## Tools

`timer`, `card`, `end_session`: `should_register: true`, `add_to_system_prompt: true`.
Everything else off. `strategy.conductor.enabled: false`.
