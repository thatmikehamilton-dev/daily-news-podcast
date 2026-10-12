import os
import sys
import json
import base64
import urllib.request

def main():
    api_key = os.environ.get("GCP_TTS_API_KEY")
    if not api_key:
        print("Error: GCP_TTS_API_KEY environment variable is not set.")
        sys.exit(1)

    os.makedirs("public", exist_ok=True)

    news_text = """Welcome to today's Daily News Briefing. 

In economic news, two American economists, Robert E. Hall and Michael Woodford, have been awarded the Nobel Memorial Prize in Economic Sciences for transforming our understanding of how business expectations and interest rates influence financial stability.

In entertainment, filmmaker Quentin Tarantino is making his stage writing debut in London's West End with a comedic play titled The Popinjay Cavalier, starring Sacha Baron Cohen. 

Meanwhile at the weekend box office, the horror feature Other Mommy claimed the top spot globally despite mixed reviews.

Thank you for listening to today's briefing."""

    url = f"[suspicious link removed]{api_key}"
    
    payload = {
        "input": {"text": news_text},
        "voice": {
            "languageCode": "en-US",
            "name": "en-US-Journey-F"
        },
        "audioConfig": {
            "audioEncoding": "MP3"
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads([suspicious link removed]().decode("utf-8"))
            audio_content = base64.b64decode(res_data["audioContent"])
            
            output_path = "public/podcast.mp3"
            with open(output_path, "wb") as f:
                f.write(audio_content)
            print(f"Successfully generated audio at {output_path}")

    except Exception as e:
        print(f"Failed to generate audio: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
