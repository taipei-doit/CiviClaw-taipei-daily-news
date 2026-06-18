import json

from config import OUTPUT_DIR

news_12pm_file = OUTPUT_DIR / 'news_12pm.json'
news_5pm_file = OUTPUT_DIR / 'news_5pm.json'
merged_news_file = OUTPUT_DIR / 'merged_news.json'

try:
    with open(news_12pm_file, 'r', encoding='utf-8-sig') as f:
        news_12pm = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    news_12pm = []

try:
    with open(news_5pm_file, 'r', encoding='utf-8-sig') as f:
        news_5pm = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    news_5pm = []

merged = {item['DataSN']: item for item in news_12pm}
for item in news_5pm:
    merged[item['DataSN']] = item

with open(merged_news_file, 'w', encoding='utf-8') as f:
    json.dump(list(merged.values()), f, ensure_ascii=False, indent=2)

print(len(merged))
