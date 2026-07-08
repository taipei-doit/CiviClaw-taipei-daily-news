import sys
from pathlib import Path

# Add scripts directory and project root to path
SCRIPTS_DIR = Path(__file__).parent.resolve()
sys.path.append(str(SCRIPTS_DIR))
sys.path.append(str(SCRIPTS_DIR.parent))

from upload_youtube import get_authenticated_service, get_video_metadata, YOUTUBE_URL_FILE

def main():
    if not YOUTUBE_URL_FILE.exists():
        print("Error: latest_youtube_url.txt not found!")
        sys.exit(1)
        
    video_url = YOUTUBE_URL_FILE.read_text(encoding="utf-8").strip()
    print(f"Latest video URL: {video_url}")
    
    # Extract video ID
    video_id = None
    if "youtu.be/" in video_url:
        video_id = video_url.split("/")[-1].split("?")[0]
    elif "v=" in video_url:
        video_id = video_url.split("v=")[1].split("&")[0]
        
    if not video_id:
        print("Error: Could not extract video ID from URL")
        sys.exit(1)
        
    print(f"Detected Video ID: {video_id}")
    
    youtube = get_authenticated_service()
    if not youtube:
        print("Error: Authentication failed")
        sys.exit(1)
        
    title, desc = get_video_metadata()
    print("\n--- NEW METADATA ---")
    print(f"Title: {title}")
    print(f"Description (first 200 chars):\n{desc[:200]}...")
    print("---------------------\n")
    
    print("Updating video metadata on YouTube...")
    try:
        request = youtube.videos().update(
            part="snippet",
            body={
                "id": video_id,
                "snippet": {
                    "title": title,
                    "description": desc,
                    "categoryId": "25"  # News & Politics
                }
            }
        )
        response = request.execute()
        print("Successfully updated video on YouTube!")
        print(f"Video URL: https://www.youtube.com/watch?v={video_id}")
    except Exception as e:
        print(f"Error updating video on YouTube: {e}")

if __name__ == "__main__":
    main()
