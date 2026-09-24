# Publishing the pack to Tough Tongue AI (`create_scenario`)

Load the `ttai:create_scenario` tool schema first — field names below are from previous successful runs but verify against the loaded schema. Fields go inside the tool's `scenario_data` argument.

| Pack section | Scenario field | Notes |
|---|---|---|
| Header + §1 + §2 (Q&A script, behavior notes) + §4/§5/§6 answer keys + §8 probe bank | `ai_instructions` | Persona (name, level), the problem statement to read aloud, the canonical answers to give when asked, behaviour notes, condensed answer keys and the probe bank. The public API has no separate context-document field, so condense rather than paste the whole pack; keep it under a few thousand words. |
| §10 timeline rows | `strategy.conductor.messages[]` (with `strategy.conductor.enabled: true`) | One entry per phase. Each needs `time_seconds`, `message`, `end_turn`, `trigger`, `content_mode`. The `message` is the conductor cue (e.g. "Move to estimation; play P10"). |
| §9 rubric | `rubrik` | Field name has no trailing "c". Accepts full markdown. |
| §9 strong/weak signals | `session_analysis.extraction_vars` (with `enable_extraction: true`) | Types supported: `"text"`, `"number"`, `"boolean"`, `"list"`, `"date"`. Typical vars: `caught_key_estimation_step` (boolean), `deep_dives_covered` (list), `sharding_choice_and_defense` (text). |
| — | `tools_config.tools.end_session` | Set `should_register: true` and `add_to_system_prompt: true` so the interviewer can end at 45 min. |

Before creating: confirm the organisational context — call `ttai:list_organizations` and ask whether this is personal or for one of the user's organizations (pass `org_id` if so). Scenarios are org-scoped. After creating, return the scenario ID and name in the reply.
