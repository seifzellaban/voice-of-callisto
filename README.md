# Voice of Callisto

A real-time pipe organ synthesizer inspired by the RAH Willis organ, built in Python. Generates sound entirely from additive synthesis with physically-modeled pipe characteristics — no samples, no soundfonts. Every note is computed in real-time from sine waves, harmonic profiles, and acoustic simulation; based on the [Organum](https://github.com/seifzellaban/organum) engine.

---

## Features

### Sound Engine
- **Additive synthesis** with per-stop harmonic profiles across four waveform families: principal, flute, reed, and string
- **24 organ stops** + Tremulant in a RAH Willis-inspired layout (Foundation, Mixture & Reeds, Pedal)
- **9 drawbars** (Hammond-style) with per-harmonic amplitude control from 16′ sub-bass to 1′ sifflöte
- **6 drawbar presets** (Full Organ, Gospel, Cathedral, Flutes, Theater, Bach)
- **Stereo cathedral reverb** — decorrelated Schroeder networks (parallel combs + series allpass) with configurable predelay
- **6 room presets** from Dry Studio to Gothic Basilica, each tuning decay, damping, predelay, and sub-bass resonance
- **Room resonance** — three tuned sine oscillators simulating stone-building standing waves
- **Tremulant** — multi-component LFO modulating wind pressure
- **4-band swell EQ** — Bass (<200Hz), Mid Low (200–600), Mid High (600–2k), Treble (>2k)
- **Alternate tunings** — Equal, Pythagorean, Meantone, Werckmeister III (switchable live)
- **Sustain pedal** — toggle holds released notes until disengaged
- **Transpose** — ±12 semitones
- **Per-stop volume** — individual level control (0–10) per stop
- **Per-pipe voicing**: chiff (wind-rush attack), tracker action click, wind noise, chorus detuning, vibrato
- **Smooth ADSR envelopes** — smoothstep attack, exponential release, click-free retrigger with Hermite crossfade
- **Voice retrigger** — re-pressing a held/releasing note crossfades back to sustain preserving oscillator phase
- **Transient suppression** — re-strikes within 500 ms suppress chiff and click to avoid machine-gun artifacts
- **Smooth voice normalization** — gain scales with 1/√N voices with linear ramp across each buffer
- **Polyphonic** — up to 24 simultaneous voices with automatic release-voice stealing
- **WAV/MP3 recording** — capture your performance to file

### Interface
- **Full-range keyboard** (C1–C7) with active octave highlighting, key labels, left/right hand color coding
- **Split keyboard** — independent left hand (Z–M) and right hand (Y–]) with separate octave ranges
- **Mouse playable** — click keys directly on screen
- **LCD-style status bar** — shows current octave ranges, active stop group, selected drawbar
- **Stop group presets** via numpad (0–9) for instant registration changes
- **MIDI file playback** — transport controls, tempo scaling (50%–200%), live note visualization
- **F11** fullscreen toggle

---

## Requirements

- Python 3.13+
- A working audio output device (PortAudio)
- `ffmpeg` (optional, for MP3 recording)

---

## Installation

```bash
git clone https://github.com/youruser/voice-of-callisto.git
cd voice-of-callisto
uv sync
```

---

## Running

```bash
uv run python main.py
```

---

## Keyboard Controls

### Playing Notes

The keyboard is split into two independent hands. Each row covers one chromatic octave.

**Left hand** — Z X C V B N M (whites) / S D G H J (sharps)

**Right hand** — Y U I O P [ ] (whites) / 7 8 0 - = (sharps)

### Octave Navigation

| Keys | Action |
|------|--------|
| `←` / `→` | Shift both hands one octave |
| `Left Ctrl` + `←` / `→` | Shift left hand only |
| `Right Ctrl` + `←` / `→` | Shift right hand only |

### Stop Group Presets (Numpad)

| Key | Registration |
|-----|-------------|
| `Num 0` | All stops on |
| `Num 1` | Foundation — Open Diapason 8' |
| `Num 2` | Great Plenum — Diapason 8' + Principal 4' + Fifteenth 2' + Mixture |
| `Num 3` | Full Plenum — adds Double Open Diapason 16' |
| `Num 4` | Reeds — Double Trumpet 16' + Trumpet 8' + Clarion 4' |
| `Num 5` | Solo Trumpet — Trumpet 8' |
| `Num 6` | Pedal Foundation — Open Diapason 16' + Principal 8' |
| `Num 7` | Pedal Full — adds Double Open Bass 32' + Ophicleide 16' |
| `Num 8` | Full Organ — all major stops |
| `Num 9` | Festal — diapason + trumpet + pedal + tremulant |

### Drawbar Control

| Keys | Action |
|------|--------|
| `Shift` + `Num 1`–`9` | Select drawbar |
| `↑` / `↓` | Adjust selected drawbar value |

### Drawbar Reference

| Pos | Footage | Harmonic |
|-----|---------|----------|
| 1 | 16′ | Sub-octave (½×) |
| 2 | 8′ | Fundamental (1×) |
| 3 | 5⅓′ | Quint (1.5×) |
| 4 | 4′ | Octave (2×) |
| 5 | 2⅔′ | Nazard (3×) |
| 6 | 2′ | Super octave (4×) |
| 7 | 1⅗′ | Tierce (5×) |
| 8 | 1⅓′ | Larigot (6×) |
| 9 | 1′ | Sifflöte (8×) |

---

## Stops Reference

### Manual — Foundation

| Stop | Character |
|------|-----------|
| **Double Open Diapason 16'** | Deep 16' foundation principal |
| **Open Diapason 8'** | The backbone — rich, full principal tone |
| **Geigen Diapason 8'** | Bright string-toned diapason |
| **Flûte Harmonique 8'** | Warm harmonic flute, round and singing |
| **Principal 4'** | Bright octave principal — clarity and definition |
| **Viola 4'** | Alto string stop — lean, penetrating colour |
| **Open Flute 4'** | Clear open flute at 4' — gentle presence |
| **Fifteenth 2'** | High principal — shimmer and brilliance |

### Manual — Mixture & Reeds

| Stop | Character |
|------|-----------|
| **Mixture IV** | Four-rank compound — crowns the plenum with brilliance |
| **Double Trumpet 16'** | Powerful reed in the 16' octave — commanding |
| **Bassoon 16'** | Smooth soft reed — orchestral bassoon colour |
| **Trumpet 8'** | Blazing solo reed — cuts through the full organ |
| **Oboe 8'** | Thin characterful reed — plaintive and singing |
| **Clarinet 8'** | Solo reed with strong fundamental — warm and woody |
| **Trompette Harmonique 8'** | Brilliant harmonic trumpet — scintillating treble |
| **Clarion 4'** | Bright trumpet at 4' — piercing solo or chorus reed |

### Pedal

| Stop | Character |
|------|-----------|
| **Double Open Bass 32'** | Massive sub-bass — the deepest foundation |
| **Open Diapason 16'** | Pedal principal — solid 16' foundation |
| **Violone 16'** | Pedal string bass — lean, articulate 16' tone |
| **Principal 8'** | Pedal principal at 8' — supports the ensemble |
| **Bourdon 8'** | Stopped flute pedal — round, soft bass |
| **Octave 4'** | Clear 4' pedal principal — definition in the bass |
| **Ophicleide 16'** | Powerful pedal reed — the voice of the pedal division |
| **Trombone 16'** | Commanding pedal reed — weight and majesty |

### Effect

| Stop | Character |
|------|-----------|
| **Tremulant** | Activates wind-pressure LFO over all active stops |

---

## Room Presets

| Preset | Character |
|--------|-----------|
| **Grand Cathedral** | Long shimmer, wide stereo, deep resonance (~4–5 s RT60) |
| **Stone Chapel** | Medium church, stone reflections |
| **Concert Hall** | Balanced reverb, natural warmth |
| **Gothic Basilica** | Extreme decay, cavernous |
| **Intimate Room** | Small hall, close and present |
| **Dry Studio** | Minimal reverb — for checking raw stop tone |

---

## Tuning Systems

| Tuning | Description |
|--------|-------------|
| **Equal** | Standard 12-TET |
| **Pythagorean** | Pure perfect fifths (3:2 ratio) |
| **Meantone** | Quarter-comma meantone (C-based) |
| **Werckmeister III** | Well-temperament (C-based) |

---

## Project Structure

```
voice-of-callisto/
├── main.py                   Entry point
├── engine/
│   ├── audio.py              sounddevice OutputStream wrapper (44100 Hz, 4096 block)
│   ├── mixer.py              Polyphonic mixer: voice pool, reverb, tremulant, normalization
│   ├── organ.py              OrganVoice — single note with chorus, chiff, envelope
│   ├── oscillator.py         Wavetable oscillator with band-limited waveforms and vibrato
│   ├── envelope.py           Smoothstep ADSR with RETRIGGER crossfade
│   ├── midi_player.py        Background-thread MIDI file player
│   ├── tunings.py            Alternate tuning tables (4 tunings)
│   └── recorder.py           WAV/MP3 recording engine
├── gui/
│   ├── main_window.py        Main window, event filter, stop groups
│   ├── keyboard.py           Full-range piano keyboard (C1–C7), split hands
│   ├── stop_panel.py         Stop toggle buttons grouped by family
│   ├── drawbars.py           9-drawbar vertical slider panel
│   ├── drawbar_presets.py    Drawbar registration presets
│   ├── swell.py              4-band swell EQ sliders
│   ├── room_panel.py         Room acoustic preset selector
│   ├── midi_panel.py         MIDI transport controls
│   └── recorder.py           Recording panel
├── stops/
│   └── profiles.py           Stop definitions, harmonic profiles, voicing parameters
└── tests/
    ├── test_envelope.py      Envelope curve correctness, retrigger smoothness
    ├── test_voice.py         Voice transient suppression, retrigger continuity
    ├── test_mixer.py         Normalization, rapid re-strikes, voice lifecycle
    ├── test_oscillator.py    Output correctness, variable block sizes, buffer reuse
    └── test_performance.py   Render budget, clipping, stereo separation
```

---

## Testing

```bash
uv run pytest tests/ -v
```

54 tests covering envelopes, voices, mixer normalization, oscillator correctness, and render budget.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| **PyQt6** | GUI framework |
| **numpy** | All audio signal processing (fully vectorized) |
| **sounddevice** | Real-time audio output (PortAudio) |
| **mido** | MIDI file parsing |
| **ffmpeg** | (optional) MP3 recording |

---

## How It Works

### Synthesis Chain

```
Key/MIDI event → Mixer.note_on() → SimpleQueue
    ↓
Mixer._process_events() → creates OrganVoice
    ↓
OrganVoice.render()
  ├── oscillator pairs (wavetable × harmonic amps)
  ├── + chiff noise burst
  ├── + tracker click impulse
  ├── + wind noise
  └── × ADSR envelope
    ↓
Sum all voices → gain normalization (1/√N, linear ramp)
    ↓
DC removal → Room resonance → Tremulant LFO
    ↓
StereoReverb (decorrelated L/R Schroeder networks)
    ↓
tanh saturation → sounddevice output buffer
```

### Oscillator

Each harmonic is rendered by a phase-accumulating wavetable lookup with linear interpolation. Four waveform families pre-computed at startup:

- **Principal** — balanced even and odd harmonics
- **Flute** — near-pure fundamental, mostly odd
- **Reed** — sawtooth-like with 1/k·0.92^k rolloff
- **String** — strong fundamental, odd-harmonic emphasis for edge

Each waveform has multiple band-limited tiers (fewer harmonics for higher pitches) to prevent aliasing. Work buffers are pre-allocated and reused across all oscillator calls to eliminate numpy GC pressure in the hot path.

### Reverb

A stereo pair of Schroeder reverbs with asymmetric delay times for wide stereo image. Each channel has:
- Pre-delay buffer (18–48 ms for room depth)
- 7 parallel comb filters (damped feedback delay lines)
- 4 series allpass filters (diffusion)

### Real-Time Architecture

Audio runs in a sounddevice callback at 4096 frames / 44100 Hz (~93 ms budget). GUI ↔ audio communication via lock-free `SimpleQueue` of `AudioEvent` objects. All signal processing is fully vectorized numpy — no per-sample Python loops. Average render time is ~45 ms for 8 voices.

---

## License

MIT
