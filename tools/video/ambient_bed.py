"""Calm ambient music bed for JOMO motion-graphics videos, made entirely in code.

    python ambient_bed.py OUT.wav SECONDS [HIT_TIMES...]

Slow pad chords (Dmaj9, Bm9, Gmaj7, A6/9) that crossfade over 1.5 s, a soft bell
note on each HIT_TIME (scene changes), a warm sub, and a long reverb. There are
no drums and every envelope is a smooth curve, so nothing clicks. JOMO owns all of
it: no samples, loops or AI music tools.
"""
import sys, wave

import numpy as np

SR = 48000
rng = np.random.default_rng(11)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def smooth_env(n, attack, release):
    t = np.arange(n) / SR
    a = np.clip(t / attack, 0, 1)
    r = np.clip((n / SR - t) / release, 0, 1)
    return (0.5 - 0.5 * np.cos(np.pi * a)) * (0.5 - 0.5 * np.cos(np.pi * r))


def lowpass(x, cutoff, taps=511):
    k = np.arange(taps) - (taps - 1) / 2
    h = np.sinc(2 * cutoff / SR * k) * np.blackman(taps)
    h /= h.sum()
    return np.convolve(x, h, mode="same")


def pad_note(freq, n, detune_cents=4):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for c in (-detune_cents, detune_cents):
        f = freq * 2 ** (c / 1200)
        ph = rng.random() * 2 * np.pi
        out += np.sin(2 * np.pi * f * t + ph) + 0.22 * np.sin(4 * np.pi * f * t + ph) + 0.06 * np.sin(6 * np.pi * f * t + ph)
    # very slow swell so the pad breathes
    return out * (0.85 + 0.15 * np.sin(2 * np.pi * 0.11 * t + rng.random() * 6))


def bell(freq, seconds=3.5):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 2.001 * t) * np.exp(-t * 2.5)
         + 0.12 * np.sin(2 * np.pi * freq * 3.003 * t) * np.exp(-t * 4))
    att = np.clip(t / 0.008, 0, 1)
    return x * att * np.exp(-t * 1.1)


def reverb(x, secs=3.2, wet=0.38):
    n = int(secs * SR)
    t = np.arange(n) / SR
    ir = lowpass(rng.standard_normal(n), 5000) * np.exp(-t * 2.2)
    ir[: int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
    ir /= np.sqrt((ir ** 2).sum())
    size = len(x) + n
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return (1 - wet) * x + wet * y


def build(seconds, hits=()):
    n = int(seconds * SR)
    L = np.zeros(n); R = np.zeros(n)
    chords = [[50, 57, 61, 64, 66], [47, 54, 57, 61, 62], [43, 50, 54, 57, 62], [45, 52, 54, 57, 59]]
    length, overlap = 4.0, 1.5
    t0, k = 0.0, 0
    while t0 < seconds:
        notes = chords[k % len(chords)]
        m = int((length + overlap) * SR)
        env = smooth_env(m, 1.4, 1.8)
        for j, note in enumerate(notes):
            x = pad_note(midi(note), m) * env * (0.05 if j else 0.035)
            pan = (j - 2) * 0.12
            i = int(t0 * SR); e = min(n, i + m)
            L[i:e] += x[: e - i] * (1 - pan); R[i:e] += x[: e - i] * (1 + pan)
        sub = np.sin(2 * np.pi * midi(notes[0] - 12) * np.arange(m) / SR) * env * 0.05
        i = int(t0 * SR); e = min(n, i + m)
        L[i:e] += sub[: e - i]; R[i:e] += sub[: e - i]
        t0 += length; k += 1
    tones = [74, 78, 81, 76, 73, 78]
    for j, h in enumerate(hits):
        b = bell(midi(tones[j % len(tones)])) * 0.07
        i = int(h * SR); e = min(n, i + len(b))
        if i < n:
            pan = 0.25 if j % 2 else -0.25
            L[i:e] += b[: e - i] * (1 - pan); R[i:e] += b[: e - i] * (1 + pan)
    L = lowpass(L, 7000); R = lowpass(R, 7000)
    L = reverb(L); R = reverb(R)
    fade_in, fade_out = int(0.8 * SR), int(2.2 * SR)
    for ch in (L, R):
        ch[:fade_in] *= 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, fade_in))
        ch[-fade_out:] *= 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, fade_out))
    st = np.stack([L, R], axis=1)
    return st / np.abs(st).max() * 0.85


if __name__ == "__main__":
    out, secs = sys.argv[1], float(sys.argv[2])
    st = build(secs, [float(h) for h in sys.argv[3:]])
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())
    print("wrote", out)
