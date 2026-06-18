import urllib.request
import json

API_KEY = "sk_dab768322eb97d8789551989fba23b6ce5ddbdf3e85d847e"
url = "https://api.elevenlabs.io/v1/models"
req = urllib.request.Request(url, headers={"xi-api-key": API_KEY})
try:
    with urllib.request.urlopen(req) as response:
        models = json.loads(response.read().decode('utf-8'))
        for m in models:
            print(f"- {m['model_id']}: {m['name']}")
except Exception as e:
    print(f"Error: {e}")
