import urllib.request
from bs4 import BeautifulSoup
import json

urls = [
    "https://www.gov.taipei/News_Content.aspx?n=2044902FC839D045&sms=72544237BBE4C5F6&s=145108D13F476FF9",
    "https://www.gov.taipei/News_Content.aspx?n=2044902FC839D045&sms=72544237BBE4C5F6&s=B4282508654FDFF1",
    "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=DDA779781380304A"
]

results = []
for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Get title
        title_tag = soup.find('h2', {'class': 'title'})
        title = title_tag.text.strip() if title_tag else soup.title.text.strip()
        
        # Get content
        content_div = soup.find('div', {'class': 'article'}) or soup.find('div', id='pnl_content') or soup.find('div', {'class': 'content'})
        content = content_div.text.strip() if content_div else "No content"
        
        # Get image
        img_url = ""
        img_tag = soup.find('img', {'class': 'Isimg'}) or soup.select_first('.article img') or soup.select_first('.pic img')
        if img_tag and img_tag.get('src'):
            src = img_tag['src']
            if not src.startswith('http'):
                src = 'https://www.gov.taipei/' + src.lstrip('/')
            img_url = src
            
        results.append({
            "url": url,
            "title": title,
            "content": content[:500] + "...", # truncate for summary
            "img_url": img_url
        })
    except Exception as e:
        results.append({"url": url, "error": str(e)})

print(json.dumps(results, indent=2, ensure_ascii=False))
