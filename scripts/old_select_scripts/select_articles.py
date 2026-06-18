import json
import urllib.request
import os
import random

# Fetch 5pm open data
url = "https://www.gov.taipei/OpenData.aspx?SN=ABBF62618F53F8DE"
req = urllib.request.urlopen(url)
data_5pm_str = req.read().decode('utf-8-sig')
data_5pm = json.loads(data_5pm_str)

# Load 12pm data
with open(os.path.expanduser('~/tw-gov-video/output/news_12pm.json'), 'r', encoding='utf-8-sig') as f:
    data_12pm = json.load(f)

# Merge data
all_articles = data_12pm + data_5pm
unique_articles = {a.get('Title', str(random.random())): a for a in all_articles}.values()

# Deduplicate
pub_file = os.path.expanduser('~/.openclaw/workspace/memory/published_articles.txt')
published = set()
if os.path.exists(pub_file):
    with open(pub_file, 'r', encoding='utf-8') as f:
        published = set([line.strip() for line in f.readlines()])

new_articles = [a for a in unique_articles if a.get('Title') not in published]

# Select best 5
selected = new_articles[:5]

# Write out
out_file = os.path.expanduser('~/tw-gov-video/output/selected_articles.json')
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump({"selected": selected}, f, ensure_ascii=False, indent=2)

# Update published
with open(pub_file, 'a', encoding='utf-8') as f:
    for a in selected:
        title = a.get('Title')
        if title:
            f.write(title + "\n")

print("Done")
