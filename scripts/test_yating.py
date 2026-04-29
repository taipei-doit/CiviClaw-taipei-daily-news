import urllib.request
import json
import base64
from pathlib import Path

API_KEY = "71afdec1fd12522431c71be2e4eab45569cf441e"
URL = "https://api.yating.tw/tts/v3/audios/synthesize-sync"

payload = {
    "input": {
        "text": "臺北市立動物園的黑天鵝夫婦今年終於迎來了健康的寶寶！為了避免鳥蛋被其他動物破壞，保育員特別使出「偷天換蛋」的妙計，將真蛋護送到人工孵化室。現在可愛的黑天鵝寶寶已經順利回到父母身邊，大家到雨林區參觀時，記得輕聲細語，不要驚擾到這溫馨的一家喔！",
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
        
        b64_audio = res.get('audioContent', '')
        if b64_audio:
            out_file = Path.home() / "tw-gov-video" / "output" / "yating_test_female2.mp3"
            with open(out_file, "wb") as f:
                f.write(base64.b64decode(b64_audio))
            print(f"Success! Saved to {out_file}")
        else:
            print("Failed to get audioContent from successful request:")
            print(json.dumps(res, indent=2))
            
except Exception as e:
    print(f"Error: {e}")
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
