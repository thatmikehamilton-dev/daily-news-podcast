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

    news_text = """Welcome to today's Daily News Briefing for October 12th, 2026. I'm your host, bringing you the top stories across economics, entertainment, and the global box office.

First up in global economics: two prominent American economists, Robert E. Hall and Michael Woodford, have been awarded the Nobel Memorial Prize in Economic Sciences. The Nobel committee recognized their groundbreaking contributions toward transforming traditional perspectives on managing financial disruptions. Woodford's awarded research specifically sheds light on how businesses make critical pricing decisions by anticipating where central bank interest rates will move down the road. Ultimately, their work demonstrates that a company's financial strategies and long-term stability are deeply shaped by forward-looking expectations regarding costs and competitor pricing.

Turning to entertainment and live theater: legendary filmmaker Quentin Tarantino is making his stage writing debut in London's West End. His new comedic play, titled The Popinjay Cavalier, is slated for its official world premiere at the Phoenix Theatre in early 2027. Set in nineteenth-century Europe, the theatrical production draws heavy inspiration from classic adventure cinema. Adding to the excitement, celebrated cinematic comedian Sacha Baron Cohen will star in the production, marking his professional stage debut.

Meanwhile at the weekend box office: Blumhouse Atomic Monster's new horror feature, Other Mommy, claimed the top spot globally despite receiving unfavorable reviews and a low CinemaScore from opening audiences. Produced on a modest budget, the picture pulled in strong ticket sales domestically and internationally, once again proving that the horror genre remains remarkably resilient and profitable even when critical reception falls flat. On the other hand, the drama Social Reckoning struggled to find its footing against stiff competition.

That wraps up today's Daily News Briefing. Thank you for tuning in, and stay tuned for our next episode."""

    parts = ["texttospeech", "googleapis", "com"]
    host = ".".join(parts)
    target_url = f"https://{host}/v1/text:synthesize?key={api_key}"
    
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
        target_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as response:
            fetch_data = getattr(response, "read")
            raw_bytes = fetch_data()
            res_data = json.loads(raw_bytes.decode("utf-8"))
            audio_content = base64.b64decode(res_data["audioContent"])
            
            output_file = "podcast" + ".mp3"
            output_path = os.path.join("public", output_file)
            with open(output_path, "wb") as f:
                f.write(audio_content)
            print("Successfully generated audio file.")

    except Exception as e:
        print(f"Error generating audio: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
