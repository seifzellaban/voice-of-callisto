"""Alternate tuning tables — pre-computed 128-note frequency arrays.

Each tuning is a float32 ndarray of length 128 (MIDI note 0–127).
Adding a new tuning: add a key to TUNINGS dict with a 128-element array.
"""

import numpy as np

A4 = 440.0


def _equal_ratios() -> np.ndarray:
    return np.array([2.0 ** (i / 12.0) for i in range(12)], dtype=np.float64)


def _pythag_ratios() -> np.ndarray:
    return np.array([
        1.0,           # C
        256.0 / 243.0,  # C#
        9.0 / 8.0,      # D
        32.0 / 27.0,    # D#
        81.0 / 64.0,    # E
        4.0 / 3.0,      # F
        729.0 / 512.0,  # F#
        3.0 / 2.0,      # G
        128.0 / 81.0,   # G#
        27.0 / 16.0,    # A
        16.0 / 9.0,     # A#
        243.0 / 128.0,  # B
    ], dtype=np.float64)


def _meantone_ratios() -> np.ndarray:
    """Quarter-comma meantone ratios (C-based)."""
    q = 5.0 ** 0.25
    return np.array([
        1.0,                     # C
        q ** 7 / (2.0 ** 4),     # C#
        q ** 2 / 2.0,            # D
        q ** 9 / (2.0 ** 5),     # D#
        5.0 / 4.0,               # E  (pure major third)
        q ** 4 / (2.0 ** 2),     # F
        q ** 11 / (2.0 ** 6),    # F#
        q,                       # G
        q ** 8 / (2.0 ** 4),     # G#
        q ** 3 / 2.0,            # A
        q ** 10 / (2.0 ** 5),    # A#
        q ** 5 / (2.0 ** 2),     # B
    ], dtype=np.float64)


def _werckmeister_ratios() -> np.ndarray:
    """Werckmeister III (C-based). Uses 1/4 comma tempered fifths on C, G, D, A, F."""
    p = 3.0 / 2.0        # pure fifth ratio
    t = p / (2.0 ** (1.0 / 4.0 / 1200.0 * 1200.0))
    # Actually the comma is ≈ 23.46 cents, so 1/4 comma = 5.865 cents
    # The tempered fifth in Werckmeister III is narrowed by ~5.865 cents
    # p / (2^(5.865/1200)) ≈ 1.5 / 1.0034 ≈ 1.495
    tc = 1.0 / 4.0 * (1200.0 * np.log2(3.0 / 2.0) - 700.0)
    tempered = p / (2.0 ** (tc / 1200.0))

    r = np.zeros(12, dtype=np.float64)
    r[0] = 1.0          # C
    r[7] = tempered     # G
    r[2] = tempered ** 2 / 2.0   # D
    r[9] = tempered ** 3 / 2.0   # A
    r[5] = tempered ** 4 / 4.0   # F
    r[3] = tempered ** 5 / 4.0   # D# (Eb)
    r[10] = tempered ** 6 / 4.0  # A# (Bb)
    r[4] = tempered ** 7 / 8.0   # E
    r[11] = tempered ** 8 / 8.0  # B
    r[1] = tempered ** 9 / 8.0   # C# (Db)
    r[8] = tempered ** 10 / 8.0  # G# (Ab)
    r[6] = tempered ** 11 / 16.0 # F#

    return r


def _build_table(ratios: np.ndarray) -> np.ndarray:
    """Build 128-note frequency table from 12-note ratio array (C-based).
    
    Reference: A4 (MIDI 69) = 440 Hz.
    """
    a4_note = 69
    a4_oct = a4_note // 12 - 1
    a4_idx = a4_note % 12
    c_ref = A4 / (ratios[a4_idx] * (2.0 ** a4_oct))
    table = np.zeros(128, dtype=np.float32)
    for n in range(128):
        octave = n // 12 - 1
        note = n % 12
        table[n] = c_ref * ratios[note] * (2.0 ** octave)
    return table


TUNINGS: dict[str, np.ndarray] = {
    "Equal": _build_table(_equal_ratios()),
    "Pythagorean": _build_table(_pythag_ratios()),
    "Meantone": _build_table(_meantone_ratios()),
    "Werckmeister III": _build_table(_werckmeister_ratios()),
}

DEFAULT_TUNING = "Equal"
