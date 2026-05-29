# Voice of Callisto Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development (recommended) or executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port the Royal Albert Hall stop layout with Manual/Pedal division into the optimized Python engine.

**Architecture:** 12-stop Willis specification with division-aware routing, layered on top of the existing wavetable additive synthesis engine. Six targeted optimizations reduce per-block render time to prevent audio overflow.

**Tech Stack:** Python 3.13, numpy, sounddevice, PyQt6

**Spec:** `docs/superpowers/specs/2026-05-29-voice-of-callisto-design.md`

---

### Task 1: Add division field to StopDefinition and replace stop profiles

**Files:**
- Modify: `stops/profiles.py` (entire file)

- [ ] **Step 1: Read the existing file**

Run: `cat stops/profiles.py`

- [ ] **Step 2: Add `division` field to StopDefinition**

Add `division: str = "manual"` after `is_mutation` in the `StopDefinition` dataclass.

- [ ] **Step 3: Replace all stop definitions with RAH specifications**

Delete all existing stop definitions (PRINCIPAL_8_DEF through TREMULANT_DEF) and replace with these:

```python
DOUBLE_OPEN_DIAPASON_16_DEF = StopDefinition(
    harmonics={1: 1.0, 2: 0.60, 3: 0.42, 4: 0.28, 5: 0.18, 6: 0.12, 7: 0.06, 8: 0.08, 9: 0.03, 10: 0.04, 12: 0.02},
    waveform="principal", chorus_detune=0.7, vibrato_depth=0.5,
    chiff_amount=0.015, chiff_ms=12.0, wind_noise=0.004, attack_ms=50.0, release_ms=750.0,
    pitch_shift=2.0, division="manual",
)

OPEN_DIAPASON_8_DEF = StopDefinition(
    harmonics={1: 1.0, 2: 0.60, 3: 0.42, 4: 0.28, 5: 0.18, 6: 0.12, 7: 0.06, 8: 0.08, 9: 0.03, 10: 0.04, 12: 0.02},
    waveform="principal", chorus_detune=0.7, vibrato_depth=0.5,
    chiff_amount=0.015, chiff_ms=12.0, wind_noise=0.004, attack_ms=50.0, release_ms=750.0,
    division="manual",
)

PRINCIPAL_4_DEF = StopDefinition(
    harmonics={2: 1.0, 4: 0.50, 6: 0.32, 8: 0.18, 10: 0.10, 12: 0.06, 14: 0.03},
    waveform="principal", chorus_detune=0.9, vibrato_depth=0.6,
    chiff_amount=0.009, chiff_ms=10.0, wind_noise=0.003, attack_ms=42.0, release_ms=700.0,
    division="manual",
)

FIFTEENTH_2_DEF = StopDefinition(
    harmonics={4: 1.0, 8: 0.55, 12: 0.35, 16: 0.18, 20: 0.08, 24: 0.04},
    waveform="principal", chorus_detune=1.1, vibrato_depth=0.7,
    chiff_amount=0.007, chiff_ms=8.0, wind_noise=0.002, attack_ms=32.0, release_ms=600.0,
    division="manual",
)

MIXTURE_IV_DEF = StopDefinition(
    harmonics={4: 0.45, 5: 0.60, 6: 0.75, 8: 1.0, 10: 0.65, 12: 0.35, 15: 0.15, 16: 0.08},
    waveform="principal", chorus_detune=1.0, vibrato_depth=0.7,
    chiff_amount=0.012, chiff_ms=10.0, wind_noise=0.003, attack_ms=40.0, release_ms=650.0,
    is_mutation=True, pitch_shift=1.0, division="manual",
)

DOUBLE_TRUMPET_16_DEF = StopDefinition(
    harmonics={1: 1.0, 2: 0.95, 3: 0.88, 4: 0.80, 5: 0.72, 6: 0.63, 7: 0.55, 8: 0.48, 9: 0.40, 10: 0.33, 11: 0.27, 12: 0.22, 13: 0.17, 14: 0.13, 15: 0.10, 16: 0.07, 17: 0.05, 18: 0.03, 19: 0.02},
    waveform="reed", chorus_detune=1.5, vibrato_depth=0.4, vibrato_rate=5.5,
    chiff_amount=0.005, chiff_ms=5.0, wind_noise=0.002, attack_ms=22.0, release_ms=450.0,
    pitch_shift=2.0, division="manual",
)

TRUMPET_8_DEF = StopDefinition(
    harmonics={1: 1.0, 2: 0.95, 3: 0.88, 4: 0.80, 5: 0.72, 6: 0.63, 7: 0.55, 8: 0.48, 9: 0.40, 10: 0.33, 11: 0.27, 12: 0.22, 13: 0.17, 14: 0.13, 15: 0.10, 16: 0.07, 17: 0.05, 18: 0.03, 19: 0.02},
    waveform="reed", chorus_detune=1.5, vibrato_depth=0.4, vibrato_rate=5.5,
    chiff_amount=0.005, chiff_ms=5.0, wind_noise=0.002, attack_ms=22.0, release_ms=450.0,
    division="manual",
)

CLARION_4_DEF = StopDefinition(
    harmonics={1: 1.0, 2: 0.90, 3: 0.75, 4: 0.65, 5: 0.55, 6: 0.45, 7: 0.38, 8: 0.30, 9: 0.24, 10: 0.20, 11: 0.16, 12: 0.12, 13: 0.09, 14: 0.07, 15: 0.05, 16: 0.03},
    waveform="reed", chorus_detune=1.2, vibrato_depth=0.8, vibrato_rate=6.2,
    chiff_amount=0.010, chiff_ms=8.0, wind_noise=0.003, attack_ms=28.0, release_ms=500.0,
    division="manual",
)

DOUBLE_OPEN_BASS_32_DEF = StopDefinition(
    harmonics={1: 1.0, 3: 0.18, 5: 0.08, 7: 0.03},
    waveform="principal", chorus_detune=0.3, vibrato_depth=0.25,
    chiff_amount=0.025, chiff_ms=28.0, wind_noise=0.007, attack_ms=70.0, release_ms=1100.0,
    pitch_shift=4.0, division="pedal",
)

OPEN_DIAPASON_16_PEDAL_DEF = StopDefinition(
    harmonics={1: 1.0, 2: 0.60, 3: 0.42, 4: 0.28, 5: 0.18, 6: 0.12, 7: 0.06, 8: 0.08, 9: 0.03, 10: 0.04, 12: 0.02},
    waveform="principal", chorus_detune=0.7, vibrato_depth=0.5,
    chiff_amount=0.015, chiff_ms=12.0, wind_noise=0.004, attack_ms=55.0, release_ms=900.0,
    pitch_shift=2.0, division="pedal",
)

PRINCIPAL_8_PEDAL_DEF = StopDefinition(
    harmonics={1: 1.0, 2: 0.60, 3: 0.42, 4: 0.28, 5: 0.18, 6: 0.12, 7: 0.06, 8: 0.08, 9: 0.03, 10: 0.04, 12: 0.02},
    waveform="principal", chorus_detune=0.7, vibrato_depth=0.5,
    chiff_amount=0.015, chiff_ms=12.0, wind_noise=0.004, attack_ms=50.0, release_ms=750.0,
    division="pedal",
)

OPHICLEIDE_16_DEF = StopDefinition(
    harmonics={1: 1.0, 2: 0.98, 3: 0.90, 4: 0.82, 5: 0.74, 6: 0.65, 7: 0.56, 8: 0.49, 9: 0.41, 10: 0.34, 11: 0.28, 12: 0.23, 13: 0.18, 14: 0.14, 15: 0.10, 16: 0.07, 17: 0.05, 18: 0.03, 19: 0.02},
    waveform="reed", chorus_detune=1.5, vibrato_depth=0.4, vibrato_rate=5.5,
    chiff_amount=0.005, chiff_ms=5.0, wind_noise=0.002, attack_ms=25.0, release_ms=500.0,
    pitch_shift=2.0, division="pedal",
)

TREMULANT_DEF = StopDefinition(
    harmonics={}, waveform="sine", is_tremulant=True,
    tremulant_depth=0.12, tremulant_rate=5.8, tremulant_pitch_cents=18.0,
    division="both",
)
```

- [ ] **Step 4: Update STOP_DEFS registry**

Replace STOP_DEFS to use all 12 new stops + Tremulant:

```python
STOP_DEFS: dict[str, StopDefinition] = {
    "Double Open Diapason 16'": DOUBLE_OPEN_DIAPASON_16_DEF,
    "Open Diapason 8'": OPEN_DIAPASON_8_DEF,
    "Principal 4'": PRINCIPAL_4_DEF,
    "Fifteenth 2'": FIFTEENTH_2_DEF,
    "Mixture IV": MIXTURE_IV_DEF,
    "Double Trumpet 16'": DOUBLE_TRUMPET_16_DEF,
    "Trumpet 8'": TRUMPET_8_DEF,
    "Clarion 4'": CLARION_4_DEF,
    "Double Open Bass 32'": DOUBLE_OPEN_BASS_32_DEF,
    "Open Diapason 16'": OPEN_DIAPASON_16_PEDAL_DEF,
    "Principal 8'": PRINCIPAL_8_PEDAL_DEF,
    "Ophicleide 16'": OPHICLEIDE_16_DEF,
    "Tremulant": TREMULANT_DEF,
}
```

STOP_REGISTRY stays the same (auto-generated from STOP_DEFS filtering out tremulant).

- [ ] **Step 5: Run tests to check nothing is broken yet**

Run: `uv run pytest tests/ -v`
Expected: Some tests may fail since stop names changed. That's expected — we'll fix in later tasks.

- [ ] **Step 6: Verify division field is on all stops**

Run: `python3 -c "from stops.profiles import STOP_DEFS; [print(f'{k}: division={v.division}') for k,v in STOP_DEFS.items()]"`

Expected: All 13 stops printed with correct division field (manual/pedal/both).

---

### Task 2: Wind noise optimization — remove np.concatenate

**Files:**
- Modify: `engine/organ.py`

- [ ] **Step 1: Add pre-allocated wind noise buffer to OrganVoice.__slots__**

Add `"_wind_noise_buf",` to the `__slots__` tuple.

- [ ] **Step 2: Initialize the buffer in `__init__`**

After the line `self._wind_noise_pos = pipe_rand.integers(0, _WIND_NOISE_SIZE)`, add:
```python
self._wind_noise_buf = np.empty(4096, dtype=np.float32)
```

- [ ] **Step 3: Replace the wind noise rendering block in `render()`**

Find this block (around line 254-269):
```python
if self._noise_level > 0:
    end_npos = self._wind_noise_pos + num_frames
    if end_npos <= _WIND_NOISE_SIZE:
        noise = _WIND_NOISE_TABLE[self._wind_noise_pos:end_npos]
    else:
        part1 = _WIND_NOISE_TABLE[self._wind_noise_pos:]
        part2 = _WIND_NOISE_TABLE[:num_frames - len(part1)]
        noise = np.concatenate((part1, part2))
    self._wind_noise_pos = end_npos % _WIND_NOISE_SIZE
```

Replace with:
```python
if self._noise_level > 0:
    end_npos = self._wind_noise_pos + num_frames
    buf = self._wind_noise_buf[:num_frames]
    if end_npos <= _WIND_NOISE_SIZE:
        buf[:] = _WIND_NOISE_TABLE[self._wind_noise_pos:end_npos]
    else:
        wrap = _WIND_NOISE_SIZE - self._wind_noise_pos
        buf[:wrap] = _WIND_NOISE_TABLE[self._wind_noise_pos:]
        buf[wrap:] = _WIND_NOISE_TABLE[:num_frames - wrap]
    self._wind_noise_pos = end_npos % _WIND_NOISE_SIZE
```

Then replace subsequent use from `noise` to `buf`:
```python
if self._fundamental > 800:
    output += buf * (self._noise_level * 1.3)
else:
    output += buf * self._noise_level
```

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/ -v`
Expected: All pass (or fail only from known stop-name issues).

---

### Task 3: Room resonance — pre-computed lookup tables

**Files:**
- Modify: `engine/mixer.py`

- [ ] **Step 1: Add sine LUT creation to RoomResonance.__init__**

In `RoomResonance.__init__`, after `self._level_smooth = 0.0`, add:
```python
self._lut_size = 2048
self._lut1 = np.sin(2 * np.pi * np.arange(self._lut_size, dtype=np.float32) / self._lut_size).astype(np.float32)
self._lut2 = np.sin(2 * np.pi * np.arange(self._lut_size, dtype=np.float32) / self._lut_size).astype(np.float32)
self._lut3 = np.sin(2 * np.pi * np.arange(self._lut_size, dtype=np.float32) / self._lut_size).astype(np.float32)
```

- [ ] **Step 2: Add phase increment fields**

In `__init__`, change phase initialization and add increments:
```python
self._phase1 = 0.0
self._phase2 = 0.0
self._phase3 = 0.0
self._phase_inc1 = 0.0
self._phase_inc2 = 0.0
self._phase_inc3 = 0.0
```

- [ ] **Step 3: Update set_freqs in StereoReverb room preset change**

In `_process_events` → `ROOM_PRESET` handler, after updating `self._room_resonance._freq1/2/3`, add:
```python
self._room_resonance._phase_inc1 = preset.resonance_freqs[0] * self._lut_size / self.sample_rate
self._room_resonance._phase_inc2 = preset.resonance_freqs[1] * self._lut_size / self.sample_rate
self._room_resonance._phase_inc3 = preset.resonance_freqs[2] * self._lut_size / self.sample_rate
```

Also compute initial increments in `RoomResonance.__init__`:
```python
self._phase_inc1 = self._freq1 * self._lut_size / sample_rate
self._phase_inc2 = self._freq2 * self._lut_size / sample_rate
self._phase_inc3 = self._freq3 * self._lut_size / sample_rate
```

- [ ] **Step 4: Replace the `process()` method body**

Replace the body of `RoomResonance.process()` with LUT-based rendering:

```python
def process(self, signal: np.ndarray, has_active_voices: bool) -> np.ndarray:
    n = len(signal)

    target = 0.025 if has_active_voices else 0.0
    rate = 0.001 if target > self._level_smooth else 0.0002
    self._level_smooth += (target - self._level_smooth) * rate

    if self._level_smooth < 0.0001:
        return signal

    # Generate resonance from LUTs using phase accumulator
    t = np.arange(n, dtype=np.float32)
    phases1 = (self._phase1 + self._phase_inc1 * t) % self._lut_size
    phases2 = (self._phase2 + self._phase_inc2 * t) % self._lut_size
    phases3 = (self._phase3 + self._phase_inc3 * t) % self._lut_size

    idx1 = phases1.astype(np.int32)
    idx2 = phases2.astype(np.int32)
    idx3 = phases3.astype(np.int32)

    res1 = self._lut1[idx1]
    res2 = self._lut2[idx2]
    res3 = self._lut3[idx3]

    self._phase1 = phases1[-1] + self._phase_inc1
    self._phase1 %= self._lut_size
    self._phase2 = phases2[-1] + self._phase_inc2
    self._phase2 %= self._lut_size
    self._phase3 = phases3[-1] + self._phase_inc3
    self._phase3 %= self._lut_size

    return signal + (res1 * 0.45 + res2 * 0.35 + res3 * 0.20) * self._level_smooth
```

Remove the old np.arange + np.sin block and phase update code.

- [ ] **Step 5: Run tests**

Run: `uv run pytest tests/ -v`
Expected: All pass.

---

### Task 4: tanh saturation — lookup table

**Files:**
- Modify: `engine/mixer.py`

- [ ] **Step 1: Add pre-computed tanh LUT at module level**

After imports in `mixer.py`, add:
```python
_TANH_LUT_SIZE = 4096
_TANH_LUT_SCALE = 4.0  # input range: [-4, 4] covers tanh saturation well
_t = np.linspace(-_TANH_LUT_SCALE, _TANH_LUT_SCALE, _TANH_LUT_SIZE, dtype=np.float32)
_TANH_LUT = np.tanh(_t)
```

- [ ] **Step 2: Replace `_saturate` method**

Replace:
```python
def _saturate(self, signal: np.ndarray) -> np.ndarray:
    scaled = signal * self._master_volume
    scaled += 0.03 * (scaled ** 2)
    return np.tanh(scaled * 2.0).astype(np.float32) * 0.55
```

With:
```python
def _saturate(self, signal: np.ndarray) -> np.ndarray:
    scaled = signal * self._master_volume
    scaled += 0.03 * (scaled ** 2)
    # Map to LUT index
    t = scaled * 2.0  # same as np.tanh(scaled * 2.0)
    idx = ((t / _TANH_LUT_SCALE) * 0.5 + 0.5) * (_TANH_LUT_SIZE - 1)
    idx = np.clip(idx, 0, _TANH_LUT_SIZE - 1).astype(np.int32)
    return _TANH_LUT[idx].astype(np.float32) * 0.55
```

- [ ] **Step 3: Run tests**

Run: `uv run pytest tests/ -v`
Expected: All pass.

---

### Task 5: Allpass filter — remove per-call allocation

**Files:**
- Modify: `engine/mixer.py`

- [ ] **Step 1: Add temp buffer to AllpassFilter.__init__**

In `AllpassFilter.__init__`, after `self._gain = gain`, add:
```python
self._temp = np.empty(delay_samples, dtype=np.float32)
```

- [ ] **Step 2: Replace `.copy()` with np.copyto in process()**

Find:
```python
delayed = self._buffer[buf_slice].copy()
v = input_signal[out_slice] - self._gain * delayed
output[out_slice] = delayed + self._gain * v
self._buffer[buf_slice] = v
```

Replace with:
```python
temp = self._temp[:chunk]
np.copyto(temp, self._buffer[buf_slice])
v = input_signal[out_slice] - self._gain * temp
output[out_slice] = temp + self._gain * v
self._buffer[buf_slice] = v
```

- [ ] **Step 3: Run tests**

Run: `uv run pytest tests/ -v`
Expected: All pass.

---

### Task 6: Raise harmonic and chorus skip thresholds

**Files:**
- Modify: `engine/mixer.py` (harmonic amp computation)
- Modify: `engine/organ.py` (chorus skip threshold)

- [ ] **Step 1: Raise harmonic skip threshold in mixer.py**

In `Mixer.render()`, find the harmonic_amps computation loop. After computing `harmonic_amps[i]`, there's no explicit skip yet — the skip happens in `OrganVoice.render()`. We just need to update the threshold there.

- [ ] **Step 2: Raise chorus skip threshold in organ.py**

In `OrganVoice.render()`, find:
```python
if osc_b is not None and amp >= 0.15:
```

Change to:
```python
if osc_b is not None and amp >= 0.20:
```

- [ ] **Step 3: Run tests**

Run: `uv run pytest tests/ -v`
Expected: All pass.

---

### Task 7: Division routing in Mixer

**Files:**
- Modify: `engine/mixer.py`

- [ ] **Step 1: Update active_stops to support two divisions**

In `Mixer.__init__`, replace `self._active_stops` and `self._active_stop_defs` with division-aware versions:

```python
self._manual_stop_defs: dict[str, StopDefinition] = {}
self._pedal_stop_defs: dict[str, StopDefinition] = {}
self._manual_active: bool = False
self._pedal_active: bool = False

# Default: open Diapason 8' on manuals
for name, sdef in STOP_DEFS.items():
    if sdef.division == "manual" and name == "Open Diapason 8'":
        self._manual_stop_defs[name] = sdef
    if sdef.division == "pedal" and name == "Principal 8'":
        self._pedal_stop_defs[name] = sdef
```

Remove the old `_active_stops` and `_active_stop_defs` dicts. Keep `_tremulant_active`.

- [ ] **Step 2: Update STOP_TOGGLE event handler**

In `_process_events()`, `STOP_TOGGLE` case:

```python
elif event.type == EventType.STOP_TOGGLE:
    stop_name = event.data
    stop_def = STOP_DEFS.get(stop_name)
    if not stop_def:
        continue

    if stop_def.is_tremulant:
        self._tremulant_active = not self._tremulant_active
        if self._tremulant_active:
            self._tremulant_depth = stop_def.tremulant_depth
            self._tremulant_rate = stop_def.tremulant_rate
            self._tremulant_pitch_depth = stop_def.tremulant_pitch_cents
        continue

    # Route to appropriate division
    if stop_def.division == "manual":
        target = self._manual_stop_defs
    elif stop_def.division == "pedal":
        target = self._pedal_stop_defs
    else:
        continue  # shouldn't happen

    if stop_name in target:
        del target[stop_name]
    else:
        target[stop_name] = stop_def
```

Remove the old STOP_TOGGLE code.

- [ ] **Step 3: Update NOTE_ON for division routing**

In `_process_events()`, `NOTE_ON` case, replace the existing voice creation logic.

The new logic: determine which divisions fire based on note range, then create voices for each:

```python
if event.type == EventType.NOTE_ON:
    note = event.data
    divisions: list[tuple[str, dict[str, StopDefinition]]] = []

    if note >= 36:
        divisions.append(("manual", self._manual_stop_defs))
    if note <= 53:
        divisions.append(("pedal", self._pedal_stop_defs))

    for div_name, stop_defs in divisions:
        # Create voice key unique to division
        if div_name == "manual":
            voice_key = note
        else:
            voice_key = -note - 1

        existing = self._voices.get(voice_key)
        if existing is not None and existing.is_active:
            if existing.is_releasing:
                existing.retrigger()
            continue

        # ... voice creation with voice_key instead of note as key ...
```

Wrap the existing voice creation logic (with mutation stops, rapid_restrike, etc.) inside this loop, replacing the key with `voice_key`.

The mutation voice keying stays the same (already uses negative keys that won't collide with `-note - 1`).

- [ ] **Step 4: Update NOTE_OFF for division-aware cleanup**

The NOTE_OFF handler already releases all voices matching a note. Since manual voices use `note` and pedal voices use `-note - 1`, both will be found and released:

```python
elif event.type == EventType.NOTE_OFF:
    note = event.data
    self._note_release_samples[note] = self._sample_clock
    # Release manual voice (key = note)
    if note in self._voices:
        self._voices[note].note_off()
    # Release pedal voice (key = -note - 1)
    pedal_key = -note - 1
    if pedal_key in self._voices:
        self._voices[pedal_key].note_off()
    # Also release mutation voices for this note
    if note in self._mutation_keys:
        for mk in self._mutation_keys[note]:
            if mk in self._voices:
                self._voices[mk].note_off()
        del self._mutation_keys[note]
```

- [ ] **Step 5: Update render() for per-division harmonic amps**

In `Mixer.render()`, replace the single `harmonic_amps` computation with division-specific ones:

```python
# Compute harmonic amps per division
def compute_harmonic_amps(stop_defs: dict[str, StopDefinition]) -> np.ndarray | None:
    if not stop_defs:
        return None
    amps = np.zeros(len(DRAWBAR_HARMONICS), dtype=np.float32)
    for sdef in stop_defs.values():
        for i, h in enumerate(DRAWBAR_HARMONICS):
            h_int = int(round(h)) if h >= 1 else 1
            if h_int in sdef.harmonics:
                amps[i] += sdef.harmonics[h_int] * self._drawbar_values[i]
    if len(stop_defs) > 1:
        max_amp = amps.max()
        if max_amp > 1.0:
            amps /= max_amp
    return amps

manual_amps = compute_harmonic_amps(self._manual_stop_defs)
pedal_amps = compute_harmonic_amps(self._pedal_stop_defs)
```

- [ ] **Step 6: Update voice rendering loop in render()**

Replace the single voice loop with division-aware rendering that passes the correct harmonic_amps:

```python
mono = np.zeros(num_frames, dtype=np.float32)
dead_notes: list[int] = []
active_count = 0

for note, voice in self._voices.items():
    if not voice.is_active:
        dead_notes.append(note)
        continue

    # Determine which harmonic amps to use based on voice key
    if note >= 0:
        # Manual voice (note is the MIDI note directly)
        amps = manual_amps
    else:
        # Could be pedal (-note-1) or mutation (-(note*1000+shift+1))
        if note < -127:  # mutation voice
            amps = manual_amps if manual_amps is not None else (pedal_amps or np.zeros(len(DRAWBAR_HARMONICS), dtype=np.float32))
        else:  # pedal voice
            amps = pedal_amps

    if amps is None:
        dead_notes.append(note)
        continue

    mono += voice.render(num_frames, amps)
    active_count += 1
```

Remove the old single-profile harmonic_amps computation block.

Note: mutation voices use the manual division amps since mutation stops are manual stops.

- [ ] **Step 7: Run tests**

Run: `uv run pytest tests/ -v`
Expected: Tests may fail due to stop name changes and registration changes. The `test_output_is_finite` and `test_output_not_clipping` should pass since engine still works. Performance tests may also pass or show changed numbers.

---

### Task 8: Update GUI — stop panel and presets

**Files:**
- Modify: `gui/stop_panel.py`
- Modify: `gui/main_window.py`

- [ ] **Step 1: Replace STOP_FAMILIES in stop_panel.py**

Replace the entire `STOP_FAMILIES` dict:
```python
STOP_FAMILIES: dict[str, list[str]] = {
    "Manual Flue": [
        "Double Open Diapason 16'",
        "Open Diapason 8'",
        "Principal 4'",
        "Fifteenth 2'",
        "Mixture IV",
    ],
    "Manual Reed": [
        "Double Trumpet 16'",
        "Trumpet 8'",
        "Clarion 4'",
    ],
    "Pedal": [
        "Double Open Bass 32'",
        "Open Diapason 16'",
        "Principal 8'",
        "Ophicleide 16'",
    ],
}
```

- [ ] **Step 2: Update tooltips in stop_panel.py**

Replace the `_stop_tooltip` tips dict:
```python
tips = {
    "Double Open Diapason 16'": "Grand foundation — the organ's voice at 16' pitch.",
    "Open Diapason 8'": "The backbone of the organ — rich, round principal tone.",
    "Principal 4'": "Bright principal, one octave above the 8'.",
    "Fifteenth 2'": "High brilliance — two octaves above the 8'.",
    "Mixture IV": "Four-rank chorus mixture — crowns the plenum.",
    "Double Trumpet 16'": "Powerful reed at 16' — the 'Voice of Jupiter'.",
    "Trumpet 8'": "Blazing solo reed — cuts through everything.",
    "Clarion 4'": "Bright reed, one octave above the Trumpet.",
    "Double Open Bass 32'": "Deepest pedal foundation — the earth mover.",
    "Open Diapason 16'": "Pedal principal at 16' — solid bass foundation.",
    "Principal 8'": "Pedal principal at 8' — clarity in the bass.",
    "Ophicleide 16'": "⚡ Powerful pedal reed — the final thunderr.",
}
```

- [ ] **Step 3: Update STOP_GROUPS in main_window.py**

Replace the `STOP_GROUPS` dict:
```python
STOP_GROUPS: dict[int, tuple[str, list[str]]] = {
    0: ("Full Organ", list(STOP_DEFS.keys())),
    1: ("Diapason Chorus", ["Double Open Diapason 16'", "Open Diapason 8'", "Principal 4'", "Fifteenth 2'", "Mixture IV"]),
    2: ("Reed Chorus", ["Double Trumpet 16'", "Trumpet 8'", "Clarion 4'", "Ophicleide 16'"]),
    3: ("Principal 8'", ["Open Diapason 8'"]),
    4: ("Pedal Stops", ["Double Open Bass 32'", "Open Diapason 16'", "Principal 8'", "Ophicleide 16'"]),
    5: ("Trumpet Solo", ["Trumpet 8'", "Double Open Bass 32'", "Open Diapason 16'", "Principal 8'"]),
    6: ("Full Swell", ["Double Open Diapason 16'", "Open Diapason 8'", "Principal 4'", "Fifteenth 2'", "Mixture IV", "Double Trumpet 16'", "Trumpet 8'", "Clarion 4'"]),
    7: ("Cathedral", ["Double Open Diapason 16'", "Open Diapason 8'", "Principal 4'", "Fifteenth 2'", "Trumpet 8'", "Double Open Bass 32'", "Open Diapason 16'", "Principal 8'"]),
    8: ("Ethereal", ["Open Diapason 8'", "Clarion 4'", "Tremulant"]),
    9: ("Pedal Solo", ["Double Open Bass 32'", "Ophicleide 16'"]),
}
```

- [ ] **Step 4: Remove drawbar stuff from main_window (if user wants to keep it simpler)**

Keep drawbar panels as-is since they still work with the new stops.

- [ ] **Step 5: Run app and check GUI loads**

Run: `uv run python main.py`
Expected: Window loads with new stop names in Manual Flue, Manual Reed, and Pedal sections. Stops toggle correctly.

- [ ] **Step 6: Run tests**

Run: `uv run pytest tests/ -v`
Expected: All tests should pass. The output-validity tests should pass since the engine still works identically (just with different stop definitions).

---

### Verification

- [ ] **Verify performance improvement**

Run: `uv run pytest tests/test_performance.py -v -s`
Expected: P95 for 8 voices should be lower than before. Compare against original if baseline available.

- [ ] **Verify output quality**

Run: `uv run pytest tests/test_render_correctness/ -v` (or the correctness tests)
Expected: All pass, stereo channels differ, no clipping, no NaN.

- [ ] **Full test suite**

Run: `uv run pytest tests/ -v`
Expected: All tests pass.
