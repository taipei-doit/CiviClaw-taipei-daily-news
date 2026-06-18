import json

selected = [
  {
    "title": "給大人的情感必修學分！臺北市情感關係工作坊4/16開放報名",
    "script": "臺北市政府民政局宣布，2026年「情感關係工作坊」於4月16日起開放網路報名。活動包含自我探索、氣味心理學與藝術創作等12場次，引導市民透過故事分享與共同創作，建立真誠的對話與理解。",
    "reason": "推廣市府舉辦的市民身心靈健康與人際關係活動，提升生活品質。",
    "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=811737C1BD88DF98",
    "DataSN": "9564383",
    "image_url": "",
    "is_ai_generated": True
  },
  {
    "title": "延續熱烈迴響！勞動事務學院第2梯次課程4月17日登場",
    "script": "臺北市勞動局持續推動勞動教育，「勞動事務學院」第1期第2梯次課程將於4月17日上午9時開放線上報名。課程涵蓋勞基法、休假權益及職場性騷擾防治等實用議題，歡迎勞工與企業踴躍參與，提升職場應對能力。",
    "reason": "關乎廣大勞工權益與進修機會，實用性極高。",
    "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=ACF642BB6CA01F56",
    "DataSN": "9564373",
    "image_url": "https://www-ws.gov.taipei/001/Upload/307/relpic/10162/9564373/861c4cf4-5a69-4199-b046-e19bb4053723.jpg",
    "is_ai_generated": True
  },
  {
    "title": "慢性阻塞性肺病",
    "script": "根據世衛組織資料，肺阻塞已成為全球第三大死因，且在台灣40歲以上民眾盛行率達6.1%。衛生局提醒，許多患者有高達四成至八成的未被診斷率，呼籲高風險族群及早檢查，守護呼吸道健康。",
    "reason": "健康衛教資訊，提醒民眾防範並正視呼吸道健康問題。",
    "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=6B9A8C7A2E9F4A5C",
    "DataSN": "9564325",
    "image_url": "https://www-ws.gov.taipei/001/Upload/446/relpic/10162/9564325/657c6732-b1cf-4033-8478-975bbe9fdfce.jpg",
    "is_ai_generated": True
  },
  {
    "title": "跌倒竟成致命危機 80歲嬤膝蓋「啪」一聲二度骨折",
    "script": "一名80歲婦人跌倒後重回活動，竟因嚴重骨質疏鬆導致膝蓋二度骨折。北市聯醫骨科提醒，長者跌倒不容小覷，若出現長期疼痛應盡速就醫，以免局部骨頭壞死引發更嚴重的健康危機。",
    "reason": "高齡化社會下的重要醫療警示，提醒長者防跌及骨質疏鬆防範。",
    "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=E27BD2F1CD834950",
    "DataSN": "9564314",
    "image_url": "https://www-ws.gov.taipei/001/Upload/446/relpic/10162/9564314/c399732b-9053-4da8-9575-6f8e41bc03a6.jpg",
    "is_ai_generated": True
  },
  {
    "title": "115年1月臺北市房市交易量減少18.64% 住宅價格指數上升0.10%",
    "script": "臺北市發布最新房市數據，115年1月實價登錄交易件數為406件，較上月減少超過一成八。然而，住宅價格指數微幅上升0.10%，顯示市場呈現「量縮價微漲」的觀望態勢。",
    "reason": "房地產市場動態為民眾高度關注之經濟議題。",
    "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=3E7A9D1C2F5B6A8C",
    "DataSN": "9564553",
    "image_url": "",
    "is_ai_generated": True
  }
]

# Quick fix: I need to ensure the correct Source URLs from fresh_articles are used. Let me re-load fresh_articles and patch the URLs.
with open('/home/benliangcs/tw-gov-video/output/fresh_articles.json') as f:
    fresh = json.load(f)

for s in selected:
    # find matching in fresh
    for f_art in fresh:
        if str(f_art.get("DataSN")) == s["DataSN"]:
            s["source_url"] = f_art.get("Source", s["source_url"])
            break

with open('/home/benliangcs/tw-gov-video/output/selected_articles.json', 'w', encoding='utf-8') as f:
    json.dump(selected, f, ensure_ascii=False, indent=2)

print("selected_articles.json written!")
