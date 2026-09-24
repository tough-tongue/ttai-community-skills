# Scenario Payload Reference

Field defaults, tool config, and boilerplate blocks shared by every PM
scenario, regardless of type. These go into the `scenario_data` argument of
`ttai:create_scenario`. Load the MCP tool schema before calling: it is the
source of truth for field types. Copy the defaults exactly; a deviation (for
example re-enabling `whiteboard`) should be a deliberate choice, not a
copy-paste miss.

## Contents

- Top-level fields
- The CRITICAL candidate-led block
- Opening block
- `tools_config` defaults
- `strategy` / `session_analysis` defaults
- `ai_model_config` / `appearance`
- `rubrik` shape

## Top-level fields

```json
{
  "name": "PM Interview: {Type} - {Case Name}",
  "type": "default",
  "user_friendly_description": "{one sentence: what they'll practice and why it matters}",
  "ai_instructions": "{interviewer prompt, see SKILL.md Step 5}",
  "user_instructions": "{candidate study guide, see SKILL.md Step 5}",
  "rubrik": "{weighted rubric, see below}",
  "is_public": true,
  "is_recording": false,
  "user_metadata": {
    "question_type": "{Product Design | Product Strategy | Analytical | Execution | Technical | Behavioral}",
    "track": "Product Manager"
  }
}
```

- `name`: use `"{Company} PM Interview: {Case Name}"` instead when the company
  is the hook (e.g. "Netflix PM Interview: Ad Tier Decision").
- `is_public: false` makes the scenario reachable only through an access
  token. Ask the user if they want it private.
- Omit `id`: the server assigns one.

## The CRITICAL candidate-led block

Paste this verbatim near the top of `ai_instructions`, right after the
Persona bullets, in every scenario:

```markdown
## Interview Approach - CRITICAL
The frameworks and solutions provided in here are reference examples only, NOT requirements. PM interviews should be candidate-led - let them drive their own approach and demonstrate their unique thinking. Your role is to:
- Ask probing questions to explore their reasoning ("Why did you choose that approach?" "What else might you consider?")
- Guide through curiosity, not prescription ("Tell me more about..." "How would you handle...")
- Accept alternative frameworks and paths as equally valid if well-reasoned
- Never force the reference framework - it's simply one of many valid approaches
Remember: You're evaluating their thinking process and problem-solving ability, not their adherence to a specific framework.
```

## Opening block (every `ai_instructions`)

Every scenario opens with the same four beats: greet, present the case
verbatim, open Notepad, invite questions.

```markdown
### Opening (2-3 minutes)
- Welcome warmly: "Hi, I'm a product manager at {Company}. Today we'll work through a {type} case."
- Present the case: "{exact case question}"
- Open Notepad using Notepad tool so the candidate can write down their thoughts and solutions.
- Add: "Take a moment to think. Feel free to ask clarifying questions."
```

## `tools_config` defaults

```json
{
  "tools": {
    "notepad":              { "should_register": true,  "add_to_system_prompt": true,  "tool_settings": null },
    "card":                 { "should_register": true,  "add_to_system_prompt": true,  "tool_settings": null },
    "end_session":          { "should_register": true,  "add_to_system_prompt": true,  "tool_settings": { "disconnectDelaySeconds": 2 } },
    "mermaid":              { "should_register": false, "add_to_system_prompt": false, "tool_settings": null },
    "whiteboard":           { "should_register": false, "add_to_system_prompt": false, "tool_settings": null },
    "timer":                { "should_register": false, "add_to_system_prompt": false, "tool_settings": null },
    "mcq":                  { "should_register": false, "add_to_system_prompt": false, "tool_settings": null },
    "pdf_upload":           { "should_register": false, "add_to_system_prompt": false, "tool_settings": null },
    "memory_search":        { "should_register": false, "add_to_system_prompt": false, "tool_settings": null },
    "knowledge_base_search":{ "should_register": false, "add_to_system_prompt": false, "tool_settings": null },
    "google_slides":        { "should_register": false, "add_to_system_prompt": false, "tool_settings": null },
    "image_generation":     { "should_register": false, "add_to_system_prompt": false, "tool_settings": null }
  }
}
```

Exception: **Technical / system-design** cases turn `mermaid.should_register`
on (candidates sketch architecture diagrams). See [other.md](other.md).

## `strategy` / `session_analysis` defaults

```json
{
  "strategy": {
    "skip_auto_start": false,
    "silence": null,
    "conductor": { "enabled": false, "messages": [] },
    "system_instructions_template": "minimal"
  },
  "session_analysis": {
    "is_auto_analysis": true,
    "is_auto_submit": false
  }
}
```

`skip_auto_start: false` means the interviewer speaks first. Keep
`is_auto_submit: false` for interview practice: the candidate decides when a
session is worth scoring.

## `ai_model_config` / `appearance`

```json
{
  "ai_model_config": { "provider": "Galaxy", "model": "medium" },
  "appearance": {
    "voice": "Puck",
    "language_code": "en-US",
    "avatar_url": null
  }
}
```

- `voice`: any native voice (Aoede, Charon, Fenrir, Kore, Puck). Pick one
  that fits the interviewer persona.
- `avatar_url`: ask the user if they have an interviewer avatar; otherwise
  leave it `null` for the platform default.

## `rubrik` shape

Weighted categories that sum to 100%, each with 4-5 evaluation questions,
then four hire tiers. Categories should mirror the type's approach steps
(e.g. Design → Goal Clarification, Segmentation, Problem Depth, Solution
Design, Prioritization, Communication).

```markdown
# {Company} PM Interview Evaluation Rubric: {Case Name}

## 1. {Category} ({Weight}%)
- {Evaluation question}
- ...

## 2. {Category} ({Weight}%)
...

## Overall Assessment Categories

### Strong Hire
- {trait}
...

### Hire
...

### Lean Hire
...

### No Hire
...
```
