import urllib.request
import json
import base64
import time
import subprocess
from pathlib import Path

API_KEY = "71afdec1fd12522431c71be2e4eab45569cf441e"
URL = "https://tts.api.yating.tw/v3/speeches/synchronize"

BASE = Path.home() / "tw-gov-video"
OUTPUT_DIR = BASE / "output"
INPUT_JSON = OUTPUT_DIR / "selected_articles.json"

def synthesize_text_yating(text, out_file):
    payload = {
        "input": {
            "text": text,
            "type": "text"
        },
        "voice": {
            "model": "female_2",
            "lang": "zh_tw"
        },
        "audioConfig": {
            "encoding": "MP3",
            "maxLength": 600000,
            "uploadFile": False
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
                with open(out_file, "wb") as f:
                    f.write(base64.b64decode(b64_audio))
                print(f"Success! Saved to {out_file} directly from audioContent.")
                return True
                
            print(f"Response did not have audioContent. Keys: {list(res.keys())}")
            
            if 'audioFile' in res and 'url' in res['audioFile'] and res['audioFile']['url']:
                audio_url = res['audioFile']['url']
                print(f"Downloading from audioFile URL...")
                time.sleep(2) # Give S3 a moment
                with urllib.request.urlopen(audio_url) as audio_res:
                    with open(out_file, "wb") as f:
                        f.write(audio_res.read())
                print(f"Success! Downloaded and saved to {out_file}")
                return True
            else:
                print(f"Raw Response JSON: {json.dumps(res, indent=2)}")
                return False
                
    except Exception as e:
        print(f"Error synthesizing text: {e}")
        if hasattr(e, 'read'):
            print(e.read().decode('utf-8'))
        return False

def main():
    if not INPUT_JSON.exists():
        print("Missing input file:", INPUT_JSON)
        return

    data = json.loads(INPUT_JSON.read_text(encoding="utf-8"))
    items = data.get("selected", [])

    print("Generating Intro...")
    intro_text = "歡迎收看今天的每日新聞！為您帶來台北市最新市政摘要。"
    synthesize_text_yating(intro_text, OUTPUT_DIR / "voice_intro.mp3")
    
    print("Generating Headlines...")
    headlines_text = "帶您快速瀏覽今天的五大重點新聞。"
    synthesize_text_yating(headlines_text, OUTPUT_DIR / "voice_headlines.mp3")
    
    for idx, item in enumerate(items):
        print(f"Generating Article {idx}...")
        text = (item.get("script") or "").strip()
        if not text: continue
        synthesize_text_yating(text, OUTPUT_DIR / f"voice_{idx}.mp3")
        
    print("Generating Outro...")
    outro_text = "以上是今天的每日新聞。感謝您的收看！如果您喜歡我們的頻道，請記得按讚、訂閱並分享，我們下次見！"
    synthesize_text_yating(outro_text, OUTPUT_DIR / "voice_outro.mp3")

if __name__ == "__main__":
    main()
