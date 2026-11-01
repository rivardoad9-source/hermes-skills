---
name: vercel-deploy-ops
description: Use when deploying or managing the user's Vercel.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vercel, deploy, nextjs, cli, oauth, device-flow]
    related_skills: [localhost-dashboard-serving, hermes-agent]
---

# Vercel deploy ops (akun user)

## When to Use
- User nanya "lu connect ke vercel gw ga sih", minta deploy/rollback/promote, atau
  minta lihat build log project Vercel-nya.
- Ada project yang harus naik ke produksi dan hostingnya Vercel.

## Aturan tetap
- **Akses CLI Vercel itu lebar**: satu login = bisa deploy, promote, dan ganti alias
  SEMUA project di akun itu. Sebutkan batas ini ke user sebelum dia approve, dan
  jangan deploy atau ubah apa pun tanpa dia minta.
- **Kredensial nggak pernah masuk chat.** Login lewat device flow; kalau kodenya
  expired, generate ulang, jangan minta token.
- Jangan bilang "udah konek" sebelum diverifikasi sendiri dari sisi server.

## Prosedur
1. **Cek dulu apa yang ada sebelum ngaku apa pun.** `which vercel`,
   `ls -d ~/.vercel ~/.config/vercel`, grep env VERCEL di `~/.hermes/.env` (cetak
   "[ADA]" saja, jangan nilainya), lalu cari link project:
   `find ~ -maxdepth 4 \( -name vercel.json -o -name .vercel \) -not -path "*/node_modules/*"`.
   Kalau kosong, jawabannya "belum konek" — bilang apa adanya.
2. **CLI nggak perlu install global**: `npx --yes vercel@latest --version` jalan tanpa
   sudo (butuh node 20+). Hindari `npm i -g` di server ini.
3. **Dapatkan kodenya lewat GitHub dulu**: `gh repo clone <owner>/<repo>`, dan
   `gh repo view <repo> --json homepageUrl,pushedAt` buat tau URL produksi plus
   seberapa hidup project-nya.
4. **Baca `.env.example` dan `package.json` sebelum janji bisa deploy.** App statis /
   localStorage (contoh: dompet-dashboard, PWA Next.js) nggak butuh satu pun
   kredensial dari user — sebutkan itu duluan, karena user takut ditanyain secret.
5. **Login device flow, background, stdout KE FILE:**
   ```
   terminal(background=true, command="cd ~/work/<repo> && npx --yes vercel@latest login > $HOME/.hermes/cache/scratch/vercel_login.txt 2>&1")
   ```
   Tunggu ~20 detik, baca filenya. URL `https://vercel.com/oauth/device?user_code=XXXX`
   cuma kelihatan di file — preview/poll proses motong kepala output, jadi yang
   kelihatan cuma spinner "Waiting for authentication...".
   Kirim URL itu ke user: suruh cek akun yang muncul, lokasi, dan waktu request
   sebelum approve. Jangan pakai wrapper `nohup`/`disown` — runtime nolak; pakai
   `background=true`.
6. **Jangan kill proses login** sebelum user approve; kodenya mati dan harus
   generate ulang. Kejadian nyata: proses login mati sendiri sebelum di-approve
   (log berhenti di "Waiting for authentication..."), jadi **cek `pgrep -af vercel`
   sebelum bilang kodenya hidup** — kalau mati, generate ulang, jangan suruh user
   ngejar link yang udah nggak nyambung ke proses apa pun.
7. **Verifikasi sendiri setelah approve**: `npx --yes vercel@latest whoami` lalu
   `npx --yes vercel@latest projects ls`. Lapor dari hasil itu, bukan dari asumsi.
   Akun user (per 13 Okt 2026): `rivardoad9-source`, tim `rivardoad9-sources-projects`,
   7 project: mango-cheese-pos, rebites_dashboard, rebites, rebites-sbgd,
   dompet-dashboard-app, dompet-dashboard, zemizdigital.
   Cek deploy terakhir: `npx --yes vercel@latest ls <project>` (kolom Age/Status/
   Environment/Duration).
8. **`vercel link --yes --project <nama>`** menyambungkan clone lokal ke project dan
   **bikin `.env.local` berisi `VERCEL_OIDC_TOKEN`**. Pastikan `.gitignore` menutup
   `.env.local` (`git check-ignore -v .env.local`) sebelum clone itu di-commit,
   kalau tidak ada token yang ikut ke-push.
8. **Deploy**: build lokal dulu kalau mau hemat build minutes dan lihat error lebih
   cepat (`npm ci && npm run build`), baru `npx --yes vercel@latest deploy` (preview)
   atau `... deploy --prod`.

## Jebakan
- Vercel MCP resmi (`https://mcp.vercel.com`, OAuth) **cuma nerima klien AI yang udah
  direview Vercel**, jadi jangan dijadikan jalur andalan. CLI device flow yang pasti
  jalan dan justru lebih lengkap buat deploy.
- `vercel login <email>` plus flag `--github/--gitlab/--oob` sudah deprecated; device
  flow adalah jalurnya.
- Output CLI Vercel penuh spinner ANSI: `tr -d '\r'` lalu buang karakter braille
  (⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏) sebelum grep atau print.
- Project user yang sudah dikenal: `dompet-dashboard` (clone `~/work/dompet-dashboard`,
  Next.js + Tailwind, PWA localStorage, produksi di dompet-dashboard.vercel.app) dan
  `zemizdigital.vercel.app`. Cek `gh repo list` kalau nemu nama baru.
