# AI Agent Workflow Guide
Every AI agent reads `AGENTS.md` at startup. Add new rules there once; all agents inherit them across every tool and IDE.
---
## 🚀 How It Works
1. **Single Source of Truth (`AGENTS.md`):** Universal project invariants, quality gates, and documentation protocols live exclusively in `AGENTS.md`. Pointer files (`CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.windsurfrules`) prevent rule drift across different AI tools.
2. **Modular Domain Pillars (`docs/pillars/`):** The roadmap is partitioned into focused pillar files.
3. **How to Instruct Agents:**
   - Instead of feeding massive context, tell the agent: **"Let's work on [Pillar Name]"** (e.g., *"Let's work on Pillar 5"* or *"Let's work on Pillar 2"*).
   - The agent reads only that pillar's focused file (~3 KB), keeping its full reasoning power on your feature while saving thousands of tokens.
4. **Updating Rules:** Add any durable engineering rules or conventions directly to `AGENTS.md`.
5. **Where things live:**
   - App (public, live on GitHub Pages): `E:\My app\plz-quran-lamp` = github.com/dalio001/plz-quran-lamp → https://dalio001.github.io/plz-quran-lamp/
   - Private research and PC tools (never public): `C:\Users\ouaja\quran-lamp-app\` (PROTOCOL.md, FEATURES.md, mawaqit_sync.py, git_sync.ps1, CHECKPOINT.md).
