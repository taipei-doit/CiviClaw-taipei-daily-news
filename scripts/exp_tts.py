import json
import base64
import time
import subprocess
import urllib.request
import urllib.error
import google.auth
import google.auth.transport.requests
from pathlib import Path

BASE = Path.home() / "tw-gov-video"
OUTPUT_DIR = BASE / "output"

credentials, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
PROJECT_ID = project or "doit-dic-itteam"

def synthesize_text(text, voice, out_file):
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
    token = credentials.token

    url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/us-central1/publishers/google/models/gemini-3.1-flash-tts-preview:generateContent"

    payload = {
        "contents": [{"role": "user", "parts": [{"text": text}]}],
        "generationConfig": {
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": voice
                    }
                }
            }
        }
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            part = res['candidates'][0]['content']['parts'][0]
            if 'inlineData' in part:
                b64_audio = part['inlineData']['data']
                wav_path = str(out_file).replace('.mp3', '.wav')
                with open(wav_path, "wb") as f:
                    f.write(base64.b64decode(b64_audio))
                
                mime = part['inlineData']['mimeType']
                if 'audio/l16' in mime:
                    subprocess.run(f"ffmpeg -y -f s16le -ar 24000 -ac 1 -i {wav_path} -codec:a libmp3lame -qscale:a 2 {out_file}", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    subprocess.run(f"ffmpeg -y -i {wav_path} -codec:a libmp3lame -qscale:a 2 {out_file}", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                print(f"Saved TTS audio to {out_file}")
                return True
            else:
                return False
    except Exception as e:
        print(f"Failed to synthesize: {e}")
        return False

def main():
    en_text = "Recently, officers from the Daan Precinct's Anhe Road Police Station successfully rescued a disoriented, elderly man suffering from dementia who wandered into heavy traffic, safely escorting him home. The police urge the public to pay closer attention to elderly family members to prevent them from wandering off."
    ja_text = "最近、大安警察署の安和路派出所の警察官が、交通量の多い道路に迷い込んだ認知症の高齢男性を無事に救出し、安全に自宅まで送り届けました。警察は、徘徊を防ぐために高齢の家族にさらに注意を払うよう呼びかけています。"
    
    # Aoede for English/multilingual (or Puck)
    synthesize_text(en_text, "Aoede", OUTPUT_DIR / "exp_en.mp3")
    synthesize_text(ja_text, "Aoede", OUTPUT_DIR / "exp_ja.mp3")

if __name__ == "__main__":
    main()
