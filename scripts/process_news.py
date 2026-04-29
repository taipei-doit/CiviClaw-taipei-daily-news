import json

with open('/home/benliangcs/tw-gov-video/output/parsed_5pm.json', 'r') as f:
    news = json.load(f)

# Filter out articles already in published_articles.txt
published_sns = set()
published_titles = set()
try:
    with open('/home/benliangcs/.openclaw/workspace/memory/published_articles.txt', 'r') as f:
        for line in f:
            if '|' in line:
                sn, title = line.split('|', 1)
                published_sns.add(sn.strip())
                published_titles.add(title.strip())
            elif ',' in line:
                sn, title = line.split(',', 1)
                published_sns.add(sn.strip())
                published_titles.add(title.strip())
except FileNotFoundError:
    pass

filtered_news = []
for item in news:
    sn = item.get('DataSN')
    title = item.get('title')
    if sn not in published_sns and title not in published_titles:
        filtered_news.append(item)

# Select top 5
selected = filtered_news[:5]

output = []
for item in selected:
    image_url = ""
    if item.get("images") and len(item["images"]) > 0:
        image_url = item["images"][0].get("url", "")
    
    output.append({
        "title": item.get("title", ""),
        "script": f"這是一則關於「{item.get('title')}」的最新消息。請持續關注相關報導。",
        "reason": "這是一則重要的地方新聞，值得讓市民了解最新動態。",
        "source_url": item.get("url", ""),
        "DataSN": item.get("DataSN", ""),
        "image_url": image_url,
        "is_ai_generated": True
    })

with open('/home/benliangcs/tw-gov-video/output/selected_articles.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

with open('/home/benliangcs/.openclaw/workspace/memory/published_articles.txt', 'a', encoding='utf-8') as f:
    for item in output:
        f.write(f"{item['DataSN']} | {item['title']}\n")

