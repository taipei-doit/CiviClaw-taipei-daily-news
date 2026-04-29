from pathlib import Path
import json
from datetime import datetime

BASE = Path.home() / "tw-gov-video"
OUTPUT_DIR = BASE / "output"
JSON_FILE = OUTPUT_DIR / "selected_articles.json"

data = json.loads(JSON_FILE.read_text(encoding="utf-8"))
item = data.get("selected", [{}])[1] if len(data.get("selected", [])) > 1 else data.get("selected", [{}])[0]

title = item.get("title", "115年3月北市批發市場蔬果農藥殘留抽驗結果")
reason = item.get("reason", "食品安全資訊，與民眾健康息息相關。")
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

css_base = """
    <link href="https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
      @font-face {
          font-family: 'Dela Local';
          src: url('file:///home/benliangcs/tw-gov-video/output/DelaGothicOne-Regular.ttf');
      }
      body { background: #facc15; color: #171717; margin: 0; font-family: 'Noto Sans TC'; height: 1080px; width: 1920px; display: flex; align-items: center; justify-content: center; overflow: hidden; }
      .card { background: #ffffff; border: 12px solid #171717; padding: 70px; width: 1700px; height: 900px; display: flex; gap: 80px; box-shadow: 30px 30px 0px #171717; box-sizing: border-box; }
      .full-card { background: #ffffff; border: 12px solid #171717; padding: 100px; width: 1700px; height: 900px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; box-shadow: 30px 30px 0px #171717; box-sizing: border-box; }
    </style>
"""

# --- Intro Slide ---
html_intro = f"""
<!DOCTYPE html>
<html>
<head>
    {css_base}
    <style>
      .badge {{ background: #171717; color: #facc15; display: inline-block; padding: 15px 40px; font-size: 36px; font-weight: 900; margin-bottom: 50px; letter-spacing: 2px; text-transform: uppercase; border: 6px solid #171717; box-shadow: 15px 15px 0px #facc15, 15px 15px 0px 6px #171717; }}
      /* Ensuring Dela Gothic One applies explicitly */
      h1 {{ font-family: 'Dela Local', 'Dela Gothic One', cursive; font-size: 220px; font-weight: normal; margin: 0; color: #171717; line-height: 1.1; }}
      h2 {{ font-size: 80px; font-weight: 900; margin: 20px 0 0 0; color: #171717; }}
    </style>
</head>
<body>
  <div class="full-card">
    <div class="badge">TAIPEI CITY GOV</div>
    <h1>每日新聞</h1>
    <h2>{today}</h2>
  </div>
</body>
</html>
"""

# --- Content Slide ---
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    {css_base}
    <style>
      .text-side {{ flex: 1.2; display: flex; flex-direction: column; justify-content: center; }}
      .img-side {{ flex: 1; border: 10px solid #171717; box-shadow: 20px 20px 0px #171717; overflow: hidden; background: #e5e5e5; display: flex; align-items: center; justify-content: center; }}
      img {{ width: 100%; height: 100%; object-fit: cover; filter: contrast(1.1); }}
      h1 {{ font-family: 'Noto Sans TC', sans-serif; font-size: 55px; font-weight: 900; line-height: 1.3; margin: 0 0 30px 0; border-bottom: 8px solid #171717; padding-bottom: 20px; }}
      .label {{ font-size: 28px; font-weight: 900; background: #facc15; border: 4px solid #171717; padding: 5px 15px; display: inline-block; margin-bottom: 15px; letter-spacing: 2px; }}
      p.reason {{ font-size: 32px; font-weight: 700; margin: 0 0 30px 0; color: #404040; line-height: 1.5; }}
      p.script-text {{ font-size: 38px; line-height: 1.6; font-weight: 700; margin: 0; }}
    </style>
</head>
<body>
  <div class="card">
    <div class="text-side">
      <h1>{title}</h1>
      <div><span class="label">推薦原因</span></div>
      <p class="reason">{reason}</p>
      <div><span class="label">播報稿</span></div>
      <p class="script-text">{script}</p>
    </div>
    <div class="img-side"><img src="{img_url}"></div>
  </div>
</body>
</html>
"""

# --- Outro Slide ---
html_outro = f"""
<!DOCTYPE html>
<html>
<head>
    {css_base}
    <style>
      h1 {{ font-family: 'Noto Sans TC', sans-serif; font-size: 140px; font-weight: 900; margin: 0 0 40px 0; color: #171717; line-height: 1.1; }}
      h2 {{ font-family: 'Noto Sans TC', sans-serif; font-size: 70px; font-weight: 900; margin: 0; color: #171717; background: #facc15; border: 8px solid #171717; padding: 20px 50px; box-shadow: 15px 15px 0px #171717; display: inline-block; }}
    </style>
</head>
<body>
  <div class="full-card">
    <h1>感謝您的收看</h1>
    <h2>喜歡請按讚、訂閱並分享！</h2>
  </div>
</body>
</html>
"""

print("Rendering Intro...")
render_design(html_intro, OUTPUT_DIR / "neo_intro.png")
print("Rendering Content...")
render_design(html_content, OUTPUT_DIR / "neo_content.png")
print("Rendering Outro...")
render_design(html_outro, OUTPUT_DIR / "neo_outro.png")

print("Done.")
