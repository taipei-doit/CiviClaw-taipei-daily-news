import json
import os
import random
import re

published_file = os.path.expanduser('/home/benliangcs/.openclaw/workspace/memory/published_articles.txt')
merged_file = os.path.expanduser('~/tw-gov-video/output/news_merged.json')
output_file = os.path.expanduser('~/tw-gov-video/output/selected_articles.json')

# Load published IDs
published_ids = set()
try:
    with open(published_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            parts = re.split(r'[|,]', line)
            if parts:
                published_ids.add(parts[0].strip())
except Exception as e:
    print("Error reading published:", e)

with open(merged_file, 'r', encoding='utf-8') as f:
    merged_data = json.load(f)

# Filter out published
fresh_articles = []
for item in merged_data:
    sn = str(item.get('DataSN', ''))
    if sn not in published_ids and sn:
        fresh_articles.append(item)

# Sort by SN (descending) to get newest roughly, or just take random.
# Actually, random selection of 5.
if len(fresh_articles) > 5:
    selected = random.sample(fresh_articles, 5)
else:
    selected = fresh_articles

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(selected, f, ensure_ascii=False, indent=2)

print(f"Selected {len(selected)} articles out of {len(fresh_articles)} fresh ones.")
