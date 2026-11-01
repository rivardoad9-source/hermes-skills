# Worked transcript — deleting the "Upload Konten" schedule (Oct 2026)

Ask: **"tolong hapusin jadwal uploud konten di google calender gw"** — one line, no ids, no scope.
Everything below is what made it a clean, verifiable delete instead of a guess.

## 0. What made the naive answer wrong

The wrapper lists only what fits: `google_api.py calendar list --start … --end …` returned **25 events**
for a 13-month window. The calendar actually held **400+ instances**. Had I reported "6 events, delete
them?" from that list I would have deleted only July's occurrences and left an infinite recurrence running.

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
svc = build("calendar", "v3", credentials=Credentials.from_authorized_user_file("$HOME/.hermes/google_token.json"))
CAL = "you@example.com"          # primary id == the email
# page on nextPageToken — never trust a single capped response
```

## 1. Enumerate masters, group by id (not by summary)

```python
masters = svc.events().list(calendarId=CAL, timeMin="2026-06-01T00:00:00+07:00",
                            timeMax="2027-12-31T23:59:59+07:00", singleEvents=False,
                            maxResults=250).execute()["items"]
up = [e for e in masters if (e.get("summary") or "").strip().lower() == "upload konten"]
```

Result — **two masters, same summary**:

| id | start | recurrence | created |
|---|---|---|---|
| `sa1u921d6obccerig66mugd6jc` | 2026-08-04T19:00+07:00 | `RRULE:FREQ=WEEKLY;BYDAY=TU,FR` | 2026-08-01 |
| `fqpt3jpns7tb7imce00jtokues` | 2026-07-20T19:00+07:00 | `RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR` | 2026-07-18 |

Instances looked like `fqpt3jpns7tb7imce00jtokues_20260720T120000Z` (19:00 WIB = 12:00Z) — same prefix,
date suffix. Two of the weekly series landing on Friday is why some days showed **two** "Upload Konten"
blocks (10-09, 10-16, 10-23, 10-30). Neither RRULE had `UNTIL`/`COUNT` → both recurred forever, so
"delete" had to mean *delete the series*, and the confirmation said so.

## 2. One confirmation with scope choices

Reported: "bukan satu seri, tapi 2 seri berulang @19:00 WIB, keduanya berulang tanpa batas — Seri A Sel+Jum,
Seri B Sen+Rab+Jum, ~424 instance belum lewat." Then a single `clarify`:

- Hapus 2 seri sekalian (semua hilang: lampau + ke depan)
- Hapus yang ke depan aja (riwayat lampau tetap ada)   ← would be an RRULE `UNTIL` truncation
- Jangan hapus, batal

Answer: **delete both series**. (Offering "future-only" as a real, implementable option is what makes the
question honest rather than performative.)

## 3. Delete by master id

```python
for mid in ["sa1u921d6obccerig66mugd6jc", "fqpt3jpns7tb7imce00jtokues"]:
    ev = svc.events().get(calendarId=CAL, eventId=mid).execute()   # print summary+rrule for the log
    svc.events().delete(calendarId=CAL, eventId=mid, sendUpdates="none").execute()
```

Two API calls, not 400. (`sendUpdates="none"` → no cancellation mail to attendees.)

## 4. Verify by reading back (the part that makes it a claim, not a hope)

Re-scanned the same wide window both ways and printed the surviving titles:

```
sisa master 'Upload Konten': 0
sisa instance 'Upload Konten': 0
event lain tetap ada (52 judul): BDC08 - Analisis Data | BDD05 - Digital Business Valuation |
  BDE04 - Manajemen Proyek Digital | BDE06 - Big Data & Business Intelligence | BDF06 - Search Engine
  Marketing | BDC08 … (+ tasks, "Date", "Seminar Hacktiv8", "Gladi Bersih Meet and Greet KMB", …)
```

And a per-window count to prove the freed slots:

```
=== 5 Okt - 5 Nov: 17 event
  3x BDC08 | 2x BDD05 | 3x BDE04 | 2x BDE06 | 3x BDF06 | 3x MND22 | 1x Indonesia Web3 Hackathon
sisa yg judulnya 'Upload Konten': 0
```

Then: `grep -rl "Upload Konten" ~/.hermes/scripts ~/.hermes/cron` → **no matches**, i.e. no cron or script
of ours recreates the schedule, so it stays gone. (If a script had matched, that grep is the finding the
user actually needs.)

## 5. Reporting shape the user accepted

Series + RRULE deleted (so they know what "all" meant) · verified 0 remain · other events intact by count
and by name · "no automation will recreate it" · offer to rebuild on a different cadence. No screenshot
needed; the numbers are the proof.

## Trap to remember

A next-10-days listing showed only the multi-day hackathon and no classes, which momentarily looked like
the delete had nuked more than intended. It hadn't — the semester simply had no classes in that window
(they resume 20 Oct). **Cound by summary over a wide window**; a narrow window's rows are not evidence.
