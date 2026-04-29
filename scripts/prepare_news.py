import json
import urllib.request
import os

published = set()
if os.path.exists('/home/benliangcs/.openclaw/workspace/memory/published_articles.txt'):
    with open('/home/benliangcs/.openclaw/workspace/memory/published_articles.txt', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 1:
                published.add(parts[0].strip())

news_12pm = []
if os.path.exists('/home/benliangcs/tw-gov-video/output/news_12pm.json'):
    with open('/home/benliangcs/tw-gov-video/output/news_12pm.json', 'r', encoding='utf-8') as f:
        try:
            news_12pm = json.load(f)
        except:
            pass

url = "https://www.gov.taipei/OpenData.aspx?SN=ABBF62618F53F8DE"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req)
news_5pm = json.loads(response.read().decode('utf-8-sig'))

all_news = news_12pm + news_5pm
unique_news = {}
for item in all_news:
    sn = item.get('DataSN')
    if sn and sn not in published and item.get('title') not in published:
        unique_news[sn] = item

selected = list(unique_news.values())[:5]

output = []
for item in selected:
    img = ""
    if item.get("相關圖片"):
        img_item = item["相關圖片"][0]
        if isinstance(img_item, dict) and "url" in img_item:
            img = img_item["url"]
    output.append({
        "title": item.get("title", ""),
        "DataSN": item.get("DataSN", ""),
        "source_url": item.get("Source", ""),
        "description": item.get("內容", ""),
        "image_url": img
    })

print(json.dumps(output, ensure_ascii=False, indent=2))
