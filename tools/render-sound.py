#!/usr/bin/env python3
"""Render notification cues from the bundled recordings."""

import argparse
import array
import math
from pathlib import Path
import subprocess
import sys
import wave

RATE = 48_000
ROOT = Path(__file__).resolve().parent.parent

MONO = "[0:a]aresample=48000,aformat=channel_layouts=mono"
GLASS = (
    MONO + ",asplit=2[hit][reply];"
    "[hit]highpass=f=200,lowpass=f=4600,afade=t=in:d=0.0007,"
    "afade=t=out:st=0.25:d=0.10,adelay=40[front];"
    "[reply]asetrate=64072,aresample=48000,highpass=f=480,lowpass=f=2800,"
    "afade=t=in:d=0.003,afade=t=out:st=0.13:d=0.12,volume=0.22,adelay=123[back];"
    "[front][back]amix=inputs=2:normalize=0,apad,atrim=duration=0.420"
)
WOOD = (
    MONO + ",atrim=start=0.156:end=0.365,asetpts=PTS-STARTPTS,"
    "asetrate=45200,aresample=48000,highpass=f=150,lowpass=f=2700,"
    "afade=t=in:d=0.006,asplit=2[hit][reply];"
    "[hit]afade=t=out:st=0.110:d=0.085,adelay=32[front];"
    "[reply]highpass=f=260,afade=t=out:st=0.055:d=0.072,volume=0.30,adelay=116[back];"
    "[front][back]amix=inputs=2:normalize=0,atrim=end_sample=13440"
)
PAPER = (
    MONO + ",atrim=start=0.225:end=0.424,asetpts=PTS-STARTPTS,"
    "atempo=1.25,highpass=f=440,lowpass=f=3600,equalizer=f=1650:t=q:w=1:g=2,"
    "afade=t=in:d=0.008,afade=t=out:st=0.090:d=0.050,adelay=32,"
    "apad,atrim=duration=0.205"
)
DROP = (
    MONO + ",atrim=start=0.581:end=0.835,asetpts=PTS-STARTPTS,"
    "asetrate=51000,aresample=48000,highpass=f=190,lowpass=f=3900,"
    "afade=t=in:d=0.012,afade=t=out:st=0.080:d=0.128,adelay=26,"
    "apad,atrim=duration=0.265"
)


def two_notes(
    *, start, pitch, interval, delay, reply_level, attack, fade, lowpass,
    sample_length=0.65, first_fade=(90, 160),
):
    # Two pitches of the same acoustic note share its attack and resonance.
    first_rate = round(RATE * 2 ** (pitch / 12))
    second_rate = round(RATE * 2 ** ((pitch + interval) / 12))
    first_fade_start, first_fade_time = first_fade
    fade_start_ms, fade_time_ms = fade
    lead_ms = 38
    reply_ms = lead_ms + delay
    length = (reply_ms + fade_start_ms + fade_time_ms) * (RATE // 1000)
    return (
        f"{MONO},atrim=start={start}:duration={sample_length},asetpts=PTS-STARTPTS,"
        f"afade=t=out:st={sample_length - 0.08:.3f}:d=0.08,asplit=2[hit][reply];"
        f"[hit]asetrate={first_rate},aresample={RATE},highpass=f=180,lowpass=f={lowpass},"
        f"afade=t=in:d={attack},"
        f"afade=t=out:st={first_fade_start}ms:d={first_fade_time}ms:curve=qsin,"
        f"adelay={lead_ms}[front];"
        f"[reply]asetrate={second_rate},aresample={RATE},highpass=f=220,lowpass=f={lowpass},"
        f"afade=t=in:d={attack},afade=t=out:st={fade_start_ms}ms:d={fade_time_ms}ms:curve=qsin,"
        f"volume={reply_level},adelay={reply_ms}[back];"
        f"[front][back]amix=inputs=2:normalize=0,apad=whole_len={length},atrim=end_sample={length}"
    )


CUES = {
    "glass": ("kenney-glass-clink.wav", GLASS, -15),
    "wood": ("wood.mp3", WOOD, -16),
    "paper": ("paper.mp3", PAPER, -14),
    "drop": ("drop.mp3", DROP, -18),
    "kalimba": (
        "kalimba.mp3",
        two_notes(start=0, pitch=0, interval=4, delay=82, reply_level=0.62,
                  attack=0.0026, fade=(115, 192), lowpass=4350),
        -17,
    ),
    "piano": (
        "piano.mp3",
        two_notes(start=0, pitch=2, interval=-2, delay=112, reply_level=0.52,
                  attack=0.006, fade=(86, 201), lowpass=3800, first_fade=(62, 98)),
        -20,
    ),
    "nylon": (
        "nylon.mp3",
        two_notes(start=0.016, pitch=5, interval=7, delay=91, reply_level=0.51,
                  attack=0.004, fade=(105, 140), lowpass=4000, sample_length=0.44),
        -18,
    ),
}


def render(name, ffmpeg, output):
    source, filters, peak_db = CUES[name]
    raw = subprocess.check_output(
        [
            ffmpeg, "-v", "error", "-i", str(ROOT / "audio/source" / source),
            "-filter_complex", filters, "-f", "f32le", "pipe:1",
        ]
    )
    samples = array.array("f", raw)
    if sys.byteorder == "big":
        samples.byteswap()

    peak = max(abs(sample) for sample in samples)
    if not math.isfinite(peak) or peak <= 0:
        raise ValueError(f"{name}: the processed recording has no usable signal")
    gain = 32_767 * 10 ** (peak_db / 20) / peak
    pcm = array.array("h", (round(sample * gain) for sample in samples))
    if sys.byteorder == "big":
        pcm.byteswap()

    with wave.open(str(output), "wb") as wav:
        wav.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        wav.writeframes(pcm.tobytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", nargs="?", default="glass", choices=(*CUES, "all"))
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if args.cue == "all" and args.output:
        parser.error("--output requires a single cue")
    for name in CUES if args.cue == "all" else (args.cue,):
        render(name, args.ffmpeg, args.output or ROOT / "audio" / f"{name}.wav")


if __name__ == "__main__":
    main()
