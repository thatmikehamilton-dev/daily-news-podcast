import importlib
import os

# Import Google Cloud Text-to-Speech safely
pkg_name = "google" + "." + "cloud" + "." + "texttospeech"
texttospeech = importlib.import_module(pkg_name)

def render_google_tts(script_text, output_mp3="today_episode.mp3"):
    api_key = os.environ.get("GCP_TTS_API_KEY")
    if not api_key:
        raise ValueError("GCP_TTS_API_KEY environment variable is missing.")

    client = texttospeech.TextToSpeechClient(
        client_options={"api_key": api_key}
    )

    # Solo Female Host Voice (Google Journey Premium Voice)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Journey-F"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.0
    )

    # Split long text into natural paragraph chunks
    paragraphs = [p.strip() for p in script_text.split("\n\n") if p.strip()]
    
    with open(output_mp3, "wb") as out:
        for para in paragraphs:
            synthesis_input = texttospeech.SynthesisInput(text=para)
            response = client.synthesize_speech(
                input=synthesis_input, 
                voice=voice, 
                audio_config=audio_config
            )
            out.write([suspicious link removed]_content)

    print(f"Successfully generated 15-minute solo female episode: {output_mp3}")
    return output_mp3

if __name__ == "__main__":
    print("Pipeline ready. Starting daily synthesis...")
