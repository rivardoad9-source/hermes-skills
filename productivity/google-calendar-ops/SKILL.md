---
name: google-calendar-ops
description: "Use when auditing or bulk-editing Google Calendar events."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [google, calendar, schedule, recurring, delete, cleanup, googleapi]
    related_skills: [google-workspace, hermes-cron-automation, cron-output-style]
---

# Google Calendar ops — audit, bulk-edit, delete recurring schedules

## When to use

Any request that touches the user's calendar, not just "create an event":

- "hapusin jadwal upload konten di google calendar gw" / "bersihin kalender" / "hapus jadwal X"
- "event apa aja minggu depan?", "bentrok ga sama kuliah?", "kenapa ada 3 jadwal sama?"
- Before scheduling anything on the user's behalf — read the calendar first so agent-created reminders
  don't collide with their real commitments (classes, hackathons, family events).

The bundled `google-workspace` skill covers auth + the basic `calendar list/create/delete` wrapper.
**Load that first for auth**; this skill carries the recurring-series and bulk-delete workflow it lacks.

## Setup / auth (one check)

```bash
GSETUP="python ~/.hermes/skills/productivity/google-workspace/scripts/setup.py"
$GSETUP --check          # must print AUTHENTICATED (token auto-refreshes)
```

- Token: `~/.hermes/google_token.json`. Never print it, never copy it into notes/repos.
- Primary calendar id **is the email**: `you@example.com` (the user's). Also present: a shared
  `family…@group.calendar.google.com`, plus read-only Indonesian holiday feeds.
- The user is **WIB (UTC+7)** — every timeMin/timeMax and event timestamp needs `+07:00`.

## The recurring-series model — this is where deletes go wrong

| Call | Returns |
|---|---|
| `events().list(singleEvents=False)` | **masters**; a recurring master carries `recurrence: ['RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR']` |
| `events().list(singleEvents=True)` | **instances**; their id is `<masterId>_<YYYYMMDDThhmmssZ>` |

- Deleting an **instance id** removes one occurrence — the series keeps producing more.
- Deleting the **master id** removes the whole series (past + future) in a single call. Use this; never
  loop-delete hundreds of instances.
- **Future-only** = truncate: patch the master's RRULE with `;UNTIL=YYYYMMDDT235959Z`. Past stays, nothing
  new appears.
- An RRULE with **no UNTIL repeats forever** — say that out loud in the confirmation, because it changes
  what "delete" means (one tap now vs an infinite schedule).
- **Two series can share one summary.** The user had "Upload Konten" weekly `TU,FR` *and* weekly
  `MO,WE,FR`, all 19:00–19:30 → ~3 uploads/week. Group by **master id**, never by summary string, before
  counting or deleting anything.

## Workflow

1. **Enumerate** over a wide window (today − 4 months → today + 15 months), both masters and instances,
   grouped by summary. Table: what / series / RRULE / time / created / how many still upcoming.
2. **Confirm scope ONCE** — one `clarify` with choices, not a chain of questions:
   `delete whole series (past+future)` / `future-only (truncate)` / `cancel`.
   Calendar deletion is destructive and the user's standing rule is "konfirmasi dulu sebelum
   send/delete/share". One crisp question is respect; five is friction.
3. **Delete by exact id** with `sendUpdates="none"` (`svc.events().delete(calendarId=CAL, eventId=master)`).
   Delete only the confirmed set — never "while I'm in there" cleanup.
4. **Verify by reading the calendar back**: assert 0 remaining for that summary *and* print the other
   event titles/summaries so the user can see nothing else was touched.
5. **Check nothing recreates it**: `grep -rl "<event summary>" ~/.hermes/scripts ~/.hermes/cron` — if a
   cron/script creates those events, deleting them is temporary.
6. **Report proof, not adjectives**: series ids + RRULE deleted, before/after counts, and the next-10-day
   listing showing the freed slots. Say plainly that classes/other events are intact.

## Pitfalls

- **The `google_api.py` wrapper's `calendar list` can under-report** (it returned 25 items for a window
  that actually held 400+ instances) — counting from it silently hides the real scale. Enumerate with
  `googleapiclient` directly, paging on `nextPageToken`, before you promise anything.
- Timezone-less timestamps, or a naive listing window, make events look missing. Always pass offsets.
- **All-day / multi-day events** (a hackathon spanning 1 Sep – 8 Oct) fill a next-N-days listing and can
  make it look like classes vanished. Judge by counts grouped by summary over a wide window, not by one
  narrow window's rows.
- Don't trust a bare `{status:"deleted"}` response as proof — re-scan.
- If the user wants a schedule rebuilt on a different cadence later, that's `calendar create` + a
  recurrence rule; keep the RRULE in one place so a later edit is a single patch.

## References

- `references/bulk-schedule-cleanup.md` — worked transcript: 2 recurring "Upload Konten" series, real
  ids/RRULEs, the scope-confirmation turn, deletion calls, and the verification output.
