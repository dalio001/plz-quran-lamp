"""Save the mosque's yearly Mawaqit calendar as times.json next to the web app.
Usage: python -I make_times.py [mosque-slug]"""
import json
import pathlib
import re
import sys
import urllib.request

slug = sys.argv[1] if len(sys.argv) > 1 else "al-taqua-moschee-essen"
req = urllib.request.Request(f"https://mawaqit.net/en/{slug}", headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
conf = json.loads(re.search(r"(?:let|var|const)\s+confData\s*=\s*(\{.*?\});\s*\n", html, re.S).group(1))
out = {
    "mosque": conf.get("name"),
    "slug": slug,
    "latitude": conf.get("latitude"),
    "longitude": conf.get("longitude"),
    "timezone": conf.get("timezone"),
    "calendar": conf["calendar"],  # 12 months, {"day": [fajr, sunrise, dhuhr, asr, maghrib, isha]}
}
path = pathlib.Path(__file__).with_name("times.json")
path.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print("saved", path, out["mosque"])
