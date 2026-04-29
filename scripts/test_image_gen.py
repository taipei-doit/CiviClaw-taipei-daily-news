import json
import base64
import urllib.request
import urllib.error
from pathlib import Path
import google.auth
import google.auth.transport.requests

BASE = Path.home() / "tw-gov-video"
OUTPUT_DIR = BASE / "output"
NEWS_JSON = OUTPUT_DIR / "news_12pm.json"

credentials, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
PROJECT_ID = project or "doit-dic-itteam"

def get_clean_visual_prompt(title, token):
    url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/us-central1/publishers/google/models/gemini-2.5-flash:generateContent"
    system_instruction = "You are a stock photo assistant. Read the news headline and output a very short 2 to 5 word English description of a purely visual, generic background scene or macro object related to the topic. CRITICAL RULES: The scene MUST NOT contain people, screens, text, banners, or signs. Just a clean landscape, architectural detail, or object. Examples: 'empty modern hospital hallway', 'close up of green leaves', 'electric car charging plug', 'empty city intersection'. Output ONLY the short English phrase, nothing else."
    payload = {
        "contents": [{"role": "user", "parts": [{"text": f"Headline: {title}"}]}],
        "systemInstruction": {"parts": [{"text": system_instruction}]}
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json; charset=utf-8")
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            return res['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        print(f"Gemini error: {e}")
        return "news event"

def generate_image(clean_subject, out_path, token):
    url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/us-central1/publishers/google/models/imagen-3.0-generate-002:predict"
    req = urllib.request.Request(url, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json; charset=utf-8")
    strict_prompt = f"A photorealistic news press photo about: {clean_subject}. CRITICAL RULE: NO TEXT, NO WRITING, NO CHARACTERS, NO WORDS, NO LOGOS, NO SIGNS. ONLY pure imagery."
    payload = {
        "instances": [{"prompt": strict_prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "16:9",
            "outputOptions": {"mimeType": "image/png"}
        }
    }
    data = json.dumps(payload).encode('utf-8')
    try:
        with urllib.request.urlopen(req, data=data) as response:
            result = json.loads(response.read().decode('utf-8'))
            b64_img = result['predictions'][0]['bytesBase64Encoded']
            with open(out_path, "wb") as f:
                f.write(base64.b64decode(b64_img))
            return True
    except Exception as e:
        print(f"Imagen error: {e}")
        return False

def main():
    data = json.loads(NEWS_JSON.read_text(encoding="utf-8-sig"))
    imageless_articles = [item for item in data if not item.get("相關圖片")]
    target_articles = imageless_articles[:5]
    
    credentials.refresh(google.auth.transport.requests.Request())
    token = credentials.token
    
    results = []
    for i, article in enumerate(target_articles):
        title = article.get("title", "")
        out_path = OUTPUT_DIR / f"test_ai_img_{i}.png"
        clean_prompt = get_clean_visual_prompt(title, token)
        print(f"[{i+1}/5] Article: {title}\n      -> Prompt: {clean_prompt}")
        if generate_image(clean_prompt, out_path, token):
            results.append((title, clean_prompt, out_path))
            
    curl_cmd = ['curl']
    content = "Here are 5 purely AI-generated images for articles that had no official photos, generated safely without touching the main pipeline:\\n\\n"
    for i, (title, prompt, path) in enumerate(results):
        content += f"**{i+1}. {title}**\\n*Gemini Extracted Subject:* `{prompt}`\\n\\n"
    
    payload_json = json.dumps({"content": content})
    curl_cmd.extend(['-F', f"payload_json={payload_json}"])
    
    for i, (title, prompt, path) in enumerate(results):
        curl_cmd.extend(['-F', f"file{i+1}=@{path}"])
        
    curl_cmd.append('https://discord.com/api/webhooks/1489170065638035509/zC-HrxYHUdOwIjvhDrusT0I6HmQkF6kTyHsmew7cmPLSIesOgJ9ORvsSlF-s5pz0IZJ6')
    
    with open(OUTPUT_DIR / "run_test_curl.sh", "w") as f:
        f.write(" ".join(curl_cmd))

if __name__ == "__main__":
    main()
