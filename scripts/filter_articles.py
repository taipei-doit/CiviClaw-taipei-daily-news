import json

with open('/home/benliangcs/tw-gov-video/output/merged_news.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

# Load published IDs and titles
published_ids = set()
published_titles = set()
try:
    with open('/home/benliangcs/.openclaw/workspace/memory/published_articles.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            # Handle different separators like '|' or ','
            if '|' in line:
                parts = line.split('|', 1)
            elif ',' in line:
                parts = line.split(',', 1)
            else:
                parts = [line]
                
            if parts:
                published_ids.add(parts[0].strip())
            if len(parts) > 1:
                published_titles.add(parts[1].strip())
except FileNotFoundError:
    pass

filtered_articles = []
for a in articles:
    dsn = a.get('DataSN', '').strip()
    title = a.get('title', '').strip()
    if dsn not in published_ids and title not in published_titles:
        filtered_articles.append(a)

print(f"Total: {len(articles)}, Filtered: {len(filtered_articles)}")
with open('/home/benliangcs/tw-gov-video/output/filtered_news.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_articles, f, ensure_ascii=False, indent=2)
