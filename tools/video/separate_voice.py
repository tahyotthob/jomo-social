"""Split a clip's audio into voice and music with Demucs (htdemucs_ft).

    python separate_voice.py SOURCE.mp4 OUT_DIR

Writes drums.wav, bass.wav, other.wav and vocals.wav to OUT_DIR. Used on
2026-10-22 to remove the CapCut background music from the AI avatar's voice
(VID-20261022-WA0017). The result, after a narrow notch at 1758 Hz to remove
one remaining tone, is source/v2-avatar-voice-only.wav. Needs a venv with
torch (CPU build), demucs and soundfile.
"""
import subprocess, sys

import numpy as np
import soundfile as sf
import torch
from demucs.apply import apply_model
from demucs.pretrained import get_model

src, out_dir = sys.argv[1], sys.argv[2]
model = get_model("htdemucs_ft")
sr = model.samplerate
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vn", "-ac", "2", "-ar", str(sr), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
wav = torch.from_numpy(np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).T.copy())
ref = wav.mean(0)
x = (wav - ref.mean()) / ref.std()
with torch.no_grad():
    stems = apply_model(model, x[None], device="cpu", split=True, overlap=0.25, shifts=2)[0]
stems = stems * ref.std() + ref.mean()
for name, stem in zip(model.sources, stems):
    sf.write(f"{out_dir}/{name}.wav", stem.numpy().T, sr)
print("stems:", model.sources)
