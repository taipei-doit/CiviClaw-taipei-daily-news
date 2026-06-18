import json

def merge_and_filter():
    try:
        with open('output/news_12pm.json', 'r', encoding='utf-8-sig') as f:
            news_12pm = json.load(f)
    except FileNotFoundError:
        news_12pm = []

    try:
        with open('output/news_5pm.json', 'r', encoding='utf-8-sig') as f:
            news_5pm = json.load(f)
    except FileNotFoundError:
        news_5pm = []

    try:
        with open('/home/benliangcs/.openclaw/workspace/memory/published_articles.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            published_ids = set()
            for line in lines:
                parts = line.split('|')
                if len(parts) > 0:
                    published_ids.add(parts[0].strip().replace(',', ''))
    except FileNotFoundError:
        published_ids = set()

    combined = news_12pm + news_5pm
    
    unique_articles = []
    seen_ids = set()
    seen_titles = set()

    for article in combined:
        data_sn = article.get('DataSN', '')
        title = article.get('title', '')
        if data_sn in seen_ids or title in seen_titles or data_sn in published_ids:
            continue
        seen_ids.add(data_sn)
        seen_titles.add(title)
        unique_articles.append(article)
        
    with open('output/merged_candidates.json', 'w', encoding='utf-8') as f:
        json.dump(unique_articles, f, ensure_ascii=False, indent=2)

merge_and_filter()
