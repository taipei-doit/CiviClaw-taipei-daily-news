import json
import urllib.request

API_KEY = "sk_dab768322eb97d8789551989fba23b6ce5ddbdf3e85d847e"
VOICE_ID = "4mU4AFOhdaBEWGnnBxL8"

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": API_KEY
}
data = {
    "text": "こんにちは、これはバージョン3のテストです。",
    "model_id": "eleven_multilingual_v2", # testing availability
}

# Just a quick check to see if v3 is allowed for your account tier/voice
data_v3 = data.copy()
data_v3["model_id"] = "eleven_multilingual_v3"

req = urllib.request.Request(url, data=json.dumps(data_v3).encode('utf-8'), headers=headers, method="POST")
try:
    with urllib.request.urlopen(req) as response:
        print("Success! v3 is available.")
except Exception as e:
    if hasattr(e, 'read'):
        print(f"Error reading v3: {e.read().decode('utf-8')}")
    else:
        print(f"Error: {e}")
