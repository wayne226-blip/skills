---
name: netlify-deploy
description: Use when deploying or updating a Netlify site, setting up a new pen name lead magnet, or verifying live changes on any of Wayne's Netlify sites.
---

# Netlify Deploy

## Overview

No CLI. Deploys via the Netlify REST API using the token at `~/.netlify/config.json`.
All known sites are mapped in `~/.netlify/sites.json`.

## Known Sites

| Name | URL | Deploy Folder |
|---|---|---|
| blake-hartley-books | blake-hartley-books.netlify.app | `authors/hockey-romance/marketing/newsletter/deploy/` |
| puzzlingpenny | puzzlingpenny.netlify.app | — |
| puzzling-penny-privacy | puzzling-penny-privacy.netlify.app | — |
| claude-onboarding | claude-onboarding.netlify.app | — |
| nano-banana-studio | nano-banana-studio.netlify.app | — |

Full site IDs in `~/.netlify/sites.json`.

## Deploying a Change

```bash
TOKEN=$(python3 -c "import json; print(json.load(open('/Users/wayne/.netlify/config.json'))['token'])")
SITE_ID="<id-from-sites.json>"
cd /path/to/deploy/folder
zip -r /tmp/netlify-deploy.zip . -x "*.DS_Store"
curl -s -X POST \
  "https://api.netlify.com/api/v1/sites/${SITE_ID}/deploys" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/zip" \
  --data-binary @/tmp/netlify-deploy.zip | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('state'), d.get('url',''))"
```

After deploy: load the live URL in `preview_eval` → `preview_screenshot` to confirm.

## New Pen Name Lead Magnet Setup

When building a lead magnet for a new pen name, do all of this:

### 1. Build the deploy folder
```
authors/[pen-name]/marketing/newsletter/deploy/
  index.html          ← signup page
  [bonus-title]/
    index.html        ← bonus content (epilogue, chapter, etc.)
  cover.png           ← cover image
```

### 2. Create the Netlify site (first time only)
Wayne does this manually:
- [app.netlify.com](https://app.netlify.com) → Add new site → Deploy manually → drag deploy folder
- Note the site name and URL

Then add to `~/.netlify/sites.json`:
```json
"[pen-name-slug]": {
  "site_id": "<from netlify dashboard>",
  "url": "https://[pen-name-slug].netlify.app",
  "deploy_folder": "authors/[pen-name]/marketing/newsletter/deploy",
  "launch_name": "[pen-name]-landing",
  "launch_port": <next available port>
}
```

### 3. Add preview server to `.claude/launch.json`
```json
{
  "name": "[pen-name]-landing",
  "runtimeExecutable": "python3",
  "runtimeArgs": ["-m", "http.server", "<port>", "-d", "/Users/wayne/calibre-hq/authors/[pen-name]/marketing"],
  "port": <port>
}
```

**Port allocation** (avoid conflicts):
- 8780 — hockey-landing (blake-hartley-books)
- 8781 — next pen name
- 8782 — next pen name
- (increment by 1 per pen name)

### 4. Future deploys
All automated — read site ID from `sites.json`, zip, POST. No manual steps.

## Deploy Folder Rule

If there's a `deploy/` folder that mirrors source files, **always update both**:
- Source: `marketing/newsletter/signup-page.html`
- Deploy copy: `marketing/newsletter/deploy/index.html`

The deploy copy is what Netlify serves. The source copy is for local editing reference.

## 18+ Warning Standard

All spicy pen name lead magnets must include this in `deploy/index.html`, below the card description:
```html
<p class="privacy-note" style="margin-bottom:1rem;color:#E8E8F0;">18+ only. The bonus epilogue contains explicit content.</p>
```

And on the bonus content page, in the header meta block:
```html
<p class="meta" style="margin-top:0.5rem;color:#9A9AA0;">18+ only &middot; Contains explicit content</p>
```
