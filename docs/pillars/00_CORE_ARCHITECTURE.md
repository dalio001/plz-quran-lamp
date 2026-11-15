# Pillar 0 — Core Architecture & Hosting ("The Shell")
> **Role:** How the app is built, hosted, cached, synced and run on the PC.
>
> **Depends on:** nothing
> **Used by:** Pillars 1, 2, 5
> **Cross-pillar impacts:** hosting limits change what Pillars 4 and 7 can offer (no backend today).
---
## 🎯 Trigger Keywords
- `"Pillar 0"`, `"hosting"`, `"deploy"`, `"GitHub Pages"`, `"sync"`, `"PWA"`, `"offline"`.
---
## 🔍 Scope
- **Static app:** one `index.html` (HTML/CSS/vanilla JS), `manifest.json`, icons, `sw.js` (offline cache), `times.json`.
- **Hosting:** GitHub Pages from `main` → https://dalio001.github.io/plz-quran-lamp/ (HTTPS, required by Web Bluetooth).
- **Local copy:** `E:\My app\plz-quran-lamp`; PC launcher `C:\Users\ouaja\quran-lamp-app\PLZ Quran Lamp.bat` + desktop icon.
- **PC tasks:** "PLZ Quran Lamp GitHub Sync" (git_sync.ps1, 20:50 + logon), "Quran Lamp Mawaqit Sync" (mawaqit_sync.py, 21:00/23:30/logon).
---
## What is Built & Verified `[x]`
- [x] **Static PWA:** installable on Android ("Add to home screen"), service worker cache `plz-quran-lamp-v1`.
- [x] **GitHub Pages deploy:** public repo, Pages built from `main`.
- [x] **Two-way sync:** git_sync.ps1 commits local changes, pulls, pushes daily; tested OK.
- [x] **Local launcher:** desktop icon serves the local copy on 127.0.0.1:8765 in Chrome.
---
## What is Left to Do `[ ]`
- [ ] **Shared engine module:** move the command table + frame/parse code from `index.html` into `engine.js` (and keep `mcp/` in step).
- [ ] **Versioning:** show app version in the More tab; bump `sw.js` CACHE automatically on change.
- [ ] **Basic tests:** small JS unit tests for frame building and list parsing (no lamp needed).
- [ ] **Hosting for selling:** decide later between GitHub Pages (free, public repo) and Cloudflare Pages / Vercel (private repo, custom domain, backend functions) — see Pillar 7.
- [ ] **Custom domain** (e.g. plz-lamp.app) when the brand is ready.
---
## ⚡ Next Immediate Action
Extract `engine.js` from `index.html` so the web app and future tools share one command table.
---
## 📹 Video references & Assets
- none yet
