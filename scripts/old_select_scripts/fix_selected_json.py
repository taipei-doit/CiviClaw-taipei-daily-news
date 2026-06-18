import json
with open('/home/benliangcs/tw-gov-video/output/selected_articles.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract the inner array directly to avoid the nested "selected" dictionaries
if "selected" in data and "selected" in data["selected"]:
    data = data["selected"]["selected"]
elif "selected" in data:
    data = data["selected"]

with open('/home/benliangcs/tw-gov-video/output/selected_articles.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Fixed JSON format")
