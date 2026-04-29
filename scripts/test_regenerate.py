import json
from pathlib import Path
import subprocess

OUTPUT_DIR = Path.home() / "tw-gov-video" / "output"
INPUT_JSON = OUTPUT_DIR / "selected_articles.json"

def main():
    if not INPUT_JSON.exists():
        print("Error: selected_articles.json not found")
        return

    data = json.loads(INPUT_JSON.read_text(encoding="utf-8"))
    items = data.get("selected", [])
    
    # We want to re-render the video using the EXACT text from 4/14, 
    # but we must ensure the HTML renderer uses the new dynamic font sizes.
    
    print(f"Loaded {len(items)} articles from 4/14.")
    
    # 1. Render HTML (this uses the new render_html.py with dynamic fonts)
    print("Running render_html.py...")
    subprocess.run(["python3", "/home/benliangcs/tw-gov-video/scripts/render_html.py"], check=True)
    
    # 2. Re-capture screenshots and stitch video
    print("Running render_video.py...")
    subprocess.run(["python3", "/home/benliangcs/tw-gov-video/scripts/render_video.py"], check=True)
    
    # 3. Upload to YouTube
    print("Running upload_youtube.py...")
    subprocess.run(["python3", "/home/benliangcs/tw-gov-video/scripts/upload_youtube.py"], check=True)
    
    print("Done!")

if __name__ == "__main__":
    main()
