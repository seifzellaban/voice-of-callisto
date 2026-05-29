"""Organ stop profiles — harmonic recipes with pipe-type waveform selection.

Each profile maps harmonic number → relative amplitude, and includes a
preferred waveform to use for realistic pipe character. Different pipe
families (principal, flute, reed, string) have fundamentally different
waveshapes, not just different harmonic balances.
"""

from typing import TypeAlias
from dataclasses import dataclass

HarmonicProfile: TypeAlias = dict[float, float]


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

# ── 16' stops: fundamental at 0.5× drawbar (16' pitch), 1.0× is 2nd harmonic ──
DOUBLE_OPEN_DIAPASON_16_DEF = StopDefinition(
    harmonics={0.5: 1.0, 1: 0.60, 2: 0.42, 3: 0.28, 4: 0.18, 5: 0.12, 6: 0.06, 7: 0.08, 8: 0.03},
    waveform="principal", chorus_detune=0.7, vibrato_depth=0.5,
    chiff_amount=0.015, chiff_ms=12.0, wind_noise=0.004, attack_ms=50.0, release_ms=750.0,
    division="manual",
)

OPEN_DIAPASON_16_PEDAL_DEF = StopDefinition(
    harmonics={0.5: 1.0, 1: 0.60, 2: 0.42, 3: 0.28, 4: 0.18, 5: 0.12, 6: 0.06, 7: 0.08, 8: 0.03},
    waveform="principal", chorus_detune=0.7, vibrato_depth=0.5,
    chiff_amount=0.015, chiff_ms=12.0, wind_noise=0.004, attack_ms=55.0, release_ms=900.0,
    division="pedal",
)

DOUBLE_TRUMPET_16_DEF = StopDefinition(
    harmonics={0.5: 1.0, 1: 0.95, 2: 0.88, 3: 0.80, 4: 0.72, 5: 0.63, 6: 0.55, 7: 0.48, 8: 0.40},
    waveform="reed", chorus_detune=1.5, vibrato_depth=0.4, vibrato_rate=5.5,
    chiff_amount=0.005, chiff_ms=5.0, wind_noise=0.002, attack_ms=22.0, release_ms=450.0,
    division="manual",
)

OPHICLEIDE_16_DEF = StopDefinition(
    harmonics={0.5: 1.0, 1: 0.95, 2: 0.88, 3: 0.80, 4: 0.72, 5: 0.63, 6: 0.55, 7: 0.48, 8: 0.40},
    waveform="reed", chorus_detune=1.5, vibrato_depth=0.4, vibrato_rate=5.5,
    chiff_amount=0.005, chiff_ms=5.0, wind_noise=0.002, attack_ms=25.0, release_ms=500.0,
    division="pedal",
)

# ── 32' stop: effective fundamental at 0.5× (16' = 2nd partial of 32'), steep roll-off ──
DOUBLE_OPEN_BASS_32_DEF = StopDefinition(
    harmonics={0.5: 1.0, 1: 0.30, 2: 0.15, 3: 0.07, 4: 0.03, 5: 0.02, 6: 0.01},
    waveform="principal", chorus_detune=0.3, vibrato_depth=0.25,
    chiff_amount=0.025, chiff_ms=28.0, wind_noise=0.007, attack_ms=70.0, release_ms=1100.0,
    division="pedal",
)

# ── 8' stops: gentle sub reinforcement at 0.5×, fundamental at 1.0× ──
OPEN_DIAPASON_8_DEF = StopDefinition(
    harmonics={0.5: 0.65, 1: 1.0, 2: 0.60, 3: 0.42, 4: 0.28, 5: 0.18, 6: 0.12, 7: 0.06, 8: 0.08, 9: 0.03, 10: 0.04, 12: 0.02},
    waveform="principal", chorus_detune=0.7, vibrato_depth=0.5,
    chiff_amount=0.015, chiff_ms=12.0, wind_noise=0.004, attack_ms=50.0, release_ms=750.0,
    division="manual",
)

PRINCIPAL_8_PEDAL_DEF = StopDefinition(
    harmonics={0.5: 0.65, 1: 1.0, 2: 0.60, 3: 0.42, 4: 0.28, 5: 0.18, 6: 0.12, 7: 0.06, 8: 0.08, 9: 0.03, 10: 0.04, 12: 0.02},
    waveform="principal", chorus_detune=0.7, vibrato_depth=0.5,
    chiff_amount=0.015, chiff_ms=12.0, wind_noise=0.004, attack_ms=50.0, release_ms=750.0,
    division="pedal",
)

TRUMPET_8_DEF = StopDefinition(
    harmonics={0.5: 0.50, 1: 1.0, 2: 0.82, 3: 0.65, 4: 0.48, 5: 0.35, 6: 0.24, 7: 0.16, 8: 0.10},
    waveform="reed", chorus_detune=1.5, vibrato_depth=0.4, vibrato_rate=5.5,
    chiff_amount=0.005, chiff_ms=5.0, wind_noise=0.002, attack_ms=22.0, release_ms=450.0,
    division="manual",
)

# ── 4' stops: fundamental at 2.0 (4' pitch), no sub-octave content ──
PRINCIPAL_4_DEF = StopDefinition(
    harmonics={2: 1.0, 3: 0.30, 4: 0.12, 5: 0.05, 6: 0.02},
    waveform="principal", chorus_detune=0.9, vibrato_depth=0.6,
    chiff_amount=0.009, chiff_ms=10.0, wind_noise=0.003, attack_ms=42.0, release_ms=700.0,
    division="manual",
)

FIFTEENTH_2_DEF = StopDefinition(
    harmonics={4: 1.0, 5: 0.30, 6: 0.12, 7: 0.05, 8: 0.02},
    waveform="principal", chorus_detune=1.1, vibrato_depth=0.7,
    chiff_amount=0.007, chiff_ms=8.0, wind_noise=0.002, attack_ms=32.0, release_ms=600.0,
    division="manual",
)

CLARION_4_DEF = StopDefinition(
    harmonics={2: 1.0, 3: 0.60, 4: 0.35, 5: 0.20, 6: 0.10, 7: 0.05, 8: 0.02},
    waveform="reed", chorus_detune=1.2, vibrato_depth=0.8, vibrato_rate=6.2,
    chiff_amount=0.010, chiff_ms=8.0, wind_noise=0.003, attack_ms=28.0, release_ms=500.0,
    division="manual",
)

MIXTURE_IV_DEF = StopDefinition(
    harmonics={4: 0.30, 5: 0.40, 6: 0.55, 8: 1.0},
    waveform="principal", chorus_detune=1.0, vibrato_depth=0.7,
    chiff_amount=0.012, chiff_ms=10.0, wind_noise=0.003, attack_ms=40.0, release_ms=650.0,
    is_mutation=True, pitch_shift=1.0, division="manual",
)

# ── 2' stop: fundamental at 4.0 (2' pitch) ──
FIFTEENTH_2_DEF = StopDefinition(
    harmonics={4: 1.0, 5: 0.40, 6: 0.20, 7: 0.10, 8: 0.04},
    waveform="principal", chorus_detune=1.1, vibrato_depth=0.7,
    chiff_amount=0.007, chiff_ms=8.0, wind_noise=0.002, attack_ms=32.0, release_ms=600.0,
    division="manual",
)

# ── Mixture IV: high mutation harmonics for brilliance ──
MIXTURE_IV_DEF = StopDefinition(
    harmonics={4: 0.45, 5: 0.60, 6: 0.75, 8: 1.0},
    waveform="principal", chorus_detune=1.0, vibrato_depth=0.7,
    chiff_amount=0.012, chiff_ms=10.0, wind_noise=0.003, attack_ms=40.0, release_ms=650.0,
    is_mutation=True, pitch_shift=1.0, division="manual",
)

# ── New Foundation stops (8' and 4' colors) ──────────────────────────

GEIGEN_DIAPASON_8_DEF = StopDefinition(
    harmonics={0.5: 0.40, 1: 1.0, 2: 0.55, 3: 0.32, 4: 0.18, 5: 0.10, 6: 0.05, 7: 0.03},
    waveform="string", chorus_detune=0.8, vibrato_depth=0.6,
    chiff_amount=0.012, chiff_ms=12.0, wind_noise=0.004, attack_ms=45.0, release_ms=700.0,
    division="manual",
)

FLUTE_HARMONIQUE_8_DEF = StopDefinition(
    harmonics={0.5: 0.30, 1: 1.0, 3: 0.20, 5: 0.06},
    waveform="flute", chorus_detune=0.5, vibrato_depth=0.5, vibrato_rate=5.2,
    chiff_amount=0.008, chiff_ms=15.0, wind_noise=0.003, attack_ms=55.0, release_ms=800.0,
    division="manual",
)

VIOLA_4_DEF = StopDefinition(
    harmonics={2: 1.0, 3: 0.50, 4: 0.30, 5: 0.15, 6: 0.08},
    waveform="string", chorus_detune=1.2, vibrato_depth=0.8, vibrato_rate=6.0,
    chiff_amount=0.010, chiff_ms=8.0, wind_noise=0.003, attack_ms=35.0, release_ms=650.0,
    division="manual",
)

OPEN_FLUTE_4_DEF = StopDefinition(
    harmonics={2: 1.0, 3: 0.15, 5: 0.04},
    waveform="flute", chorus_detune=0.4, vibrato_depth=0.4, vibrato_rate=5.0,
    chiff_amount=0.006, chiff_ms=14.0, wind_noise=0.003, attack_ms=50.0, release_ms=750.0,
    division="manual",
)

# ── New Reed stops ──────────────────────────────────────────────────

OBOE_8_DEF = StopDefinition(
    harmonics={0.5: 0.40, 1: 1.0, 2: 0.65, 3: 0.40, 4: 0.25, 5: 0.15, 6: 0.08, 7: 0.04},
    waveform="reed", chorus_detune=1.2, vibrato_depth=0.5, vibrato_rate=5.5,
    chiff_amount=0.006, chiff_ms=6.0, wind_noise=0.002, attack_ms=40.0, release_ms=500.0,
    division="manual",
)

CLARINET_8_DEF = StopDefinition(
    harmonics={0.5: 0.20, 1: 1.0, 2: 0.30, 3: 0.60, 4: 0.20, 5: 0.45, 6: 0.15},
    waveform="reed", chorus_detune=1.0, vibrato_depth=0.6, vibrato_rate=5.0,
    chiff_amount=0.004, chiff_ms=8.0, wind_noise=0.003, attack_ms=35.0, release_ms=600.0,
    division="manual",
)

BASSOON_16_DEF = StopDefinition(
    harmonics={0.5: 1.0, 1: 0.80, 2: 0.55, 3: 0.35, 4: 0.20, 5: 0.10},
    waveform="reed", chorus_detune=0.8, vibrato_depth=0.3, vibrato_rate=4.8,
    chiff_amount=0.005, chiff_ms=10.0, wind_noise=0.003, attack_ms=50.0, release_ms=900.0,
    division="manual",
)

TROMPETTE_HARMONIQUE_8_DEF = StopDefinition(
    harmonics={0.5: 0.60, 1: 1.0, 2: 0.90, 3: 0.80, 4: 0.70, 5: 0.60, 6: 0.50, 7: 0.40},
    waveform="reed", chorus_detune=1.6, vibrato_depth=0.5, vibrato_rate=5.8,
    chiff_amount=0.007, chiff_ms=4.0, wind_noise=0.002, attack_ms=18.0, release_ms=450.0,
    division="manual",
)

# ── New Pedal stops ─────────────────────────────────────────────────

VIONE_16_PEDAL_DEF = StopDefinition(
    harmonics={0.5: 1.0, 1: 0.70, 2: 0.40, 3: 0.22, 4: 0.12, 5: 0.06},
    waveform="string", chorus_detune=0.6, vibrato_depth=0.3,
    chiff_amount=0.010, chiff_ms=14.0, wind_noise=0.004, attack_ms=55.0, release_ms=850.0,
    division="pedal",
)

BOURDON_8_PEDAL_DEF = StopDefinition(
    harmonics={0.5: 0.50, 1: 1.0, 3: 0.12, 5: 0.03},
    waveform="flute", chorus_detune=0.3, vibrato_depth=0.25,
    chiff_amount=0.008, chiff_ms=18.0, wind_noise=0.004, attack_ms=60.0, release_ms=950.0,
    division="pedal",
)

OCTAVE_4_PEDAL_DEF = StopDefinition(
    harmonics={2: 1.0, 3: 0.40, 4: 0.20, 5: 0.08},
    waveform="principal", chorus_detune=0.8, vibrato_depth=0.5,
    chiff_amount=0.011, chiff_ms=10.0, wind_noise=0.003, attack_ms=45.0, release_ms=700.0,
    division="pedal",
)

TROMBONE_16_PEDAL_DEF = StopDefinition(
    harmonics={0.5: 1.0, 1: 0.95, 2: 0.85, 3: 0.72, 4: 0.60, 5: 0.48},
    waveform="reed", chorus_detune=1.4, vibrato_depth=0.4, vibrato_rate=5.5,
    chiff_amount=0.005, chiff_ms=5.0, wind_noise=0.002, attack_ms=20.0, release_ms=550.0,
    division="pedal",
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
    "Geigen Diapason 8'": GEIGEN_DIAPASON_8_DEF,
    "Flûte Harmonique 8'": FLUTE_HARMONIQUE_8_DEF,
    "Principal 4'": PRINCIPAL_4_DEF,
    "Viola 4'": VIOLA_4_DEF,
    "Open Flute 4'": OPEN_FLUTE_4_DEF,
    "Fifteenth 2'": FIFTEENTH_2_DEF,
    "Mixture IV": MIXTURE_IV_DEF,
    "Double Trumpet 16'": DOUBLE_TRUMPET_16_DEF,
    "Bassoon 16'": BASSOON_16_DEF,
    "Trumpet 8'": TRUMPET_8_DEF,
    "Oboe 8'": OBOE_8_DEF,
    "Clarinet 8'": CLARINET_8_DEF,
    "Trompette Harmonique 8'": TROMPETTE_HARMONIQUE_8_DEF,
    "Clarion 4'": CLARION_4_DEF,
    "Double Open Bass 32'": DOUBLE_OPEN_BASS_32_DEF,
    "Open Diapason 16'": OPEN_DIAPASON_16_PEDAL_DEF,
    "Violone 16'": VIONE_16_PEDAL_DEF,
    "Principal 8'": PRINCIPAL_8_PEDAL_DEF,
    "Bourdon 8'": BOURDON_8_PEDAL_DEF,
    "Octave 4'": OCTAVE_4_PEDAL_DEF,
    "Ophicleide 16'": OPHICLEIDE_16_DEF,
    "Trombone 16'": TROMBONE_16_PEDAL_DEF,
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
