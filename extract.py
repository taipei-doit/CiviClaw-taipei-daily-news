import json

with open('output/merged_candidates.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

for a in articles[:5]:
    print("---------------------------------")
    print(f"Title: {a.get('title')}")
    print(f"DataSN: {a.get('DataSN')}")
    print(f"URL: {a.get('Source') or a.get('Link')}")
    images = a.get('相關圖片', [])
    if images:
        print(f"Image: {images[0].get('URL', '')}")
    else:
        print("Image: ")
    print(f"Content: {a.get('內容', '')[:300]}...")
