import os
import sys
import json
import base64
import urllib.request

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

def main():
    api_key = os.environ.get("GCP_TTS_API_KEY")
    if not api_key:
        print("Error: GCP_TTS_API_KEY environment variable is not set.")
        sys.exit(1)

    os.makedirs("public", exist_ok=True)

    # Multi-paragraph comprehensive news script (~1,200 words = ~7-8 minutes of audio)
    paragraphs = [
        """Welcome to today's Daily News Briefing for October 12th, 2026. I am your host, bringing you our in-depth coverage across global economics, West End theatrical breakthroughs, and the latest North American box office results.

We begin today in Stockholm, Sweden, with major developments in global macroeconomic policy. American economists Robert E. Hall of Stanford University and Michael Woodford of Columbia University have officially been awarded the 2026 Sveriges Riksbank Prize in Economic Sciences in Memory of Alfred Nobel. The Royal Swedish Academy of Sciences announced the prestigious twelve-million Swedish kronor prize on Monday, recognizing the two laureates for their transformative models that have provided central banks and governments with essential tools to navigate severe economic shocks, inflationary pressures, and energy crises.""",

        """To understand the significance of Hall and Woodford's work, we must look back at traditional Keynesian economics. For decades, policymakers adhered to Keynesian principles, believing that economic management involved simple trade-offs: during downturns, governments would cut taxes and increase spending to spur demand, assuming unemployment and inflation moved in predictable opposite directions. However, the severe stagflation of the 1970s—characterized by simultaneous high inflation and soaring unemployment—shattered those classical assumptions and proved the old recipe insufficient.""",

        """In response, Robert E. Hall and Michael Woodford spearheaded a fundamental paradigm shift. Rather than viewing the economy purely from a macro, bird's-eye perspective, their research built micro-level models grounded in how real households and businesses make forward-looking decisions based on future expectations.

In a landmark 1982 paper with Fredric Mishkin, Robert E. Hall discovered that approximately eighty percent of consumers make spending decisions based on their expectations of future income and overall financial stability, while the remaining twenty percent live hand-to-mouth out of economic necessity. Hall demonstrated that consumer optimism or pessimism directly drives spending behavior long before official policy shifts take effect.""",

        """Meanwhile, Michael Woodford focused his analysis on corporate pricing behavior. Woodford established that businesses do not set prices based merely on current costs, but rather on where they anticipate interest rates, inflation, and competitor prices will move in the future. If a firm expects its future operating costs or competitor prices to rise, it will adjust its pricing upward immediately.

This discovery transformed central banking worldwide. Woodford's work proved that central banks, such as the United States Federal Reserve, must provide clear, credible, and transparent communication regarding their future policy intentions. Today, central banks around the globe rely on Woodford's theoretical foundation to guide forward guidance and keep inflation expectations anchored.""",

        """Turning from high finance to the performing arts, legendary filmmaker Quentin Tarantino is making major waves in London's theatrical scene. The two-time Academy Award-winning director and screenwriter behind Pulp Fiction, Kill Bill, and Reservoir Dogs has officially announced his first major stage writing credit: a brand new comedic play titled The Popinjay Cavalier.

The production will make its world premiere in London's West End at the historic Phoenix Theatre, with preview performances commencing on February 23rd, 2027, ahead of its official opening night on March 18th.""",

        """Set in 1830s Europe, The Popinjay Cavalier is described as a rambunctious comedy of deception, disguise, and swashbuckling adventure, drawing artistic inspiration from classic Hollywood cinema and the writings of George Bruce, Ernst Vajda, and Jesse Lasky Jr.

In a landmark casting announcement, acclaimed cinematic satirist Sacha Baron Cohen will star in the title role as Rupert Sebastian Thomas Jr., marking his professional stage and West End debut. Cohen, famous for his iconic characters Ali G, Borat, Brüno, and his performance as Signor Adolfo Pirelli in the 2007 film adaptation of Sweeney Todd, expressed his enthusiasm for the project. Cohen quipped that when Quentin called, he accepted before Tarantino could even finish his sentence, adding that he is beyond delighted for them to make their West End debuts together.""",

        """Finally, we turn to the weekend box office, where horror continues to dominate theatrical earnings. Universal Pictures and Blumhouse Atomic Monster's horror title, Other Mommy, claimed the top spot in North America with an impressive twenty-seven point five million dollars in its opening weekend across more than thirty-three hundred theaters. Overseas markets brought in an additional seventeen point seven million dollars, elevating its global debut to forty-five point two million dollars against a modest nineteen million dollar production budget.

Despite receiving unfavorable critical reviews and a rare D-plus CinemaScore—joining films like Megalopolis and Hereditary—Other Mommy drew diverse crowds, with domestic attendance evenly split between men and women, and two-thirds of ticket buyers falling between the ages of eighteen and thirty-four.""",

        """In contrast, Sony Pictures' topically charged drama, The Social Reckoning, faced a difficult debut. Directed and written by Aaron Sorkin and starring Mikey Madison, Jeremy Allen White, and Jeremy Strong, the film centers on a Facebook whistleblower leaking incriminating documents to Wall Street Journal reporters. The thirty million dollar production generated five point five million dollars in its opening weekend, reflecting the unpredictable nature of topical dramas at the autumn box office.

Overall, the annual domestic box office crossed the eight billion dollar mark this weekend, standing nineteen percent higher than last year's figures.

That concludes our comprehensive Daily News Briefing for October 12th, 2026. Thank you for listening, and stay tuned for our next episode."""
    ]

    full_audio = bytearray()
    for idx, para in enumerate(paragraphs, 1):
        print(f"Synthesizing paragraph {idx}/{len(paragraphs)} ({len(para)} chars)...")
        chunk_bytes = synthesize_text_chunk(para, api_key)
        full_audio.extend(chunk_bytes)

    output_path = os.path.join("public", "podcast.mp3")
    with open(output_path, "wb") as f:
        f.write(full_audio)
    
    print(f"Successfully generated full podcast episode at {output_path} ({len(full_audio)} bytes).")

if __name__ == "__main__":
    main()
