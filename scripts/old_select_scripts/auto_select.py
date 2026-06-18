import json
import urllib.request
import os

url = "https://www.gov.taipei/OpenData.aspx?SN=ABBF62618F53F8DE"
out_dir = os.path.expanduser("~/tw-gov-video/output")
os.makedirs(out_dir, exist_ok=True)

# Fetch 5pm data
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    raw_data = response.read().decode('utf-8-sig')
    data_5pm = json.loads(raw_data)

# Load 12pm data
data_12pm = []
if os.path.exists(os.path.join(out_dir, "news_12pm.json")):
    try:
        with open(os.path.join(out_dir, "news_12pm.json"), "r", encoding="utf-8-sig") as f:
            data_12pm = json.load(f)
    except:
        pass

# Merge
merged = data_12pm + data_5pm

# Deduplicate by DataSN
unique_articles = {}
for article in merged:
    sn = article.get("DataSN")
    if sn and sn not in unique_articles:
        unique_articles[sn] = article

# Load published articles
published_sns = set()
pub_file = os.path.expanduser("~/.openclaw/workspace/memory/published_articles.txt")

if os.path.exists(pub_file):
    with open(pub_file, "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                published_sns.add(line.split("|")[0].strip())

# Filter
fresh_articles = []
for sn, article in unique_articles.items():
    if sn not in published_sns:
        fresh_articles.append(article)

with open(os.path.join(out_dir, "fresh_articles.json"), "w", encoding="utf-8") as f:
    json.dump(fresh_articles, f, ensure_ascii=False, indent=2)

print(f"Fresh articles: {len(fresh_articles)}")
