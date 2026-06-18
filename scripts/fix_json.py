import json
from pathlib import Path

from config import INPUT_JSON

fixed_items = [
    {
      "title": "搶攻高薪職缺！北市企業徵才開跑　40K起跳、高薪上看70K",
      "script": "準備換跑道的朋友們注意了！臺北市政府就業服務處本週舉辦多家企業聯合徵才活動，釋出大量高薪職缺。其中多數職缺起薪達4萬元以上，更有知名企業開出上看7萬元的高薪，歡迎有意求職的民眾踴躍參與，把握挑戰高薪的機會。",
      "reason": "就業市場與高薪職缺與民眾生計息息相關，屬於高關注度的民生經濟新聞。",
      "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=E0BEAA8946777BB7",
      "DataSN": "9562097",
      "is_ai_generated": False,
      "image_url": "https://www-ws.gov.taipei/001/Upload/307/relpic/10162/9562097/bd21bda6-c993-40ca-8581-e8e0b2520a63.jpg"
    },
    {
      "title": "唱頌城市螢火蟲奇蹟 大安森林公園音樂會閃亮登場",
      "script": "臺北市的夜晚越來越浪漫！大安森林公園年度盛事「螢火蟲季」正式起跑，同時舉辦「唱頌城市螢火蟲奇蹟」星空音樂會。民眾不僅能欣賞精彩的音樂演出，還能在市中心體驗賞螢樂趣，感受臺北市生態復育的豐碩成果。",
      "reason": "大型生態展演與戶外音樂會，非常適合家庭週末休閒，具極高軟性新聞價值。",
      "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=9DBD944C3CF2192A",
      "DataSN": "9559745",
      "is_ai_generated": False,
      "image_url": "https://www-ws.gov.taipei/001/Upload/348/relpic/10162/9559745/f079f64d-33cd-428f-9d6b-5971c92fa38c.jpg"
    },
    {
      "title": "七旬婦巷內體力不支迷途 暖警靠「這條手環」助姊妹團圓",
      "script": "大同區發生一起感人的尋人故事！一名七旬老婦人因體力不支迷失在巷弄內，所幸路過熱心民眾報案。警方到場後，眼尖發現老婦人手上配戴有防走失手環，成功透過系統聯繫上家屬，讓老婦人平安返家，結束這場驚魂記。",
      "reason": "溫馨社會案件，並能有效宣導「防走失手環」的社會安全網機制。",
      "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=FAD67FACF4357CF4",
      "DataSN": "9562379",
      "is_ai_generated": False,
      "image_url": "https://www-ws.gov.taipei/001/Upload/502/relpic/10162/9562379/ddaf8a65-314d-4639-8a47-6b7959ce2157.jpg"
    },
    {
      "title": "北市FRC機器人團隊國際競賽再創佳績  建中勇奪「卓越影響力獎」，晉級美國休士頓世界總決賽",
      "script": "臺北市科技教育在國際發光發熱！建國中學FRC機器人團隊代表臺灣出國征戰，成功勇奪大會最高榮譽「卓越影響力獎」，並順利晉級美國休士頓的世界總決賽。這項成就再次證明臺灣學子在STEM領域的頂尖實力！",
      "reason": "展現臺北市科技教育卓越成果與學生榮耀，是激勵人心的正面教育新聞。",
      "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=65549A086FF0780C",
      "DataSN": "9562377",
      "is_ai_generated": False,
      "image_url": "https://www-ws.gov.taipei/001/Upload/342/relpic/10162/9562377/114829f8-df58-4a52-b560-e1e0092af7c0.jpg"
    },
    {
      "title": "國際寵物日「狗狗春遊趣」登場　蔣萬安：打造毛孩BMW友善環境",
      "script": "響應國際寵物日，臺北市長蔣萬安親自出席「狗狗春遊趣」活動，與市民及毛小孩同樂。市長強調，臺北市正全力推動寵物友善空間，目標是為毛小孩打造包含搭乘捷運、公車與步行空間在內的「BMW友善交通環境」。",
      "reason": "寵物友善政策受大量市民關注，且活動具備極高的節日應景性質。",
      "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=83AB70898A28E353",
      "DataSN": "9562376",
      "is_ai_generated": False,
      "image_url": "https://www-ws.gov.taipei/001/Upload/297/relpic/10162/9562376/e31e6923-bf34-41bc-8edd-72a26bbfae50.jpg"
    }
]

INPUT_JSON.write_text(json.dumps({"selected": fixed_items}, ensure_ascii=False, indent=2), encoding="utf-8")
