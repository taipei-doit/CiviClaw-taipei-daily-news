import json

with open('/home/benliangcs/tw-gov-video/output/selected_articles.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if isinstance(data, list):
    new_data = {"selected": data}
    with open('/home/benliangcs/tw-gov-video/output/selected_articles.json', 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    print("Fixed to dict with 'selected' key")
