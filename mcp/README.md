# PLZ Quran Lamp — MCP server

Lets Claude (Claude Code, Claude Desktop) control the lamp through this PC's Bluetooth.
The PC must be near the lamp, the lamp must be ON, and no phone may be connected to it.

## Install
```
python -m pip install -r requirements.txt
claude mcp add --scope user plz-quran-lamp -e LAMP_ADDRESS=02:D6:F2:0D:08:59 -- python "E:\My app\plz-quran-lamp\mcp\server.py"
```
Claude Desktop: Settings → Developer → Edit config, add under `"mcpServers"`:
```json
"plz-quran-lamp": { "command": "python", "args": ["E:\\My app\\plz-quran-lamp\\mcp\\server.py"] }
```

## Tools
`lamp_status`, `play_pause`, `skip`, `play_surah`, `list_items`, `choose`, `set_volume`, `light`, `sleep_timer`,
`prayer_times`, `set_prayer_time`, `sync_mosque_times`, `azan_switch`.

Ask e.g. "play Surah Al-Kahf with Sudais", "volume 12", "move Isha 5 minutes later", "copy my mosque's times".

Env: `LAMP_ADDRESS` (optional), `MAWAQIT_MOSQUE` (default `al-taqua-moschee-essen`).
Self-test against a real lamp: `python selftest.py`.
