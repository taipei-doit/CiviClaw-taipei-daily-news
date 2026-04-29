from pathlib import Path
import json
import subprocess
import os

BASE = Path.home() / "tw-gov-video"
OUTPUT_DIR = BASE / "output"
INPUT_JSON = OUTPUT_DIR / "selected_articles.json"
HTML_FILE = OUTPUT_DIR / "slides_playwright.html"
VIDEO_FILE = OUTPUT_DIR / "video.mp4"
CONCAT_FILE = OUTPUT_DIR / "concat.txt"
AUDIO_CONCAT_FILE = OUTPUT_DIR / "audio_concat.txt"
TIMESTAMPS_FILE = OUTPUT_DIR / "youtube_timestamps.txt"

def get_audio_duration(file_path):
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", 
            "format=duration", "-of", 
            "default=noprint_wrappers=1:nokey=1", str(file_path)
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return float(result.stdout.strip())
    except Exception:
        return 10.0

def format_timestamp(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def main():
    data = json.loads(INPUT_JSON.read_text(encoding="utf-8"))
    items = data.get("selected", [])
    
    concat_lines = []
    audio_concat_lines = []
    timestamps = []
    current_time_sec = 0.0
    
    print("Capturing HTML slides with Playwright...")
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--no-sandbox', '--disable-setuid-sandbox'])
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        
        page.goto(f"file://{HTML_FILE.absolute()}")
        page.evaluate("document.fonts.ready")
        
        # 1. Capture Intro
        page.evaluate("showSlide('slide_intro')")
        page.wait_for_timeout(500)
        intro_img = OUTPUT_DIR / "frame_intro.png"
        page.screenshot(path=str(intro_img))
        
        dur_intro = get_audio_duration(OUTPUT_DIR / "voice_intro.mp3")
        concat_lines.append(f"file '{intro_img}'")
        concat_lines.append(f"duration {dur_intro}")
        audio_concat_lines.append(f"file '{OUTPUT_DIR / 'voice_intro.mp3'}'")
        
        timestamps.append(f"{format_timestamp(current_time_sec)} 每日新聞開場")
        current_time_sec += dur_intro
        
        # 2. Capture Headlines Slide
        page.evaluate("showSlide('slide_headlines')")
        page.wait_for_timeout(500)
        headlines_img = OUTPUT_DIR / "frame_headlines.png"
        page.screenshot(path=str(headlines_img))
        
        dur_headlines = get_audio_duration(OUTPUT_DIR / "voice_headlines.mp3")
        concat_lines.append(f"file '{headlines_img}'")
        concat_lines.append(f"duration {dur_headlines}")
        audio_concat_lines.append(f"file '{OUTPUT_DIR / 'voice_headlines.mp3'}'")
        
        timestamps.append(f"{format_timestamp(current_time_sec)} 今日重點新聞提要")
        current_time_sec += dur_headlines
        
        # 3. Capture Content Slides
        for idx, item in enumerate(items):
            page.evaluate(f"showSlide('slide_{idx}')")
            page.wait_for_timeout(500)
            img_path = OUTPUT_DIR / f"frame_{idx}.png"
            page.screenshot(path=str(img_path))
            
            dur = get_audio_duration(OUTPUT_DIR / f"voice_{idx}.mp3")
            concat_lines.append(f"file '{img_path}'")
            concat_lines.append(f"duration {dur}")
            audio_concat_lines.append(f"file '{OUTPUT_DIR / f'voice_{idx}.mp3'}'")
            
            title = item.get("title", f"重點新聞 {idx+1}")
            timestamps.append(f"{format_timestamp(current_time_sec)} {title}")
            current_time_sec += dur
            
        # 4. Capture Outro
        page.evaluate("showSlide('slide_outro')")
        page.wait_for_timeout(500)
        outro_img = OUTPUT_DIR / "frame_outro.png"
        page.screenshot(path=str(outro_img))
        
        dur_outro = get_audio_duration(OUTPUT_DIR / "voice_outro.mp3")
        concat_lines.append(f"file '{outro_img}'")
        concat_lines.append(f"duration {dur_outro}")
        audio_concat_lines.append(f"file '{OUTPUT_DIR / 'voice_outro.mp3'}'")
        
        timestamps.append(f"{format_timestamp(current_time_sec)} 結語")
        
        concat_lines.append(f"file '{outro_img}'")
        concat_lines.append(f"duration 3.0")
        
        browser.close()

    CONCAT_FILE.write_text("\n".join(concat_lines))
    AUDIO_CONCAT_FILE.write_text("\n".join(audio_concat_lines))
    TIMESTAMPS_FILE.write_text("\n".join(timestamps))
    
    print(f"Generated YouTube Timestamps:\n{TIMESTAMPS_FILE.read_text()}")
    
    temp_video = OUTPUT_DIR / "temp_video.mp4"
    temp_audio = OUTPUT_DIR / "temp_audio.mp3"
    
    print("Rendering video from CSS screenshots...")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(CONCAT_FILE), "-fps_mode", "vfr", "-pix_fmt", "yuv420p", str(temp_video)], check=True)
    
    print("Concatenating audio...")
    num_audio = len(items) + 3 # Intro + Headlines + Outro
    filter_complex = "".join([f"[{i}:0]" for i in range(num_audio)]) + f"concat=n={num_audio}:v=0:a=1[out]"
    audio_inputs = []
    for line in audio_concat_lines:
        filepath = line.split("'")[1]
        audio_inputs.extend(["-i", filepath])
        
    subprocess.run(["ffmpeg", "-y", *audio_inputs, "-filter_complex", filter_complex, "-map", "[out]", str(temp_audio)], check=True)
    subprocess.run(["ffmpeg", "-y", "-i", str(temp_video), "-i", str(temp_audio), "-c:v", "copy", "-c:a", "aac", str(VIDEO_FILE)], check=True)
    print(f"Rendered final video: {VIDEO_FILE}")

if __name__ == "__main__":
    main()
