from playwright.sync_api import sync_playwright
import os

IMAGE_PATH = "/home/benliangcs/.openclaw/media/inbound/84fd2a38-b495-47b4-938d-92671b39a55b.png"

def create_premium_html(style, filename):
    if style == "glass":
        # Glassmorphism, very Apple/Modern Smart City
        css = """
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;500;700;900&family=Outfit:wght@400;700&display=swap');
        body { margin: 0; padding: 0; width: 1920px; height: 1080px; overflow: hidden; background: #eef2f6; font-family: 'Noto Sans TC', sans-serif; }
        .bg { position: absolute; top:0; left:0; width:100%; height:100%; z-index: 0; overflow: hidden; }
        .orb1 { position: absolute; width: 1000px; height: 1000px; background: radial-gradient(circle, rgba(66,133,244,0.3) 0%, rgba(0,0,0,0) 70%); top: -300px; left: -200px; border-radius: 50%; filter: blur(60px); }
        .orb2 { position: absolute; width: 1200px; height: 1200px; background: radial-gradient(circle, rgba(15,157,88,0.2) 0%, rgba(0,0,0,0) 70%); bottom: -400px; right: -200px; border-radius: 50%; filter: blur(80px); }
        .orb3 { position: absolute; width: 800px; height: 800px; background: radial-gradient(circle, rgba(219,68,55,0.15) 0%, rgba(0,0,0,0) 70%); top: 200px; right: 300px; border-radius: 50%; filter: blur(50px); }
        
        .container { position: absolute; top: 0; left: 0; width: 1920px; height: 1080px; padding: 100px; box-sizing: border-box; z-index: 10; display: flex; flex-direction: column; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }
        .badge { font-family: 'Outfit', sans-serif; background: linear-gradient(135deg, #4285f4, #0f9d58); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700; font-size: 32px; letter-spacing: 4px; }
        .logo-text { font-family: 'Outfit', sans-serif; font-size: 28px; font-weight: 700; color: #5f6368; letter-spacing: 2px; }
        
        .glass-panel { flex: 1; background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(40px); -webkit-backdrop-filter: blur(40px); border: 1px solid rgba(255, 255, 255, 0.8); border-radius: 40px; box-shadow: 0 30px 60px rgba(0,0,0,0.08), inset 0 0 0 2px rgba(255,255,255,0.5); display: flex; overflow: hidden; padding: 60px; gap: 60px; }
        
        .content { flex: 1.2; display: flex; flex-direction: column; justify-content: center; }
        h1 { font-size: 65px; font-weight: 900; color: #1f2937; line-height: 1.2; margin-top: 0; margin-bottom: 30px; letter-spacing: -1px; }
        .highlight { color: #4285f4; }
        p { font-size: 42px; font-weight: 300; color: #4b5563; line-height: 1.6; margin: 0; }
        
        .image-wrapper { flex: 1; position: relative; border-radius: 30px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.15); border: 8px solid rgba(255,255,255,0.8); }
        img { width: 100%; height: 100%; object-fit: cover; }
        """
        html = f"""
        <html><head><style>{css}</style></head><body>
            <div class="bg"><div class="orb1"></div><div class="orb2"></div><div class="orb3"></div></div>
            <div class="container">
                <div class="header">
                    <div class="badge">SMART CITY VISION</div>
                    <div class="logo-text">TAIPEI GOV AI</div>
                </div>
                <div class="glass-panel">
                    <div class="content">
                        <h1>Taipei & Himeji Sign <br><span class="highlight">Historic Friendship Pact</span></h1>
                        <p>Taipei Mayor Chiang Wan-an and Himeji Mayor Hideyasu Kiyomoto signed a friendship exchange agreement today. The pact focuses on youth talent cultivation, tourism marketing, and economic cooperation.</p>
                    </div>
                    <div class="image-wrapper"><img src="file://{IMAGE_PATH}"></div>
                </div>
            </div>
        </body></html>
        """
    else:
        # Dark Tech/Futuristic
        css = """
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;500;700;900&family=Space+Grotesk:wght@400;700&display=swap');
        body { margin: 0; padding: 0; width: 1920px; height: 1080px; overflow: hidden; background: #05070a; font-family: 'Noto Sans TC', sans-serif; }
        .grid { position: absolute; width: 100%; height: 100%; background-image: radial-gradient(#1e3a8a 1px, transparent 1px); background-size: 30px 30px; opacity: 0.3; }
        .glow { position: absolute; width: 100%; height: 100%; background: radial-gradient(circle at 80% 50%, rgba(37,99,235,0.15) 0%, rgba(0,0,0,0) 60%); }
        
        .layout { display: flex; width: 100%; height: 100%; position: relative; z-index: 10; }
        .text-col { flex: 1.1; padding: 100px; display: flex; flex-direction: column; justify-content: center; position: relative; }
        
        .tagline { display: flex; align-items: center; gap: 20px; margin-bottom: 30px; }
        .line { width: 60px; height: 3px; background: #3b82f6; box-shadow: 0 0 10px #3b82f6; }
        .tag { font-family: 'Space Grotesk', sans-serif; color: #60a5fa; font-size: 24px; font-weight: 700; letter-spacing: 5px; }
        
        h1 { font-size: 70px; font-weight: 900; color: #ffffff; line-height: 1.2; margin: 0 0 40px 0; }
        p { font-size: 40px; font-weight: 300; color: #9ca3af; line-height: 1.7; border-left: 4px solid #3b82f6; padding-left: 30px; }
        
        .img-col { flex: 1; position: relative; padding: 80px 80px 80px 0; }
        .img-frame { width: 100%; height: 100%; position: relative; border-radius: 20px; overflow: hidden; border: 1px solid rgba(59,130,246,0.3); box-shadow: 0 0 50px rgba(37,99,235,0.2); }
        .img-frame::after { content: ''; position: absolute; inset: 0; box-shadow: inset 0 0 100px #05070a; pointer-events: none; }
        img { width: 100%; height: 100%; object-fit: cover; opacity: 0.9; filter: contrast(1.1) brightness(1.1); }
        
        .ui-element { position: absolute; font-family: 'Space Grotesk', sans-serif; color: #3b82f6; font-size: 14px; letter-spacing: 2px; }
        .ui-1 { top: 50px; left: 100px; }
        .ui-2 { bottom: 50px; right: 100px; }
        """
        html = f"""
        <html><head><style>{css}</style></head><body>
            <div class="grid"></div><div class="glow"></div>
            <div class="ui-element ui-1">SYS.OP.2026 // TPE_GOV_AI</div>
            <div class="ui-element ui-2">DATA_LINK_ACTIVE</div>
            <div class="layout">
                <div class="text-col">
                    <div class="tagline"><div class="line"></div><div class="tag">DIGITAL GOVERNMENT</div></div>
                    <h1>Taipei & Himeji Sign Historic Friendship Pact</h1>
                    <p>Taipei Mayor Chiang Wan-an and Himeji Mayor Hideyasu Kiyomoto signed a friendship exchange agreement today. The pact focuses on youth talent cultivation, tourism marketing, and economic cooperation.</p>
                </div>
                <div class="img-col">
                    <div class="img-frame"><img src="file://{IMAGE_PATH}"></div>
                </div>
            </div>
        </body></html>
        """
    
    out_path = f"proto_premium_{style}.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    
    for style in ["glass", "darktech"]:
        html_path = create_premium_html(style, style)
        page.goto(f"file://{os.path.abspath(html_path)}")
        page.wait_for_timeout(1000)
        page.screenshot(path=f"proto_premium_{style}.png")
        print(f"Generated proto_premium_{style}.png")
        
    browser.close()
