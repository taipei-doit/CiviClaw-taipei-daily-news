import requests

webhook_url = "https://discord.com/api/webhooks/1489170065638035509/zC-HrxYHUdOwIjvhDrusT0I6HmQkF6kTyHsmew7cmPLSIesOgJ9ORvsSlF-s5pz0IZJ6"

files = {}
from config import OUTPUT_DIR
for i in range(5):
    files[f"file{i}"] = open(OUTPUT_DIR / f"test_ai_img_{i}.png", "rb")

content = (
    "Here are 5 purely AI-generated images for real articles that had no official photos, generated safely without touching the main pipeline:\\n\\n"
    "**1. 臺北市衛生局公布115年第1季生鮮禽畜肉品(含蛋)抽驗結果均符合規定**\\n*Gemini Extracted Subject:* `Assorted raw meats and eggs`\\n\\n"
    "**2. 老翁騎鐵馬騎到腳麻  暖警協助護送返家**\\n*Gemini Extracted Subject:* `Empty bicycle on path`\\n\\n"
    "**3. 臺北市俞振華副秘書長率團訪問矽谷 攜手NVIDIA擘劃北士科「AI 創新中心」願景**\\n*Gemini Extracted Subject:* `Computer circuit board`\\n\\n"
    "**4. 淨山健行活動暨防災宣導園遊會**\\n*Gemini Extracted Subject:* `Mountain forest path`\\n\\n"
    "**5. 赴市議會接受施政報告質詢 蔣萬安：感謝議會支持市民有感政策 持續讓臺北更貼近市民需求**\\n*Gemini Extracted Subject:* `Modern urban architecture`"
)

payload = {"payload_json": '{"content": "' + content + '"}'}

try:
    requests.post(webhook_url, data=payload, files=files)
    print("Sent.")
except Exception as e:
    print(e)
