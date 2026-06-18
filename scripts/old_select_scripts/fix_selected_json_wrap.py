import json
with open('/home/benliangcs/tw-gov-video/output/selected_articles.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# The scripts might expect exactly {"selected": [ ... ]}
if isinstance(data, list):
    data = {"selected": data}
elif isinstance(data, dict) and "selected" in data and isinstance(data["selected"], dict) and "selected" in data["selected"]:
    data = {"selected": data["selected"]["selected"]}

with open('/home/benliangcs/tw-gov-video/output/selected_articles.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Fixed JSON format for wrapping")
