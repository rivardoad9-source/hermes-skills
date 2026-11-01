---
name: external-skill-adoption
description: Install third-party skill bundles from GitHub into Hermes.
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [skills, install, github, plugin, claude-code, onboarding]
    related_skills: [hermes-agent-skill-authoring, localhost-dashboard-serving]
---

# Adopting an external skill bundle (GitHub → Hermes)

The user drops a repo URL with *"tambahin skill ini"* / *"install this skill"* / *"pakai skill ini"*.
The deliverable is **the skill loadable in Hermes, its own tooling proven to run, and a one-line
how-to** — not a `git clone` left in `/tmp` and a summary of what the README says.

## When to Use

- user pastes a GitHub URL of a skill / "skill pack" / Claude Code plugin and asks to add it
- the guidance you need ships only inside an external bundle (e.g. a UI/design search engine)
- the ask is open-ended — *"cari skill di GitHub/hub yang penting dan berguna buat lu"* →
  use the hub path below (`hermes skills search / inspect / install`), no clone needed
- Don't use for: authoring a NEW skill of your own (`hermes-agent-skill-authoring`)

## Procedure

1. **Clone shallow and locate the payload.** `git clone --depth 1 <url>` into a scratch dir, then find
   the `SKILL.md` files. Bundles often hide them under `.claude/skills/<name>/` (Claude plugin layout)
   or `src/**`; the repo README usually advertises a *bundle* of siblings. Completion: you can name the
   one skill the user asked for **and** how many siblings exist.
2. **Read its SKILL.md** to learn the intended invocation. Relative paths (`scripts/…`,
   `references/…`, `data/…`) must resolve *inside the skill directory* — that dictates what you copy.
3. **Dependency probe before installing.** AST-walk the scripts for top-level imports
   (`Import`/`ImportFrom`) and confirm the set is stdlib or already installed, then run the entry
   point's `--help` inside the clone. Completion: usage prints locally.
4. **Install by copying the whole skill dir** — `~/.hermes/skills/<category>/<name>/` with SKILL.md +
   `references/` + `scripts/` + `data/`. Copying (rather than `skill_manage create`) preserves the
   bundled data files the scripts read at runtime.
   Install **only** the skill(s) the user named. A 7-sibling bundle copied whole adds 7 rows to the
   always-loaded skill index — mention the rest and offer them instead.
5. **Verify it loads**: `skill_view(<name>)` must return the SKILL.md *and* a `linked_files` list
   matching the upstream directories.
6. **Run one real query and show the output.** That is the proof, and it converts the skill from
   "installed" to "used". For search-style skills, dump the JSON keys once (`--json` / `--help`) before
   writing a parser — **key names differ per domain/file** in these datasets.
7. **Report**: install path, the exact command to invoke it, the first few findings, and — if it
   informed a deliverable — where it changed your output.

## Hub path: install straight from the registry (no clone)

For an open-ended "find skills that make you better at X" ask, search the hub instead of the web.

1. **Search.** `hermes skills search "<kata kunci>" --limit 8 --json`, then print
   `name | source | identifier | description` with python. Four sources come back: `official`,
   `skills.sh` (GitHub repos indexed by skills.sh), `clawhub`, and local skills. Identifier
   shape differs per source — `@author/name` (clawhub) vs `skills-sh/<owner>/<repo>/<skill>`
   (skills.sh). Run *several* keyword searches; one query misses whole categories, and the
   install line only accepts the exact identifier (`hermes skills inspect ffmpeg` returns a
   disambiguation table when the name exists in more than one source).
2. **Inspect before installing.** `hermes skills inspect <identifier>` prints trust level,
   license, `promptOnly`/`hasExecutableCode`, required env vars, and a SKILL.md preview.
   Prefer prompt-only skills with no paid API key (a subtitle skill that needs a hosted
   API key is worthless when local whisper already covers it).
3. **Install.** `hermes skills install <identifier> --category <cat> -y`. **`-y` is required
   in a non-interactive shell** — without it the prompt is auto-answered "N" and the install
   silently ends in "Installation cancelled". The installer prints a `skills-guard` scan
   verdict. `--force` clears only lower-severity blocks: a **DANGEROUS** verdict is refused even
   with `--force`, so a bundle like that needs the manual path in the next section. Installs land in `~/.hermes/skills/<category>/<name>/` and are
   tracked in `~/.hermes/skills/.hub/lock.json` (source, identifier, scan verdict, content hash).
4. **Audit what landed anyway** — the scan is a gate, not a guarantee, and community skills
   are *instructions*, so injected prose is the risk, not just binaries:
   `grep -rIn -E "curl [^|]*\| *(ba)?sh|base64 -d|ignore (all )?previous|rm -rf /|API_KEY|\.env" ~/.hermes/skills/<category>/<name>`.
5. **Verify and report.** `skill_view(<name>)` returns content immediately; `hermes skills list`
   shows source + trust + `enabled`. Report source/trust/license **and what the skill changed
   in your output** — an install nobody used is not the deliverable.
6. **Generic upstream names can look like a collision.** The installed directory name comes
   from the skill's own frontmatter (`name: social`), not the identifier, so a skill can land
   on a path that looks like a pre-existing one. Before claiming something got shadowed,
   check what actually existed: `tar -tzf ~/.hermes/skills/.curator_backups/<latest>/skills.tar.gz
   | grep -i <name>` (weekly full backup of the skills tree), plus `created_by`/`created_at`
   per skill in `~/.hermes/skills/.usage.json` and `.curator_ledger.jsonl`. Do that check
   *before* the install when the name is generic and it matters.

## When skills-guard blocks a legitimate skill

A DANGEROUS verdict comes from a text-pattern scan, not from running the code, so official vendor
docs trip it: `jailbreak_dev_mode` fires on any explanation of a real "developer mode" setting, and
`deception_hide` fires on the anti-hallucination rule *"do not tell the user the swap succeeded yet"*.
Treat the block as stop-and-classify, never as a silent bypass.

1. **Read every finding, not the verdict.** `hermes skills install <id> --category <cat> -y > /tmp/inst.txt 2>&1`
   then read the file; the report prints rule, `file:line`, and the matching snippet. Expect
   `--force` to be refused on DANGEROUS — do not retry it.
2. **Open those exact lines in a shallow clone** and judge intent. More honest or more cautious
   instructions toward the user are false positives. The `.hub/quarantine/` directory is emptied
   once the block is recorded, so re-fetch the bundle (`git clone --depth 1`) instead of hunting
   for the files there. Real findings hide actions from the user, pipe
   remote content into a shell, read credentials, or unpin a download.
3. **Install manually only when the content is clean**: `mkdir -p ~/.hermes/skills/<category> &&
   cp -r <repo>/<path>/<skill> ~/.hermes/skills/<category>/`. This skips the hub lockfile, so state
   the upstream commit and that the install bypassed the guard.
4. **Install the runtime separately.** Frontmatter names it (`metadata.openclaw.requires.bins` +
   `requiredCliVersion`); install that exact version (`npm i -g <pkg>@<version>`), then prove it with
   a command that needs no credentials: `--version`, `cli-check --json`, `wallet status --json`.
   A wallet/broker CLI grants no account access on install — login stays user-mediated (QR scan) —
   but say that out loud and keep "no state-changing command without explicit confirmation".
5. **Report verdict, classification, guardrail.** Which rules fired, why each is a false positive
   (or not), where it landed, and what you will not do without a fresh yes. Bypassing a security
   gate without telling the user is the one unacceptable outcome.

## Pitfalls

- **`npx skills add <owner>/<repo> --skill <name>` does not install into Hermes.** The skills.sh CLI
  writes to the project's `.claude/skills/`, which Hermes never reads. Translate the request to
  `hermes skills search` → the `skills-sh/<owner>/<repo>/<name>` identifier; the user pasting an npx
  command is describing the skill they want, not the install mechanism.
- **An installed external skill is user-owned.** Read and query it; do not patch it (writes are refused,
  and the content is upstream's). Improvements belong in *your* skills, or upstream.
- **Don't install into the middle of a tree.** Follow the category layout of
  `hermes-agent-skill-authoring`: `~/.hermes/skills/<category>/<name>/SKILL.md`.
- **The running session's skill index is cached** — `skill_view` works immediately after copying, but
  the system-prompt index may not list the new skill until a new session. Say so instead of calling it
  a failure.
- Bundles whose scripts import `pandas`/`numpy`/`requests` need a venv; stdlib-only ones run on plain
  `python3`. Check the LICENSE before redistributing anything from the bundle.
- Don't mirror the whole upstream doc set into your own skill — capture only the queries and outputs you
  actually used (see `references/ui-ux-pro-max-queries.md`).

## Verification

- [ ] `skill_view(<name>)` returns content plus `linked_files`
- [ ] the entry point was executed inside the installed dir and real output was shown to the user
- [ ] install path + invocation line reported, siblings listed as an offer

## References

- `references/ui-ux-pro-max-queries.md` — worked example: the design-search bundle
  (`nextlevelbuilder/ui-ux-pro-max-skill`), its layout, the query commands, and what each returned.
