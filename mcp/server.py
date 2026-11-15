"""PLZ Quran Lamp MCP server: lets Claude control the SQ-122 Quran lamp over this PC's Bluetooth.

Run: python server.py   (stdio transport; registered in Claude Desktop / Claude Code, see mcp/README.md)
"""
import os

from mcp.server.fastmcp import FastMCP

import lamp as L

ADDRESS = os.environ.get("LAMP_ADDRESS")  # optional, e.g. 02:D6:F2:0D:08:59
MOSQUE = os.environ.get("MAWAQIT_MOSQUE", "al-taqua-moschee-essen")

mcp = FastMCP("plz-quran-lamp", instructions=(
    "Controls a Bluetooth Quran speaker lamp (Equantu SQ-122). The lamp must be switched ON with its remote and not "
    "connected to a phone. Prayer order is Fajr, Sunrise, Dhuhr, Asr, Maghrib, Isha. The owner prays with the "
    "Mawaqit times of his mosque; prefer sync_mosque_times over manual changes."))


def lamp():
    return L.Lamp(ADDRESS)


def surah_label(s, v):
    return f"Surah {s + 1} {L.SURAHS[s]}, verse {v + 1} of {L.VERSES[s]}"


@mcp.tool()
async def lamp_status() -> dict:
    """Read what the lamp is doing: play state, volume, current reciter/translation/book, azan on/off, prayer times."""
    async with lamp() as l:
        model = await l.ask(0x00)
        vol = await l.ask(0x41)
        state = await l.ask(0x60)
        reader, trans, book = await l.ask(0x16), await l.ask(0x17), await l.ask(0x40)
        master = await l.ask(0x95)
        mask = await l.ask(0x99)
        _fmt, now, _calc = await l.times()
    play = {0: "off/standby", 2: "paused", 3: "playing"}.get(state[2] if state else -1, "unknown")
    m = mask[2] if mask else 0
    return {
        "model": model[2:10].decode(errors="replace").strip() if model else None,
        "play_state": play,
        "volume": vol[2] if vol else None,
        "reciter": L.READERS.get(reader[2], f"#{reader[2]}") if reader else None,
        "translation": L.TRANS.get(trans[2], f"#{trans[2]}") if trans else None,
        "book": L.BOOKS.get(book[2], f"#{book[2]}") if book else None,
        "azan_on": bool(master and master[2]),
        "prayer_times": dict(zip(L.PRAYERS, now)),
        "azan_per_prayer": {p: bool(m & (1 << i)) for i, p in enumerate(L.PRAYERS)},
    }


@mcp.tool()
async def play_pause() -> str:
    """Toggle play / pause of the Quran recitation."""
    async with lamp() as l:
        r = await l.ask(0x02)
    return {1: "playing", 3: "playing", 0: "paused", 2: "paused"}.get(r[2] if r else -1, "sent (no answer)")


@mcp.tool()
async def skip(direction: str, unit: str = "verse") -> str:
    """Go to the next or previous verse or surah. direction: 'next' | 'previous'; unit: 'verse' | 'surah'."""
    cmd = {("next", "verse"): 0x06, ("previous", "verse"): 0x05,
           ("next", "surah"): 0x04, ("previous", "surah"): 0x03}[(direction.lower(), unit.lower())]
    async with lamp() as l:
        r = await l.ask(cmd)
    if r and len(r) >= 6 and cmd in (0x03, 0x04):
        return "Now " + surah_label(r[2], (r[3] << 8) | r[4])
    return f"{direction} {unit} sent"


@mcp.tool()
async def play_surah(surah: str, verse: int = 1) -> str:
    """Play a surah from a verse. surah: number 1-114 or name, e.g. '18', 'Al-Kahf', 'Ya-Sin', 'Mulk'."""
    s = L.find_surah(surah) - 1
    v = min(max(1, verse), L.VERSES[s]) - 1
    async with lamp() as l:
        r = await l.ask(0x15, [s, v >> 8, v & 0xFF])
    if r and r[2] == 0:
        return "Playing " + surah_label(s, v)
    return "Lamp refused: it may be in standby or not in MP3 (card) mode." if r else "No answer from the lamp."


@mcp.tool()
async def list_items(kind: str) -> list:
    """List what is on the lamp's card. kind: 'reciters' | 'translations' | 'books' (Hadith, Ruqyah, Duaa...)."""
    async with lamp() as l:
        return await l.named_list(kind.lower())


@mcp.tool()
async def choose(kind: str, name: str) -> str:
    """Select a reciter, a translation language, or play a book. kind: 'reciter' | 'translation' | 'book'.
    name: part of the name (e.g. 'Sudais', 'French', 'Bukhari') or the id number."""
    kind = kind.lower().rstrip("s")
    list_kind, cmd = {"reciter": ("reciters", 0x37), "translation": ("translations", 0x38), "book": ("books", 0x1B)}[kind]
    async with lamp() as l:
        items = await l.named_list(list_kind)
        n = L.norm(name)
        hit = next((i for i in items if str(i["id"]) == name.strip() or n in L.norm(i["name"])), None)
        if not hit:
            return f"Not found. Available: {', '.join(i['name'] for i in items)}"
        await l.send(cmd, [hit["id"]])
    return f"{kind.capitalize()} set to {hit['name']}"


@mcp.tool()
async def set_volume(level: int) -> str:
    """Set the volume, 0 (silent) to 30 (max)."""
    level = min(max(0, level), 30)
    async with lamp() as l:
        ok = await l.ok(0x42, [level])
    return f"Volume {level}" if ok else "Lamp refused the volume"


@mcp.tool()
async def light(color: str = "", brightness: int = -1, toggle: bool = False) -> str:
    """Control the lamp light. color: preset name (warm white, cool white, red, green, blue, yellow, purple,
    light blue, dark yellow, orange, colour cycle) or hex like '#ff8800'. brightness 0-100. toggle=True switches it on/off."""
    async with lamp() as l:
        if toggle:
            await l.send(0x1F)
        b = brightness if 0 <= brightness <= 100 else 80
        if color.startswith("#") and len(color) == 7:
            await l.send(0x33, [b, int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)])
        elif color:
            mode = L.LIGHTS.get(color.lower())
            if not mode:
                return f"Unknown colour. Use one of: {', '.join(L.LIGHTS)}"
            await l.send(0x1D, [b, mode])
        elif brightness >= 0:
            await l.send(0x1E, [b])
    return "Light updated"


@mcp.tool()
async def sleep_timer(minutes: int) -> str:
    """Switch the lamp off after this many minutes (1-1440)."""
    minutes = min(max(1, minutes), 1440)
    async with lamp() as l:
        ok = await l.ok(0x31, [minutes >> 8, minutes & 0xFF])
    return f"Lamp switches off in {minutes} min" if ok else "Lamp refused the timer"


@mcp.tool()
async def prayer_times() -> dict:
    """Prayer times stored in the lamp now, and the lamp's own calculated times."""
    async with lamp() as l:
        _fmt, now, calc = await l.times()
    return {"used_by_lamp": dict(zip(L.PRAYERS, now)), "lamp_calculation": dict(zip(L.PRAYERS, calc))}


@mcp.tool()
async def set_prayer_time(prayer: str, time: str = "", shift_minutes: int = 0) -> dict:
    """Change one prayer time: give time 'HH:MM', or shift_minutes (e.g. 5 or -3). Max 2 h from the lamp's own time."""
    idx = next(i for i, p in enumerate(L.PRAYERS) if p.lower() == prayer.lower())
    async with lamp() as l:
        _fmt, now, _calc = await l.times()
        if time:
            now[idx] = time
        else:
            m = (int(now[idx][:2]) * 60 + int(now[idx][3:5]) + shift_minutes) % 1440
            now[idx] = f"{m // 60:02}:{m % 60:02}"
        result = await l.set_times(now)
    return dict(zip(L.PRAYERS, result))


@mcp.tool()
async def sync_mosque_times(mosque_slug: str = "") -> dict:
    """Copy today's (after Isha: tomorrow's) times of a Mawaqit mosque into the lamp and set its clock.
    mosque_slug: the part after mawaqit.net/en/ (default: the owner's mosque)."""
    name, day, times = L.mawaqit_times(mosque_slug or MOSQUE)
    async with lamp() as l:
        await l.sync_clock()
        result = await l.set_times(times)
    return {"mosque": name, "date": str(day), "lamp_now_has": dict(zip(L.PRAYERS, result))}


@mcp.tool()
async def azan_switch(on: bool, prayer: str = "all") -> dict:
    """Turn the azan on or off: prayer='all' for the master switch, or one prayer name (Fajr, Dhuhr, Asr, Maghrib, Isha)."""
    async with lamp() as l:
        if prayer.lower() == "all":
            ok = await l.ok(0x94, [1 if on else 0])
        else:
            idx = next(i for i, p in enumerate(L.PRAYERS) if p.lower() == prayer.lower())
            ok = await l.ok(0x98, [idx + 1, 1 if on else 0])
        master, mask = await l.ask(0x95), await l.ask(0x99)
    m = mask[2] if mask else 0
    return {"ok": ok, "azan_on": bool(master and master[2]),
            "per_prayer": {p: bool(m & (1 << i)) for i, p in enumerate(L.PRAYERS)}}


if __name__ == "__main__":
    mcp.run()
