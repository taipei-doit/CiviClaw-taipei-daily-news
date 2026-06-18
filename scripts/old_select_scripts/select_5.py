import json

articles = [
    {
        "DataSN": "9568624",
        "title": "玉成國小80校慶 蔣萬安：三代同堂共寫歷史",
        "script": "臺北市長蔣萬安出席玉成國小80週年校慶，表揚跨世代校友的傳承。他並宣布今年9月起北市中小學營養午餐全面免費，持續投資教育的未來。",
        "reason": "慶祝在地名校校慶與重大教育政策宣示，具備地方與市政雙重意義。",
        "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=37F98391B08B8E41",
        "image_url": "https://www-ws.gov.taipei/001/Upload/297/relpic/10162/9568624/8807ca13-168a-4a98-ad08-aa3fe4be4320.jpg",
        "is_ai_generated": True
    },
    {
        "DataSN": "9568586",
        "title": "私立靜心高中-2026 ACT夢想家國際論壇",
        "script": "靜心高中主辦的國際論壇邀請多國學生代表，針對全球永續發展指標提出行動方案。透過跨國交流，培養學子面對未來社會所需的溝通與解決能力。",
        "reason": "展現臺北市學子對永續發展的參與及國際教育交流成果。",
        "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=24E365B4875781F0",
        "image_url": "https://www-ws.gov.taipei/001/Upload/342/relpic/10162/9568586/9a0ecaab-2aed-4afb-a2f1-49b1f0fa3271.jpg",
        "is_ai_generated": True
    },
    {
        "DataSN": "9568584",
        "title": "立農國小啟動SDGs氣候行動 培育未來公民",
        "script": "立農國小配合世界閱讀日，舉辦雙語氣候行動闖關活動。學童不僅親手測量樹木碳匯，還透過實踐計畫為地球種下數十棵樹。",
        "reason": "以具體行動響應世界地球日，適合鼓勵市民關心環境議題。",
        "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=481C2C93900A7E88",
        "image_url": "https://www-ws.gov.taipei/001/Upload/342/relpic/10162/9568584/b0f3f244-3152-41ff-a509-405036fd4cc7.jpg",
        "is_ai_generated": True
    },
    {
        "DataSN": "9568582",
        "title": "陽明山國小與富安國小山海聯手重現藍染技法",
        "script": "陽明山國小與富安國小進行山海交流，學生親身體驗大菁採摘與藍染工藝。課程結合生態觀察與地方創生，實現知識走出書本的教育願景。",
        "reason": "突顯在地文化與自然生態結合的創新教育體驗。",
        "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=5C4527D889F931A3",
        "image_url": "https://www-ws.gov.taipei/001/Upload/342/relpic/10162/9568582/c5e55111-c686-4929-923a-52cb05c7fc10.jpg",
        "is_ai_generated": True
    },
    {
        "DataSN": "9568563",
        "title": "貓空纜車纜索裁剪作業完成 4月25日恢復營運",
        "script": "為維持行車安全，貓空纜車經過數日的鋼纜裁剪與重編作業，已順利完工。系統將於25日全面恢復營運，邀請民眾再次搭乘享受山林美景。",
        "reason": "市民與觀光客關心的重要交通設施營運資訊更新。",
        "source_url": "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=5C4527D889F931A3",
        "image_url": "https://www-ws.gov.taipei/001/Upload/405/relpic/10162/9568563/d5c058a6-f508-4637-8a1b-3c7de2cc2b56.jpg",
        "is_ai_generated": True
    }
]

with open('/home/benliangcs/tw-gov-video/output/selected_articles.json', 'w', encoding='utf-8') as f:
    json.dump({"selected": articles}, f, ensure_ascii=False, indent=2)

print("Selected JSON created.")