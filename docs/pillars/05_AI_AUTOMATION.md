# Pillar 5 — AI & Automation ("The lamp works by itself")
> **Role:** Control the lamp by asking Claude (MCP server) and run recitations on a schedule from the PC.
>
> **Depends on:** Pillar 2 (commands), Pillar 4 (Mawaqit)
> **Used by:** Pillar 7 (premium features)
> **Cross-pillar impacts:** the MCP server keeps its own copy of the command table — keep it equal to Pillar 2.
---
## 🎯 Trigger Keywords
- `"Pillar 5"`, `"MCP"`, `"Claude"`, `"schedule"`, `"Al-Kahf"`, `"Al-Mulk"`, `"adhkar"`, `"notification"`.
---
## 🔍 Scope
- **MCP server** (`mcp/`): Python + `mcp` SDK + `bleak`, runs on the PC near the lamp, stdio transport,
  registered in Claude Desktop and Claude Code. Tools: status, play/pause, next/prev, play surah+verse,
  reciter/translation/book lists and select, volume, light, sleep timer, prayer times, set/shift times, azan switches, sync mosque.
- **Schedules:** Windows tasks that call the same engine at set times.
---
## What is Built & Verified `[x]`
- [x] **Daily Mawaqit → lamp sync** (PC task, private tool `mawaqit_sync.py`).
- [x] **MCP server built** — `mcp/server.py` (13 tools) + `mcp/lamp.py`; registered in Claude Code (user scope), server starts ("Connected").
---
## What is Left to Do `[ ]`
- [ ] **Test every MCP tool on the lamp** (`mcp/selftest.py` first; first run failed because the lamp was busy/not visible).
- [ ] **Register in Claude Desktop** (add `mcpServers` entry via Settings → Developer → Edit config).
- [ ] **Friday Al-Kahf:** every Friday morning play Surah 18 (Al-Kahf) automatically.
- [ ] **Bedtime Al-Mulk:** at a set time play Surah 67 (Al-Mulk), then sleep timer switches off.
- [ ] **Morning and evening adhkar:** play Hisnul Muslim (book 4) after Fajr and after Asr.
- [ ] **Alert if a sync fails:** phone notification (e.g. Telegram or ntfy) when the daily Mawaqit copy or git sync fails.
- [ ] **Voice:** "Hey Claude, play Ya-Sin" via Claude mobile → remote MCP (needs a cloud bridge; later).
---
## ⚡ Next Immediate Action
Run `python mcp/selftest.py` with the lamp ON and no phone connected, then ask Claude "lamp status".
---
## 📹 Video references & Assets
- none yet
