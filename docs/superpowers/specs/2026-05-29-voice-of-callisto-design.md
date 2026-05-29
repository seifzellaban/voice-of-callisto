# Voice of Callisto — Design Spec

Voice of Callisto: an optimized, division-aware pipe organ
synthesizer built on the existing Python wavetable engine.

## Goals

1. Replace stop layout with Royal Albert Hall (Willis/Harrison) specification
2. Add Manual / Pedal division routing
3. Optimize the audio pipeline so it no longer overflows (target: <60ms at 8
   active voices on modest hardware)

Non-goals: changing the synthesis character, reducing stereo quality, adding
Rust dependencies, changing the GUI toolkit.

## Architecture

### Division Support

The Mixer maintains two independent stop sets:

- **Manual division**: stops sound on MIDI notes ≥ 36 (C2)
- **Pedal division**: stops sound on MIDI notes ≤ 53 (F3)
- Overlapping notes (36–53) fire both divisions simultaneously

Each division computes its own `harmonic_amps` array from its active stop
profiles + drawbar values. Voice pools remain global (shared 24-voice limit).
Both divisions feed into the same reverb chain — no second reverb instance.

Voice key encoding: manual voices use `note` as key, pedal voices use
`-note - 1` (negative, non-overlapping with mutation voices which use
`-(note * 1000 + shift_id + 1)`). The `_process_events()` method checks the
incoming note number and creates voices for each applicable division. Note-off
releases all voices for that note regardless of division key.

### Stop Definitions

`StopDefinition` gains a `division: Literal["manual", "pedal"]` field. The
Tremulant remains global (`division="both"`).

Each new stop reuses an existing harmonic profile or defines a new one:

| Division | Stop | Waveform | Pitch Shift | Harmonics (profile key → amplitude) |
|---|---|---|---|---|
| Manual | Double Open Diapason 16' | principal | 2.0 (16' = 2× 8') | Same as Principal 8': {1:1.0, 2:0.60, 3:0.42, 4:0.28, 5:0.18, 6:0.12, 7:0.06, 8:0.08, 9:0.03, 10:0.04, 12:0.02} |
| Manual | Open Diapason 8' | principal | 1.0 | Same as Principal 8' |
| Manual | Principal 4' | principal | 1.0 | Octave 4' profile: {2:1.0, 4:0.50, 6:0.32, 8:0.18, 10:0.10, 12:0.06, 14:0.03} |
| Manual | Fifteenth 2' | principal | 1.0 | Super Oct 2' profile: {4:1.0, 8:0.55, 12:0.35, 16:0.18, 20:0.08, 24:0.04} |
| Manual | Mixture IV | principal | 1.0 | Mixture: {4:0.45, 5:0.60, 6:0.75, 8:1.0, 10:0.65, 12:0.35, 15:0.15, 16:0.08} with `is_mutation=True` |
| Manual | Double Trumpet 16' | reed | 2.0 | Trumpet: {1:1.0, 2:0.95, 3:0.88, ... 19:0.02} |
| Manual | Trumpet 8' | reed | 1.0 | Trumpet 8' profile (same harmonics as above) |
| Manual | Clarion 4' | reed | 1.0 | Reed 8' profile: {1:1.0, 2:0.90, 3:0.75, ... 16:0.03} with brighter attack/shorter release |
| Pedal | Double Open Bass 32' | principal | 4.0 (32' = 4× 8') | Bourdon-style: {1:1.0, 3:0.18, 5:0.08, 7:0.03} |
| Pedal | Open Diapason 16' | principal | 2.0 | Principal 8' profile |
| Pedal | Principal 8' | principal | 1.0 | Principal 8' profile |
| Pedal | Ophicleide 16' | reed | 2.0 | Trumpet profile with extra low-harmonic weight: {1:1.0, 2:0.98, 3:0.90, 4:0.82, ... 19:0.02} |
| Global | Tremulant | — | — | Existing effect, unchanged |

### Presets / Stop Groups

Updated to match the new stop list:

| # | Name | Stops |
|---|------|-------|
| 0 | Full Organ | All 12 |
| 1 | Diapason Chorus | Double Open Diapason 16', Open Diapason 8', Principal 4', Fifteenth 2', Mixture IV |
| 2 | Reed Chorus | Double Trumpet 16', Trumpet 8', Clarion 4', Ophicleide 16' |
| 3 | Flute Chorus | Double Open Diapason 16', Open Diapason 8' |
| 4 | Principal 8' | Open Diapason 8' only |
| 5 | Pedal Stops | Double Open Bass 32', Open Diapason 16', Principal 8', Ophicleide 16' |
| 6 | Trumpet Solo | Trumpet 8' + Pedal stops |
| 7 | Full Swell | All manuals |
| 8 | Cathedral | Diapason Chorus + Trumpet 8' + Pedal |
| 9 | Ethereal | Open Diapason 8' + Clarion 4' + Tremulant |

## Optimizations

All optimizations are zero-to-negligible quality impact. None alter the
reverb character, stereo width, or synthesis engine.

### 1. Wind noise — remove np.concatenate

File: `engine/organ.py`

Replace:
```python
end_npos = self._wind_noise_pos + num_frames
if end_npos <= _WIND_NOISE_SIZE:
    noise = _WIND_NOISE_TABLE[self._wind_noise_pos:end_npos]
else:
    part1 = _WIND_NOISE_TABLE[self._wind_noise_pos:]
    part2 = _WIND_NOISE_TABLE[:num_frames - len(part1)]
    noise = np.concatenate((part1, part2))
```

With: pre-allocated `_wind_noise_buf` per voice, fill via slice copies.

### 2. Room resonance — pre-computed tables

File: `engine/mixer.py`

Pre-compute a 1-cycle lookup table per resonant frequency at init. Replace
per-block `np.sin(2π·freq·t/sr + phase)` with phase accumulator + linear
interpolation into the LUT.

### 3. tanh saturation — lookup table

File: `engine/mixer.py`

Pre-compute `np.tanh` into a 4096-entry `float32` array at module load.
Map input sample → nearest index via `(sample * scale + offset).astype(int)`.

### 4. Allpass filter — remove per-call allocation

File: `engine/mixer.py`

Replace `delayed = self._buffer[buf_slice].copy()` with a pre-allocated
temp buffer and `np.copyto`.

### 5. Raise harmonic skip threshold

File: `engine/mixer.py`

Skip harmonic render if `harmonic_amps[i] < 0.02` instead of 0.01.

### 6. Raise chorus skip threshold

File: `engine/mixer.py` (propagated to voice rendering)

Skip chorus partner if `amp < 0.20` instead of 0.15.

## Files Changed

| File | Changes |
|---|---|
| `stops/profiles.py` | Replace 11 stops with 12 RAH stops + division field |
| `engine/mixer.py` | Division routing, room resonance LUT, tanh LUT, thresholds, allpass temp buf |
| `engine/organ.py` | Wind noise pre-allocated buffer |
| `gui/stop_panel.py` | Two labeled sections (Manual / Pedal) |
| `gui/main_window.py` | Stop groups updated, division display |

No changes to: `engine/oscillator.py`, `engine/envelope.py`, `engine/audio.py`.

## Verification

Run existing performance tests after each change:
```
uv run pytest tests/ -v
```

Performance target: P95 render time for 8 voices < 80ms (currently ~80ms+,
should improve to ~65-70ms).

Manual test: hold 10+ voice chord with Grand Cathedral reverb, verify no
audio glitches for 30+ seconds.
