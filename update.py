import json, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone

FEEDS = [
    ("BBC Arabic", "https://feeds.bbci.co.uk/arabic/rss.xml"),
    ("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("BBC Business", "https://feeds.bbci.co.uk/news/business/rss.xml"),
    ("Guardian World", "https://www.theguardian.com/world/rss"),
    ("Guardian Business", "https://www.theguardian.com/uk/business/rss"),
    ("NPR World", "https://feeds.npr.org/1004/rss.xml"),
    ("Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml"),
]

items = []
for name, url in FEEDS:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = r.read()
        root = ET.fromstring(raw)
        for el in root.findall(".//item")[:8]:
            title = ""
            link = ""
            date = ""
            for c in list(el):
                tag = c.tag.split("}")[-1]
                if tag == "title" and c.text:
                    title = c.text.strip()
                elif tag == "link" and c.text:
                    link = c.text.strip()
                elif tag == "pubDate" and c.text:
                    date = c.text.strip()
            if title:
                items.append({"title": title, "link": link, "date": date, "source": name})
        print("ok", name)
    except Exception as e:
        print("fail", name, e)

out = {"updated": datetime.now(timezone.utc).isoformat(), "items": items}
with open("news.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("saved", len(items))
