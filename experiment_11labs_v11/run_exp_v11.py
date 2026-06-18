import os
import json
import urllib.request
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

WORK_DIR = Path.home() / "tw-gov-video" / "experiment_11labs_v11"
API_KEY = "sk_dab768322eb97d8789551989fba23b6ce5ddbdf3e85d847e"
VOICE_ID = "4mU4AFOhdaBEWGnnBxL8"

# Ensure we download the 3 images
images = [
    "https://www-ws.gov.taipei/001/Upload/297/relpic/10162/9472201/f48ed8a7-c1ea-4de6-b79b-b4c69064fc38.jpg",
    "https://www-ws.gov.taipei/001/Upload/297/relpic/10162/9394542/39050e2f-0c27-4344-b19e-e7f9b4562b6b.jpg",
    "https://www-ws.gov.taipei/001/Upload/297/relpic/10162/9120783/3d71e5da-e28e-416c-8aa9-7c5d9f7322e8.jpg"
]
local_imgs = []
for i, url in enumerate(images):
    local_path = WORK_DIR / f"img_{i}.jpg"
    if not local_path.exists():
        urllib.request.urlretrieve(url, local_path)
    local_imgs.append(str(local_path))

def generate_tts(text, filename):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_v3",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method="POST")
    raw_path = WORK_DIR / f"raw_{filename}"
    out_path = WORK_DIR / filename
    try:
        with urllib.request.urlopen(req) as response:
            with open(raw_path, "wb") as f:
                f.write(response.read())
        subprocess.run(f"ffmpeg -y -i {raw_path} -af 'apad=pad_dur=0.4' {out_path}", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return out_path
    except Exception as e:
        print(f"TTS Error for {filename}:", e)
        return None

def create_single_slide_html(slide_type, data, idx=0):
    font_family = "'Noto Sans JP', sans-serif"
    
    if slide_type == "intro":
        body_content = f"""
        <div class="slide title-slide" style="display: flex;">
            <div class="badge">FOCUS NEWS</div>
            <h1>{data['title']}</h1>
            <div class="subtitle-box">{data['en_sub']}</div>
        </div>
        """
    elif slide_type == "content":
        img_path = local_imgs[idx]
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
                        <img src="file://{img_path}" class="content-img">
                    </div>
                </div>
            </div>
            <div class="subtitle-box">{data['en_sub']}</div>
        </div>
        """
    else:
        body_content = f"""
        <div class="slide outro-slide" style="display: flex;">
            <h1>{data['title']}</h1>
            <h2>{data['script']}</h2>
            <div class="subtitle-box">{data['en_sub']}</div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1920, height=1080, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body, html {{
            margin: 0; padding: 0; width: 1920px; height: 1080px;
            background-color: #f8f9fa;
            background-image: radial-gradient(#bdc3c7 2px, transparent 2px);
            background-size: 40px 40px;
            font-family: {font_family};
            overflow: hidden; color: #2c3e50; position: relative;
        }}
        .bg-circle {{ position: absolute; border-radius: 50%; background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%); opacity: 0.6; z-index: -1; }}
        .bg-c1 {{ width: 800px; height: 800px; top: -200px; right: -200px; }}
        .bg-c2 {{ width: 600px; height: 600px; bottom: -150px; left: -100px; }}
        .slide {{ width: 1920px; height: 1080px; position: absolute; top: 0; left: 0; flex-direction: column; align-items: center; justify-content: center; padding: 80px; box-sizing: border-box; }}
        
        .title-slide h1 {{ font-family: 'Dela Gothic One', sans-serif; font-size: 180px; font-weight: normal; color: #2c3e50; margin: 0; text-align: center; text-shadow: 6px 6px 0px rgba(52, 152, 219, 0.2); }}
        .title-slide .badge {{ background: #2c3e50; color: white; padding: 15px 40px; border-radius: 5px; font-size: 36px; font-weight: bold; margin-bottom: 40px; letter-spacing: 2px; text-transform: uppercase; }}

        .content-box {{ background: white; border-radius: 20px; padding: 50px 70px; width: 90%; height: 80%; box-shadow: 0 25px 60px rgba(0,0,0,0.08); display: flex; flex-direction: column; position: relative; z-index: 10; margin-bottom: 50px; }}
        .slide-title {{ font-weight: 900; font-size: 45px; color: #2980b9; margin: 0 0 20px 0; line-height: 1.3; border-bottom: 4px solid #f1c40f; padding-bottom: 10px; }}
        .layout-split {{ display: flex; flex: 1; gap: 50px; height: calc(100% - 100px); }}
        .text-column {{ flex: 1.2; display: flex; flex-direction: column; justify-content: center; }}
        .image-column {{ flex: 1; display: flex; justify-content: center; align-items: center; border-radius: 15px; overflow: hidden; position: relative; background: #ecf0f1; box-shadow: inset 0 0 20px rgba(0,0,0,0.05); }}
        .content-img {{ width: 100%; height: 100%; object-fit: cover; border-radius: 15px; border: 3px solid rgba(189, 195, 199, 0.4); box-sizing: border-box; }}
        .label {{ font-weight: 900; color: #e74c3c; font-size: 28px; margin-bottom: 15px; display: inline-block; border-left: 8px solid #e74c3c; padding-left: 15px; text-transform: uppercase; letter-spacing: 1px; }}
        .script-text {{ font-size: 38px; line-height: 1.5; color: #34495e; margin: 0; font-weight: 700; }}

        .outro-slide h1 {{ font-weight: 900; font-size: 140px; color: #2c3e50; margin: 0 0 30px 0; text-align: center; }}
        .outro-slide h2 {{ color: #e74c3c; font-size: 70px; margin:0; text-align: center; }}
        
        .subtitle-box {{ position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.85); color: #fff; font-size: 38px; font-weight: 700; padding: 15px 40px; border-radius: 10px; width: 85%; text-align: center; line-height: 1.4; font-family: sans-serif; box-shadow: 0 10px 20px rgba(0,0,0,0.2); z-index: 100; border: 2px solid rgba(255,255,255,0.2); }}
    </style>
</head>
<body>
    <div class="bg-circle bg-c1"></div>
    <div class="bg-circle bg-c2"></div>
    {body_content}
</body>
</html>
"""
    out_html = WORK_DIR / f"slide_{slide_type}_{idx}.html"
    out_html.write_text(html, encoding="utf-8")
    return out_html

def make_clip(img_path, audio_path, out_path):
    cmd = f"ffmpeg -y -loop 1 -framerate 25 -i {img_path} -i {audio_path} -c:v libx264 -preset veryfast -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest -fflags +shortest -max_muxing_queue_size 1024 {out_path}"
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    slides = [
        {
            "type": "intro",
            "title": "台北市政ニュース",
            "tts": "台北市政ニュース。AIによって作成されました。",
            "en_sub": "Taipei City News. Created by AI."
        },
        {
            "type": "content",
            "title": "東京都副知事が台北市を訪問",
            "script": "宮坂東京都副知事が台北市を訪問し、蔣万安市長と面会しました。双方はデジタルトランスフォーメーションとスタートアップ支援における協力強化で合意しました。",
            "tts": "宮坂東京都副知事が台北市を訪問し、蔣万安市長と面会しました。双方はデジタルトランスフォーメーションとスタートアップ支援における協力強化で合意しました。",
            "en_sub": "Tokyo Vice Governor Miyasaka visited Taipei to meet with Mayor Chiang Wan-an. Both sides agreed to strengthen cooperation in digital transformation and startup support."
        },
        {
            "type": "content",
            "title": "東京高円寺阿波おどりが台北で公演",
            "script": "台北市の松山慈祐宮で開催された文化祭に、東京の高円寺阿波おどりが参加しました。蔣万安市長は、日台の文化交流の架け橋として高く評価しました。",
            "tts": "台北市の松山慈祐宮で開催された文化祭に、東京の高円寺阿波おどりが参加しました。蔣万安市長は、日台の文化交流の架け橋として高く評価しました。",
            "en_sub": "Tokyo's Koenji Awa Odori participated in the Songshan cultural festival. Mayor Chiang Wan-an praised the event as a bridge for cultural exchange between Japan and Taiwan."
        },
        {
            "type": "content",
            "title": "小池東京都知事が台北市を訪問",
            "script": "小池百合子東京都知事が台北市を訪問しました。蔣万安市長は、防災、人口対策、環境保護、スポーツ大会の開催など、多分野での交流を深めることを確認しました。",
            "tts": "小池百合子東京都知事が台北市を訪問しました。蔣万安市長は、防災、人口対策、環境保護、スポーツ大会の開催など、多分野での交流を深めることを確認しました。",
            "en_sub": "Tokyo Governor Yuriko Koike visited Taipei. Mayor Chiang Wan-an confirmed the deepening of exchanges in various fields, including disaster prevention and sports events."
        },
        {
            "type": "outro",
            "title": "おわり",
            "script": "ご視聴ありがとうございました",
            "tts": "台北市政ニュースをご視聴いただき、ありがとうございました。",
            "en_sub": "Thank you for watching Taipei City News."
        }
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        clips = []
        content_idx = 0
        
        for idx, slide in enumerate(slides):
            print(f"Processing slide {idx}...")
            audio_path = generate_tts(slide["tts"], f"v11_audio_{idx}.mp3")
            
            html_path = create_single_slide_html(slide["type"], slide, content_idx if slide["type"] == "content" else 0)
            page.goto(f"file://{os.path.abspath(html_path)}")
            page.wait_for_timeout(500)
            
            img_path = WORK_DIR / f"v11_frame_{idx}.png"
            page.screenshot(path=str(img_path))
            
            clip_path = WORK_DIR / f"v11_clip_{idx}.mp4"
            make_clip(img_path, audio_path, clip_path)
            clips.append(f"file '{clip_path.name}'")
            
            if slide["type"] == "content":
                content_idx += 1
                
        concat_file = WORK_DIR / f"v11_concat.txt"
        concat_file.write_text("\n".join(clips))
        
        final_video = WORK_DIR / f"final_v11_ja.mp4"
        concat_cmd = f"cd {WORK_DIR} && ffmpeg -y -f concat -safe 0 -i {concat_file.name} -c copy {final_video.name}"
        subprocess.run(concat_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"Generated {final_video}")
        browser.close()

if __name__ == "__main__":
    main()
