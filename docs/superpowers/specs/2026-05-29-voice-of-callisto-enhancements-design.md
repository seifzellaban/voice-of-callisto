# Voice of Callisto — Feature Enhancements Design

> **Goal:** Add 12 new organ stops, sustain pedal, per-stop volume, transpose, alternate tunings, and WAV/MP3 recording.

**Architecture:** All features follow existing patterns — mixer event queue for thread-safe GUI→audio communication, pre-computed tables where possible, minimal new dependencies. No structural refactoring needed.

**Tech Stack:** Python 3.13, PyQt6, numpy, mido, ffmpeg (for MP3 export), wave (stdlib for WAV).

---

## 1. Additional Stops

Add 4 more stops to each of the 3 groups (12 new stops total), bringing each group to 8 stops.

### Manual — Foundation (+4)

| Stop | Waveform | Voice Parameters |
|---|---|---|
| Geigen Diapason 8' | **string** | Brighter stringy diapason. Harmonics: 0.5:0.40, 1:1.0, 2:0.55, 3:0.32, 4:0.18, 5:0.10, 6:0.05, 7:0.03. Chorus detune 0.8. |
| Flûte Harmonique 8' | **flute** | Warm rich harmonic flute. Harmonics: 0.5:0.30, 1:1.0, 3:0.20, 5:0.06. Chorus detune 0.5, softer attack (55ms). |
| Viola 4' | **string** | Bright alto string. Harmonics: 2:1.0, 3:0.50, 4:0.30, 5:0.15, 6:0.08. Chorus detune 1.2, faster attack (35ms). |
| Open Flute 4' | **flute** | Round 4' flute clarity. Harmonics: 2:1.0, 3:0.15, 5:0.04. Chorus detune 0.4. |

### Manual — Mixture & Reeds (+4)

| Stop | Waveform | Voice Parameters |
|---|---|---|
| Oboe 8' | **reed** | Thin characterful reed. Harmonics: 0.5:0.40, 1:1.0, 2:0.65, 3:0.40, 4:0.25, 5:0.15, 6:0.08, 7:0.04. Gentle attack (40ms). |
| Clarinet 8' | **reed** | Solo reed with strong fundamental. Harmonics: 0.5:0.20, 1:1.0, 2:0.30, 3:0.60, 4:0.20, 5:0.45, 6:0.15. Odd-harmonic heavy. |
| Bassoon 16' | **reed** | Soft smooth reed in 16' octave. Harmonics: 0.5:1.0, 1:0.80, 2:0.55, 3:0.35, 4:0.20, 5:0.10. Gentle attack (50ms), long release (900ms). |
| Trompette Harmonique 8' | **reed** | Brilliant trumpet variant. Harmonics: 0.5:0.60, 1:1.0, 2:0.90, 3:0.80, 4:0.70, 5:0.60, 6:0.50, 7:0.40. Fast attack (18ms). |

### Pedal (+4)

| Stop | Waveform | Voice Parameters |
|---|---|---|
| Violone 16' | **string** | String bass for pedal. Harmonics: 0.5:1.0, 1:0.70, 2:0.40, 3:0.22, 4:0.12, 5:0.06. Division: pedal. |
| Bourdon 8' | **flute** | Stopped flute pedal. Harmonics: 0.5:0.50, 1:1.0, 3:0.12, 5:0.03. Division: pedal, slow attack (60ms). |
| Octave 4' | **principal** | Clear 4' pedal principal. Harmonics: 2:1.0, 3:0.40, 4:0.20, 5:0.08. Division: pedal. |
| Trombone 16' | **reed** | Powerful pedal reed. Harmonics: 0.5:1.0, 1:0.95, 2:0.85, 3:0.72, 4:0.60, 5:0.48. Division: pedal, fast attack (20ms), longer release (550ms). |

### GUI Changes
- Update `STOP_FAMILIES` in `gui/stop_panel.py` with new stop names
- Add tooltip strings for each new stop
- Register all new stops in `STOP_DEFS` in `stops/profiles.py`

---

## 2. WAV/MP3 Recording

### Data Flow
1. A shared `RecorderState` object (thread-safe, holds `recording: bool` flag and `buffers: list[np.ndarray]`) lives on the mixer
2. Record button toggles `recording` flag via `mixer.event_queue`
3. In `AudioEngine._callback`, after each `mixer.render(frames)`, check `mixer._recorder.recording` — if True, copy the stereo output into `mixer._recorder.buffers`
4. On stop: take ownership of the buffers list, concatenate all frames, write WAV via stdlib `wave`, then optionally re-encode to MP3 via `subprocess.run(["ffmpeg", ...])` in a background thread
5. Save file dialog (QFileDialog) lets user pick location and format
6. Status label shows "Recording..." / "Encoding..." / "Saved."

### Thread Safety
- `recording` flag is `threading.Event` (thread-safe)
- Buffers are appended from audio callback thread; ownership transferred to GUI thread on stop via a lock or simple flag-check + list swap

### Files
- **Create:** `gui/recorder.py` — `RecorderPanel` widget (record button, format selector, status label)
- **Create:** `engine/recorder.py` — `RecorderState` class with `recording` flag and `buffers` list, `start()`, `stop() -> bytes` (WAV data), `save(path, format)` method
- **Modify:** `engine/mixer.py` — hold `RecorderState` instance
- **Modify:** `engine/audio.py` — capture frames when recorder active
- **Modify:** `gui/main_window.py` — add recorder panel, connect to mixer

### Dependencies
- `wave` (stdlib) for WAV writing
- `ffmpeg` (external, subprocess) for MP3 conversion

---

## 3. Sustain Pedal

### Data Flow
- GUI toggle button for sustain pedal (temporary; architecture ready for MIDI CC 64 input later)
- Button emits `sustain_toggled(bool)` → mixer `EventType.SUSTAIN_PEDAL`
- In mixer `_process_events`:
  - **On:** set `_sustain_active = True`
  - **Off:** set `_sustain_active = False`, release all `_sustained_notes` (call `voice.note_off()` on each)
- On `NOTE_OFF` while sustain active: add note to `_sustained_notes`, do NOT call `voice.note_off()`
- On `NOTE_OFF` when sustain inactive: normal release (immediately)
- The `_sustained_notes` set tracks notes held by sustain (not by key)

### GUI
- Small toggle button "Sustain" below the keyboard or in status row
- Lights up when active (golden border)
- Keyboard shortcut: assignable

### Files
- **Modify:** `engine/mixer.py` — add `SUSTAIN_PEDAL` event type, `_sustain_active: bool`, `_sustained_notes: set[int]`, handle both in `_process_events`
- **Modify:** `gui/main_window.py` — add sustain toggle button, connect signal

---

## 4. Per-Stop Volume

### Data Flow
- Each stop in the panel gets a small vertical slider (narrow, ~50px tall, 0–10 range)
- Slider emits `stop_volume_changed(stop_name, float)` → mixer `EventType.STOP_VOLUME`
- Mixer stores `_stop_volumes: dict[str, float]` defaulting to 1.0 (range 0.0–1.5)
- In `render()`, when summing harmonic contributions per profile, multiply amp sum by `_stop_volumes.get(stop_name, 1.0)`

### GUI
- Grid expands to 4 columns: `[button] [slider] [button] [slider]` per row
- Sliders: 16px wide, 50px tall, range 0–10, mapped to 0.0–1.5 gain
- No value label to save space

### Files
- **Modify:** `gui/stop_panel.py` — expand grid to 4 columns with slider per stop, emit `stop_volume_changed(stop_name, value)` signal
- **Modify:** `engine/mixer.py` — add `STOP_VOLUME` event type, `_stop_volumes: dict[str, float]` defaulting to 1.0, apply multiplier in `render()` harmonic summing
- **Modify:** `gui/main_window.py` — connect signal

---

## 5. Transpose

### Data Flow
- Mixer stores `_transpose: int = 0` (range -12 to +12)
- In `_process_events`, on `NOTE_ON`/`NOTE_OFF`: add transpose to note number, clamp to 0-127
- GUI: small label showing current transpose (+0, -2, +5, etc.) with up/down arrow buttons

### GUI
- Add transpose controls to status row area or bottom bar
- Two buttons (▲/▼) + label showing current value

### Files
- **Modify:** `engine/mixer.py` — add `TRANSPOSE_SET` event, `_transpose` offset in note handling
- **Modify:** `gui/main_window.py` — add transpose controls, connect to mixer

---

## 6. Alternate Tunings

### Approach
- Pre-compute 4 tuning tables (128 float32 values each) mapping MIDI note → frequency
- Tunings: Equal (default), Meantone, Werckmeister III, Pythagorean
- Store in `engine/tunings.py`
- Pass active tuning table to `OrganVoice.__init__` instead of calling `midi_to_freq(note)`
- GUI: cycle button or dropdown

### Tuning Formulas
- **Equal:** `440 * 2^((n-69)/12)` (current formula)
- **Pythagorean:** Pure fifths (ratio 3:2), all 12 notes derived via circle of fifths
- **Meantone:** Pure major thirds (ratio 5:4), quarter-comma meantone
- **Werckmeister III:** Baroque well-temperament, unequal but playable in all keys

### Pre-computation
- `engine/tunings.py` exports `TUNINGS: dict[str, np.ndarray]` (128-element arrays)
- `OrganVoice` stores a reference to the active table
- Changing tuning requires re-creating voices — simplest approach: clear all voices on tuning change

### Files
- **Create:** `engine/tunings.py` — four tuning tables
- **Modify:** `engine/organ.py` — accept tuning table in `__init__`, use for `_fundamental`
- **Modify:** `engine/organ.py` — `midi_to_freq` kept for backward compat but OrganVoice uses table
- **Modify:** `engine/mixer.py` — add `TUNING_SET` event, re-create voices on change
- **Modify:** `gui/main_window.py` — add tuning selector

---

## Event Types Summary

New event types in `mixer.EventType`:
- `SUSTAIN_PEDAL` — data: `bool` (on/off)
- `STOP_VOLUME` — data: `(str stop_name, float volume)`
- `TRANSPOSE_SET` — data: `int` (semitones)
- `TUNING_SET` — data: `str` (tuning name)

---

## Files Summary

| File | Action |
|---|---|
| `stops/profiles.py` | Add 12 new `StopDefinition` entries + `STOP_DEFS` registration |
| `gui/stop_panel.py` | Update `STOP_FAMILIES`, tooltips; add per-stop volume sliders |
| `gui/recorder.py` | **Create** — record/stop panel |
| `gui/audio.py` | Add recording frame capture |
| `gui/main_window.py` | Add recorder, sustain, transpose, tuning controls |
| `engine/mixer.py` | Add all new event types, sustain, transpose, stop volumes, tuning |
| `engine/organ.py` | Accept tuning table in `__init__` |
| `engine/tunings.py` | **Create** — 4 tuning tables |
| `engine/midi_player.py` | Forward sustain CC 64 |
