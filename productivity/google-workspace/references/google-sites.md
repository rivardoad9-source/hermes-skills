# Google Sites: what an agent can and cannot do

Check this before answering "can you connect to Google Sites?" or agreeing to build/update a Site.

## Read is possible through Drive

A Site is a Drive file with `mimeType = application/vnd.google-apps.site`. With the Drive scope
already on the token you can:

```python
dv.files().list(q="mimeType='application/vnd.google-apps.site'").execute()
```

Useful fields: `owners`, `lastModifyingUser`, `createdTime`, `modifiedTime`, `parents`,
`webViewLink`. `lastModifyingUser` is how you tell which account actually built a shared site.

Reading the page text is also possible without any Sites API — export it:

```python
dv.files().export(fileId=SITE_ID, mimeType="text/plain").execute()
```

A site that has never been filled exports as the default template only (site name, "Halaman Muka",
"Judul halaman Anda" / "Your page title"). That is a fast, reliable way to prove a site is still
empty — far cheaper than asking the user to screenshot the editor.

## Write is not available

There is no public REST API to create pages, add text or images, or publish. Google retired the
Sites API in 2017; `https://sites.googleapis.com/v1/sites` answers 404. Do not plan an automation
around the Sites editor, and do not promise it after "checking again" later.

## What to offer instead

1. **Static HTML deployed elsewhere** — Vercel, GitHub Pages, Netlify. These have real APIs, so the
   page can be built, deployed and updated end to end without the user touching an editor.
2. **Content authored by the agent, pasted by the user** — deliver the final copy and the section
   order, plus a screenshot of the reference design, so filling the Sites editor is mechanical.

State the limitation in one sentence and move to option 1; do not stall on the limitation.
