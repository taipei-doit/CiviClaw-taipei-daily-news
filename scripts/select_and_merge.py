import json
import os

with open('/home/benliangcs/tw-gov-video/output/news_12pm.json', 'r', encoding='utf-8-sig') as f:
    d1 = json.load(f)
with open('/home/benliangcs/tw-gov-video/output/news_5pm.json', 'r', encoding='utf-8-sig') as f:
    d2 = json.load(f)

merged = {item['DataSN']: item for item in d1 + d2}

published = set()
pub_file = '/home/benliangcs/.openclaw/workspace/memory/published_articles.txt'
if os.path.exists(pub_file):
    with open(pub_file, 'r') as f:
        published = set(line.strip() for line in f)

available = [v for k, v in merged.items() if k not in published]

with open('/home/benliangcs/tw-gov-video/output/available_news.json', 'w', encoding='utf-8') as f:
    json.dump(available, f, ensure_ascii=False, indent=2)

