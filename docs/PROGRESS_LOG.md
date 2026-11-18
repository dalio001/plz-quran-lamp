# Progress Log
Session history recorded newest first. Carries the reasoning behind decisions and timestamps of completed milestones.
- Roadmap: `docs/MASTER_PLAN.md`
- Governance: `AGENTS.md`
---
## 2026-11-18 — "Lamp off" button moved to the Quran tab Buttons (removed from More).

## 2026-11-16 — Lamp stays awake on the charger (verified overnight, azan on time); tip added to app.

## 2026-11-15 — MCP server for Claude (Pillar 5)
Added `mcp/` (Python, mcp + bleak, 13 tools) and registered it in Claude Code. Not yet tested on the lamp.

## 2026-11-15 — Initialized Modular Pillar Architecture & Agent Governance
Analyzed codebase, established tailored domain pillars in `docs/pillars/` (0, 1, 2, 4, 5, 7), created universal `AGENTS.md` contract, and wired multi-agent IDE pointer files.

## 2026-11-15 — First release of PLZ Quran Lamp
Decoded the lamp's Bluetooth protocol from the maker's Android app (research kept private), built the full web app
(Quran, reciters, translations, books, keypad, light, timers, azan + Mawaqit copy), published on GitHub Pages,
added PC tasks: daily Mawaqit → lamp sync and daily git sync. Azan switched on (5 prayers). Lamp must stay ON:
when switched off with the remote its Bluetooth is off and only the infrared remote can wake it.
