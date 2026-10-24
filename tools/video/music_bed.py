"""Original music bed for JOMO reels (made in code, so no licence issues).

Usage: python music_bed.py OUT.wav SECONDS [--calm]
Uplifting vi-IV-I-V progression at 100 BPM: pad, plucked arpeggio, sub bass,
soft kick/clap/hats. --calm drops the drums for use under speech.
"""
import sys, wave
import numpy as np

SR = 48000
BPM = 100
BEAT = 60 / BPM
rng = np.random.default_rng(7)

def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)

def env(n, a, r, sustain=1.0):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * sustain
    tail = np.clip((n / SR - t) / max(r, 1e-4), 0, 1)
    return e * tail

def lowpass(x, cutoff, taps=255):
    n = np.arange(taps) - (taps - 1) / 2
    h = np.sinc(2 * cutoff / SR * n) * np.hanning(taps)
    h /= h.sum()
    return np.convolve(x, h, mode="same")

def highpass(x, cutoff):
    return x - lowpass(x, cutoff)

def saw(freq, n, detune=0.0):
    t = np.arange(n) / SR
    ph = (freq * (1 + detune) * t + rng.random()) % 1.0
    return 2 * ph - 1

def pluck(freq, dur, bright=0.5):
    n = int(dur * SR)
    period = int(SR / freq)
    buf = rng.uniform(-1, 1, period) * bright + rng.uniform(-1, 1, period) * (1 - bright) * 0.3
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % period]
        buf[i % period] = 0.996 * 0.5 * (buf[i % period] + buf[(i + 1) % period])
    return out * env(n, 0.002, 0.05)

def kick(dur=0.35):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 9)

def clap(dur=0.25):
    n = int(dur * SR); t = np.arange(n) / SR
    x = highpass(lowpass(rng.uniform(-1, 1, n), 5000), 900)
    e = np.exp(-t * 18) * (1 + 0.6 * (t < 0.012))
    return x * e

def hat(dur=0.06):
    n = int(dur * SR); t = np.arange(n) / SR
    return highpass(rng.uniform(-1, 1, n), 7000) * np.exp(-t * 70)

def reverb(x, secs=1.6, wet=0.22):
    n = int(secs * SR); t = np.arange(n) / SR
    ir = rng.uniform(-1, 1, n) * np.exp(-t * 4.5)
    ir = lowpass(ir, 6000)
    ir /= np.sqrt((ir ** 2).sum())
    size = len(x) + n
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return (1 - wet) * x + wet * y

def add(buf, x, start):
    i = int(start * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(x))
    buf[i:j] += x[: j - i]

def build(seconds, calm=False):
    n = int(seconds * SR)
    L = np.zeros(n + SR * 2); R = np.zeros(n + SR * 2)
    # vi - IV - I - V in C major
    chords = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]
    bar = 4 * BEAT
    bars = int(np.ceil(seconds / bar))
    for b in range(bars):
        root, notes = chords[b % 4]
        t0 = b * bar
        # pad: detuned saws, filtered, stereo
        pn = int(bar * SR) + int(0.4 * SR)
        padL = sum(saw(midi(m), pn, -0.004) for m in notes + [notes[0] + 12])
        padR = sum(saw(midi(m), pn, 0.004) for m in notes + [notes[0] + 12])
        e = env(pn, 0.35, 0.6)
        add(L, lowpass(padL, 2400) * e * 0.05, t0); add(R, lowpass(padR, 2400) * e * 0.05, t0)
        # sub bass, pumping on each beat
        for k in range(4):
            bn = int(BEAT * SR)
            tt = np.arange(bn) / SR
            s = np.sin(2 * np.pi * midi(root - 12) * tt) * (0.25 + 0.75 * np.minimum(1, tt / 0.12)) * env(bn, 0.01, 0.08)
            add(L, s * 0.11, t0 + k * BEAT); add(R, s * 0.11, t0 + k * BEAT)
        # plucked arpeggio in eighths
        arp = [notes[0] + 12, notes[1] + 12, notes[2] + 12, notes[1] + 24, notes[2] + 12, notes[1] + 12, notes[0] + 24, notes[2] + 12]
        for k, m in enumerate(arp):
            p = pluck(midi(m), 0.9, bright=0.8) * 0.2
            pan = 0.35 if k % 2 else -0.35
            add(L, p * (1 - pan), t0 + k * BEAT / 2); add(R, p * (1 + pan), t0 + k * BEAT / 2)
        if not calm and b >= 1:
            for k in range(4):
                if k in (0, 2):
                    add(L, kick() * 0.34, t0 + k * BEAT); add(R, kick() * 0.34, t0 + k * BEAT)
                if k in (1, 3) and b >= 2:
                    c = clap() * 0.2
                    add(L, c, t0 + k * BEAT); add(R, c, t0 + k * BEAT)
            for k in range(8):
                h = hat() * (0.09 if k % 2 else 0.06)
                add(L, h * 0.8, t0 + k * BEAT / 2); add(R, h * 1.2, t0 + k * BEAT / 2)
    # final chord ring-out on the tonic
    ring = int(2.5 * SR)
    fin = sum(np.sin(2 * np.pi * midi(m) * np.arange(ring) / SR) for m in [48, 55, 60, 64, 67])
    fin = fin * np.exp(-np.arange(ring) / SR * 1.6) * 0.06
    add(L, fin, seconds - 2.2); add(R, fin, seconds - 2.2)
    L = reverb(L)[:n]; R = reverb(R)[:n]
    fade = int(1.2 * SR)
    for ch in (L, R):
        ch[-fade:] *= np.linspace(1, 0, fade) ** 1.5
        ch[: int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))
    st = np.stack([L, R], axis=1)
    st = np.tanh(st * 1.4) / np.tanh(1.4)
    st /= np.abs(st).max() / 0.89
    return st

if __name__ == "__main__":
    out, secs = sys.argv[1], float(sys.argv[2])
    st = build(secs, calm="--calm" in sys.argv)
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())
    print("wrote", out, f"{secs}s")
