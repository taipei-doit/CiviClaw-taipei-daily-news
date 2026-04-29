import urllib.request
import json
from pathlib import Path
from datetime import datetime

BASE = Path.home() / "tw-gov-video"
OUTPUT_DIR = BASE / "output"
URL = "https://www.gov.taipei/OpenData.aspx?SN=ABBF62618F53F8DE"

def fetch_data():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8-sig'))
        return data

def do_12pm_fetch():
    data = fetch_data()
    out_file = OUTPUT_DIR / "news_12pm.json"
    out_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"12PM fetch complete. Saved {len(data)} articles to {out_file}")
    return len(data)

def get_merged_articles():
    # Load 5pm (current) fetch
    current_data = fetch_data()
    merged_list = current_data
    
    # Load 12pm fetch if exists
    news_12pm = OUTPUT_DIR / "news_12pm.json"
    if news_12pm.exists():
        try:
            data_12pm = json.loads(news_12pm.read_text(encoding="utf-8"))
            merged_list.extend(data_12pm)
        except Exception as e:
            print(f"Failed reading 12pm data: {e}")
            
    # Deduplicate by DataSN
    unique_articles = {}
    for item in merged_list:
        sn = item.get("DataSN", item.get("title", ""))
        if sn not in unique_articles:
            unique_articles[sn] = item
            
    return list(unique_articles.values())

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "12pm":
        do_12pm_fetch()
