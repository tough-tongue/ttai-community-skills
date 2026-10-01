# Maintaining the community skills

Step-by-step recipes for updating these skills and getting the change into
every app. If you're working through Claude, you can also just say "follow
MAINTAINING.md to push my change" from a session opened in this folder.

## Where things live

| What | Where |
|---|---|
| Source of truth | <https://github.com/tough-tongue/ttai-community-skills> (public) |
| Your working copy | `~/coding/ttai-community-skills` |
| What Claude Code, Cursor and Codex load on your Mac | Links in `~/.claude/skills`, `~/.cursor/skills`, `~/.agents/skills` pointing at the working copy |
| What Cowork loads | The **ttai-community** plugin, installed from the GitHub marketplace |
| Old personal copies | `~/.skills-backup/<timestamp>/` |

Edits in the working copy take effect immediately on your Mac. Cowork, your
team and everyone else only get them after you **ship** (below).

## Ship a change

Run these from `~/coding/ttai-community-skills` after any edit:

```bash
scripts/bump-version.sh
```

```bash
claude plugin validate .
```

```bash
git add -A && git commit -m "<skill>: what changed" && git push
```

- `bump-version.sh` raises the version in all four manifests (patch by
  default). Use `minor` when you add a skill. **Skipping this is the #1 reason
  an update doesn't show up**: Claude Code, Cowork and Codex only offer an
  update when the version changes.
- Then refresh each app: see [Get the update into each app](#get-the-update-into-each-app).

## Recipes

### I edited a skill directly in the working copy

1. Test it: it's already live in Claude Code, Cursor and Codex on this Mac.
2. [Ship it](#ship-a-change).

### I edited a skill inside Claude or Cowork and exported a patch

```bash
cd ~/coding/ttai-community-skills && git pull
```

```bash
patch --dry-run skills/<name>/SKILL.md ~/Downloads/<name>.patch
```

If the dry run is clean, run the same command without `--dry-run`, check the
change against the rules in [AGENTS.md](AGENTS.md), then [ship it](#ship-a-change).
In Cowork, accept the warning that the update overwrites your local edit:
the update now contains it.

### I want to add a new skill

1. Copy the skill folder into `skills/<name>/`.
2. Scrub anything personal or internal. This must print nothing:

   ```bash
   grep -rnIiE '/Users/|/mnt/|/home/|jarvis|created_by|cloudfront' skills/<name>
   ```

   Also check: scenarios are created with `ttai:create_scenario` (not written
   into a repo), no internal IDs, no customer names, "Tough Tongue AI" spelled
   as two words. Full rules: [AGENTS.md](AGENTS.md).
3. Add `skills/<name>/agents/openai.yaml` (copy a sibling's; keep the ttai MCP
   dependency only if the skill creates scenarios).
4. Add a row for it to the table in [README.md](README.md).
5. Link it into your local agents:

   ```bash
   scripts/link-local.sh
   ```

6. [Ship it](#ship-a-change) with `scripts/bump-version.sh minor`.

If a personal copy of the same skill exists in your skill folders,
`link-local.sh` moves it to `~/.skills-backup/` and links the repo version in
its place.

### I'm setting up a new computer

```bash
git clone https://github.com/tough-tongue/ttai-community-skills.git ~/coding/ttai-community-skills
```

```bash
~/coding/ttai-community-skills/scripts/link-local.sh
```

Don't also install the plugin in Claude Code on that machine, or every skill
shows up twice.

## Get the update into each app

| App | How to update |
|---|---|
| Claude Code, Cursor, Codex on your Mac | Nothing to do: they read the working copy |
| Cowork | Customize → Plugins → **Update** on the `ttai-community-skills` marketplace |
| Claude Code elsewhere | `claude plugin marketplace update ttai-community-skills`, then `claude plugin update ttai-community@ttai-community-skills` |
| Codex elsewhere | `codex plugin marketplace upgrade ttai-community-skills`, then `codex plugin add ttai-community@ttai-community-skills` |
| Anything installed with `npx skills` | `npx skills update` |

First-time install in each app: see [README.md](README.md#install).

## Troubleshooting

| Problem | Fix |
|---|---|
| Cowork: "Plugin cannot be installed" | The real error is in `~/Library/Logs/Claude/main.log` (search for `Failed to install plugin`). If it says `Permission denied (publickey)`, the marketplace entry has slipped back to an SSH source: `.claude-plugin/marketplace.json` must use `"source": "url"` with the HTTPS `.git` URL. |
| Cowork's **Update** doesn't pick up the change | Check that you ran `bump-version.sh` and pushed. If it still says you're on the latest version, remove the marketplace and add it again (known Cowork bug). |
| A skill shows up twice | Usually an old copy uploaded to claude.ai (remove it under Customize → Skills), or the plugin installed in Claude Code on a machine that also has the local links. |
| I want an old personal copy back | Delete the link in the skill folder, then move the folder back from `~/.skills-backup/<timestamp>/`. |
| A field I set doesn't stick on the scenario | The public `create_scenario` API ignores or rejects some fields (`pdf_context`, `strategy.welcome_instructions`). Load the tool schema and check. |
