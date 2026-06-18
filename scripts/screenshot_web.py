from playwright.sync_api import sync_playwright
import os

from config import BASE_DIR, OUTPUT_DIR
html_path = f"file:///{str((BASE_DIR / 'docs' / 'index.html').absolute()).replace('\\', '/')}"
out_path = str((OUTPUT_DIR / 'web_preview.png').absolute())

with sync_playwright() as p:
    # Use a mobile viewport size to show how it looks on a phone
    browser = p.chromium.launch(args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = browser.new_page(viewport={"width": 414, "height": 896}) 
    page.goto(html_path)
    page.wait_for_timeout(1000)
    page.screenshot(path=out_path, full_page=True)
    browser.close()
    print(f"Screenshot saved to {out_path}")
