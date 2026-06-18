from playwright.sync_api import sync_playwright
import os

IMAGE_PATH = "/home/benliangcs/.openclaw/media/inbound/84fd2a38-b495-47b4-938d-92671b39a55b.png"

def create_html(style, filename):
    if style == "cyber":
        css = """
        body { background-color: #0b0f19; color: #00f0ff; font-family: 'Noto Sans TC', sans-serif; margin: 0; overflow: hidden; width: 1920px; height: 1080px; }
        .slide { display: flex; flex-direction: column; padding: 100px; height: 1080px; box-sizing: border-box; background: linear-gradient(135deg, rgba(11,15,25,1) 0%, rgba(13,37,63,1) 100%); }
        .grid { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: linear-gradient(rgba(0, 240, 255, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 240, 255, 0.1) 1px, transparent 1px); background-size: 50px 50px; z-index: 0; }
        .content-box { z-index: 10; border: 2px solid #00f0ff; background: rgba(0, 20, 40, 0.8); box-shadow: 0 0 30px rgba(0, 240, 255, 0.3); border-radius: 10px; padding: 60px; height: 100%; display: flex; flex-direction: column; position: relative; }
        .title { font-size: 60px; font-weight: 900; border-bottom: 4px solid #ff0055; padding-bottom: 20px; text-shadow: 0 0 10px rgba(0, 240, 255, 0.5); margin-top: 0; }
        .flex { display: flex; gap: 50px; height: 100%; margin-top: 40px; }
        .text { font-size: 45px; color: #e0f8ff; line-height: 1.6; flex: 1; }
        .img-container { flex: 1; border: 2px solid #ff0055; box-shadow: 0 0 20px rgba(255, 0, 85, 0.4); border-radius: 10px; overflow: hidden; }
        img { width: 100%; height: 100%; object-fit: cover; }
        .badge { position: absolute; top: -30px; right: 40px; background: #ff0055; color: white; padding: 10px 30px; font-size: 30px; font-weight: bold; border-radius: 5px; box-shadow: 0 0 15px #ff0055; }
        """
    elif style == "smart":
        css = """
        body { background-color: #f0f4f8; color: #1a365d; font-family: 'Noto Sans TC', sans-serif; margin: 0; overflow: hidden; width: 1920px; height: 1080px; }
        .slide { display: flex; flex-direction: column; padding: 100px; height: 1080px; box-sizing: border-box; }
        .bg-shapes { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; overflow: hidden; }
        .circle1 { position: absolute; width: 800px; height: 800px; border-radius: 50%; background: linear-gradient(135deg, rgba(66, 153, 225, 0.2), rgba(49, 130, 206, 0.1)); top: -200px; right: -200px; }
        .circle2 { position: absolute; width: 600px; height: 600px; border-radius: 50%; background: linear-gradient(135deg, rgba(72, 187, 120, 0.2), rgba(56, 161, 105, 0.1)); bottom: -100px; left: -100px; }
        .content-box { z-index: 10; background: white; border-radius: 30px; padding: 60px; height: 100%; display: flex; flex-direction: column; box-shadow: 0 20px 50px rgba(0,0,0,0.05); position: relative; border-left: 10px solid #3182ce; }
        .title { font-size: 60px; font-weight: 900; color: #2b6cb0; margin-top: 0; margin-bottom: 20px; }
        .flex { display: flex; gap: 60px; height: 100%; margin-top: 20px; }
        .text { font-size: 45px; color: #4a5568; line-height: 1.6; flex: 1; }
        .img-container { flex: 1; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        img { width: 100%; height: 100%; object-fit: cover; }
        .badge { display: inline-block; background: #e2e8f0; color: #4a5568; padding: 10px 20px; font-size: 24px; font-weight: bold; border-radius: 50px; margin-bottom: 20px; letter-spacing: 2px; }
        """
    else:
        css = """
        body { background-color: #000000; color: white; font-family: 'Noto Sans TC', sans-serif; margin: 0; overflow: hidden; width: 1920px; height: 1080px; }
        .slide { display: flex; flex-direction: column; padding: 0; height: 1080px; box-sizing: border-box; }
        .content-box { display: flex; flex-direction: row; height: 100%; }
        .text-side { flex: 1.2; padding: 100px; background: linear-gradient(90deg, #111 0%, #222 100%); border-right: 5px solid #00ffcc; display: flex; flex-direction: column; justify-content: center; position: relative;}
        .img-side { flex: 1; position: relative; }
        img { width: 100%; height: 100%; object-fit: cover; opacity: 0.8; }
        .img-overlay { position: absolute; top:0; left:0; width:100%; height:100%; background: linear-gradient(0deg, rgba(0,255,204,0.3) 0%, transparent 50%); }
        .title { font-size: 65px; font-weight: 900; margin-top: 0; margin-bottom: 40px; color: #ffffff; text-transform: uppercase; letter-spacing: 2px; }
        .text { font-size: 42px; color: #cccccc; line-height: 1.7; }
        .badge { color: #00ffcc; font-size: 28px; font-weight: bold; letter-spacing: 5px; margin-bottom: 20px; display: block; border-left: 5px solid #00ffcc; padding-left: 15px; }
        .dots { position: absolute; bottom: 50px; right: 50px; color: #00ffcc; font-size: 40px; letter-spacing: 10px; }
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
        <style>{css}</style>
    </head>
    <body>
        <div class="slide">
            {"<div class='grid'></div>" if style == "cyber" else ""}
            {"<div class='bg-shapes'><div class='circle1'></div><div class='circle2'></div></div>" if style == "smart" else ""}
            
            <div class="content-box">
                {'''
                <div class="badge">AI GENERATED</div>
                <h2 class="title">Taipei & Himeji Sign Historic Friendship Pact</h2>
                <div class="flex">
                    <div class="text">Taipei Mayor Chiang Wan-an and Himeji Mayor Hideyasu Kiyomoto signed a friendship exchange agreement today. The pact focuses on youth talent cultivation, tourism marketing, and economic cooperation.</div>
                    <div class="img-container"><img src="file://''' + IMAGE_PATH + '''"></div>
                </div>
                ''' if style in ["cyber", "smart"] else '''
                <div class="text-side">
                    <span class="badge">DIGITAL GOVERNMENT</span>
                    <h2 class="title">Taipei & Himeji Sign Historic Friendship Pact</h2>
                    <div class="text">Taipei Mayor Chiang Wan-an and Himeji Mayor Hideyasu Kiyomoto signed a friendship exchange agreement today. The pact focuses on youth talent cultivation, tourism marketing, and economic cooperation.</div>
                    <div class="dots">...</div>
                </div>
                <div class="img-side">
                    <img src="file://''' + IMAGE_PATH + '''">
                    <div class="img-overlay"></div>
                </div>
                '''}
            </div>
        </div>
    </body>
    </html>
    """
    
    out_path = f"proto_{style}.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    
    for style in ["cyber", "smart", "neon"]:
        html_path = create_html(style, style)
        page.goto(f"file://{os.path.abspath(html_path)}")
        page.wait_for_timeout(1000)
        page.screenshot(path=f"proto_{style}.png")
        print(f"Generated proto_{style}.png")
        
    browser.close()
