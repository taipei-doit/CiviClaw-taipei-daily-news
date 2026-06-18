import json
import os

with open('/home/benliangcs/tw-gov-video/output/news_5pm.json', 'r', encoding='utf-8-sig') as f:
    news_5pm = json.load(f)

news_12pm = []
if os.path.exists('/home/benliangcs/tw-gov-video/output/news_12pm.json'):
    with open('/home/benliangcs/tw-gov-video/output/news_12pm.json', 'r', encoding='utf-8-sig') as f:
        try:
            news_12pm = json.load(f)
        except json.JSONDecodeError:
            pass

all_news = news_12pm + news_5pm

published = set()
if os.path.exists('/home/benliangcs/memory/published_articles.txt'):
    with open('/home/benliangcs/memory/published_articles.txt', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split('|')
            if len(parts) > 0:
                published.add(parts[0].strip())
            parts2 = line.split(',')
            if len(parts2) > 0:
                published.add(parts2[0].strip())

unique_news = {}
for item in all_news:
    sn = str(item.get('DataSN', '')).strip()
    title = item.get('title', '').strip()
    if sn not in published and title not in published and sn not in unique_news:
        unique_news[sn] = item

fresh_news = list(unique_news.values())

with open('/home/benliangcs/tw-gov-video/output/fresh_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(fresh_news[:10], f, ensure_ascii=False, indent=2)

print(f"Extracted {len(fresh_news)} fresh articles. Saved top 10 candidates.")
