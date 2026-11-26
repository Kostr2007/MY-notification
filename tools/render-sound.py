#!/usr/bin/env python3
"""Render notification cues from the bundled recordings."""

import argparse
import array
import json
import math
from pathlib import Path
import subprocess
import sys
from typing import NamedTuple
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
    sample_length=0.65, first_fade=(90, 160), lead_ms=38,
):
    # Two pitches of the same acoustic note share its attack and resonance.
    first_rate = round(RATE * 2 ** (pitch / 12))
    second_rate = round(RATE * 2 ** ((pitch + interval) / 12))
    first_fade_start, first_fade_time = first_fade
    fade_start_ms, fade_time_ms = fade
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


VOLUME = (
    MONO + ",asetrate=35959,aresample=48000,highpass=f=240,lowpass=f=3000,"
    "afade=t=in:d=0.004,afade=t=out:st=0.022:d=0.063,atrim=duration=0.085"
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
    "lullaby": (
        "kalimba.mp3",
        two_notes(pitch=0, interval=-3, delay=126, reply_level=0.46,
                  start=0, attack=0.005, fade=(155, 234), first_fade=(123, 198),
                  lowpass=2900),
        -12,
    ),
    "volume": ("kalimba.mp3", VOLUME, -24),
    "connect": (
        "kalimba.mp3",
        two_notes(pitch=-7, interval=7, delay=68, reply_level=0.67,
                  start=0, attack=0.004, fade=(52, 114), first_fade=(48, 96),
                  lowpass=3450, lead_ms=0),
        -19,
    ),
    "disconnect": (
        "kalimba.mp3",
        two_notes(pitch=-3, interval=-4, delay=74, reply_level=0.53,
                  start=0, attack=0.005, fade=(68, 111), first_fade=(50, 107),
                  lowpass=2900, lead_ms=0),
        -20,
    ),
    "attention": (
        "kalimba.mp3",
        two_notes(pitch=-2, interval=0, delay=93, reply_level=0.72,
                  start=0, attack=0.003, fade=(44, 137), first_fade=(44, 90),
                  lowpass=3750, lead_ms=0),
        -17,
    ),
    "error": (
        "kalimba.mp3",
        two_notes(pitch=-5, interval=-6, delay=86, reply_level=0.69,
                  start=0, attack=0.004, fade=(70, 123), first_fade=(60, 110),
                  lowpass=3100, lead_ms=0),
        -17,
    ),
}


class Note(NamedTuple):
    source: str
    onset_ms: int
    gain: float
    attack_ms: int
    fade_start_ms: int
    fade_ms: int
    treble_db: float = 2.2


# The E5 and G4 recordings are louder than C5. The gains balance the
# individual attacks and keep the later notes quieter.
PHRASES = {
    "lullaby-dawn": (
        Note("kalimba.mp3", 36, 1.00, 2, 78, 120),
        Note("kalimba-e5.mp3", 142, 0.24, 3, 115, 174),
    ),
    "lullaby-sway": (
        Note("kalimba.mp3", 36, 1.00, 2, 66, 105),
        Note("kalimba-e5.mp3", 116, 0.22, 3, 62, 117),
        Note("kalimba.mp3", 218, 0.48, 4, 105, 179),
    ),
    "lullaby-glow": (
        Note("kalimba-g4.mp3", 36, 0.57, 2, 65, 118, treble_db=-2.0),
        Note("kalimba.mp3", 136, 0.77, 3, 101, 174),
        Note("kalimba-e5.mp3", 159, 0.10, 5, 109, 182),
    ),
}
PHRASE_RMS_DB = -21.5
PHRASE_PEAK_DB = -10
WINDOW_SAMPLES = RATE * 5 // 1000


def read_pcm(ffmpeg, inputs, filters):
    raw = subprocess.check_output(
        [ffmpeg, "-v", "error", *inputs, *filters, "-f", "f32le", "pipe:1"]
    )
    samples = array.array("f", raw)
    if sys.byteorder == "big":
        samples.byteswap()
    return samples


def window_energies(samples):
    return [
        sum(value * value for value in samples[i:i + WINDOW_SAMPLES])
        for i in range(0, len(samples), WINDOW_SAMPLES)
    ]


def loudest_50ms(energies):
    return max(sum(energies[i:i + 10]) for i in range(len(energies))) / (10 * WINDOW_SAMPLES)


def power_db(power):
    return round(10 * math.log10(max(power, 1e-12)), 1)


def analyze(path, ffmpeg):
    inputs = ["-i", str(path)]
    mono = MONO.removeprefix("[0:a]")
    samples = read_pcm(ffmpeg, inputs, ["-af", mono])
    energies = window_energies(samples)
    if not energies or max(energies) <= 0:
        raise ValueError(f"{path}: no audible signal")

    peak_window = max(energies)
    first = next(i for i, energy in enumerate(energies) if energy >= peak_window * 0.001)
    last = max(i for i, energy in enumerate(energies) if energy >= peak_window * 10 ** (-3.5))
    presence_pcm = read_pcm(ffmpeg, inputs, ["-af", f"{mono},highpass=f=2500,lowpass=f=6000"])
    front = slice(first * WINDOW_SAMPLES, (first + 12) * WINDOW_SAMPLES)
    front_energy = sum(value * value for value in samples[front])
    presence = sum(value * value for value in presence_pcm[front]) / front_energy
    return {
        "file": str(path),
        "duration_ms": round(1000 * len(samples) / RATE, 1),
        "onset_ms": first * 5,
        "active_end_ms": min((last + 1) * 5, round(1000 * len(samples) / RATE, 1)),
        "peak_dbfs": power_db(max(map(abs, samples)) ** 2),
        "max_50ms_rms_dbfs": power_db(loudest_50ms(energies)),
        "attack_2500_6000_hz_db": power_db(presence),
    }


def render_phrase(notes, ffmpeg):
    inputs = []
    graph = []
    for i, note in enumerate(notes):
        inputs += ["-i", str(ROOT / "audio/source" / note.source)]
        graph.append(
            f"[{i}:a]{MONO.removeprefix('[0:a]')},highpass=f=175,lowpass=f=6200,"
            f"treble=f=2700:g={note.treble_db},afade=t=in:d={note.attack_ms}ms,"
            f"afade=t=out:st={note.fade_start_ms}ms:d={note.fade_ms}ms:curve=qsin,"
            f"volume={note.gain},adelay={note.onset_ms}[note{i}]"
        )
    length = max(note.onset_ms + note.fade_start_ms + note.fade_ms for note in notes)
    pads = "".join(f"[note{i}]" for i in range(len(notes)))
    graph.append(
        f"{pads}amix=inputs={len(notes)}:normalize=0,"
        "acompressor=threshold=0.10:ratio=2.5:attack=0.2:release=14:knee=2:detection=peak,"
        f"atrim=end_sample={length * RATE // 1000}"
    )
    return read_pcm(ffmpeg, inputs, ["-filter_complex", ";".join(graph)])


def render(name, ffmpeg, output):
    if name in PHRASES:
        samples = render_phrase(PHRASES[name], ffmpeg)
        peak_db = PHRASE_PEAK_DB
    else:
        source, filters, peak_db = CUES[name]
        samples = read_pcm(ffmpeg, ["-i", str(ROOT / "audio/source" / source)], ["-filter_complex", filters])

    peak = max((abs(sample) for sample in samples), default=0.0)
    if not math.isfinite(peak) or peak <= 0:
        raise ValueError(f"{name}: the processed recording has no usable signal")
    gain = 10 ** (peak_db / 20) / peak
    if name in PHRASES:
        rms = math.sqrt(loudest_50ms(window_energies(samples)))
        gain = min(gain, 10 ** (PHRASE_RMS_DB / 20) / rms)
    pcm = array.array("h", (round(sample * (32_767 * gain)) for sample in samples))
    if sys.byteorder == "big":
        pcm.byteswap()

    with wave.open(str(output), "wb") as wav:
        wav.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        wav.writeframes(pcm.tobytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    cues = (*CUES, *PHRASES)
    parser.add_argument("cue", nargs="?", choices=(*cues, "all"))
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--analyze", nargs="+", type=Path, metavar="FILE",
                        help="report duration, attack presence, peak and loudest 50 ms RMS")
    args = parser.parse_args()

    if args.analyze:
        if args.cue or args.output:
            parser.error("--analyze takes input files only")
        print(json.dumps([analyze(path, args.ffmpeg) for path in args.analyze], ensure_ascii=False, indent=2))
        return
    if args.cue == "all" and args.output:
        parser.error("--output requires a single cue")
    for name in cues if args.cue == "all" else (args.cue or "glass",):
        render(name, args.ffmpeg, args.output or ROOT / "audio" / f"{name}.wav")


if __name__ == "__main__":
    main()
