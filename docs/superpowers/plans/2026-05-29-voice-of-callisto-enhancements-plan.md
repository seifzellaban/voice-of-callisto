# Voice of Callisto — Feature Enhancements Implementation Plan

> **For agentic workers:** Use subagent-driven-development or executing-plans.

**Goal:** Add 12 organ stops, WAV/MP3 recording, sustain pedal, per-stop volume, transpose, and alternate tunings.

**Architecture:** All features follow existing patterns — mixer event queue for thread-safe GUI→audio communication, pre-computed tables, minimal new deps. New files: `engine/tunings.py`, `engine/recorder.py`, `gui/recorder.py`.

**Tech Stack:** Python 3.13, PyQt6, numpy, mido, wave (stdlib), ffmpeg (external).

---

### Task 1: Add 12 new stops to profiles.py

**Files:**
- Modify: `stops/profiles.py`
- Modify: `gui/stop_panel.py` (STOP_FAMILIES + tooltips)

**Steps:**

- Append 12 new `StopDefinition` constants and register in `STOP_DEFS`
- Update `STOP_FAMILIES` in `stop_panel.py` with new names (8 per group)
- Update tooltips dict with descriptions for new stops

### Task 2: Alternate tunings — engine/tunings.py

**Files:**
- Create: `engine/tunings.py`
- Modify: `engine/organ.py` (accept tuning table)
- Modify: `engine/mixer.py` (TUNING_SET event, re-create voices)

### Task 3: Transpose

**Files:**
- Modify: `engine/mixer.py` (TRANSPOSE_SET event, offset in note handling)
- Modify: `gui/main_window.py` (transpose GUI controls)

### Task 4: Sustain Pedal

**Files:**
- Modify: `engine/mixer.py` (SUSTAIN_PEDAL event, sustain logic)
- Modify: `gui/main_window.py` (sustain toggle button)

### Task 5: Per-stop volume

**Files:**
- Modify: `gui/stop_panel.py` (sliders per stop, signal)
- Modify: `engine/mixer.py` (STOP_VOLUME event, apply in render)
- Modify: `gui/main_window.py` (connect signal)

### Task 6: Recording (WAV/MP3)

**Files:**
- Create: `engine/recorder.py`
- Create: `gui/recorder.py`
- Modify: `engine/mixer.py` (hold RecorderState)
- Modify: `engine/audio.py` (capture frames)
- Modify: `gui/main_window.py` (add recorder panel)

---

## Execution

All 6 tasks. Run tests after each.
