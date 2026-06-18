import asyncio
from playwright.async_api import async_playwright
import os

from config import OUTPUT_DIR

async def generate_pdf():
    html_file = OUTPUT_DIR / "CiviClaw_Presentation.html"
    html_path = f"file:///{html_file.absolute().as_posix()}"
    pdf_path = str((OUTPUT_DIR / "CiviClaw_Intro.pdf").absolute())
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Load the HTML
        await page.goto(html_path, wait_until="networkidle")
        
        # Give Mermaid diagrams a couple of seconds to render completely
        await page.wait_for_timeout(3000)
        
        # Save as PDF (landscape 1920x1080 approx -> A4 landscape or specific dimensions)
        # 1920px by 1080px is 16:9 ratio. 
        # width: 19.2in, height: 10.8in
        await page.pdf(
            path=pdf_path,
            width="19.2in",
            height="10.8in",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}
        )
        
        await browser.close()
        print(f"PDF generated successfully at {pdf_path}")

if __name__ == "__main__":
    asyncio.run(generate_pdf())