import json

with open('/home/benliangcs/tw-gov-video/output/news_12pm.json', 'r', encoding='utf-8-sig') as f:
    try:
        news_12pm = json.load(f)
    except json.JSONDecodeError:
        news_12pm = []

with open('/home/benliangcs/tw-gov-video/output/news_5pm.json', 'r', encoding='utf-8-sig') as f:
    news_5pm = json.load(f)

merged = {item['DataSN']: item for item in news_12pm}
for item in news_5pm:
    merged[item['DataSN']] = item

with open('/home/benliangcs/tw-gov-video/output/merged_news.json', 'w', encoding='utf-8') as f:
    json.dump(list(merged.values()), f, ensure_ascii=False, indent=2)

print(len(merged))
