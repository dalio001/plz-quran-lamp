"""Bluetooth LE engine for the SQ-122 Quran lamp (same command table as index.html, see docs/pillars/02_LAMP_ENGINE.md).

Frames: EA <cmd> <args...> 00 AE. Replies: EB <cmd> <data...> 00 AE.
Every public call opens a short connection and closes it, so the phone app can still connect in between.
"""
import asyncio
import datetime as dt
import json
import re
import urllib.request

from bleak import BleakClient, BleakScanner

WRITE = "0000ae01-0000-1000-8000-00805f9b34fb"
NOTIFY = "0000ae02-0000-1000-8000-00805f9b34fb"
NAME_PREFIX = "XDT_"

PRAYERS = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
READERS = {2: "Muhammad Siddiq al-Minshawi (with children)", 3: "Saud ash-Shuraim", 4: "al-Tablawi",
           5: "Abu Bakr ash-Shatri", 6: "Abdullah Matrood", 7: "Maher al-Muaiqly", 8: "Abdullah Basfar",
           9: "Al-Minshawi", 10: "Abdul Basit", 11: "Muhammad Jibreel", 12: "Muhammad Ayyub", 13: "Al-Husary",
           14: "Al-Ajmi", 15: "Al-Fasy", 16: "Al-Hudhaify", 17: "Saad al-Ghamdi", 18: "As-Sudais"}
TRANS = {1: "English", 2: "Urdu", 3: "French", 4: "Bangla", 5: "Dari", 6: "Indonesian", 7: "Malay", 8: "Pashto",
         9: "Farsi", 10: "Somali", 11: "Swahili", 12: "Turkish", 13: "Hindi", 14: "Tamil", 16: "Russian", 17: "Uzbek",
         18: "Azerbaijani", 19: "Gujarati", 20: "Kazakh", 21: "Spanish", 22: "Bosnian", 23: "Malayalam",
         24: "Persian", 25: "German", 26: "Kurdish"}
BOOKS = {1: "Sahih al-Bukhari", 2: "Sahih Muslim", 3: "Ar-Ruqyah", 4: "Hisnul Muslim", 5: "Qaida Noorania",
         6: "Salat method / Duaa", 7: "40 Hadith", 50: "Idris Abkar", 51: "Hazza al-Balushi", 52: "Mansour as-Salimi"}
LIGHTS = {"warm white": 1, "cool white": 2, "red": 3, "green": 4, "blue": 5, "yellow": 6, "purple": 7,
          "light blue": 8, "dark yellow": 9, "orange": 10, "colour cycle": 11, "color cycle": 11}
VERSES = [7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52, 99, 128, 111, 110, 98, 135, 112, 78, 118,
          64, 77, 227, 93, 88, 69, 60, 34, 30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53, 89, 59, 37, 35, 38, 29, 18, 45,
          60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11, 11, 18, 12, 12, 30, 52, 52, 44, 28, 28, 20, 56, 40, 31, 50,
          40, 46, 42, 29, 19, 36, 25, 22, 17, 19, 26, 30, 20, 15, 21, 11, 8, 8, 19, 5, 8, 8, 11, 11, 8, 3, 9, 5, 4,
          7, 3, 6, 3, 5, 4, 5, 6]
SURAHS = ("Al-Fatiha,Al-Baqarah,Al Imran,An-Nisa,Al-Ma'idah,Al-An'am,Al-A'raf,Al-Anfal,At-Tawbah,Yunus,Hud,Yusuf,"
          "Ar-Ra'd,Ibrahim,Al-Hijr,An-Nahl,Al-Isra,Al-Kahf,Maryam,Ta-Ha,Al-Anbiya,Al-Hajj,Al-Mu'minun,An-Nur,"
          "Al-Furqan,Ash-Shu'ara,An-Naml,Al-Qasas,Al-Ankabut,Ar-Rum,Luqman,As-Sajdah,Al-Ahzab,Saba,Fatir,Ya-Sin,"
          "As-Saffat,Sad,Az-Zumar,Ghafir,Fussilat,Ash-Shura,Az-Zukhruf,Ad-Dukhan,Al-Jathiyah,Al-Ahqaf,Muhammad,"
          "Al-Fath,Al-Hujurat,Qaf,Adh-Dhariyat,At-Tur,An-Najm,Al-Qamar,Ar-Rahman,Al-Waqi'ah,Al-Hadid,Al-Mujadilah,"
          "Al-Hashr,Al-Mumtahanah,As-Saff,Al-Jumu'ah,Al-Munafiqun,At-Taghabun,At-Talaq,At-Tahrim,Al-Mulk,Al-Qalam,"
          "Al-Haqqah,Al-Ma'arij,Nuh,Al-Jinn,Al-Muzzammil,Al-Muddaththir,Al-Qiyamah,Al-Insan,Al-Mursalat,An-Naba,"
          "An-Nazi'at,Abasa,At-Takwir,Al-Infitar,Al-Mutaffifin,Al-Inshiqaq,Al-Buruj,At-Tariq,Al-A'la,Al-Ghashiyah,"
          "Al-Fajr,Al-Balad,Ash-Shams,Al-Layl,Ad-Duha,Ash-Sharh,At-Tin,Al-Alaq,Al-Qadr,Al-Bayyinah,Az-Zalzalah,"
          "Al-Adiyat,Al-Qari'ah,At-Takathur,Al-Asr,Al-Humazah,Al-Fil,Quraysh,Al-Ma'un,Al-Kawthar,Al-Kafirun,An-Nasr,"
          "Al-Masad,Al-Ikhlas,Al-Falaq,An-Nas").split(",")


class LampNotFound(RuntimeError):
    pass


def norm(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def find_surah(query):
    """Surah by number ('18') or name ('kahf', 'Al-Kahf', 'yasin'). Returns 1-based number."""
    q = str(query).strip()
    if q.isdigit() and 1 <= int(q) <= 114:
        return int(q)
    n = norm(q)
    for i, name in enumerate(SURAHS):
        if norm(name) == n or norm(name).removeprefix("al").removeprefix("an").removeprefix("as") == n:
            return i + 1
    for i, name in enumerate(SURAHS):
        if n and n in norm(name):
            return i + 1
    raise ValueError(f"Unknown surah: {query}")


class Lamp:
    """One short Bluetooth session. Use: async with Lamp() as lamp: await lamp.ask(0x41)"""

    def __init__(self, address=None):
        self.address = address
        self.client = None
        self.waiters = []

    async def __aenter__(self):
        device = None
        if self.address:
            device = await BleakScanner.find_device_by_address(self.address, timeout=10)
        if device is None:
            device = await BleakScanner.find_device_by_filter(
                lambda d, _a: bool(d.name) and d.name.startswith(NAME_PREFIX), timeout=12)
        if device is None:
            raise LampNotFound("Lamp not found. It must be switched ON (remote power button) and no phone may be "
                               "connected to it (close Koran Player / press Disconnect in the web app).")
        # Windows may cache an old service list; always read the services fresh from the lamp.
        self.client = BleakClient(device, timeout=20, winrt={"use_cached_services": False})
        await self.client.connect()
        if self.client.services.get_characteristic(NOTIFY) is None:
            await self.client.disconnect()
            raise LampNotFound(f"{device.name} answered but is not a Quran lamp (no AE02 service). Try again.")
        await self.client.start_notify(NOTIFY, self._on_reply)
        return self

    async def __aexit__(self, *_exc):
        try:
            await self.client.stop_notify(NOTIFY)
        finally:
            await self.client.disconnect()

    def _on_reply(self, _char, data):
        d = bytes(data)
        if len(d) < 3:
            return
        for w in self.waiters:
            if w["cmd"] == d[1]:
                w["parts"].append(d)
                if w["collect"] is None or w["collect"](w["parts"]):
                    self.waiters.remove(w)
                    w["future"].set_result(w["parts"])
                return

    async def send(self, cmd, args=()):
        frame = bytes([0xEA, cmd, *[a & 0xFF for a in args], 0x00, 0xAE])
        await self.client.write_gatt_char(WRITE, frame, response=False)
        await asyncio.sleep(0.15)

    async def ask(self, cmd, args=(), collect=None, timeout=2.5):
        """Send and wait for the reply with the same command byte. Returns bytes, or a list of packets if collect."""
        fut = asyncio.get_running_loop().create_future()
        w = {"cmd": cmd, "parts": [], "collect": collect, "future": fut}
        self.waiters.append(w)
        await self.send(cmd, args)
        try:
            parts = await asyncio.wait_for(fut, timeout)
        except asyncio.TimeoutError:
            if w in self.waiters:
                self.waiters.remove(w)
            parts = w["parts"]
            if not parts:
                return [] if collect else None
        return parts if collect else parts[0]

    async def ok(self, cmd, args=()):
        r = await self.ask(cmd, args)
        return bool(r and r[2] == 1)

    # ---- lists ----
    @staticmethod
    def _list_done(parts):
        last = parts[-1]
        if 0xFF in last[2:18]:
            return True
        return not (len(last) > 18 and last[18] != 0)

    @staticmethod
    def _list_ids(parts):
        ids = []
        for p in parts:
            for b in p[2:18]:
                if b == 0xFF:
                    return ids
                ids.append(b)
        return ids

    async def ids(self, cmd):
        return self._list_ids(await self.ask(cmd, collect=self._list_done, timeout=3))

    async def name(self, cmd, item_id):
        r = await self.ask(cmd, [item_id])
        return r[2:-2].decode("utf-8", "replace").strip("\x00 ") if r else f"#{item_id}"

    async def named_list(self, kind):
        count_cmd, ids_cmd, name_cmd, table = {
            "reciters": (0x70, 0x72, 0x76, READERS),
            "translations": (0x71, 0x75, 0x77, TRANS),
            "books": (0x78, 0x79, 0x80, BOOKS),
        }[kind]
        await self.ask(count_cmd)
        out = []
        for i in await self.ids(ids_cmd):
            if kind == "books" and i == 15:
                continue
            out.append({"id": i, "name": table.get(i) or await self.name(name_cmd, i)})
        return out

    # ---- times ----
    @staticmethod
    def _pairs(d):
        return [f"{d[3 + i * 2]:02}:{d[4 + i * 2]:02}" for i in range(6)]

    async def times(self):
        now, calc = await self.ask(0x91), await self.ask(0x93)
        if not now or not calc:
            raise RuntimeError("Lamp did not answer the prayer time queries")
        return now[2], self._pairs(now), self._pairs(calc)

    async def set_times(self, times):
        fmt, _now, calc = await self.times()
        to_min = lambda t: int(t[:2]) * 60 + int(t[3:5])  # noqa: E731
        for name, t, c in zip(PRAYERS, times, calc):
            if abs(to_min(t) - to_min(c)) > 120:
                raise ValueError(f"{name} {t} is more than 2 hours from the lamp's own time {c}")
        args = [fmt] + [x for t in times for x in (int(t[:2]), int(t[3:5]))]
        if not await self.ok(0x92, args):
            raise RuntimeError("Lamp refused the new times")
        return (await self.times())[1]

    async def sync_clock(self):
        n = dt.datetime.now()
        await self.send(0x90, [n.year >> 8, n.year & 0xFF, n.month, n.day, n.hour, n.minute, n.second])


def mawaqit_times(slug, day=None):
    """6 times (Fajr, Sunrise, Dhuhr, Asr, Maghrib, Isha) for a Mawaqit mosque. After Isha, tomorrow's times."""
    req = urllib.request.Request(f"https://mawaqit.net/en/{slug}", headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
    conf = json.loads(re.search(r"(?:let|var|const)\s+confData\s*=\s*(\{.*?\});\s*\n", html, re.S).group(1))
    now = dt.datetime.now()
    day = day or now.date()
    times = conf["calendar"][day.month - 1][str(day.day)]
    isha = int(times[5][:2]) * 60 + int(times[5][3:5])
    if day == now.date() and now.hour * 60 + now.minute > isha:
        day += dt.timedelta(days=1)
        times = conf["calendar"][day.month - 1][str(day.day)]
    return conf.get("name", slug), day, times
