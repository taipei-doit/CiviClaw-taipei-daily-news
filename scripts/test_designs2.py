from pathlib import Path
import json
from datetime import datetime

BASE = Path.home() / "tw-gov-video"
OUTPUT_DIR = BASE / "output"
JSON_FILE = OUTPUT_DIR / "selected_articles.json"

data = json.loads(JSON_FILE.read_text(encoding="utf-8"))
item = data.get("selected", [{}])[1] if len(data.get("selected", [])) > 1 else data.get("selected", [{}])[0]

title = item.get("title", "115年3月北市批發市場蔬果農藥殘留抽驗結果")
script = item.get("script", "臺北市市場處公布三月份批發市場蔬果農藥殘留抽驗結果，共攔截並銷毀超過八千公斤的不合格蔬果，主要違規品項包含辣椒與豌豆，嚴格把關市民食安。")
today = datetime.now().strftime("%Y-%m-%d")

img_url = f"file://{OUTPUT_DIR}/dl_img_1.jpg"
if not (OUTPUT_DIR / "dl_img_1.jpg").exists():
    img_url = f"file://{OUTPUT_DIR}/dl_img_0.jpg"

def render_design(html_content, out_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--no-sandbox', '--disable-setuid-sandbox'])
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.set_content(html_content)
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(500)
        page.screenshot(path=str(out_path))
        browser.close()

# --- Design 4: Neo-Brutalism ---
html4 = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
      body {{ background: #facc15; color: #171717; margin: 0; font-family: 'Noto Sans TC'; height: 1080px; width: 1920px; display: flex; align-items: center; justify-content: center; }}
      .card {{ background: #ffffff; border: 12px solid #171717; border-radius: 0; padding: 60px; width: 1600px; height: 800px; display: flex; gap: 80px; box-shadow: 30px 30px 0px #171717; box-sizing: border-box; }}
      .text-side {{ flex: 1.2; display: flex; flex-direction: column; justify-content: center; }}
      .img-side {{ flex: 1; border: 10px solid #171717; box-shadow: 20px 20px 0px #171717; overflow: hidden; background: #e5e5e5; }}
      img {{ width: 100%; height: 100%; object-fit: cover; filter: contrast(1.2); }}
      h1 {{ font-size: 75px; font-weight: 900; line-height: 1.2; margin: 0 0 40px 0; border-bottom: 8px solid #171717; padding-bottom: 20px; text-transform: uppercase; }}
      p {{ font-size: 45px; line-height: 1.6; font-weight: 700; margin: 0; }}
      .badge {{ background: #171717; color: #facc15; display: inline-block; padding: 15px 30px; font-size: 30px; font-weight: 900; margin-bottom: 30px; letter-spacing: 2px; }}
    </style>
</head>
<body>
  <div class="card">
    <div class="text-side">
      <div><span class="badge">ALERT // {today}</span></div>
      <h1>{title}</h1>
      <p>{script}</p>
    </div>
    <div class="img-side"><img src="{img_url}"></div>
  </div>
</body>
</html>
"""

# --- Design 5: Soft & Organic ---
html5 = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
      body {{ background: #fdfaf6; color: #4a4a4a; margin: 0; font-family: 'Noto Sans TC'; height: 1080px; width: 1920px; position: relative; overflow: hidden; }}
      .blob1 {{ position: absolute; top: -200px; left: -100px; width: 800px; height: 800px; background: #ffdfd3; border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%; z-index: -1; }}
      .blob2 {{ position: absolute; bottom: -300px; right: -200px; width: 1000px; height: 1000px; background: #e0ece4; border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; z-index: -1; }}
      .container {{ display: flex; width: 100%; height: 100%; padding: 120px; box-sizing: border-box; gap: 100px; align-items: center; }}
      .text-side {{ flex: 1.2; }}
      .img-side {{ flex: 1; height: 100%; }}
      img {{ width: 100%; height: 100%; object-fit: cover; border-radius: 40px 120px 40px 120px; box-shadow: 0 40px 80px rgba(0,0,0,0.06); }}
      h1 {{ font-size: 70px; font-weight: 900; color: #333; margin: 0 0 50px 0; line-height: 1.4; }}
      p {{ font-size: 42px; line-height: 1.8; color: #666; }}
      .date {{ font-size: 30px; color: #999; margin-bottom: 20px; letter-spacing: 2px; }}
    </style>
</head>
<body>
  <div class="blob1"></div>
  <div class="blob2"></div>
  <div class="container">
    <div class="text-side">
      <div class="date">{today}</div>
      <h1>{title}</h1>
      <p>{script}</p>
    </div>
    <div class="img-side"><img src="{img_url}"></div>
  </div>
</body>
</html>
"""

# --- Design 6: Cinematic / Full Bleed ---
html6 = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
      body {{ margin: 0; font-family: 'Noto Sans TC'; height: 1080px; width: 1920px; background: #000; color: white; position: relative; overflow: hidden; }}
      .bg-img {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0.4; filter: blur(10px) brightness(0.5); z-index: 0; }}
      .overlay {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to right, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.5) 50%, rgba(0,0,0,0) 100%); z-index: 1; }}
      .content {{ position: absolute; z-index: 2; display: flex; width: 100%; height: 100%; align-items: center; padding: 100px; box-sizing: border-box; gap: 80px; }}
      .text-side {{ flex: 1.5; }}
      .img-side {{ flex: 1; height: 700px; border-radius: 20px; overflow: hidden; box-shadow: 0 50px 100px rgba(0,0,0,0.8); border: 2px solid rgba(255,255,255,0.1); }}
      .main-img {{ width: 100%; height: 100%; object-fit: cover; }}
      h1 {{ font-size: 85px; font-weight: 900; line-height: 1.2; margin: 0 0 40px 0; text-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
      p {{ font-size: 45px; line-height: 1.6; color: #ddd; text-shadow: 0 5px 15px rgba(0,0,0,0.5); border-left: 6px solid #e74c3c; padding-left: 30px; }}
    </style>
</head>
<body>
  <img src="{img_url}" class="bg-img">
  <div class="overlay"></div>
  <div class="content">
    <div class="text-side">
      <h1>{title}</h1>
      <p>{script}</p>
    </div>
    <div class="img-side"><img src="{img_url}" class="main-img"></div>
  </div>
</body>
</html>
"""

print("Rendering Design 4...")
render_design(html4, OUTPUT_DIR / "design4.png")
print("Rendering Design 5...")
render_design(html5, OUTPUT_DIR / "design5.png")
print("Rendering Design 6...")
render_design(html6, OUTPUT_DIR / "design6.png")

print("Done.")
