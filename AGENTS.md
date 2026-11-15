# AGENTS.md — Universal AI Agent Contract & Project Rules
> **Single Source of Truth for all AI Agents (Claude, Cursor, Windsurf, Gemini, Codex, Antigravity).**
> Add new rules here once; all agents inherit them across all IDEs and tools.
> For workflow explanations, see docs/WORKFLOW.md.

**Project:** PLZ Quran Lamp — a Web Bluetooth app (Chrome on Android/PC) that fully controls Equantu SQ-122 Quran
speaker lamps: Quran playback, reciters, translations, books, light, timers, azan times synced from a Mawaqit mosque.
Goal: grow it step by step into a sellable product (more lamp models, MCP/AI control, scheduled recitations).

---
## 🏛️ Pillar Documentation Update Protocol
Every AI agent working on this codebase MUST follow this protocol without exception:
1. **Mandatory Pillar Sync:** Every completed task, bug fix, or feature MUST update its corresponding Pillar file in `docs/pillars/`.
2. **Pillar Identification:** Match tasks to the active project pillars:
   - **Pillar 0 — Core Architecture & Hosting** (`docs/pillars/00_CORE_ARCHITECTURE.md`): app shell, PWA/service worker, GitHub Pages, local copy + sync, PC scheduled tasks.
   - **Pillar 1 — UI & Design** (`docs/pillars/01_UI_DESIGN.md`): screens, tabs, layout, theming, languages, accessibility.
   - **Pillar 2 — Lamp Control Engine** (`docs/pillars/02_LAMP_ENGINE.md`): Bluetooth link, command frames, replies/pushes, lists, models.
   - **Pillar 4 — Integrations & Platform Limits** (`docs/pillars/04_INTEGRATIONS.md`): Mawaqit times, Web Bluetooth limits, IR power-on, browsers.
   - **Pillar 5 — AI & Automation** (`docs/pillars/05_AI_AUTOMATION.md`): MCP server for Claude, scheduled recitations, notifications.
   - **Pillar 7 — Product & Distribution** (`docs/pillars/07_PRODUCT_DISTRIBUTION.md`): branding, landing page, selling, legal, support.
3. **Mark Completed Items:** Change `[ ]` to `[x]` for items completed in the current session.
4. **Log New Tasks:** Add new tasks and feature requests under `[ ]` with a clear, concise description.
5. **Video & Asset References:** If a video file path, link, or asset was provided, append it to the task and the "Video references" section of that pillar file.
6. **Next Immediate Action:** Always update the "⚡ Next Immediate Action" line at the bottom of that pillar file so the next agent knows exactly where to pick up.
7. **Strict Pillar Isolation:** Do NOT edit other pillar files unless the current task explicitly alters their cross-pillar dependencies or shared UI components.
8. **Progress Log Record:** Update `docs/PROGRESS_LOG.md` with a one-line summary and today's date (`YYYY-MM-DD`).

---
## ⚙️ Universal Engineering Rules
- **Branch Hygiene:** All development work is on branch `main` (GitHub Pages serves `main` directly, so every push is live).
  For risky changes, work on a feature branch and merge when tested.
- **Quality Gates:** Every session modifying code must pass:
  - Lint: `python -m py_compile make_times.py make_icons.py` (no JS linter yet; see Pillar 0)
  - Test: serve locally with `python -m http.server 8765 --bind 127.0.0.1`, open `http://127.0.0.1:8765/` in Chrome,
    no errors in the console; for lamp features, test against a real lamp (Connect, run the changed control).
  - Build: none (static site). Bump `CACHE` in `sw.js` when `index.html` changes so phones pick up the new version.
- **Public repo:** This repository is PUBLIC. NEVER commit the maker's APK, decompiled code, `src/` folders, secrets, or
  personal data. Protocol research lives outside the repo in `C:\Users\ouaja\quran-lamp-app\` (PROTOCOL.md, FEATURES.md).
- **Auto-sync:** A Windows task runs `C:\Users\ouaja\quran-lamp-app\git_sync.ps1` daily (20:50 + logon): it refreshes
  `times.json`, commits everything in this folder and pushes. Do not leave half-finished work here at those times.
- **Lamp safety:** Read-only queries first; only send write commands whose meaning is documented in Pillar 2.
  One Bluetooth connection at a time (phone app, web app and PC scripts must not overlap).
- **Database Migrations:** No database. If one is added, schema changes must include a migration.
- **Git Commit Messages:** Conventional commit format (`feat: ...`, `fix: ...`, `refactor: ...`, `chore: ...`, `docs: ...`).
