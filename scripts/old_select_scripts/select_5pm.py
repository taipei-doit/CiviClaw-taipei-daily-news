import json
import os
import random

news_5pm_path = os.path.expanduser("~/tw-gov-video/output/news_5pm.json")
news_12pm_path = os.path.expanduser("~/tw-gov-video/output/news_12pm.json")

all_news = []
if os.path.exists(news_12pm_path):
    with open(news_12pm_path, "r", encoding="utf-8-sig") as f:
        all_news.extend(json.load(f))

if os.path.exists(news_5pm_path):
    with open(news_5pm_path, "r", encoding="utf-8-sig") as f:
        all_news.extend(json.load(f))

unique_news = {}
for n in all_news:
    unique_news[n['DataSN']] = n

published = set()
pub_path = os.path.expanduser("memory/published_articles.txt")
if os.path.exists(pub_path):
    with open(pub_path, "r", encoding="utf-8-sig") as f:
        for line in f:
            if "|" in line:
                sn = line.split("|")[0].strip()
                published.add(sn)
            elif "," in line:
                sn = line.split(",")[0].strip()
                published.add(sn)
            else:
                published.add(line.strip())

available_news = [n for sn, n in unique_news.items() if sn not in published]

with open(os.path.expanduser("~/tw-gov-video/output/available_news.json"), "w", encoding="utf-8") as f:
    json.dump(available_news, f, ensure_ascii=False, indent=2)

print(f"Total available: {len(available_news)}")
