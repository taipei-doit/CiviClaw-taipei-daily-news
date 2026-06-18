import json
from pathlib import Path
from datetime import datetime

from config import BASE_DIR, OUTPUT_DIR
NEWS_5PM = OUTPUT_DIR / "news_5pm.json"
NEWS_12PM = OUTPUT_DIR / "news_12pm.json"
PUBLISHED_FILE = BASE_DIR / "memory" / "published_articles.txt"

def main():
    data = []
    if NEWS_5PM.exists():
        data += json.loads(NEWS_5PM.read_text(encoding="utf-8-sig"))
    if NEWS_12PM.exists():
        data += json.loads(NEWS_12PM.read_text(encoding="utf-8-sig"))
        
    published = set()
    if PUBLISHED_FILE.exists():
        published = set(PUBLISHED_FILE.read_text(encoding="utf-8").splitlines())
        
    unique_articles = {}
    for item in data:
        sn = item.get("DataSN", "")
        title = item.get("title", "")
        if not sn or sn in published or title in published:
            continue
        key = sn
        if key not in unique_articles:
            unique_articles[key] = item
            
    # Sort by date
    def parse_date(x):
        try:
            return datetime.strptime(x.get("日期時間", ""), "%Y-%m-%dT%H:%M:%S")
        except:
            return datetime.min

    sorted_list = sorted(unique_articles.values(), key=parse_date, reverse=True)
    
    candidates = []
    for item in sorted_list[:100]: # Take up to 100 titles
        candidates.append({
            "DataSN": item.get("DataSN", ""),
            "title": item.get("title", "")
        })
        
    out_file = OUTPUT_DIR / "llm_candidates.json"
    out_file.write_text(json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Prepared {len(candidates)} candidates for LLM in {out_file.name}")

if __name__ == "__main__":
    main()