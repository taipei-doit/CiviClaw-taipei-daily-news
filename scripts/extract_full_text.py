import sys
import json
from pathlib import Path

from config import OUTPUT_DIR
NEWS_5PM = OUTPUT_DIR / "news_5pm.json"
NEWS_12PM = OUTPUT_DIR / "news_12pm.json"

def main():
    sn_list = sys.argv[1:]
    if not sn_list:
        print("Please provide DataSNs as arguments.")
        return
        
    data = []
    if NEWS_5PM.exists():
        try:
            data += json.loads(NEWS_5PM.read_text(encoding="utf-8-sig"))
        except:
            pass
    if NEWS_12PM.exists():
        try:
            data += json.loads(NEWS_12PM.read_text(encoding="utf-8-sig"))
        except:
            pass

    found_sns = set()
    for sn in sn_list:
        for item in data:
            if item.get("DataSN") == sn and sn not in found_sns:
                found_sns.add(sn)
                print(f"[{sn}] {item.get('title')}")
                print(f"Source URL: {item.get('Source') or item.get('Link')}")
                print(f"Content:\n{item.get('內容', '')}\n")
                print("-" * 50)
                break

if __name__ == "__main__":
    main()
