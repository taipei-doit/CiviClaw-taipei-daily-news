import json
import os

input_file = os.path.expanduser('~/tw-gov-video/output/selected_articles.json')

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

scripts = {
    "9564514": {
        "script": "台北市長蔣萬安親自主持捷運東環段開工典禮，這項工程將大幅改善內湖交通。未來完工後，從內科到士林只需短短11分鐘，大幅節省通勤時間，為市民帶來更便利的生活。",
        "reason": "捷運建設直接關乎市民通勤，這項重大工程將有效紓解內湖交通瓶頸，具備高度民生價值。"
    },
    "9565573": {
        "script": "北投人的母親之河「磺港溪」終於迎來重生！台北市政府推動的再造工程正式竣工，不僅改善了水質與防洪能力，更結合周邊環境打造出美麗的親水綠帶，讓市民多了一個休閒好去處。",
        "reason": "治水工程與親水空間營造是城市永續發展的重要指標，磺港溪的重生展現了市府對在地環境改善的用心。"
    },
    "9565533": {
        "script": "關心教育發展！台北市長蔣萬安接連出席內湖高工與泰北高中的校慶活動，強調市府將持續投入資源，因為投資年輕世代，就是為台北的未來打下最堅實的基礎。",
        "reason": "市長親自參與學校校慶，表達市府對教育及年輕世代的重視，能引起教育圈與家長的共鳴。"
    },
    "9565480": {
        "script": "響應世界地球日，台北市環境教育中心推出四大亮點活動，邀請市民朋友一起身體力行！透過多元的體驗與學習，將淨零減碳的觀念落實到日常生活中，共同守護我們的地球。",
        "reason": "配合世界地球日，環保議題具備時效性與教育意義，鼓勵市民參與淨零減碳行動。"
    },
    "9565151": {
        "script": "為了打造更安全的學習環境，松山分局與在地教育機關攜手合作，建立多重防護網。透過加強校園周邊巡邏與安全宣導，全面提升校園安全機制，讓家長更放心。",
        "reason": "校園安全是家長最關心的議題，警方與教育單位的合作能有效安定民心，展現市府對孩童安全的保護。"
    }
}

formatted_data = []
for item in data:
    sn = str(item.get("DataSN", ""))
    s_data = scripts.get(sn, {"script": "預設文稿", "reason": "預設原因"})
    
    image_url = ""
    if item.get("相關圖片") and len(item["相關圖片"]) > 0:
        image_url = item["相關圖片"][0].get("url", "")
        
    formatted_item = {
        "title": item.get("title", ""),
        "script": s_data["script"],
        "reason": s_data["reason"],
        "source_url": item.get("Source", "") or item.get("Link", ""),
        "DataSN": sn,
        "image_url": image_url,
        "is_ai_generated": True
    }
    formatted_data.append(formatted_item)

with open(input_file, 'w', encoding='utf-8') as f:
    json.dump(formatted_data, f, ensure_ascii=False, indent=2)

print("Formatting complete.")
