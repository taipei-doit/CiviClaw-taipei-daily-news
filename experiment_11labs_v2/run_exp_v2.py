import os
import json
import urllib.request
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

WORK_DIR = Path.home() / "tw-gov-video" / "experiment_11labs_v2"
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

def create_html(slide_type, data, lang):
    css = """
    <style>
        body { width: 1920px; height: 1080px; margin: 0; font-family: 'Noto Sans TC', sans-serif; 
               background: radial-gradient(circle, #fdfbfb 0%, #ebedee 100%); 
               display: flex; align-items: center; justify-content: center; overflow: hidden; }
        .bg-shape-1 { position: absolute; width: 800px; height: 800px; border-radius: 50%; background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%); opacity: 0.6; top: -200px; right: -200px; z-index: -1; }
        .bg-shape-2 { position: absolute; width: 600px; height: 600px; border-radius: 50%; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); opacity: 0.6; bottom: -150px; left: -100px; z-index: -1; }
        .card { background: white; padding: 60px; border-radius: 30px; box-shadow: 0 20px 50px rgba(0,0,0,0.1); 
                display: flex; width: 85%; height: 75%; z-index: 10; border-top: 12px solid #3498db; }
        .center-card { flex-direction: column; text-align: center; justify-content: center; align-items: center; }
        .split-card { gap: 60px; }
        .badge { background: #e74c3c; color: white; padding: 15px 40px; border-radius: 50px; font-size: 35px; margin-bottom: 30px; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; }
        .title-main { font-size: 110px; color: #2c3e50; margin: 0; font-weight: 900; }
        .title-sub { font-size: 60px; color: #7f8c8d; margin-top: 20px; }
        .text-col { flex: 1.2; display: flex; flex-direction: column; justify-content: center; }
        .content-title { font-size: 60px; color: #2c3e50; border-bottom: 5px solid #3498db; padding-bottom: 20px; margin-bottom: 30px; line-height: 1.3; font-weight: bold; }
        .content-script { font-size: 48px; color: #34495e; line-height: 1.6; }
        .img-col { flex: 1; display: flex; align-items: center; justify-content: center; background: #f8f9fa; border-radius: 20px; padding: 20px; }
        img { width: 100%; height: 100%; object-fit: cover; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.15); }
    </style>
    """
    
    if slide_type == "intro":
        body = f"""
        <div class="card center-card">
            <div class="badge">TAIPEI NEWS</div>
            <h1 class="title-main">{data['title']}</h1>
        </div>"""
    elif slide_type == "content":
        body = f"""
        <div class="card split-card">
            <div class="text-col">
                <div class="badge" style="width: fit-content; font-size: 25px; padding: 10px 25px; background: #3498db;">今日焦點 / HOT NEWS</div>
                <div class="content-title">{data['title']}</div>
                <div class="content-script">{data['script']}</div>
            </div>
            <div class="img-col">
                <img src="file://{IMAGE_PATH}">
            </div>
        </div>"""
    else: # outro
        body = f"""
        <div class="card center-card" style="border-top-color: #e74c3c;">
            <h1 class="title-main">{data['title']}</h1>
            <h2 class="title-sub">{data['script']}</h2>
        </div>"""

    html = f"""<!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
        {css}
    </head>
    <body>
        <div class="bg-shape-1"></div>
        <div class="bg-shape-2"></div>
        {body}
    </body>
    </html>"""
    
    out_html = WORK_DIR / f"{slide_type}_{lang}.html"
    out_html.write_text(html, encoding="utf-8")
    return out_html

def make_clip(img_path, audio_path, out_path):
    cmd = f"ffmpeg -y -loop 1 -i {img_path} -i {audio_path} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest {out_path}"
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    # Keep texts extremely concise to fit under 20s total.
    content = {
        "en": {
            "intro": {"title": "Taipei City News", "script": "Taipei City News Update."},
            "content": {"title": "Taipei & Fukuoka Pact", "script": "Mayor Chiang and Fukuoka Mayor Takashima signed a friendship pact today, promising closer cooperation."},
            "outro": {"title": "Thank You", "script": "Thanks for watching!"}
        },
        "ja": {
            "intro": {"title": "台北市政ニュース", "script": "台北市政ニュースです。"},
            "content": {"title": "台北市と福岡市が協定締結", "script": "蒋万安市長と高島福岡市長は本日、友好交流協定に署名し、協力関係を深めました。"},
            "outro": {"title": "おわり", "script": "ご視聴ありがとうございました。"}
        }
    }

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        for lang, sections in content.items():
            print(f"Processing {lang}...")
            clips = []
            for slide_type in ["intro", "content", "outro"]:
                data = sections[slide_type]
                audio_path = generate_tts(data["script"], f"audio_{slide_type}_{lang}.mp3")
                html_path = create_html(slide_type, data, lang)
                
                page.goto(f"file://{html_path}")
                page.wait_for_timeout(500) # wait for fonts
                img_path = WORK_DIR / f"frame_{slide_type}_{lang}.png"
                page.screenshot(path=str(img_path))
                
                clip_path = WORK_DIR / f"clip_{slide_type}_{lang}.mp4"
                make_clip(img_path, audio_path, clip_path)
                clips.append(f"file '{clip_path.name}'")
            
            # Concat clips
            concat_file = WORK_DIR / f"concat_{lang}.txt"
            concat_file.write_text("\n".join(clips))
            
            final_video = WORK_DIR / f"final_pretty_{lang}.mp4"
            concat_cmd = f"cd {WORK_DIR} && ffmpeg -y -f concat -safe 0 -i {concat_file.name} -c copy {final_video.name}"
            subprocess.run(concat_cmd, shell=True, check=True)
            print(f"Generated {final_video}")

        browser.close()

if __name__ == "__main__":
    main()
