"""Organ stop profiles — harmonic recipes with pipe-type waveform selection.

Each profile maps harmonic number → relative amplitude, and includes a
preferred waveform to use for realistic pipe character. Different pipe
families (principal, flute, reed, string) have fundamentally different
waveshapes, not just different harmonic balances.
"""

from typing import TypeAlias
from dataclasses import dataclass

HarmonicProfile: TypeAlias = dict[int, float]


@dataclass
class StopDefinition:
    """Full stop definition with harmonics, waveform, and voicing parameters."""
    harmonics: HarmonicProfile
    waveform: str = "sine"          # Oscillator waveform name
    chorus_detune: float = 0.8      # Hz — chorus detuning amount
    vibrato_depth: float = 0.6      # Hz — vibrato/tremulant depth
    vibrato_rate: float = 5.8       # Hz — vibrato/tremulant rate
    chiff_amount: float = 0.015     # Attack chiff noise intensity
    chiff_ms: float = 15.0          # Chiff duration in ms
    wind_noise: float = 0.004       # Continuous wind noise level
    attack_ms: float = 45.0         # Envelope attack time
    release_ms: float = 800.0       # Envelope release time
    is_tremulant: bool = False       # True = not a pipe rank, but an effect
    tremulant_depth: float = 0.0     # Amplitude modulation depth (0–1)
    tremulant_rate: float = 6.5      # Amplitude modulation rate (Hz)
    tremulant_pitch_cents: float = 0.0  # Pitch modulation depth in cents
    pitch_shift: float = 1.0         # Pitch multiplier (e.g. 2.0 = octave up)
    is_mutation: bool = False        # True = mutation rank (fixed pitch ratio)
    division: str = "manual"         # Manual division ("manual", "pedal", or "both")


# ──────────────────────────────────────────────────────────────────────
# Stop definitions — Royal Albert Hall Willis organ profiles
# ──────────────────────────────────────────────────────────────────────

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

# ──────────────────────────────────────────────────────────────────────
# Registries
# ──────────────────────────────────────────────────────────────────────

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

# Legacy harmonic-only registry (for backward compat)
# Exclude Tremulant since it has no harmonics
STOP_REGISTRY: dict[str, HarmonicProfile] = {
    name: sdef.harmonics for name, sdef in STOP_DEFS.items()
    if not sdef.is_tremulant
}

# Drawbar harmonic numbers (Hammond convention)
DRAWBAR_HARMONICS = [0.5, 1, 1.5, 2, 3, 4, 5, 6, 8]

# Drawbar labels
DRAWBAR_LABELS = ["16'", "8'", "5⅓'", "4'", "2⅔'", "2'", "1⅗'", "1⅓'", "1'"]
