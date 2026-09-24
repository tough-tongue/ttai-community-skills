# Tough Tongue AI Community Skills

Community-supported agent skills for [Tough Tongue AI](https://app.toughtongueai.com),
the platform for tough conversations: some the AI takes (voice agents that
call, demo, screen, and book), others you nail (realistic practice for
interviews, negotiations, and coaching).

The skills here are helpful, battle-tested workflows that sit outside the
core product plugin. Most of them build mock interviews and the study
material that goes with them. They work in Claude Code, Codex, Cursor, and
any agent that supports the [Agent Skills](https://agentskills.io) format.

> **Community-supported** means these skills are maintained on a
> best-effort basis and evolve faster than the core plugin. For the officially
> supported skills and the MCP server, see
> [tough-tongue/toughtongue-skills](https://github.com/tough-tongue/toughtongue-skills).

## Skills

| Skill | Use it when you say… | What it does | Needs |
|---|---|---|---|
| [pm-scenario-builder](skills/pm-scenario-builder) | "Turn this PM case into a scenario", "PM mock interview for…" | Classifies a PM interview case (Design, Strategy, Analytical, Execution, Technical, Behavioral), writes a full reference solution, and creates a candidate-led AI interviewer with a study guide and hire/no-hire rubric. | ttai MCP |
| [case-interview-builder](skills/case-interview-builder) | "Turn Case 7 into a mock case interview" | Builds an interviewer-led consulting case: a polished exhibit deck in Gamma, then a scenario that reveals each exhibit on cue, keeps the answer key hidden, and scores the math. | ttai MCP, Gamma MCP, Google Slides |
| [slides-scenario-builder](skills/slides-scenario-builder) | "Use slides instead of cards", "embed this deck" | Generates a teaching deck in Gamma and wires any scenario to a published Google Slides embed with a slide map the agent navigates. | ttai MCP, Gamma MCP, Google Slides |
| [system-design-interview-guide](skills/system-design-interview-guide) | "Make a study guide for Design Uber", "turn this Xu chapter into a scenario" | Turns a system design problem into a 20–25 page study guide PDF and an interviewer context pack, optionally published as a scenario. | Your source chapters; optional ttai MCP; pandoc, mermaid-cli, Chrome for the PDF |
| [case-interview-study-guide](skills/case-interview-study-guide) | "Make notes on Case 4" | Turns one casebook case into a phase-by-phase Word study guide with original notes, reference answers, and recreated exhibit charts. | docx, pdf, and dataviz skills |
| [mba-essay-guide](skills/mba-essay-guide) | "Essay guide for Kellogg", "what does Wharton's adcom look for" | Researches a school's essays and video essay across official, admissions-officer, applicant-reported, and consultant sources, and writes one tiered, source-tagged guide. | Web search |

## Install

### Prerequisite: the Tough Tongue AI MCP server

Skills that create scenarios call the Tough Tongue AI MCP server (`ttai`).
The easiest way to get it is the core plugin, which also brings the
`scenario-creator` and `scenario-refiner` skills these skills hand off to:

```bash
claude plugin marketplace add tough-tongue/toughtongue-skills
```

```bash
claude plugin install toughtongue@toughtongue-skills
```

Other agents: see the
[core setup guide](https://github.com/tough-tongue/toughtongue-skills#set-up).
The case-interview and slides skills also need the
[Gamma](https://gamma.app) MCP connector.

### Claude Code

```bash
claude plugin marketplace add tough-tongue/ttai-community-skills
```

```bash
claude plugin install ttai-community@ttai-community-skills
```

Skills are then available as `/ttai-community:pm-scenario-builder`,
`/ttai-community:case-interview-builder`, and so on, or just describe the task
and Claude picks the right one.

### Any agent (Agent Skills CLI)

```bash
npx skills add tough-tongue/ttai-community-skills
```

The CLI asks which skills to install and which agents to configure. Update
later with `npx skills update`.

### Manual

Copy any folder under `skills/` into your agent's skills directory (for
Claude Code, `~/.claude/skills/`).

## Try it

```text
Here's a PM case: "Spotify can build only one of two features this quarter:
collaborative playlists or a podcast discovery feed. Which one?" Turn it into
a Tough Tongue AI mock interview.
```

```text
Make a system design study guide for "Design a Rate Limiter" from the Xu
chapter I attached, then publish the interviewer pack as a scenario.
```

## Contributing

New skills are welcome. Read [AGENTS.md](AGENTS.md) first: community skills
have to be portable (no personal paths, internal repos, or internal IDs),
MCP-first when they create scenarios, and respectful of source copyright.
Open a pull request with the skill under `skills/<name>/` and a row in the
table above.

## License

[MIT](LICENSE)
