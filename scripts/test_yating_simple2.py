import urllib.request
import json
import base64

API_KEY = "71afdec1fd12522431c71be2e4eab45569cf441e"
URL = "https://tts.api.yating.tw/v3/speeches/synchronize"

payload = {
    "input": {
        "text": "歡迎收看今天的每日新聞！為您帶來台北市最新市政摘要。",
        "type": "text"
    },
    "voice": {
        "model": "female_2",
        "lang": "zh_tw"
    },
    "audioConfig": {
        "encoding": "MP3"
    }
}

req = urllib.request.Request(URL, data=json.dumps(payload).encode('utf-8'), method="POST")
req.add_header("key", API_KEY)
req.add_header("Content-Type", "application/json")

try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        print(f"Type of audioFile: {type(res.get('audioFile'))}")
        if isinstance(res.get('audioFile'), str):
            print(f"Length of base64 string: {len(res['audioFile'])}")
            with open("/home/benliangcs/tw-gov-video/output/test_direct.mp3", "wb") as f:
                f.write(base64.b64decode(res['audioFile']))
            print("Successfully decoded and saved mp3")
except Exception as e:
    print(f"Error: {e}")
