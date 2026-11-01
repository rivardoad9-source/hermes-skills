---
name: work-activity-reporting
description: "Use when the user asks what work has been done."
triggers:
  - check in rutinitas mingguan
  - rekap minggu ini
  - apakah kita ada improvement
  - laporan mingguan kerja
  - laporan kerja magang
  - apa aja yang dikerjain
  - rekap kerja mingguan
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [reporting, worklog, evidence, honesty]
    related_skills: [weekly-review-planning, session-librarian, obsidian, hermes-cron-automation]
---

# Work activity reporting

Use when the ask is "kasih laporan apa aja yg udh dikerjain", "what have you done so far", "report
everything from this project", or an end-of-block summary. The user wants a record of work **done**,
not a plan and not reassurance.

## Gather from artifacts, never from memory alone

```bash
cronjob action=list                                   # what is active / paused, and last output
gh api 'repos/OWNER/REPO/commits?since=<ISO>' --jq '.[].commit.message' | head
ls -lt ~/obsidian-vault | head -20                    # deliverables this lane produced
process action=list ; pm2 list                        # services actually running vs stopped
grep -a -c . ~/.hermes/<lane>/sales.log               # `-a`: these logs read as "binary file"
```

Counting real events beats impressions. In the Oct 2026 report the sales log held only test events
(`TESTREF001`, `TUNNELTEST001`), which turned "no sales yet" from a guess into an evidenced line.

## Structure that worked

1. One section per lane (A, B, C …) — what was executed, in order, with the command or path that
   proves it.
2. A dedicated **"Yang jujur belum selesai"** section, as its own numbered list.
3. A table of every artifact produced: path + one-line description.

The gaps section is the most valued part, not a disclaimer: missed deadlines, zero revenue, adapters
never tested against the real provider, features still single-tenant.

## Rules

- Never claim a completion you cannot point at a file, commit, exit code, or live URL. If it was not
  verified, write "belum diverifikasi" rather than implying success.
- Report counts of artifacts (files, tests passing, rules added), not achievements. "25 dari 25
  skenario uji lulus" is defensible; "produk siap jual" is not.
- Reuse numbers already verified earlier in the session (test counts, config counts, listing counts);
  do not derive a new metric for the report.
- The report answers what WAS done — keep next steps in a short, clearly separate closing section so
  it does not read as a to-do list.
- Do not pad with intentions or plans. Empty lanes are reported as empty.

## Style for this user

Indonesian, santai, akrab, `gw/lu`. **No hyphen characters** — use numbered or line-separated items.
Write the full report as a markdown note in `~/obsidian-vault/` so it is readable on the phone, then
lead the chat message with what changed, followed by the honest gaps and the nearest next steps.
Attach deliverables with `MEDIA:` lines when the report refers to files.

## Weekly check-in delivered later (deck + scheduled send)

When the user asks for a recap "nanti jam 20:00" while away from the keyboard, do NOT schedule a job
that builds the report at fire time. Build and verify it NOW, then schedule only the delivery:

1. Gather evidence (cron job list + `cron/output/<job_id>/` file counts, `cron/jobs.json`
   `created_at` for "what is new this week", `git log --since` per repo, vault file mtimes).
   `executions.db` only keeps ~1 day, so file counts are the durable weekly evidence.
2. Say explicitly what did NOT happen: repos whose last commit predates the window, lanes whose
   verdict was "stay out", loop outputs with zero promotions. This is the section the user values.
3. Build the deck with the `powerpoint` skill (JSON spec → `pptx_create.py`), then make the index
   slide clickable with internal jump links: `slide.part.relate_to(target.part, RT.SLIDE)` for the
   rId, then append to the run's `a:rPr` an `a:hlinkClick action="ppaction://hlinksldjump"` holding
   `a:sldTgt r:id=...`. Re-open the file and count the links to verify.
4. Write the same recap as a vault markdown note, and a plain "send verbatim" text file
   (message + trailing `MEDIA:/abs/path.pptx`).
5. Schedule a one-shot cron AT the requested time whose prompt is only: read that file and output it
   character for character, never paraphrase, keep the `MEDIA:` line. Use `attach_to_session: true`
   so the user can reply into it. Avoid spaces in the media filename (`MEDIA:` parsing is safer).
