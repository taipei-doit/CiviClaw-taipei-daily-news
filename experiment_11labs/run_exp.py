import os
import json
import urllib.request
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

WORK_DIR = Path.home() / "tw-gov-video" / "experiment_11labs"
IMAGE_PATH = "/home/benliangcs/.openclaw/media/inbound/84fd2a38-b495-47b4-938d-92671b39a55b.png"
API_KEY = "sk_dab768322eb97d8789551989fba23b6ce5ddbdf3e85d847e"
VOICE_ID = "4mU4AFOhdaBEWGnnBxL8"

def generate_tts(text, lang):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY
    }
    data = {
        "text": text,
        # Trying eleven_multilingual_v2 as the reliable multilingual model. 
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method="POST")
    out_path = WORK_DIR / f"audio_{lang}.mp3"
    try:
        with urllib.request.urlopen(req) as response:
            with open(out_path, "wb") as f:
                f.write(response.read())
        return out_path
    except Exception as e:
        print(f"TTS Error for {lang}:", e)
        if hasattr(e, 'read'):
            print(e.read().decode())
        return None

def create_html(title, script, lang):
    html = f"""<!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
            body {{ width: 1920px; height: 1080px; margin: 0; font-family: 'Noto Sans TC', sans-serif; background: #f0f4f8; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
            .card {{ background: white; padding: 60px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); display: flex; width: 85%; height: 75%; gap: 50px; }}
            .text-col {{ flex: 1.2; display: flex; flex-direction: column; justify-content: center; }}
            h1 {{ font-size: 65px; color: #2c3e50; border-bottom: 5px solid #3498db; padding-bottom: 20px; line-height: 1.3; }}
            p {{ font-size: 45px; color: #34495e; line-height: 1.6; }}
            .img-col {{ flex: 1; display: flex; align-items: center; justify-content: center; }}
            img {{ max-width: 100%; max-height: 100%; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); object-fit: cover; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="text-col">
                <h1>{title}</h1>
                <p>{script}</p>
            </div>
            <div class="img-col">
                <img src="file://{IMAGE_PATH}">
            </div>
        </div>
    </body>
    </html>
    """
    out_html = WORK_DIR / f"slide_{lang}.html"
    out_html.write_text(html, encoding="utf-8")
    return out_html

def main():
    content = {
        "en": {
            "title": "Taipei & Fukuoka Sign Friendship Pact",
            "script": "Taipei Mayor Chiang Wan-an and Fukuoka Mayor Soichiro Takashima officially signed a friendship agreement today, deepening ties and promising closer cooperation between our two great cities."
        },
        "ja": {
            "title": "台北市と福岡市が友好協定を締結",
            "script": "蒋万安（しょう・ばんあん）台北市長と高島宗一郎（たかしま・そういちろう）福岡市長は本日、友好交流協定に署名しました。両都市の絆を深め、今後の更なる協力を約束しました。"
        }
    }

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        for lang, data in content.items():
            print(f"Processing {lang}...")
            audio_path = generate_tts(data["script"], lang)
            html_path = create_html(data["title"], data["script"], lang)
            
            page.goto(f"file://{html_path}")
            # wait a bit for font loading
            page.wait_for_timeout(1000)
            img_path = WORK_DIR / f"frame_{lang}.png"
            page.screenshot(path=str(img_path))
            
            video_path = WORK_DIR / f"video_{lang}.mp4"
            
            # Render video with ffmpeg
            cmd = f"ffmpeg -y -loop 1 -i {img_path} -i {audio_path} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest {video_path}"
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Generated {video_path}")
            
        browser.close()

if __name__ == "__main__":
    main()
