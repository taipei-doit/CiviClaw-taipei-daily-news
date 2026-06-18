import os
from googleapiclient.discovery import build
import google_auth_oauthlib.flow
import google.oauth2.credentials
import google.auth.transport.requests

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
from config import BASE_DIR
CLIENT_SECRETS_FILE = str(BASE_DIR / "scripts" / "client_secrets.json")
CREDENTIALS_FILE = str(BASE_DIR / "scripts" / "youtube_credentials.json")

def get_authenticated_service():
    creds = None
    if os.path.exists(CREDENTIALS_FILE):
        creds = google.oauth2.credentials.Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing token...")
            creds.refresh(google.auth.transport.requests.Request())
        else:
            print("Fetching new token...")
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080, open_browser=False)
            
            with open(CREDENTIALS_FILE, 'w') as token:
                token.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)

get_authenticated_service()
print("Success!")
