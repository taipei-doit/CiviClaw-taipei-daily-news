import os
import json
import base64
import html
from datetime import datetime
from config import BASE_DIR as BASE, OUTPUT_DIR, INPUT_JSON, YOUTUBE_URL_FILE
WEB_DIR = BASE / "docs"

LINE_FRIEND_LINK = "https://page.line.me/290wqpej"

def main():
    if not WEB_DIR.exists():
        WEB_DIR.mkdir(parents=True, exist_ok=True)
        
    if not INPUT_JSON.exists():
        print("No articles found to build website.")
        return

    data = json.loads(INPUT_JSON.read_text(encoding="utf-8"))
    items = data.get("selected", [])
    today = datetime.now().strftime("%Y-%m-%d")
    
    youtube_url = "#"
    youtube_embed = ""
    if YOUTUBE_URL_FILE.exists():
        youtube_url = YOUTUBE_URL_FILE.read_text().strip()
        if "watch?v=" in youtube_url:
            video_id = youtube_url.split("watch?v=")[1].split("&")[0]
            youtube_embed = f"""
            <div class="video-container">
                <iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            </div>
            """
    
    page = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>臺北市政府每日新聞摘要 - {today}</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Noto Sans TC', sans-serif;
            background-color: #f8f9fa;
            color: #2c3e50;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }}
        .header h1 {{ margin: 0; font-size: 2.5rem; }}
        .header p {{ margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9; }}
        .line-promo {{
            background: #00B900;
            color: white;
            text-align: center;
            padding: 15px;
            font-weight: bold;
            font-size: 1.1rem;
        }}
        .line-promo a {{
            color: white;
            text-decoration: underline;
        }}
        
        .container {{
            max-width: 900px;
            margin: 40px auto;
            padding: 0 20px;
        }}
        
        .video-container {{
            position: relative;
            padding-bottom: 56.25%; /* 16:9 */
            height: 0;
            overflow: hidden;
            border-radius: 12px;
            margin-bottom: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            background: #000;
        }}
        .video-container iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }}
        
        .article-card {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            padding: 30px;
            margin-bottom: 30px;
            border-left: 5px solid #e74c3c;
        }}
        
        .article-title {{
            font-size: 1.8rem;
            color: #2c3e50;
            margin-top: 0;
            margin-bottom: 20px;
            font-weight: 900;
        }}
        
        .label {{
            font-weight: bold;
            color: #e74c3c;
            font-size: 1.1rem;
            margin-bottom: 10px;
            text-transform: uppercase;
        }}
        
        .script-box {{
            background: #fdfaf6;
            padding: 20px;
            border-radius: 8px;
            font-size: 1.2rem;
            color: #34495e;
            margin-bottom: 20px;
            border: 1px solid #eee;
        }}
        
        .btn {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            transition: background 0.2s;
        }}
        .btn:hover {{ background: #2980b9; }}
        
        .carousel {{
            position: relative;
            width: 100%;
            margin-top: 20px;
            border-radius: 8px;
            overflow: hidden;
            background: #eee;
        }}
        .carousel-images {{
            display: flex;
            transition: transform 0.5s ease-in-out;
            width: 100%;
        }}
        .carousel-images img {{
            width: 100%;
            flex-shrink: 0;
            object-fit: cover;
        }}
        .carousel-btn {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(0,0,0,0.5);
            color: white;
            border: none;
            cursor: pointer;
            padding: 10px 15px;
            font-size: 1.5rem;
            border-radius: 5px;
            z-index: 10;
        }}
        .carousel-btn:hover {{ background: rgba(0,0,0,0.8); }}
        .carousel-prev {{ left: 10px; }}
        .carousel-next {{ right: 10px; }}
        .carousel-indicators {{
            position: absolute;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 5px;
            z-index: 10;
        }}
        .indicator {{
            width: 10px;
            height: 10px;
            background: rgba(255,255,255,0.5);
            border-radius: 50%;
            cursor: pointer;
        }}
        .indicator.active {{ background: white; }}
        
        .img-container {{
            margin-top: 20px;
            border-radius: 8px;
            overflow: hidden;
            background: #eee;
            position: relative;
        }}
        .img-container img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .ai-watermark {{
            position: absolute;
            bottom: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.8rem;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 50px 20px;
            margin-top: 50px;
        }}
        .footer-content {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 40px;
            max-width: 900px;
            margin: 0 auto;
            flex-wrap: wrap;
        }}
        .footer-section {{
            flex: 1;
            min-width: 300px;
        }}
        .footer-divider {{
            width: 1px;
            height: 250px;
            background-color: #4a5d70;
            display: none;
        }}
        @media (min-width: 768px) {{
            .footer-divider {{
                display: block;
            }}
        }}
        .footer img {{
            width: 150px;
            border-radius: 10px;
            margin: 20px 0;
            border: 4px solid white;
        }}
    </style>
</head>
<body>
    <div class="line-promo">
        📱 訂閱我們的 LINE 官方帳號，每天自動接收最新臺北市政摘要！ <a href="{LINE_FRIEND_LINK}" target="_blank">點此加入好友</a>
    </div>
    <div class="header">
        <h1>臺北市政府新聞摘要</h1>
        <p>{today} - 每日為您整理五大重點新聞</p>
    </div>
    
    <div class="container">
        {youtube_embed}
        <div style="text-align: center; margin-bottom: 30px;">
            <a href="https://www.youtube.com/@CiviClaw-TP" target="_blank" class="btn" style="background: #e74c3c;">📺 訂閱我們的 YouTube 頻道</a>
        </div>
"""
    
    for idx, item in enumerate(items):
        title = html.escape(item.get("title", ""))
        script = html.escape(item.get("script", ""))
        reason = html.escape(item.get("reason", ""))
        source_url = html.escape(item.get("source_url", "#"))
        img_url = item.get("image_url", "")
        image_urls = item.get("image_urls", [])
        is_ai = item.get("is_ai_generated", False)
        
        if not image_urls and img_url:
            image_urls = [img_url]
            
        img_html = ""
        # Remove duplicate image URLs and only keep http links, UNLESS it's our local AI image
        clean_urls = []
        for u in image_urls:
            if u.startswith("http"):
                if u not in clean_urls:
                    clean_urls.append(u)
            elif "ai_article" in u:
                # Local AI image - convert to base64 so we can embed it directly in the HTML
                try:
                    with open(u.replace("file://", ""), "rb") as f:
                        b64_data = base64.b64encode(f.read()).decode()
                        clean_urls.append(f"data:image/png;base64,{b64_data}")
                except Exception as e:
                    print(f"Could not load AI image {u}: {e}")
                    
        image_urls = clean_urls
        
        if len(image_urls) > 1:
            img_html = f"""
            <div class="carousel" id="carousel-{idx}">
                <button class="carousel-btn carousel-prev" onclick="moveCarousel({idx}, -1)">&#10094;</button>
                <button class="carousel-btn carousel-next" onclick="moveCarousel({idx}, 1)">&#10095;</button>
                <div class="carousel-images" id="images-{idx}">
            """
            for i, u in enumerate(image_urls):
                img_html += f'<img src="{u}" alt="News Image {i+1}">'
            
            img_html += f"""
                </div>
                <div class="carousel-indicators" id="indicators-{idx}">
            """
            for i in range(len(image_urls)):
                active = "active" if i == 0 else ""
                img_html += f'<div class="indicator {active}" onclick="setCarousel({idx}, {i})"></div>'
            img_html += """
                </div>
            </div>
            """
        elif len(image_urls) == 1:
            watermark = '<div class="ai-watermark">本圖片由AI自動生成</div>' if is_ai else ''
            img_html = f"""
            <div class="img-container">
                <img src="{image_urls[0]}" alt="News Image">
                {watermark}
            </div>
            """
            
        page += f"""
        <div class="article-card">
            <h2 class="article-title">{idx+1}. {title}</h2>
            
            <div class="label">播報稿 / 引用重點</div>
            <div class="script-box">{script}</div>
            
            <p><strong>選錄原因：</strong>{reason}</p>
            
            <a href="{source_url}" target="_blank" class="btn">查看官方原文與聯絡人</a>
            {img_html}
        </div>
"""

    page += f"""
    </div>

    <div class="footer">
        <div class="footer-content">
            <div class="footer-section">
                <h2>掃描加入 LINE 好友</h2>
                <p>掌握臺北市大小事，重點新聞不漏接！</p>
                <img src="line_qr.png" alt="LINE QR Code">
                <br>
                <a href="{LINE_FRIEND_LINK}" style="color: #3498db; font-size: 1.2rem; text-decoration: none; font-weight: bold;">或點擊此處直接加入</a>
            </div>
            
            <div class="footer-divider"></div>
            
            <div class="footer-section">
                <h2>收聽 Podcast 每日摘要</h2>
                <p>通勤時間用聽的，市政重點不漏接！</p>
                <img src="spotify_qr.png" alt="Spotify QR Code">
                <br>
                <a href="https://open.spotify.com/show/033jJtZiN097aPxw99mHYW" target="_blank" style="color: #1DB954; font-size: 1.2rem; text-decoration: none; font-weight: bold;">或點擊此處前往 Spotify 收聽</a>
            </div>
        </div>
    </div>

    <script>
        const carousels = {{}};
        
        function initCarousels() {{
            document.querySelectorAll('.carousel').forEach(c => {{
                const id = c.id.split('-')[1];
                carousels[id] = 0;
            }});
        }}
        
        function updateCarousel(id) {{
            const images = document.getElementById(`images-${{id}}`);
            const indicators = document.getElementById(`indicators-${{id}}`).children;
            const index = carousels[id];
            
            images.style.transform = `translateX(-${{index * 100}}%)`;
            
            for (let i = 0; i < indicators.length; i++) {{
                indicators[i].classList.remove('active');
            }}
            indicators[index].classList.add('active');
        }}
        
        function moveCarousel(id, direction) {{
            const total = document.getElementById(`images-${{id}}`).children.length;
            carousels[id] += direction;
            if (carousels[id] >= total) carousels[id] = 0;
            if (carousels[id] < 0) carousels[id] = total - 1;
            updateCarousel(id);
        }}
        
        function setCarousel(id, index) {{
            carousels[id] = index;
            updateCarousel(id);
        }}
        
        window.onload = initCarousels;
    </script>
</body>
</html>
"""

    index_path = WEB_DIR / "index.html"
    archive1_path = WEB_DIR / "archive1.html"
    archive2_path = WEB_DIR / "archive2.html"
    
    # Rotate archives ONLY if the content actually changes (prevents manual testing from wiping archives)
    should_rotate = False
    if index_path.exists():
        try:
            existing_html = index_path.read_text(encoding="utf-8")
            # We check if the first article title in the existing HTML matches the one we are about to generate
            first_article_title = items[0].get("title", "")
            if first_article_title not in existing_html:
                should_rotate = True
        except Exception:
            should_rotate = True
            
    if should_rotate:
        if archive1_path.exists():
            archive1_path.replace(archive2_path)
        index_path.replace(archive1_path)
        
    # Inject Pagination Buttons into HTML before writing
    pagination_html = """
    <div style="text-align: center; margin: 40px 0;">
        <h3>歷史回顧</h3>
        <a href="index.html" class="btn pagination-btn">今日新聞</a>
        <a href="archive1.html" class="btn pagination-btn">昨日新聞</a>
        <a href="archive2.html" class="btn pagination-btn">前日新聞</a>

    <script>
        // Set active pagination button based on current URL
        document.addEventListener("DOMContentLoaded", function() {
            let currentPath = window.location.pathname.split('/').pop();
            if (!currentPath) currentPath = 'index.html'; // Default to index
            
            document.querySelectorAll('.pagination-btn').forEach(btn => {
                if (btn.getAttribute('href') === currentPath) {
                    btn.style.background = '#e74c3c';
                } else {
                    btn.style.background = '#3498db';
                }
            });
        });
    </script>

    </div>
    """
    
    page = page.replace('</div>\n\n    <div class="footer">', pagination_html + '</div>\n    <div class="footer">')

    index_path.write_text(page, encoding="utf-8")
    
    # Create empty placeholders if archives don't exist
    placeholder_html = """<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="UTF-8"><title>即將更新</title>
    <style>body{font-family:sans-serif;text-align:center;padding:50px;} .btn{display:inline-block;background:#3498db;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;margin:10px;}</style></head>
    <body><h2>歷史資料即將更新 (Will update soon)</h2>
    <a href="index.html" class="btn">返回今日新聞</a></body></html>"""
    
    if not archive1_path.exists():
        archive1_path.write_text(placeholder_html, encoding="utf-8")
    if not archive2_path.exists():
        archive2_path.write_text(placeholder_html, encoding="utf-8")

    print(f"Web portal successfully generated at {index_path}")

if __name__ == "__main__":
    main()
