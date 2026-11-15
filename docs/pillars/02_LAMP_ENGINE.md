# Pillar 2 — Lamp Control Engine ("Talking to the lamp")
> **Role:** The Bluetooth LE link and every command, reply and push the lamp understands.
>
> **Depends on:** Pillar 0
> **Used by:** Pillars 1, 5
> **Cross-pillar impacts:** any change here must be mirrored in `index.html` and `mcp/lamp.py`.
---
## 🎯 Trigger Keywords
- `"Pillar 2"`, `"Bluetooth"`, `"command"`, `"protocol"`, `"reply"`, `"new lamp model"`.
---
## 🔍 Scope
- **Link:** BLE service `0000ae00-…`, write `0000ae01-…` (without response), notify `0000ae02-…`. Lamp name `XDT_SQ122`, model reply "SQ953".
- **Frame:** `EA <cmd> <args…> 00 AE`; replies `EB <cmd> <data…> 00 AE`. One connection at a time.
- **Full spec (private, not in this repo):** `C:\Users\ouaja\quran-lamp-app\PROTOCOL.md` and `FEATURES.md`.
- **Key commands:** 02 play/pause · 03/04 prev/next surah · 05/06 prev/next verse · 15 S Vhi Vlo go to verse (0-based) ·
  37 reciter · 38 translation · 1B book · 42 volume 0–30 · 1D/1E/33 light · 31/3E sleep/off time ·
  90 clock · 91/93 times · 92 set 6 times · 94/95 azan master · 98/99 per prayer · 9E/9F azan sound · 96/97 method/Asr · A6/A7 summer · 53 place (TZ index: h≥0→h, h<0→24+h).
- **Lists:** 72/75/79 ids, ≤16 per packet, FF ends, byte 18 ≠ 0 = more; unknown names via 76/77/80 (UTF-8).
---
## What is Built & Verified `[x]`
- [x] **Read queries** on the real lamp (model, volume, times, switches, method, lists).
- [x] **Writes** verified: volume, 92 times, 94 master on, mask 3D.
- [x] **Power behaviour:** remote power-off = Bluetooth off; app cannot wake it (tested 2026-11-15).
---
## What is Left to Do `[ ]`
- [ ] **Verify on lamp from the web app:** lists, surah+verse, light, sleep timer, place (TZ index).
- [ ] **Confirm meaning of keys 05/06/07/09** (verse vs reciter; mode; word-by-word).
- [ ] **Python engine for the MCP server** (`mcp/lamp.py`), same command table — see Pillar 5.
- [ ] **Model registry:** table of known models (SQ-122/SQ953, SQ-112, SQ-600…) and which features each supports.
- [ ] **Reconnect + keep-alive** in the web app when the link drops.
---
## ⚡ Next Immediate Action
Test lists, surah+verse and light from the web app against the real lamp and mark them verified.
---
## 📹 Video references & Assets
- Maker app (not in repo): https://equantu.com/uploads/KoranPlayer.apk
