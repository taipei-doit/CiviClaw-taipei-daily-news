import json
import urllib.request
from pathlib import Path

from config import BASE_DIR as BASE, OUTPUT_DIR, INPUT_JSON

if not INPUT_JSON.exists():
    print("Files missing.")
    exit(0)

# Fetch latest 50 articles directly from OpenData to ensure we have the correct images
url = "https://www.gov.taipei/OpenData.aspx?SN=ABBF62618F53F8DE"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    import ssl
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=context) as response:
        news_data = json.loads(response.read().decode('utf-8-sig'))
except Exception as e:
    print(f"Failed to fetch OpenData: {e}")
    # Fallback to local files if fetch fails
    news_data = []
    for filename in ["news_live.json", "news_12pm.json"]:
        try:
            filepath = OUTPUT_DIR / filename
            if filepath.exists():
                news_data.extend(json.loads(filepath.read_text(encoding="utf-8-sig")))
        except Exception as ex:
            print(f"Failed to read fallback {filename}: {ex}")

data = json.loads(INPUT_JSON.read_text(encoding="utf-8-sig"))

image_lookup = {}
images_list_lookup = {}
for article in news_data:
    sn = article.get("DataSN", "")
    pics = article.get("相關圖片", [])
    if pics and len(pics) > 0:
        image_lookup[sn] = pics[0].get("url", "")
        images_list_lookup[sn] = [p.get("url", "") for p in pics if p.get("url")]

items = data.get("selected", [])
for item in items:
    sn = item.get("DataSN", "")
    if sn in image_lookup and image_lookup[sn]:
        print(f"Auto-injecting official images for {sn}: {len(images_list_lookup[sn])} found")
        item["image_url"] = image_lookup[sn]
        item["image_urls"] = images_list_lookup.get(sn, [])
        item["is_ai_generated"] = False
    elif "ai_article" in item.get("image_url", "") or not item.get("image_url", ""):
        item["image_url"] = ""
        item["image_urls"] = []

INPUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
