const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  
  const htmlPath = 'file://' + path.resolve('/home/benliangcs/tw-gov-video/output/slides_playwright.html');
  console.log(`Loading: ${htmlPath}`);
  
  await page.goto(htmlPath);
  
  // Wait for fonts to load
  await page.evaluate(() => document.fonts.ready);
  
  await page.evaluate("showSlide('slide_intro')");
  await page.waitForTimeout(2000); // wait for animation
  await page.screenshot({ path: '/home/benliangcs/tw-gov-video/output/pw_intro.png' });
  console.log("Intro screenshot captured.");
  
  await browser.close();
})();
