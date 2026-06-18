import json

articles = [
  {
    "title": "糖尿病患者必知的低血糖「15法則」",
    "script": "台北市立聯合醫院提醒糖尿病患者，不可輕忽低血糖的嚴重性，可能導致昏迷甚至死亡。若發生低血糖，請務必牢記救命秘訣「15法則」：立刻補充15公克糖分，15分鐘後再測量，若未改善需立即就醫。",
    "reason": "健康宣導資訊，對於高齡長者及糖尿病患者非常實用且具備急救觀念。",
    "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=B2E084BECAEA6988",
    "DataSN": "9567549",
    "image_url": "https://www-ws.gov.taipei/001/Upload/446/relpic/10162/9567549/9bced23e-87b1-4fbb-a3f4-961ae737938e.png",
    "is_ai_generated": True
  },
  {
    "title": "幽門螺旋桿菌不可輕忽 醫師提醒及早篩檢降低胃癌風險",
    "script": "幽門螺旋桿菌被世界衛生組織列為第一級致癌因子，會大幅增加罹患胃癌的機率。衛生福利部已全面提供45至74歲民眾，終身一次公費糞便抗原檢測，呼籲民眾及早篩檢與治療，保護胃部健康。",
    "reason": "推廣政府免費公費篩檢政策，有助於降低市民罹癌風險。",
    "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=200C49A6CF0B77E8",
    "DataSN": "9567553",
    "image_url": "https://www-ws.gov.taipei/001/Upload/446/relpic/10162/9567553/e6775863-2601-48c4-80ff-aa1e1ec121fa.png",
    "is_ai_generated": True
  },
  {
    "title": "擺脫憂鬱與焦慮雙重困擾 松德院區提供腦刺激個人化醫療",
    "script": "面對重度憂鬱合併焦慮的雙重困擾，北市聯醫松德院區成立腦刺激治療中心滿一週年。中心引進深部經顱磁刺激儀器，為藥物治療反應有限的患者，提供安全且個人化的非侵入性治療新選擇。",
    "reason": "介紹新式精神醫療資源，幫助受憂鬱與焦慮困擾的市民找到新療法。",
    "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=9063473DDEE07264",
    "DataSN": "9567559",
    "image_url": "https://www-ws.gov.taipei/001/Upload/446/relpic/10162/9567559/20f240ba-0517-4b9f-b239-0e45fe2ffa33.jpg",
    "is_ai_generated": True
  },
  {
    "title": "丹頂鶴育雛 經過路過請安靜來欣賞",
    "script": "台北市立動物園傳來好消息！睽違四年，丹頂鶴KIKA與BIG再次成功孵育出可愛的鶴寶寶。園方特別提醒民眾，參觀時請保持安靜，避免驚嚇到親鳥與雛鶴，最佳觀賞地點就在兩棲爬蟲動物館廊道。",
    "reason": "動物園溫馨趣味的新聞，適合調劑嚴肅市政新聞，增添生活感。",
    "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=CB8E81E9D9F013D0",
    "DataSN": "9567454",
    "image_url": "https://www-ws.gov.taipei/001/Upload/432/relpic/10162/9567454/af9762ff-64bd-4880-8212-c4321b0d3005.jpg",
    "is_ai_generated": True
  },
  {
    "title": "25公尺綠巨人 掌葉蘋婆化身新生公園大遮陽傘",
    "script": "新生公園迎來春日新風景，高達25公尺的「綠巨人」掌葉蘋婆正值花期。雖然花朵會散發特殊氣味吸引昆蟲傳粉，但其挺拔的樹幹與繁盛枝葉，是夏日乘涼的最佳天然遮陽傘，歡迎市民前往探索自然生態。",
    "reason": "推廣北市公園生態之美，鼓勵市民走向戶外感受自然。",
    "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=8B0B9C3057332935",
    "DataSN": "9567073",
    "image_url": "https://www-ws.gov.taipei/001/Upload/348/relpic/10162/9567073/d2ed1cb5-0274-4ba4-9478-340b470f1735.jpg",
    "is_ai_generated": True
  }
]

with open('/home/benliangcs/tw-gov-video/output/selected_articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
