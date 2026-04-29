from pathlib import Path
import json
from datetime import datetime

BASE = Path.home() / "tw-gov-video"
OUTPUT_DIR = BASE / "output"
JSON_FILE = OUTPUT_DIR / "selected_articles.json"

data = json.loads(JSON_FILE.read_text(encoding="utf-8"))
# Try to get an article with an image
item = data.get("selected", [{}])[1] if len(data.get("selected", [])) > 1 else data.get("selected", [{}])[0]

title = item.get("title", "115年3月北市批發市場蔬果農藥殘留抽驗結果")
script = item.get("script", "臺北市市場處公布三月份批發市場蔬果農藥殘留抽驗結果，共攔截並銷毀超過八千公斤的不合格蔬果，主要違規品項包含辣椒與豌豆，嚴格把關市民食安。")
today = datetime.now().strftime("%Y-%m-%d")

# Use a local downloaded image to avoid network issues
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

# --- Design 1: Dark Cyber/Tech ---
html1 = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
      body {{ background: #0f172a; color: #f8fafc; font-family: 'Noto Sans TC', sans-serif; margin: 0; display: flex; align-items: center; justify-content: center; height: 1080px; width: 1920px; }}
      .container {{ display: flex; width: 1700px; height: 900px; gap: 70px; }}
      .text-side {{ flex: 1.2; border-left: 8px solid #38bdf8; padding-left: 60px; display: flex; flex-direction: column; justify-content: center; }}
      .img-side {{ flex: 1; border-radius: 20px; overflow: hidden; position: relative; box-shadow: 0 0 40px rgba(56, 189, 248, 0.2); }}
      img {{ width: 100%; height: 100%; object-fit: cover; opacity: 0.9; filter: contrast(1.1); }}
      h1 {{ font-size: 70px; color: #f8fafc; margin-bottom: 40px; line-height: 1.3; font-weight: 900; }}
      h3 {{ color: #38bdf8; font-size: 30px; letter-spacing: 4px; margin-bottom: 20px; }}
      p {{ font-size: 42px; color: #cbd5e1; line-height: 1.7; }}
    </style>
</head>
<body>
  <div class="container">
    <div class="text-side">
      <h3>LATEST UPDATE</h3>
      <h1>{title}</h1>
      <p>{script}</p>
    </div>
    <div class="img-side"><img src="{img_url}"></div>
  </div>
</body>
</html>
"""

# --- Design 2: Glassmorphism / Vibrant ---
html2 = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
      body {{ background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%); margin: 0; font-family: 'Noto Sans TC'; height: 1080px; width: 1920px; display: flex; align-items: center; justify-content: center; }}
      .glass {{ background: rgba(255, 255, 255, 0.35); backdrop-filter: blur(25px); border: 2px solid rgba(255, 255, 255, 0.6); border-radius: 40px; padding: 80px; width: 1650px; height: 850px; display: flex; gap: 60px; box-shadow: 0 30px 60px rgba(0,0,0,0.1); box-sizing: border-box; }}
      .text-side {{ flex: 1.2; display: flex; flex-direction: column; justify-content: center; }}
      .img-side {{ flex: 1; border-radius: 30px; overflow: hidden; }}
      img {{ width: 100%; height: 100%; object-fit: cover; }}
      h1 {{ font-size: 65px; color: #2c3e50; margin: 0 0 30px 0; font-weight: 900; line-height: 1.3; }}
      p {{ font-size: 40px; color: #34495e; line-height: 1.6; }}
      .tag {{ background: white; color: #a6c1ee; padding: 12px 25px; border-radius: 30px; display: inline-block; font-weight: 900; font-size: 24px; margin-bottom: 30px; letter-spacing: 1px; }}
    </style>
</head>
<body>
  <div class="glass">
    <div class="text-side">
      <div><span class="tag">TRENDING</span></div>
      <h1>{title}</h1>
      <p>{script}</p>
    </div>
    <div class="img-side"><img src="{img_url}"></div>
  </div>
</body>
</html>
"""

# --- Design 3: Modern Editorial / Minimalist ---
html3 = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
      body {{ background: #fdfbf7; color: #1a1a1a; margin: 0; font-family: 'Noto Sans TC'; height: 1080px; width: 1920px; display: flex; flex-direction: column; padding: 90px; box-sizing: border-box; }}
      .header {{ border-bottom: 8px solid #1a1a1a; padding-bottom: 30px; margin-bottom: 60px; display: flex; justify-content: space-between; align-items: flex-end; }}
      .header h2 {{ font-size: 45px; margin: 0; text-transform: uppercase; font-weight: 900; letter-spacing: 2px; }}
      .content {{ display: flex; gap: 90px; flex: 1; }}
      .text-side {{ flex: 1.2; }}
      .img-side {{ flex: 1; border: 4px solid #1a1a1a; padding: 15px; background: white; }}
      img {{ width: 100%; height: 100%; object-fit: cover; filter: grayscale(15%); }}
      h1 {{ font-size: 80px; font-weight: 900; margin: 0 0 50px 0; line-height: 1.2; }}
      p {{ font-size: 42px; line-height: 1.7; color: #333; }}
    </style>
</head>
<body>
  <div class="header">
    <h2>TAIPEI DAILY BRIEFING</h2>
    <h2>{today}</h2>
  </div>
  <div class="content">
    <div class="text-side">
      <h1>{title}</h1>
      <p>{script}</p>
    </div>
    <div class="img-side"><img src="{img_url}"></div>
  </div>
</body>
</html>
"""

print("Rendering Design 1...")
render_design(html1, OUTPUT_DIR / "design1.png")
print("Rendering Design 2...")
render_design(html2, OUTPUT_DIR / "design2.png")
print("Rendering Design 3...")
render_design(html3, OUTPUT_DIR / "design3.png")

print("Done.")
