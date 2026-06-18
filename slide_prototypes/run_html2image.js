const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  
  for (const style of ['glass', 'darktech']) {
      await page.goto('file://' + path.resolve(__dirname, `proto_premium_${style}.html`));
      await page.waitForTimeout(1000);
      await page.screenshot({ path: path.resolve(__dirname, `proto_premium_${style}.png`) });
  }
  await browser.close();
})();
