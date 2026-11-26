#!/usr/bin/env python3
"""Render the notification cue from the bundled glass recording."""

import argparse
import array
import math
from pathlib import Path
import subprocess
import sys
import wave

RATE = 48_000
ROOT = Path(__file__).resolve().parent.parent

# Use the same hit twice. The raised, filtered copy is a quiet resonance.
FILTERS = (
    "[0:a]aresample=48000,aformat=channel_layouts=mono,asplit=2[hit][reply];"
    "[hit]highpass=f=200,lowpass=f=4600,afade=t=in:d=0.0007,"
    "afade=t=out:st=0.25:d=0.10,adelay=40[front];"
    "[reply]asetrate=64072,aresample=48000,highpass=f=480,lowpass=f=2800,"
    "afade=t=in:d=0.003,afade=t=out:st=0.13:d=0.12,volume=0.22,adelay=123[back];"
    "[front][back]amix=inputs=2:normalize=0,apad,atrim=duration=0.420"
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--output", type=Path, default=ROOT / "audio/glass.wav")
    args = parser.parse_args()

    raw = subprocess.check_output(
        [
            args.ffmpeg, "-v", "error", "-i", str(ROOT / "audio/source/kenney-glass-clink.wav"),
            "-filter_complex", FILTERS, "-f", "f32le", "pipe:1",
        ]
    )
    samples = array.array("f", raw)
    if sys.byteorder == "big":
        samples.byteswap()

    peak = max(abs(sample) for sample in samples)
    if not math.isfinite(peak) or peak <= 0:
        raise ValueError("The processed recording has no usable signal")
    gain = 32_767 * 10 ** (-15 / 20) / peak
    pcm = array.array("h", (round(sample * gain) for sample in samples))
    if sys.byteorder == "big":
        pcm.byteswap()

    with wave.open(str(args.output), "wb") as wav:
        wav.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        wav.writeframes(pcm.tobytes())


if __name__ == "__main__":
    main()
