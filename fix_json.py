import json

with open("output/selected_articles.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, list):
    output = {"selected": data}
    with open("output/selected_articles.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
