"""Make Tobi's and Amara's voice lines with Azure AI Speech (Nigerian English neural voices).
Needs AZURE_SPEECH_KEY and AZURE_SPEECH_REGION in the environment (set them as environment secrets,
never in the repo). Usage: python3 tts.py lines.json outdir
lines.json: [{"id": "01", "who": "tobi", "text": "..."}, ...]
Writes outdir/<id>-<who>.wav (24 kHz mono) and outdir/<id>-<who>.env.json (mouth-openness per 1/30 s)."""
import json, os, sys, pathlib, urllib.request, wave, struct, math
VOICE = {"tobi": "en-NG-AbeoNeural", "amara": "en-NG-EzinneNeural"}
FPS = 30

def synth(text, voice, out):
    key, region = os.environ["AZURE_SPEECH_KEY"], os.environ["AZURE_SPEECH_REGION"]
    ssml = (f'<speak version="1.0" xml:lang="en-NG"><voice name="{voice}">'
            f'<prosody rate="-4%">{text}</prosody></voice></speak>')
    req = urllib.request.Request(f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1", data=ssml.encode(),
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/ssml+xml",
                 "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm", "User-Agent": "jomo-social"})
    out.write_bytes(urllib.request.urlopen(req, timeout=60).read())

def envelope(wav):
    """Loudness per video frame, 0..1, used to open and close the mouth."""
    with wave.open(str(wav)) as w:
        n, sr = w.getnframes(), w.getframerate(); data = struct.unpack(f"<{n}h", w.readframes(n))
    hop = sr // FPS; vals = []
    for i in range(0, n, hop):
        chunk = data[i:i + hop]; vals.append(math.sqrt(sum(s * s for s in chunk) / max(1, len(chunk))))
    peak = max(vals) or 1
    return [round(min(1, v / (0.6 * peak)), 3) for v in vals]

if __name__ == "__main__":
    lines, outdir = json.loads(pathlib.Path(sys.argv[1]).read_text()), pathlib.Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
    for l in lines:
        wav = outdir / f'{l["id"]}-{l["who"]}.wav'
        synth(l["text"], VOICE[l["who"]], wav)
        (outdir / f'{l["id"]}-{l["who"]}.env.json').write_text(json.dumps(envelope(wav)))
        print("ok", wav.name)
