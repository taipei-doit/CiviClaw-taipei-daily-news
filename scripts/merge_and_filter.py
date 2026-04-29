import json
import os
import sys

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    return []

articles_12pm = load_json('/home/benliangcs/tw-gov-video/output/news_12pm.json')
articles_5pm = load_json('/home/benliangcs/tw-gov-video/output/news_5pm.json')

published = set()
if os.path.exists('/home/benliangcs/.openclaw/workspace/memory/published_articles.txt'):
    with open('/home/benliangcs/.openclaw/workspace/memory/published_articles.txt', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().replace(',', '|').split('|')
            if len(parts) > 0:
                published.add(parts[0].strip())

merged = {}
for article in articles_12pm + articles_5pm:
    sn = article.get('DataSN', '')
    title = article.get('title', '')
    if sn not in published and sn not in merged:
        merged[sn] = article

# Print out a summary to pick 5
count = 0
for sn, art in merged.items():
    print(f"[{sn}] {art['title']}")
    count += 1
    if count >= 10:
        break

print(f"Total available: {len(merged)}")
with open('/home/benliangcs/tw-gov-video/output/merged_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(list(merged.values()), f, ensure_ascii=False, indent=2)

