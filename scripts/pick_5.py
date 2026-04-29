import json
from pathlib import Path

BASE = Path.home() / "tw-gov-video"
OUTPUT_DIR = BASE / "output"

with open(OUTPUT_DIR / "merged_unique.json", "r", encoding="utf-8") as f:
    out = json.load(f)

# Pick specific indices
indices = [0, 9, 11, 12, 19]

selected = []
for idx in indices:
    item = out[idx]
    
    # Generate simple script
    title = item.get("title", "")
    content = item.get("內容", item.get("content", ""))
    
    script = f"為您播報最新市政消息：{title}。{content[:100]}..."
    
    selected.append({
        "title": title,
        "script": script,
        "DataSN": item.get("DataSN", "")
    })

with open(OUTPUT_DIR / "selected_articles.json", "w", encoding="utf-8") as f:
    json.dump(selected, f, ensure_ascii=False, indent=2)
    
print("Saved 5 articles to selected_articles.json")
