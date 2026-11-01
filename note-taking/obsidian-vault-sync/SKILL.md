---
name: obsidian-vault-sync
description: Sync server Obsidian vault to user devices via git+GitHub.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Git, Sync, GitHub]
    related_skills: [obsidian]
---

# Obsidian Vault — Git Sync

Use when the user asks to access/sync the Obsidian vault from their own device, or when vault git sync needs setup, maintenance, or troubleshooting.

## Vault location & file ops
- Vault: `$HOME/obsidian-vault` (`OBSIDIAN_VAULT_PATH` set in `~/.hermes/.env`)
- Reading/writing/searching notes = use the `obsidian` skill (file tools; it resolves the path from the env var). This skill only covers sync/setup.
- `Sistem yang Berjalan.md` inside the vault is the live snapshot of all running automations (cron jobs, services, scripts, integrations, guardrails) — update it whenever infra changes. The user expects it kept current; it is their reference for "what is running".

## Current state (as of 2026-08-23)
- git repo initialized (branch `main`), initial commit done, `.gitignore` in place
- `~/.hermes/scripts/vault_sync.sh` ready: commits + pushes; exits 0 silently when no origin remote or no changes (cron-safe)
- NOT yet pushed to GitHub — awaiting the user's GitHub username + classic PAT (scope: `repo`). Until `origin` exists the sync script no-ops.

## Finishing the GitHub sync (when user provides PAT)
1. Never write the token into notes or commits. Store via git credential helper, file mode 600.
2. Create the private repo:
   `curl -X POST -H "Authorization: token $PAT" https://api.github.com/user/repos -d '{"name":"obsidian-vault","private":true}'`
3. `cd $HOME/obsidian-vault && git remote add origin https://github.com/<user>/obsidian-vault.git && git push -u origin main`
   then persist creds: `printf 'https://<user>:<token>@github.com\n' >> ~/.git-credentials && chmod 600 ~/.git-credentials`
4. Wire a cron every 30m running `~/.hermes/scripts/vault_sync.sh` (same pattern as the existing `config_backup.sh` cron).
5. Verify: `git log origin/main` shows the push, and the user confirms the clone works on their laptop.

## Laptop onboarding (give to user, plain language)
- `git clone https://github.com/<user>/obsidian-vault.git`
- Obsidian → "Open folder as vault" → pick the cloned folder
- Optional two-way auto-sync: install the community plugin **Obsidian Git** (auto commit+push+pull on an interval)
- Result: notes Hermes writes on the server appear on the laptop; edits on the laptop push back to the server.

## Pitfalls
- `.gitignore` MUST exclude `.obsidian/workspace*.json`, `.obsidian/cache`, `.obsidian/graph.json`, `.trash/` — workspace files differ per device and cause merge conflicts. Template: `templates/obsidian-gitignore`.
- The sync script must be idempotent (silent no-op when no remote or no changes) so a cron can fire it freely.
- Never commit `.env`, tokens, or merchant keys — the repo is private, but still.
- If the user prefers Syncthing over git: works well on Android, awkward on iPhone (paid 3rd-party app); git+GitHub is the recommended path for laptop-only setups.

## Files
- `scripts/vault_sync.sh` — the sync script (mirror of the live one at `~/.hermes/scripts/vault_sync.sh`)
- `templates/obsidian-gitignore` — proven `.gitignore` for an Obsidian vault
