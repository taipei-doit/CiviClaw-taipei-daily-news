import json

data = {
  "selected": [
    {
      "title": "搶進職場黃金檔！北市28企業釋出千職缺 餐飲、長照職位最吸睛",
      "script": "臺北市就業服務處將於4月28日至30日舉辦現場徵才，邀集28家企業釋出超過1000個職缺。不僅有知名餐飲品牌開出高薪，長照與醫療領域也積極招募人才，想轉職或求職的民眾千萬別錯過。",
      "reason": "提供市民最新的就業資訊與高薪職缺機會，與大眾民生息息相關。",
      "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=6971A04C80679837",
      "DataSN": "9568382",
      "image_url": "https://www-ws.gov.taipei/001/Upload/307/relpic/10162/9568382/11b85826-9932-44b4-9aba-2ce58e3eeedb.jpg",
      "is_ai_generated": True
    },
    {
      "title": "捷運線上看見龍貓森林 石牌、唭哩岸站公園故事多",
      "script": "紅線捷運高架橋下的線型公園不僅有綠意盎然的「龍貓森林」，還隱藏著「石牌漢番界碑」與打石場等歷史遺跡。週末假日不妨搭捷運來趟城市探索，感受自然與歷史交會的獨特魅力。",
      "reason": "推廣臺北市內結合綠意與歷史的特色景點，適合市民假日休憩。",
      "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=0B249992C7740CB8",
      "DataSN": "9567074",
      "image_url": "https://www-ws.gov.taipei/001/Upload/348/relpic/10162/9567074/16d1161f-9acd-4d89-8207-cd99949fa844.jpg",
      "is_ai_generated": True
    },
    {
      "title": "《源源不絕！2026嘻哈大賞》現場決賽 學子用創作傳遞愛",
      "script": "第三屆「源源不絕！嘻哈大賞」決賽於自來水園區熱烈展開，全國超過百組青年學子參賽展現創意。最終由武陵、桃園等四校學生組成的團隊奪下最佳現場演出獎，為嘻哈盛事劃下完美句點。",
      "reason": "展現臺北市支持青年藝文創作與次文化的努力，活動充滿青春活力。",
      "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=AB6BC62F75D7E694",
      "DataSN": "9568648",
      "image_url": "https://www-ws.gov.taipei/001/Upload/306/relpic/10162/9568648/08a621c8-49b8-458c-afb5-a0bf442de580.jpg",
      "is_ai_generated": True
    },
    {
      "title": "2026文山茶筍節 蔣萬安：「臺北迎尪公」正式登錄無形文化資產",
      "script": "結合二百多年歷史的「尪公巡田園」文化，2026文山茶筍節盛大登場。市長蔣萬安親自出席扛鑾轎祈福，並宣布「臺北迎尪公」正式登錄為臺北市無形文化資產，期盼優質茶筍產業與傳統文化永續傳承。",
      "reason": "宣傳臺北市重要的無形文化資產與在地特色農產節慶，具文化傳承意義。",
      "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=257C58383403C5B1",
      "DataSN": "9568640",
      "image_url": "https://www-ws.gov.taipei/001/Upload/297/relpic/10162/9568640/c91a0a66-804c-4a7b-b49f-f57b26f2ad3a.jpg",
      "is_ai_generated": True
    },
    {
      "title": "夢想臺北 兒童造市！2026臺北兒童月主活動盛大登場",
      "script": "2026臺北兒童月主活動於信義區香堤大道與國父紀念館周邊登場，現場設置32個科技探險攤位與大型工程車展示。讓孩子們打破課室框架，在遊戲與實作中體驗城市運作，盡情探索與追夢。",
      "reason": "報導臺北市重大親子活動，鼓勵兒童自主學習與體驗城市發展。",
      "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=176406E2F7F2E7F5",
      "DataSN": "9568643",
      "image_url": "https://www-ws.gov.taipei/001/Upload/342/relpic/10162/9568643/306caf06-c4c8-4e81-858a-238d919ac2d4.jpg",
      "is_ai_generated": True
    }
  ]
}

with open('/home/benliangcs/tw-gov-video/output/selected_articles.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved selected_articles.json")
