import os
import json
import urllib.request
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

WORK_DIR = Path.home() / "tw-gov-video" / "experiment_11labs_v8"
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
    raw_path = WORK_DIR / f"raw_{filename}"
    out_path = WORK_DIR / filename
    try:
        with urllib.request.urlopen(req) as response:
            with open(raw_path, "wb") as f:
                f.write(response.read())
        
        # Add only 0.4s of padding to prevent abrupt FFmpeg cutoffs, removing the long awkward silences
        subprocess.run(f"ffmpeg -y -i {raw_path} -af 'apad=pad_dur=0.4' {out_path}", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return out_path
    except Exception as e:
        print(f"TTS Error for {filename}:", e)
        return None

def create_single_slide_html(slide_type, lang, data):
    font_family = "'Noto Sans TC', sans-serif" if lang == "en" else "'Noto Sans JP', sans-serif"
    
    # We build the body content based on the exact slide type. No JS hiding/showing to ensure 100% sync.
    if slide_type == "intro":
        body_content = f"""
        <div class="slide title-slide" style="display: flex;">
            <div class="badge">FOCUS NEWS</div>
            <h1>{data['title']}</h1>
        </div>
        """
    elif slide_type == "content":
        body_content = f"""
        <div class="slide content-slide" style="display: flex;">
            <div class="content-box">
                <h2 class="slide-title">{data['title']}</h2>
                <div class="layout-split">
                    <div class="text-column">
                        <div class="label">NEWS UPDATE</div>
                        <p class="script-text">{data['script']}</p>
                    </div>
                    <div class="image-column">
                        <img src="file://{IMAGE_PATH}" class="content-img">
                    </div>
                </div>
            </div>
        </div>
        """
    else: # outro
        body_content = f"""
        <div class="slide outro-slide" style="display: flex;">
            <h1>{data['title']}</h1>
            <h2>{data['script']}</h2>
        </div>
        """

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
            flex-direction: column; align-items: center; justify-content: center;
            padding: 80px; box-sizing: border-box; 
        }}
        
        .title-slide h1 {{
            font-family: 'Dela Gothic One', sans-serif; font-size: 180px; font-weight: normal; color: #2c3e50; margin: 0; text-align: center;
            text-shadow: 6px 6px 0px rgba(52, 152, 219, 0.2);
        }}
        .title-slide .badge {{
            background: #2c3e50; color: white; padding: 15px 40px; border-radius: 5px;
            font-size: 36px; font-weight: bold; margin-bottom: 40px; letter-spacing: 2px; text-transform: uppercase;
        }}

        .content-box {{
            background: white; border-radius: 20px; padding: 50px 70px;
            width: 90%; height: 85%; box-shadow: 0 25px 60px rgba(0,0,0,0.08);
            display: flex; flex-direction: column; position: relative; z-index: 10;
        }}
        .slide-title {{
            font-weight: 900; font-size: 55px; color: #2980b9; margin: 0 0 30px 0;
            line-height: 1.3; border-bottom: 4px solid #f1c40f; padding-bottom: 15px;
        }}
        .layout-split {{ display: flex; flex: 1; gap: 50px; height: calc(100% - 130px); }}
        .text-column {{ flex: 1.2; display: flex; flex-direction: column; justify-content: center; }}
        .image-column {{
            flex: 1; display: flex; justify-content: center; align-items: center;
            border-radius: 15px; overflow: hidden; position: relative;
            background: #ecf0f1; box-shadow: inset 0 0 20px rgba(0,0,0,0.05);
        }}
        .content-img {{ width: 100%; height: 100%; object-fit: cover; border-radius: 15px; border: 3px solid rgba(189, 195, 199, 0.4); box-sizing: border-box; }}
        .label {{
            font-weight: 900; color: #e74c3c; font-size: 28px; margin-bottom: 15px;
            display: inline-block; border-left: 8px solid #e74c3c; padding-left: 15px;
            text-transform: uppercase; letter-spacing: 1px;
        }}
        .script-text {{ font-size: 40px; line-height: 1.5; color: #34495e; margin: 0; font-weight: 700; }}

        .outro-slide h1 {{ font-weight: 900; font-size: 140px; color: #2c3e50; margin: 0 0 30px 0; text-align: center; }}
        .outro-slide h2 {{ color: #e74c3c; font-size: 70px; margin:0; text-align: center; }}
    </style>
</head>
<body>
    <div class="bg-circle bg-c1"></div>
    <div class="bg-circle bg-c2"></div>
    {body_content}
</body>
</html>
"""
    out_html = WORK_DIR / f"slide_{slide_type}_{lang}.html"
    out_html.write_text(html, encoding="utf-8")
    return out_html

def make_clip(img_path, audio_path, out_path):
    # Using specific framerate and audio settings to ensure perfect sync during concat
    cmd = f"ffmpeg -y -loop 1 -framerate 25 -i {img_path} -i {audio_path} -c:v libx264 -preset veryfast -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest -fflags +shortest -max_muxing_queue_size 1024 {out_path}"
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    content = {
        "en": {
            "intro": {"title": "Taipei City News", "tts": "Taipei City News Update, created by AI."},
            "content": {
                "title": "Taipei & Fukuoka Sign Historic Friendship Pact", 
                "script": "Taipei Mayor Chiang Wan-an and Fukuoka Mayor Takashima signed a memorandum of understanding today. The pact marks a milestone in bilateral relations, promoting cooperation in business, startup incubation, and cultural exchange.", 
                "tts": "Taipei Mayor Chiang Wan-an and Fukuoka Mayor Takashima signed a memorandum of understanding today. The pact marks a milestone in bilateral relations, promoting cooperation in business, startup incubation, and cultural exchange."
            },
            "outro": {"title": "Thank You", "script": "Please subscribe and share!", "tts": "Thank you for watching Taipei City News."}
        },
        "ja": {
            "intro": {"title": "台北市政ニュース", "tts": "台北市政ニュース。AIによって作成されました。"},
            "content": {
                "title": "台北市と福岡市が歴史的な友好交流協定を締結", 
                "script": "蒋万安台北市長と高島福岡市長は本日、覚書に署名しました。この協定は二国間関係の節目となり、ビジネスやスタートアップ支援、文化交流における協力を促進します。", 
                "tts": "蒋万安台北市長と高島福岡市長は本日、覚書に署名しました。この協定は二国間関係の節目となり、ビジネスやスタートアップ支援、文化交流における協力を促進します。"
            },
            "outro": {"title": "おわり", "script": "ご視聴ありがとうございました", "tts": "台北市政ニュースをご視聴いただき、ありがとうございました。"}
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
                audio_path = generate_tts(data["tts"], f"v8_audio_{slide_type}_{lang}.mp3")
                
                # Create dedicated HTML per slide to guarantee no sync/DOM overlap issues
                html_path = create_single_slide_html(slide_type, lang, data)
                page.goto(f"file://{html_path}")
                page.wait_for_timeout(500) # Wait for rendering
                
                img_path = WORK_DIR / f"v8_frame_{slide_type}_{lang}.png"
                page.screenshot(path=str(img_path))
                
                clip_path = WORK_DIR / f"v8_clip_{slide_type}_{lang}.mp4"
                make_clip(img_path, audio_path, clip_path)
                clips.append(f"file '{clip_path.name}'")
                
            concat_file = WORK_DIR / f"v8_concat_{lang}.txt"
            concat_file.write_text("\n".join(clips))
            
            final_video = WORK_DIR / f"final_v8_{lang}.mp4"
            concat_cmd = f"cd {WORK_DIR} && ffmpeg -y -f concat -safe 0 -i {concat_file.name} -c copy {final_video.name}"
            subprocess.run(concat_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            print(f"Generated {final_video}")

        browser.close()

if __name__ == "__main__":
    main()
