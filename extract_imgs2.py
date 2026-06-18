import urllib.request
import re

urls = [
    "https://www.gov.taipei/News_Content.aspx?n=2044902FC839D045&sms=72544237BBE4C5F6&s=145108D13F476FF9",
    "https://www.gov.taipei/News_Content.aspx?n=2044902FC839D045&sms=72544237BBE4C5F6&s=B4282508654FDFF1",
    "https://www.gov.taipei/News_Content.aspx?n=F0DDAF49B89E9413&s=DDA779781380304A"
]

for i, url in enumerate(urls):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'data-src="(https://www-ws\.gov\.taipei/[^"]+\.jpg)"', html)
    if not match:
        match = re.search(r'data-src="(https://www-ws\.gov\.taipei/[^"]+\.png)"', html)
    if match:
        print(f"IMG {i+1}: {match.group(1)}")
    else:
        print(f"IMG {i+1}: NOT FOUND")
