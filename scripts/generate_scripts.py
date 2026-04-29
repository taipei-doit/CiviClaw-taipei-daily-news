import json
import google.auth
import google.auth.transport.requests
import urllib.request
from pathlib import Path

credentials, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
credentials.refresh(google.auth.transport.requests.Request())
token = credentials.token

PROJECT_ID = project or "doit-dic-itteam"
LOCATION = "us-central1"
URL = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/gemini-2.5-flash:generateContent"

def ask_gemini(article):
    prompt = f"""
    You are an expert Taiwanese news anchor for the Taipei City Government.
    Analyze the following government press release and write a short, engaging voiceover script.
    
    CRITICAL RULES:
    1. The script MUST be exactly 2 to 4 sentences long. Target around 80 to 120 Chinese characters, providing a good balance of detail without overflowing the screen. Do not write a massive paragraph.
    2. DO NOT use trailing ellipses "..." or cut off mid-sentence.
    3. Write entirely in natural Traditional Chinese (zh-TW).
    4. Provide a 1 sentence "reason" (選錄原因) explaining why this news is important. Keep it under 25 Chinese characters. DO NOT use generic templates like "Top news item selected for relevance". Write the actual, specific reason concisely.
    
    Return ONLY a valid JSON object with EXACTLY these two keys: "script" and "reason".
    
    TITLE: {article.get('title')}
    CONTENT: {article.get('內容')}
    """
    
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2}
    }
    
    req = urllib.request.Request(URL, data=json.dumps(payload).encode('utf-8'), method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json; charset=utf-8")
    
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            text = res['candidates'][0]['content']['parts'][0]['text'].strip()
            if text.startswith("```json"): text = text[7:]
            if text.endswith("```"): text = text[:-3]
            return json.loads(text)
    except Exception as e:
        print(e)
        return {"script": f"為您播報：{article.get('title')}。詳情請見臺北市政府官網。", "reason": "市政動態更新。"}

def main():
    data = json.loads(Path("/home/benliangcs/tw-gov-video/output/top_5.json").read_text())
    
    out = []
    for item in data:
        print(f"Generating script for: {item.get('title')}")
        result = ask_gemini(item)
        
        image_url = ""
        pics = item.get("相關圖片", [])
        if pics and len(pics) > 0:
            image_url = pics[0].get("url", "")
            
        out.append({
            "title": item.get("title", ""),
            "script": result.get("script", ""),
            "reason": result.get("reason", ""),
            "source_url": item.get("Source", ""),
            "DataSN": item.get("DataSN", ""),
            "image_url": image_url,
            "is_ai_generated": False if image_url else True
        })
        
    Path("/home/benliangcs/tw-gov-video/output/selected_articles.json").write_text(
        json.dumps({"selected": out}, ensure_ascii=False, indent=2), encoding="utf-8"
    )

if __name__ == "__main__":
    main()
