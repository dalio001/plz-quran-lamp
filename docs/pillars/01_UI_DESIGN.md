# Pillar 1 — UI & Design ("What the user touches")
> **Role:** Screens, tabs, controls, theme and languages of the web app.
>
> **Depends on:** Pillar 0 (shell), Pillar 2 (commands), Pillar 4 (Mawaqit data)
> **Used by:** Pillar 7 (screenshots, store listing)
> **Cross-pillar impacts:** new controls need a documented command in Pillar 2.
---
## 🎯 Trigger Keywords
- `"Pillar 1"`, `"UI"`, `"screen"`, `"button"`, `"tab"`, `"design"`, `"Arabic"`, `"dark mode"`.
---
## 🔍 Scope
- **5 tabs:** Quran (player, surah+verse, keypad), Reciters (reciters, translations, books), Azan, Light, More.
- **Theme:** light/dark via CSS tokens, mobile-first (375 px), bottom navigation.
- **"How to start the lamp"** help box at the top.
---
## What is Built & Verified `[x]`
- [x] **Quran tab:** play/pause, verse/surah prev-next, volume 0–30, surah+verse picker (114 surahs), keypad buttons.
- [x] **Reciters tab:** lists loaded from the lamp, tap to select; translations; books (Bukhari, Muslim, Ruqyah, Hisnul Muslim, Qaida, Duaa, 40 Hadith).
- [x] **Azan tab:** 6 times with ±1/±5, per-prayer on/off, sound + preview, master switch, "Copy my mosque's times", method, Asr, summer time, place.
- [x] **Light tab:** 11 presets, colour picker, brightness.
- [x] **More tab:** sleep timer, switch-off time, clock sync, reload, factory reset.
- [x] **Power button removed** (it put the lamp in standby where only the IR remote wakes it).
---
## What is Left to Do `[ ]`
- [ ] **Arabic and French UI** (right-to-left for Arabic, Arabic surah names).
- [ ] **Now-playing detail:** show reciter + translation names on the Quran tab.
- [ ] **Connection helper:** clear message when the lamp is not found (is it on? Koran Player closed?).
- [ ] **Screenshots for every tab** after each UI change (before/after rule).
- [ ] **Accessibility pass:** large text option, button labels for screen readers.
---
## ⚡ Next Immediate Action
Add reciter/translation names to the Quran tab "now playing" card.
---
## 📹 Video references & Assets
- `C:\Users\ouaja\quran-lamp-app\app_screen.jpg` (v1), `app_screen_after.jpg` (PLZ v2 mobile).
