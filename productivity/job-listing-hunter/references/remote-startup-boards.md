# Board remote/startup — mana yang tembus tanpa browser (diuji 7 Okt 2026)

Probe: `curl -sL -A "<browser UA>" -H "Accept: application/json, */*" <url>`.
Hasil nyata, bukan asumsi — beberapa board populer ternyata mati untuk scraping keyless.

## TEMBUS (pakai ini)

| Board | Endpoint | Catatan |
|---|---|---|
| **RemoteOK** | `https://remoteok.com/api` | JSON, ~100 job, elemen `[0]` = legal notice (lewati). Startup-heavy. Field `location` **tidak** = hak kerja → parse deskripsi. |
| **Remotive** | `https://remotive.com/api/remote-jobs?limit=50&search=<q>` | `candidate_required_location` **autoritatif**. `job-count` untuk jumlah. |
| **Himalayas** | `https://himalayas.app/jobs/api?limit=100` | `locationRestrictions` + `seniority` + `timezoneRestrictions` autoritatif. Ada cursor pagination. |
| **Jobicy** | `https://jobicy.com/api/v2/remote-jobs?count=50` | `jobGeo` / `jobLevel`; `jobGeo:"Anywhere"` = worldwide. |
| **Arbeitnow** | `https://www.arbeitnow.com/api/job-board-api` | ~325 job, mayoritas Jerman; flag `remote` boolean. |
| **Kalibrr** | `https://www.kalibrr.com/kjs/job_board/search?limit=30&offset=<n>&text=<q>` | JSON; flag **`is_work_from_home`** / `is_hybrid` + `google_location` asli + `is_open_to_fresh_grads` + `application_end_date`. Mayoritas PH (payroll lokal) tapi paling akurat untuk flag WFH. |
| **LinkedIn guest** | `…/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=<q>&location=<loc>&f_WT=2&start=<n>` | `f_WT=2` = remote-only. Kartu `<li>` berisi title/company/location/url/datetime — regex, bukan browser. `location=Indonesia` dan `location=Worldwide` dua-duanya berguna. |

## MATI (jangan buang waktu)

| Board | Hasil |
|---|---|
| WeWorkRemotely RSS | 0 byte |
| Glints | HTML, diblok/butuh JS |
| Dealls (`api.sejutacita.id`) | `{"status":"Not Found"}` |
| web3.career `/api/v1` | HTML landing |
| crypto.jobs / cryptojobslist | Cloudflare challenge ("Just a moment...") |
| Jobstreet | butuh browser/login |

Jalan lain kalau board mati: **Google News `site:x.com/<handle>`** untuk update perusahaan, atau
portal ATS langsung (Greenhouse/Workable/BambooHR — URL apply-nya fetchable biasa).

## Aturan label kelayakan (yang bikin report kepake)

```
🇮🇩 id      = Indonesia (Jakarta/Bekasi/Bali/… atau "Indonesia")        -> tier A
🌍 world   = worldwide | anywhere | global | fully remote (no geo)      -> tier A
🌏 asia    = India/PH/VN/Pakistan/SG/…                                  -> tier B (payroll lokal)
⚠️ locked  = US/EU/UK/CA/AU/JP/KR/DE/dll                                 -> tier C
❓ unknown = board global tanpa petunjuk geo -> "cek deskripsi"          -> tier B
```

Tier A = `geo ∈ (id, world)` **dan** judul masuk level (junior/entry/associate/staff/specialist/
executive/creator/coordinator/analyst/assistant) **dan** posting ≤60 hari.
Judul yang mengandung senior/lead/head/manager/architect → buang, kecuali ada kata intern.

## Filter tambahan yang dibakar ke script

- ROLE: sosmed/content/community/growth/marketing/ops/BD/customer success/VA/admin/data entry/
  bookkeep-account-finance-tax-payroll/research/AI-automation (bukan programmer).
- DROP: engineer/developer/designer/3d/kasir/driver/nurse/paralegal/account-executive/dll.
- LANG: buang yang minta Danish/German/Mandarin/Somali/Arabic/… (bahasa lain ≠ lane user).
- `remote: true` wajib (board global sudah remote, tapi Kalibrr/Arbeitnow punya flag → cek).

## Rate limit

`ThreadPoolExecutor(8)` untuk fetch (aman), **`ThreadPoolExecutor(3)` untuk verify** (LinkedIn
429 kalau lebih). Verifikasi hanya tier A, cap 47–60 URL; ~9 dari 34 terverifikasi sudah tutup —
jadi verifikasi itu wajib, bukan opsional.
