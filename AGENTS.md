# ttai-community-skills — Agent Guide

Community-supported skills for Tough Tongue AI. These are useful workflows
that are not part of the core product plugin
([tough-tongue/toughtongue-skills](https://github.com/tough-tongue/toughtongue-skills)).
This repo is public and installs directly into end users' agents, so every
word ships.

## Rules

- **Portable, not personal.** No absolute paths (`/Users/...`, `/mnt/...`,
  `/home/...`), no references to internal Tough Tongue AI repos, CLIs, or
  scenario files, no internal user/org/creator IDs, no customer or partner
  names. A skill must work for someone who has only the public MCP server
  and this repo.
- **MCP-first when a skill creates scenarios.** Scenario-building workflows
  end in `ttai:create_scenario` / `ttai:update_scenario`, never in "write a
  file into a repo and run an upload command". Use only fields the public
  `create_scenario` schema accepts (no `id` on create, no `created_by`,
  `metadata`, `is_featured`, `is_paid`, `pdf_context`, or
  `strategy.welcome_instructions`; use `user_metadata` for tags). When in
  doubt, load the tool schema: it is the source of truth.
- **Qualified tool names.** Reference MCP tools as `server:tool`
  (`ttai:create_scenario`, `Gamma:generate`). Don't name host-specific agent
  tools (`present_files`, `SendUserFile`, `AskQuestion`, `tool_search`);
  describe the action instead ("share the file with the user").
- **No secrets.** Never hardcode tokens. Authentication is the MCP client's
  OAuth flow; the only credential ever named is the `TTAI_PAT` environment
  variable, by name only.
- **Respect copyright.** Skills that work from books or casebooks produce
  original notes and adapted solutions. Never ship verbatim excerpts from a
  source book in a skill file, and keep quotes in outputs under 15 words.
- **Token discipline.** Keep SKILL.md under ~250 lines; push depth into
  `references/` files that the skill tells the agent to load. Files over 100
  lines carry a Contents block at the top.
- **Public bar.** "Tough Tongue AI" (two words), not "ToughTongue". No
  unfinished sections or hallucinated features.

## Structure

- `skills/<name>/SKILL.md` — frontmatter (`name`, `description`) + workflow.
  The description doubles as the trigger: front-load the key use case in the
  first sentence and include the phrases users actually say.
- `skills/<name>/references/`, `assets/`, `scripts/` — depth files, templates,
  and helper scripts the skill points to.
- `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` — Claude
  Code plugin and marketplace manifests. The marketplace plugin `source` must
  stay `{ "source": "url", "url": "https://github.com/tough-tongue/ttai-community-skills.git" }`.
  Don't use `{ "source": "github", ... }`: installs clone it over SSH and fail
  with "Plugin cannot be installed" for anyone without a GitHub SSH key.
  Don't use the string shorthand `"."` either: Claude Desktop/Cowork sync
  rejects it.
- `plugin.json` (root) — Agent Plugins 1.0.0 manifest
  (<https://agent-plugins.org>).
- `scripts/link-local.sh` — links every skill into the local agents' skill
  folders for development; `scripts/bump-version.sh` — keeps the manifest
  versions in sync.
- This plugin deliberately ships **no MCP config**: the core `toughtongue`
  plugin registers the ttai MCP server, and registering it twice creates
  duplicate servers.

## Adding a skill

1. Copy the skill folder into `skills/<name>/`.
2. Scrub it against the Rules above. A quick check:
   `grep -rnIiE '/Users/|/mnt/|/home/|jarvis|created_by|cloudfront' skills/<name>`
   must return nothing.
3. Add a row to the catalog table in `README.md` (what it does, what it needs).
4. Run `scripts/bump-version.sh` (bumps `version` in `plugin.json` and
   `.claude-plugin/plugin.json` together). Without a bump, Claude Code and
   Cowork users on marketplace installs don't update.
5. `claude plugin validate .` must pass.
