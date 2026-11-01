# Deadline reminders for courses/certs — one-shot, never a recurring lane

Companion to `indonesia-course-cert-sources.md`. Records what to do with the dated items after the
opportunity list has been delivered (verified 6 Okt 2026).

## The preference that governs this

The user **refused a recurring cron for the job/internship hunter** ("ga ush jadi cron job") but
accepted — and valued — **one-shot deadline reminders** for dated course/cert items. So:

- Do **not** re-propose a recurring scanner for courses, internships or certs.
- **Do** set one-shot reminders yourself for anything with a closing date, and say plainly in the reply
  that they are removable (one line: "kalau ga mau, bilang aja gw cabut").

## Pattern that worked (3 reminders: Rakamin H-2, Accurate H-1, AWS AI Academy H-2)

1. One tiny script per reminder under `~/.hermes/scripts/` that just `cat`s the message text —
   deterministic, 0 tokens, no LLM in the loop:

   ```bash
   #!/usr/bin/env bash
   # Reminder sekali-jalan: deadline Rakamin Project-Based Internship (H-2)
   cat <<'MSG'
   🎓 REMINDER — Rakamin Project-Based Internship

   Deadline daftar: 11 Okt 2026 (H-2 dari sekarang).
   Magang virtual 28 hari, tanpa seleksi, Rp180.000/program.
   Output: sertifikat magang resmi dari perusahaan mitra + portfolio + talent pool.

   Daftar: https://app.rakamin.com/virtual-internship-experience
   MSG
   ```

2. `cronjob(action="create", schedule="2026-10-09T09:00:00", no_agent=true,
   script="course_remind_rakamin.sh", deliver="origin", name="Reminder: …")`
   — an ISO timestamp fires **once**; the host TZ is already WIB, so no `TZ=` gymnastics.

3. `bash <script>` once before scheduling. A heredoc typo ships a reminder that only fails at the
   deadline, when it is too late to matter.

4. Fire at **H-2 / H-1**, not on the deadline day — the user needs a day to register and pay.

5. Put the **date inside the message body**, not only in the cron name: the job name is invisible when
   the message arrives. Include price + one-line "kenapa ini penting" so the reminder is self-contained.

## Pair the reminder with the answer, not instead of it

The reminders are a bonus after a complete, verified answer — the chat reply still carries the full list
with prices, dates and links (see `indonesia-course-cert-sources.md`), plus the markdown artifact under
`~/.hermes/data/` delivered with `MEDIA:`. Never let "I set a reminder" stand in for the actual list.
