# Hermes Skills

A working collection of 120 agent skills: Markdown playbooks (`SKILL.md`) that tell an
AI agent how to actually do a job — with the procedures, the verification steps, and the
pitfalls that cost real time.

Most of these run daily on a Linux VPS driven by an agent: research, design, documents,
PR workflows, dashboards, cron jobs, media pipelines. Some are original, some are ports
of public skills with their attribution kept intact.

## Layout

```
creative/            24  design, HTML artifacts, infographics, diagrams, video, music
productivity/        28  docs, PDF, slides, sheets, calendar, job hunting, planning
software-development/15  debugging, TDD, code review, planning, security audit
github/               7  auth, repos, PR workflow, review, issues, issue-to-PR, account ops
research/            10  arxiv, citations, monitoring, market/claim verification
devops/               8  cron automation, dashboards, tunnels, MCP servers, deploys
media/                7  captions, clipping, subtitles, short-form video, YouTube
autonomous-ai-agents/ 6  driving Claude Code, Codex, OpenCode, a real desktop, Hermes itself
mlops/                5  HF Hub, vLLM, llama.cpp, eval harness, Weights & Biases
social-media/         3  X/Twitter posting and lookup
email/                2  inbox triage, himalaya CLI
note-taking/          2  Obsidian, vault sync
no-ai-slop/           1  strip AI-isms from writing
smart-home/           1  Philips Hue via OpenHue
web/                  1  recovering blocked pages
```

## Install

```bash
git clone https://github.com/rivardoad9-source/hermes-skills.git
cp -r hermes-skills/*/ ~/.hermes/skills/          # Hermes Agent (categories map 1:1)
cp -r hermes-skills/creative/* ~/.claude/skills/  # Claude Code style: copy the leaves
```

ZIP: <https://github.com/rivardoad9-source/hermes-skills/archive/refs/heads/main.zip>

## What a skill looks like

```markdown
---
name: localhost-dashboard-serving
description: Use when serving agent data as a phone-accessible page.
---

## When to Use
...
## Pitfalls
- A live tunnel process can serve a dead URL ...
```

The `description` line is the trigger: an agent matches on it before reading the body.
The `Pitfalls` section is the part worth reading first — it is a list of failures, not
advice.

## Not included

Anything tied to a live trading book, private wallets, client work, or a specific
business is deliberately left out of this repo. These are the generic, reusable parts.

## Third-party skills

`humanizer` (Siqi Chen, MIT), `claude-design` (BadTechBandit, MIT), the `docx` / `pdf` /
`xlsx` / `powerpoint` document skills (Anthropic, MIT), and several others keep their
original frontmatter and LICENSE files. Check the header of any skill before you
redistribute it further.

## License

MIT for the material authored here. See `LICENSE`. Third-party skills stay under their
own licenses.
