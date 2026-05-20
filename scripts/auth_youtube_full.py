import os
import google_auth_oauthlib.flow
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]
CLIENT_SECRETS_FILE = Path.home() / "tw-gov-video" / "scripts" / "client_secrets.json"
CREDENTIALS_FILE = Path.home() / "tw-gov-video" / "scripts" / "youtube_credentials.json"

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    str(CLIENT_SECRETS_FILE), SCOPES)
creds = flow.run_local_server(port=8080, open_browser=False)

with open(str(CREDENTIALS_FILE), 'w') as token:
    token.write(creds.to_json())
print("Successfully authenticated and saved new credentials!")
