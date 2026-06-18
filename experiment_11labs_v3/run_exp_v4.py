import os
import json
import urllib.request
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

WORK_DIR = Path.home() / "tw-gov-video" / "experiment_11labs_v3"
IMAGE_PATH = "/home/benliangcs/.openclaw/media/inbound/84fd2a38-b495-47b4-938d-92671b39a55b.png"
API_KEY = "sk_dab768322eb97d8789551989fba23b6ce5ddbdf3e85d847e"
VOICE_ID = "4mU4AFOhdaBEWGnnBxL8"

def generate_tts(text, filename):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method="POST")
    out_path = WORK_DIR / filename
    try:
        with urllib.request.urlopen(req) as response:
            with open(out_path, "wb") as f:
                f.write(response.read())
        return out_path
    except Exception as e:
        print(f"TTS Error for {filename}:", e)
        return None

def create_html(lang, data):
    font_family = "'Noto Sans TC', sans-serif" if lang == "en" else "'Noto Sans JP', sans-serif"
    
    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1920, height=1080, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Noto+Sans+TC:wght@400;700;900&family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body, html {{
            margin: 0; padding: 0; width: 1920px; height: 1080px;
            background-color: #f8f9fa;
            background-image: radial-gradient(#bdc3c7 2px, transparent 2px);
            background-size: 40px 40px;
            font-family: {font_family};
            overflow: hidden; color: #2c3e50; position: relative;
        }}
        .bg-circle {{
            position: absolute; border-radius: 50%;
            background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
            opacity: 0.6; z-index: -1;
        }}
        .bg-c1 {{ width: 800px; height: 800px; top: -200px; right: -200px; }}
        .bg-c2 {{ width: 600px; height: 600px; bottom: -150px; left: -100px; }}
        .slide {{
            width: 1920px; height: 1080px; position: absolute; top: 0; left: 0;
            display: none; flex-direction: column; align-items: center; justify-content: center;
            padding: 80px; box-sizing: border-box; opacity: 1; 
        }}
        .slide.active {{ display: flex; }}
        
        /* Intro Slide */
        .title-slide h1 {{
            font-family: 'Dela Gothic One', sans-serif;
            font-size: 200px; font-weight: normal; color: #2c3e50; margin: 0;
            text-shadow: 6px 6px 0px rgba(52, 152, 219, 0.2);
            text-align: center;
        }}
        .title-slide .badge {{
            background: #2c3e50; color: white; padding: 15px 40px; border-radius: 5px;
            font-size: 36px; font-weight: bold; margin-bottom: 40px; letter-spacing: 2px; text-transform: uppercase;
        }}

        /* Content Slide */
        .content-box {{
            background: white; border-radius: 20px; padding: 60px 80px;
            width: 90%; height: 85%; box-shadow: 0 25px 60px rgba(0,0,0,0.08);
            display: flex; flex-direction: column; position: relative; z-index: 10;
        }}
        .slide-title {{
            font-weight: 900; font-size: 65px; color: #2980b9; margin: 0 0 40px 0;
            line-height: 1.3; border-bottom: 4px solid #f1c40f; padding-bottom: 20px;
        }}
        .layout-split {{ display: flex; flex: 1; gap: 60px; height: calc(100% - 150px); }}
        .text-column {{ flex: 1.2; display: flex; flex-direction: column; justify-content: center; }}
        .image-column {{
            flex: 1; display: flex; justify-content: center; align-items: center;
            border-radius: 15px; overflow: hidden; position: relative;
            background: #ecf0f1; box-shadow: inset 0 0 20px rgba(0,0,0,0.05);
        }}
        .content-img {{ width: 100%; height: 100%; object-fit: cover; border-radius: 15px; border: 3px solid rgba(189, 195, 199, 0.4); box-sizing: border-box; }}
        .label {{
            font-weight: 900; color: #e74c3c; font-size: 30px; margin-bottom: 15px;
            display: inline-block; border-left: 8px solid #e74c3c; padding-left: 15px;
            text-transform: uppercase; letter-spacing: 1px;
        }}
        .script-text {{ font-size: 45px; line-height: 1.6; color: #34495e; margin: 0; font-weight: 700; }}

        /* Outro Slide */
        .outro-slide h1 {{ font-weight: 900; font-size: 140px; color: #2c3e50; margin: 0 0 30px 0; text-align: center; }}
        .outro-slide h2 {{ color: #e74c3c; font-size: 70px; margin:0; text-align: center; }}
    </style>
</head>
<body>
    <div class="bg-circle bg-c1"></div>
    <div class="bg-circle bg-c2"></div>

    <div id="slide_intro" class="slide title-slide">
        <div class="badge">FOCUS NEWS</div>
        <h1>{data['intro']['title']}</h1>
    </div>

    <div id="slide_content" class="slide">
        <div class="content-box">
            <h2 class="slide-title">{data['content']['title']}</h2>
            <div class="layout-split">
                <div class="text-column">
                    <div class="label">NEWS UPDATE</div>
                    <p class="script-text">{data['content']['script']}</p>
                </div>
                <div class="image-column">
                    <img src="file://{IMAGE_PATH}" class="content-img">
                </div>
            </div>
        </div>
    </div>

    <div id="slide_outro" class="slide outro-slide">
        <h1>{data['outro']['title']}</h1>
        <h2>{data['outro']['script']}</h2>
    </div>

    <script>
        function showSlide(slideId) {{
            document.querySelectorAll('.slide').forEach(el => el.classList.remove('active'));
            document.getElementById(slideId).classList.add('active');
        }}
    </script>
</body>
</html>
"""
    out_html = WORK_DIR / f"slides_{lang}.html"
    out_html.write_text(html, encoding="utf-8")
    return out_html

def make_clip(img_path, audio_path, out_path):
    cmd = f"ffmpeg -y -loop 1 -i {img_path} -i {audio_path} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest {out_path}"
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    content = {
        "en": {
            "intro": {"title": "Taipei City News", "tts": "Taipei City News."},
            "content": {"title": "Taipei & Fukuoka Pact", "script": "Mayor Chiang and Fukuoka Mayor Takashima signed a friendship pact today, promising closer cooperation.", "tts": "Mayor Chiang and Fukuoka Mayor Takashima signed a friendship pact today, promising closer cooperation."},
            "outro": {"title": "Thank You", "script": "Please subscribe and share!", "tts": "Thanks for watching!"}
        },
        "ja": {
            "intro": {"title": "台北市政ニュース", "tts": "台北市政ニュース。"},
            "content": {"title": "台北市と福岡市が協定締結", "script": "蒋万安市長と高島福岡市長は本日、友好交流協定に署名し、協力関係を深めました。", "tts": "蒋万安市長と高島福岡市長は本日、友好交流協定に署名し、協力関係を深めました。"},
            "outro": {"title": "おわり", "script": "ご視聴ありがとうございました", "tts": "ご視聴ありがとうございました。"}
        }
    }

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        for lang, sections in content.items():
            print(f"Processing {lang}...")
            html_path = create_html(lang, sections)
            page.goto(f"file://{html_path}")
            page.wait_for_timeout(1000)
            
            clips = []
            for slide_type in ["intro", "content", "outro"]:
                audio_path = generate_tts(sections[slide_type]["tts"], f"v4_audio_{slide_type}_{lang}.mp3")
                page.evaluate(f"showSlide('slide_{slide_type}')")
                page.wait_for_timeout(200)
                img_path = WORK_DIR / f"v4_frame_{slide_type}_{lang}.png"
                page.screenshot(path=str(img_path))
                
                clip_path = WORK_DIR / f"v4_clip_{slide_type}_{lang}.mp4"
                make_clip(img_path, audio_path, clip_path)
                clips.append(f"file '{clip_path.name}'")
                
            concat_file = WORK_DIR / f"v4_concat_{lang}.txt"
            concat_file.write_text("\n".join(clips))
            
            final_video = WORK_DIR / f"final_v4_{lang}.mp4"
            concat_cmd = f"cd {WORK_DIR} && ffmpeg -y -f concat -safe 0 -i {concat_file.name} -c copy {final_video.name}"
            subprocess.run(concat_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            print(f"Generated {final_video}")

        browser.close()

if __name__ == "__main__":
    main()
