import sys
import re
from pathlib import Path

# Add scripts directory and project root to path
SCRIPTS_DIR = Path(__file__).parent.resolve()
sys.path.append(str(SCRIPTS_DIR))
sys.path.append(str(SCRIPTS_DIR.parent))

from upload_youtube import get_authenticated_service, PLAYLIST_ID

def clean_line_promo(text):
    if not text:
        return text
    
    # 1. 移除 LINE 好友連結 (不分大小寫)
    text = re.sub(r"https?://page\.line\.me/290wqpej\s*\n*", "", text, flags=re.IGNORECASE)
    
    # 2. 移除推廣引言（相容中文：📱 加入 LINE 官方帳號... 或日文：📱 LINE公式アカウント...）
    # 匹配模式：📱? [任何空白] (加入 LINE 官方帳號 | LINE公式アカウント) [直到冒號或換行] [後續換行]
    text = re.sub(r"📱?\s*(加入\s*LINE\s*官方帳號|LINE公式アカウント).*?(\n+|$)", "", text, flags=re.IGNORECASE)
    
    return text.strip()

def main():
    youtube = get_authenticated_service()
    if not youtube:
        print("Error: YouTube Authentication failed")
        sys.exit(1)
        
    print(f"Fetching videos from playlist: {PLAYLIST_ID}...")
    
    # 取得 Playlist 下的所有影片
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
        
    print(f"Found {len(video_ids)} videos. Scanning and removing LINE promotions from descriptions...")
    
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
            title = snippet.get("title", "")
            old_desc = snippet.get("description", "")
            category_id = snippet.get("categoryId", "25")
            
            new_desc = clean_line_promo(old_desc)
            
            if old_desc != new_desc:
                print(f"  -> LINE promotion detected in description! Cleaning up...")
                # 顯示舊的部分描述做對比
                promo_lines = [line for line in old_desc.split("\n") if "line.me" in line.lower() or "line" in line.lower()]
                print(f"     Found promo lines: {promo_lines}")
                
                # 執行更新
                update_req = youtube.videos().update(
                    part="snippet",
                    body={
                        "id": video_id,
                        "snippet": {
                            "title": title,
                            "description": new_desc,
                            "categoryId": category_id
                        }
                    }
                )
                update_req.execute()
                print(f"  ✅ Video {video_id} cleaned successfully (LINE removed)!")
                updated_count += 1
            else:
                print(f"  ✨ Video {video_id} is already clean (no LINE promotion found).")
                
        except Exception as e:
            print(f"  ❌ Error processing video {video_id}: {e}")
            
    print(f"\n🎉 Batch Clean Finished! Total videos updated: {updated_count}")

if __name__ == "__main__":
    main()
