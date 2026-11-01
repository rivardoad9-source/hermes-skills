# Creating events from chat mentions — dedupe first (worked transcript, Oct–Nov 2026)

Two asks arrived back to back:

1. A photo of the UTS (mid-term) schedule — "sesuaiin google calender" → create the exams.
2. In passing: *"tgl 11 november gw ada presentasi tugas kampus, terus nnti tgl 12 ada web 3 asia"*.

The second one is the trap. The user **had already put both in his own calendar** under short names:

| date | his own entry | what the chat message implied |
|---|---|---|
| 11 Nov | `Presentasi SEM` | "presentasi tugas kampus" |
| 12 Nov | `Event Web3 week asia` | "web 3 asia" |

Creating straight from the message produced two duplicates (`Presentasi tugas kampus`,
`Web3 Week Asia 2026 (W3W)`) that he would have seen twice on his phone. The save was that the insert
returned ids, so the undo was exact.

## Rule 1 — scan the window BEFORE the insert

Enumerate the target range first and fuzzy-match 2–3 key tokens per mention (course code, event-name
stem, `presentasi`, `web3`). Classify `already present` / `missing`, then insert only the missing rows.
An after-the-fact verification that *finds* duplicates is too late — the user has already seen them.

Read back the whole window, not just the new rows; that listing is also what surfaces the near-miss
names (`Presentasi SEM` vs `Presentasi tugas kampus` never match on exact string — match on stems).

## Rule 2 — keep the returned ids; that map is the undo

```python
mine = {}                                     # id -> label, for safe rollback
for body in ev:
    r = svc.events().insert(calendarId=CAL, body=body).execute()
    mine[r["id"]] = body["summary"]
```

Rollback deletes **only those ids** — never by summary (a summary match on `Presentasi` eats the user's
own event too):

```python
for e in [x for x in listing if x["id"] in mine]:
    svc.events().delete(calendarId=CAL, eventId=e["id"], sendUpdates="none").execute()
# then re-list and assert 0 remain, printing the surviving rows
```

Post-clean state verified: `sisa duplikat: 0`, his `Presentasi SEM` + `Event Web3 week asia` untouched.

## Rule 3 — all-day, `end` is EXCLUSIVE

His convention for date-only items is an all-day event (`date`, no `dateTime`):

```python
{"summary": "…", "start": {"date": "2026-11-11"}, "end": {"date": "2026-11-12"}}
```

11–12 Nov → `start 2026-11-11`, `end 2026-11-13`. Off-by-one here silently makes the event one day short.

## Rule 4 — enrich the vague mention, then flag the mismatch (do not trust the date silently)

`web3 asia tgl 12` → real event is **Web3 Week Asia 2026 (W3W)**: **11–12 Nov 2026**, Grand Ballroom,
Kuningan City, Jakarta — `w3w.asia`, `@W3WOfficial` (confirmed across the event site, X, IG).
So it is a **two-day** event, day 1 is the same day as his campus presentation, and his own entry covered
day 2 only. Correct move: state the real span, name the day-1 clash, and **offer to extend his entry** —
never create a competing event to hold the extra day. Editing/deleting *his* event needs an explicit OK
(the standing rule is "konfirmasi dulu sebelum send/delete/share").

## Rule 5 — what "done" sounds like

Created list · skipped list **with the reason** (date already today/past; already exists in his calendar) ·
what still lacks detail (no jam, which MK) · the one real discovery (2-day span + clash). One line each.
Do not close with "mau gw buatkan?".

## Rule 6 — agent reminders must not land inside a commitment

The one-shot Dawn reminder was scheduled 12 Oct 09:00. Reading the calendar first showed
`UTS BDC08 - Analisis Data 08:00–09:40 R702` — the reminder would have fired mid-exam and been useless.
Moved the cron to `2026-10-12T19:00:00` (still the same "Dawn Trade Trial" day he'd blocked all-day) and
told him why it moved. Always read the target day before choosing a fire time for any user-facing cron.

## Also worth knowing (same session)

- UTS events created as timed events with the `R#### (Lt. 7 - Kampus Ancol)` location format and
  description carrying KMK / No Kursi / Jam WIB / Sumber; verified 5/5 by re-reading 7–17 Oct.
- Skipped two rows on purpose: the 06 Oct exam (already today) and the online 24–25 Sep simulations (past).
