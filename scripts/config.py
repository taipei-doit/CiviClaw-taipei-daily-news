import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# BASE_DIR defaults to the repository root, but can be customized via environment variable
BASE_DIR_ENV = os.getenv("TW_GOV_VIDEO_BASE")
if BASE_DIR_ENV:
    BASE_DIR = Path(BASE_DIR_ENV)
else:
    BASE_DIR = Path(__file__).parent.parent.resolve()

OUTPUT_DIR = BASE_DIR / "output"

# Ensure output directory exists when imported
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Common File Paths
INPUT_JSON = OUTPUT_DIR / "selected_articles.json"
JP_JSON = OUTPUT_DIR / "selected_articles_jp.json"
JP_VIDEO = OUTPUT_DIR / "video_jp.mp4"
YOUTUBE_URL_FILE = OUTPUT_DIR / "latest_youtube_url.txt"

# Heartbeat pipeline state (same location the scheduler reads: <repo>/memory/)
STATE_FILE = BASE_DIR / "memory" / "heartbeat-state.json"
