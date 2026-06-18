from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    
    for style in ["glass", "darktech"]:
        html_path = f"proto_premium_{style}.html"
        page.goto(f"file://{os.path.abspath(html_path)}")
        page.wait_for_timeout(1000)
        page.screenshot(path=f"proto_premium_{style}.png")
        print(f"Generated proto_premium_{style}.png")
        
    browser.close()
