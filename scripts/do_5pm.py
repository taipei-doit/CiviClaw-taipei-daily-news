import urllib.request
import json
from pathlib import Path

from config import BASE_DIR as BASE, OUTPUT_DIR
URL = "https://www.gov.taipei/OpenData.aspx?SN=ABBF62618F53F8DE"

req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    data_5pm = json.loads(response.read().decode('utf-8-sig'))

news_12pm = OUTPUT_DIR / "news_12pm.json"
if news_12pm.exists():
    data_12pm = json.loads(news_12pm.read_text(encoding="utf-8-sig"))
else:
    data_12pm = []

merged = data_5pm + data_12pm
unique_articles = {}
for item in merged:
    sn = item.get("DataSN", "")
    title = item.get("title", "")
    key = sn if sn else title
    if key not in unique_articles:
        unique_articles[key] = item
        
# Output the unique articles so we can use LLM to pick top 5
out = list(unique_articles.values())
# Just save them all to a temp file, and print titles to pick
with open(OUTPUT_DIR / "merged_unique.json", "w", encoding="utf-8-sig") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

for i, item in enumerate(out[:20]):
    print(f"{i}. {item.get('title')}")
