import json

from config import BASE_DIR, OUTPUT_DIR

merged_news_file = OUTPUT_DIR / 'merged_news.json'
published_file = BASE_DIR / 'memory' / 'published_articles.txt'
filtered_news_file = OUTPUT_DIR / 'filtered_news.json'

with open(merged_news_file, 'r', encoding='utf-8') as f:
    articles = json.load(f)

# Load published IDs and titles
published_ids = set()
published_titles = set()
try:
    with open(published_file, 'r', encoding='utf-8') as f:
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
with open(filtered_news_file, 'w', encoding='utf-8') as f:
    json.dump(filtered_articles, f, ensure_ascii=False, indent=2)
