import json

articles = [
  {
    "title": "臺北市接軌國際！STEAM矽谷見學團拓展全球視野，學子跨海探索科技脈動與永續未來",
    "script": "臺北市政府教育局為推動STEAM教育並拓展學生國際視野，特別遴選16位高中生前往美國矽谷進行交流。這次的見學行程不僅讓學子入班體驗，更親身探索全球科技脈動與永續未來，為培育具備全球移動力的人才奠定基礎。",
    "reason": "展現臺北市在教育與國際接軌的努力，對市民及學生家長具吸引力。",
    "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=7C3F321D8466FE3D",
    "DataSN": "9567429",
    "image_url": "",
    "is_ai_generated": True
  },
  {
    "title": "多元資源打造中小企業永續競爭力 北市府「永續臺北好企機」申請開跑！",
    "script": "北市府產業發展局針對中小企業推出「永續臺北好企機」ESG輔導計畫，即日起開放申請。計畫將招募並提供一對一深度顧問輔導，協助企業因應永續轉型趨勢，打造專屬的綠色競爭力。",
    "reason": "與市民及在地企業經濟發展息息相關的重要市政補助計畫。",
    "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=B25ADEC4C10A4CF4",
    "DataSN": "9567196",
    "image_url": "",
    "is_ai_generated": True
  },
  {
    "title": "大安警銀聯防奏效　成功攔阻詐騙48萬元",
    "script": "大安分局警方與金融機構聯手合作，成功攔阻一名差點遭詐騙新臺幣48萬元的婦人。警方耐心勸說並戳破詐騙集團的謊言，再次呼籲民眾提高警覺，防範交友詐騙陷阱。",
    "reason": "防詐騙宣導為重要社會議題，能有效提醒市民注意財產安全。",
    "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=95604E5A19E47C1D",
    "DataSN": "9567389",
    "image_url": "",
    "is_ai_generated": True
  },
  {
    "title": "七旬翁獨自上山散步跌倒受傷   文山暖警即刻救援護送就醫",
    "script": "一名七旬老翁獨自在文山區山區散步時不慎跌倒受傷，所幸警方接獲通報後即刻趕赴現場救援。員警不僅將老翁攙扶至安全處，更以警車護送就醫並聯繫家屬，展現了警方暖心為民服務的一面。",
    "reason": "溫馨的地方社會新聞，同時也能提醒長者外出注意安全。",
    "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=B892F3E54A16ABCB",
    "DataSN": "9567373",
    "image_url": "",
    "is_ai_generated": True
  },
  {
    "title": "「115年度臺北市原住民族事業體扶植計畫」獎勵金50萬元  北市原民會即日起開放徵件",
    "script": "臺北市政府原民會「115年原住民族事業體扶植計畫」即日起開放報名，最高將發放50萬元獎勵金。計畫提供業師輔導、創業培力與資源媒合，協助原住民族青年打造具文化價值的永續創業品牌。",
    "reason": "鼓勵青年與原住民創業的補助計畫，是具實用價值的市政資訊。",
    "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=A37E3283F5B1CAE1",
    "DataSN": "9567274",
    "image_url": "",
    "is_ai_generated": True
  }
]

with open('output/selected_articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
