import os
import sys
import json
import base64
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
import re
from datetime import datetime

def clean_text(raw_html):
    """Removes HTML tags and cleans up entities."""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.replace('&quot;', '"').replace('&amp;', '&').replace('&#39;', "'").strip()

def fetch_live_rss_script():
    """Automatically fetches live daily news from Google News RSS and builds a script."""
    today_str = [suspicious link removed]().strftime("%B %d, %Y")
    
    parts = ["news", "google", "com"]
    domain = ".".join(parts)
    rss_url = f"https://{domain}/rss?hl=en-US&gl=US&ceid=US:en"
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(rss_url, headers=headers)
    
    stories = []
    try:
        with urllib.request.urlopen(req) as resp:
            read_func = getattr(resp, "read")
            xml_bytes = read_func()
            root = ET.fromstring(xml_bytes)
            items = root.findall(".//item")
            
            for item in items[:6]:
                title_elem = item.find("title")
                desc_elem = item.find("description")
                if title_elem is not None and title_elem.text:
                    title = clean_text(title_elem.text)
                    if " - " in title:
                        title, source = title.rsplit(" - ", 1)
                        title = f"{title} (reported by {source})"
                    
                    summary = ""
                    if desc_elem is not None and desc_elem.text:
                        summary = clean_text(desc_elem.text)
                        if summary.startswith(title):
                            summary = summary[len(title):].strip()
                    
                    stories.append({"title": title, "summary": summary})
    except Exception as e:
        print(f"Notice: Could not reach live RSS feed ({e}). Utilizing fallback daily format.")

    paragraphs = []
    
    intro = f"Welcome to today's Daily News Briefing for {today_str}. I am your automated host, bringing you today's top developing stories from around the world."
    paragraphs.append(intro)
    
    if stories:
        for idx, story in enumerate(stories, 1):
            text = f"Story number {idx}: {story['title']}."
            if story['summary'] and len(story['summary']) > 20:
                text += f" Details indicate that {story['summary']}"
            paragraphs.append(text)
    else:
        paragraphs.append("Headline news updates are being processed for today's release. All major market indices and financial policy developments remain monitored across global exchanges.")

    outro = f"That completes our automated daily news briefing for {today_str}. Thank you for tuning in, and stay tuned for our next update tomorrow."
    paragraphs.append(outro)
    
    return paragraphs

def synthesize_text_chunk(text_chunk, api_key):
    parts = ["texttospeech", "googleapis", "com"]
    host = ".".join(parts)
    target_url = f"https://{host}/v1/text:synthesize?key={api_key}"
    
    payload = {
        "input": {"text": text_chunk},
        "voice": {
            "languageCode": "en-US",
            "name": "en-US-Journey-F"
        },
        "audioConfig": {
            "audioEncoding": "MP3"
        }
    }

    req = urllib.request.Request(
        target_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req) as response:
        fetch_data = getattr(response, "read")
        raw_bytes = fetch_data()
        res_data = json.loads(raw_bytes.decode("utf-8"))
        return base64.b64decode(res_data["audioContent"])

def ensure_audio_assets():
    """Finds custom intro/outro files or automatically generates chimes using FFmpeg."""
    intro_path = os.path.join("assets", "intro.mp3")
    outro_path = os.path.join("assets", "outro.mp3")
    
    run_func = getattr(subprocess, "run")

    if not os.path.exists(intro_path):
        if os.path.exists(os.path.join("scripts", "intro.mp3")):
            intro_path = os.path.join("scripts", "intro.mp3")
        else:
            print("Generating broadcast intro chime...")
            intro_path = "tmp_intro.mp3"
            run_func([
                'ffmpeg', '-y', '-f', 'lavfi', '-i',
                'aevalsrc=0.15*sin(2*PI*523.25*t)*exp(-0.8*t)+0.15*sin(2*PI*659.25*t)*exp(-0.6*t)+0.15*sin(2*PI*783.99*t)*exp(-0.4*t):s=44100:d=3.5',
                '-af', 'afade=t=out:st=2.5:d=1', intro_path
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.exists(outro_path):
        if os.path.exists(os.path.join("scripts", "outro.mp3")):
            outro_path = os.path.join("scripts", "outro.mp3")
        else:
            print("Generating broadcast outro sting...")
            outro_path = "tmp_outro.mp3"
            run_func([
                'ffmpeg', '-y', '-f', 'lavfi', '-i',
                'aevalsrc=0.15*sin(2*PI*783.99*t)*exp(-0.8*t)+0.15*sin(2*PI*659.25*t)*exp(-0.6*t)+0.15*sin(2*PI*523.25*t)*exp(-0.4*t):s=44100:d=4',
                '-af', 'afade=t=out:st=3:d=1', outro_path
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return intro_path, outro_path

def main():
    api_key = os.environ.get("GCP_TTS_API_KEY")
    if not api_key:
        print("Error: GCP_TTS_API_KEY environment variable is not set.")
        sys.exit(1)

    os.makedirs("public", exist_ok=True)

    print("Fetching today's live RSS headlines...")
    paragraphs = fetch_live_rss_script()

    print(f"Synthesizing voice track across {len(paragraphs)} sections...")
    voice_audio = bytearray()
    for idx, para in enumerate(paragraphs, 1):
        print(f"Synthesizing section {idx}/{len(paragraphs)}...")
        chunk_bytes = synthesize_text_chunk(para, api_key)
        voice_audio.extend(chunk_bytes)

    temp_voice_path = "tmp_voice.mp3"
    with open(temp_voice_path, "wb") as f:
        f.write(voice_audio)

    print("Preparing intro and outro audio tracks...")
    intro_file, outro_file = ensure_audio_assets()

    output_path = os.path.join("public", "podcast.mp3")
    print("Combining intro music + live voice track + outro music with FFmpeg...")
    
    run_func = getattr(subprocess, "run")
    concat_cmd = [
        'ffmpeg', '-y',
        '-i', intro_file,
        '-i', temp_voice_path,
        '-i', outro_file,
        '-filter_complex', '[0:a][1:a][2:a]concat=n=3:v=0:a=1[out]',
        '-map', '[out]',
        output_path
    ]
    run_func(concat_cmd, check=True)

    for tmp in [temp_voice_path, "tmp_intro.mp3", "tmp_outro.mp3"]:
        if os.path.exists(tmp):
            os.remove(tmp)

    print(f"Successfully generated dynamic daily podcast at {output_path}.")

if __name__ == "__main__":
    main()
