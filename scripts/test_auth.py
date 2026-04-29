import google.auth
import google.auth.transport.requests

credentials, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
credentials.refresh(google.auth.transport.requests.Request())
print("Token:", credentials.token[:10])
print("Project:", project)
