import sys
import re
from pathlib import Path

# Add scripts directory and project root to path
SCRIPTS_DIR = Path(__file__).parent.resolve()
sys.path.append(str(SCRIPTS_DIR))
sys.path.append(str(SCRIPTS_DIR.parent))

from upload_youtube import get_authenticated_service, PLAYLIST_ID

def update_text(text):
    if not text:
        return text
    # 1. 將 GovClaw 替換為 CiviClaw
    # 2. 將 GovClaw-taipei-daily-news 網址或名稱替換為 CiviClaw-taipei-daily-news
    # 3. 根據 Rex 的 commit 決策，不要更改 govclaw@gmail.com 郵件地址（如果有）
    
    # 暫時把 email 保護起來
    email_placeholder = "___EMAIL_PLACEHOLDER___"
    has_email = "govclaw@gmail.com" in text.lower()
    if has_email:
        # 不分大小寫替換 email 為 placeholder
        text = re.sub(re.escape("govclaw@gmail.com"), email_placeholder, text, flags=re.IGNORECASE)
    
    # 替換專案名稱與主品牌名
    text = re.sub(r"GovClaw", "CiviClaw", text)
    text = re.sub(r"govclaw", "civiclaw", text) # 處理全小寫情況
    
    # 還原 email
    if has_email:
        text = text.replace(email_placeholder, "govclaw@gmail.com")
        
    return text

def main():
    youtube = get_authenticated_service()
    if not youtube:
        print("Error: YouTube Authentication failed")
        sys.exit(1)
        
    print(f"Fetching videos from playlist: {PLAYLIST_ID}...")
    
    # 1. 取得 Playlist 下的所有影片
    video_ids = []
    next_page_token = None
    
    while True:
        try:
            req = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=PLAYLIST_ID,
                maxResults=50,
                pageToken=next_page_token
            )
            res = req.execute()
            
            for item in res.get("items", []):
                v_id = item.get("contentDetails", {}).get("videoId")
                if v_id:
                    video_ids.append(v_id)
                    
            next_page_token = res.get("nextPageToken")
            if not next_page_token:
                break
        except Exception as e:
            print(f"Error fetching playlist items: {e}")
            break
            
    if not video_ids:
        print("No videos found in the playlist.")
        sys.exit(0)
        
    print(f"Found {len(video_ids)} videos. Checking details and updating brand metadata...")
    
    updated_count = 0
    for idx, video_id in enumerate(video_ids, 1):
        print(f"\n[{idx}/{len(video_ids)}] Checking Video ID: {video_id}")
        try:
            # 取得詳細資訊
            v_req = youtube.videos().list(
                part="snippet",
                id=video_id
            )
            v_res = v_req.execute()
            
            items = v_res.get("items", [])
            if not items:
                print(f"  Warning: Video {video_id} info not found.")
                continue
                
            snippet = items[0]["snippet"]
            old_title = snippet.get("title", "")
            old_desc = snippet.get("description", "")
            category_id = snippet.get("categoryId", "25")
            
            new_title = update_text(old_title)
            new_desc = update_text(old_desc)
            
            if old_title != new_title or old_desc != new_desc:
                print(f"  -> Brand mismatch detected! Preparing update...")
                if old_title != new_title:
                    print(f"     Old Title: {old_title}")
                    print(f"     New Title: {new_title}")
                if "GovClaw" in old_desc or "govclaw" in old_desc:
                    print(f"     Description needs updates (found old brand name)")
                
                # 執行更新
                update_req = youtube.videos().update(
                    part="snippet",
                    body={
                        "id": video_id,
                        "snippet": {
                            "title": new_title,
                            "description": new_desc,
                            "categoryId": category_id
                        }
                    }
                )
                update_req.execute()
                print(f"  ✅ Video {video_id} updated successfully!")
                updated_count += 1
            else:
                print(f"  ✨ Video {video_id} is already up to date (no brand mismatch).")
                
        except Exception as e:
            print(f"  ❌ Error processing video {video_id}: {e}")
            
    print(f"\n🎉 Batch Update Finished! Total videos updated: {updated_count}")

if __name__ == "__main__":
    main()
