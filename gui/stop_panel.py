"""Stop panel — toggle buttons for organ stops with fighter-jet aesthetics.

Stops are organized into functional groups (families).
"""

from PyQt6.QtWidgets import (
    QGroupBox, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
    QSlider,
)
from PyQt6.QtCore import pyqtSignal, Qt
from stops.profiles import STOP_DEFS


# ── Stop organization by family ─────────────────────────────────────
# Order matters: this is the display order in each section.
STOP_FAMILIES: dict[str, list[str]] = {
    "Manual — Foundation": [
        "Double Open Diapason 16'",
        "Open Diapason 8'",
        "Geigen Diapason 8'",
        "Flûte Harmonique 8'",
        "Principal 4'",
        "Viola 4'",
        "Open Flute 4'",
        "Fifteenth 2'",
    ],
    "Manual — Mixture & Reeds": [
        "Mixture IV",
        "Double Trumpet 16'",
        "Bassoon 16'",
        "Trumpet 8'",
        "Oboe 8'",
        "Clarinet 8'",
        "Trompette Harmonique 8'",
        "Clarion 4'",
    ],
    "Pedal": [
        "Double Open Bass 32'",
        "Open Diapason 16'",
        "Violone 16'",
        "Principal 8'",
        "Bourdon 8'",
        "Octave 4'",
        "Ophicleide 16'",
        "Trombone 16'",
    ],
}


class StopPanel(QGroupBox):
    """Grid of toggle buttons for organ stops, grouped by family."""

    stop_toggled = pyqtSignal(str, bool)
    stop_volume_changed = pyqtSignal(str, float)

    def __init__(self, stop_names: list[str], active_stops: set[str]) -> None:
        super().__init__("Organ Stops")
        self._buttons: dict[str, QPushButton] = {}
        self._vol_sliders: dict[str, QSlider] = {}

        outer = QVBoxLayout()
        outer.setSpacing(8)

        # ── Family sections ──────────────────────────────────────────
        families_row = QHBoxLayout()
        families_row.setSpacing(12)

        for family_name, family_stops in STOP_FAMILIES.items():
            section = self._build_family_section(
                family_name, family_stops, active_stops
            )
            families_row.addWidget(section)

        outer.addLayout(families_row)

        self.setLayout(outer)
        self.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #e0d4c0;
                border: 1px solid #5a4a3a;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 18px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
            }
        """)

    def _build_family_section(
        self,
        family_name: str,
        stop_names: list[str],
        active_stops: set[str],
    ) -> QGroupBox:
        """Build a bordered sub-section for a stop family."""
        group = QGroupBox(family_name)
        group.setStyleSheet("""
            QGroupBox {
                font-size: 11px;
                font-weight: bold;
                color: #a09080;
                border: 1px solid #3a2a1a;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 14px;
                padding-bottom: 4px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px;
            }
        """)

        grid = QGridLayout()
        grid.setSpacing(4)
        grid.setHorizontalSpacing(2)

        for idx, name in enumerate(stop_names):
            stop_def = STOP_DEFS.get(name)
            if stop_def is None:
                continue

            row = idx // 2
            col = (idx % 2) * 2

            # Build label: show pitch info for mutations
            label = name
            if stop_def.is_mutation:
                label = f"◆ {name}"

            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setChecked(name in active_stops)
            btn.setMinimumHeight(40)
            btn.setMinimumWidth(100)
            btn.setStyleSheet(self._button_style(name in active_stops))
            btn.setToolTip(self._stop_tooltip(name, stop_def))
            btn.clicked.connect(
                lambda checked, n=name: self._on_toggle(n, checked)
            )
            self._buttons[name] = btn
            grid.addWidget(btn, row, col)

            # Tiny volume slider
            slider = QSlider(Qt.Orientation.Vertical)
            slider.setMinimum(0)
            slider.setMaximum(10)
            slider.setValue(10)  # default 1.0
            slider.setFixedWidth(12)
            slider.setFixedHeight(50)
            slider.setStyleSheet("""
                QSlider::groove:vertical {
                    background: #2a1a0a;
                    width: 6px;
                    border-radius: 3px;
                }
                QSlider::handle:vertical {
                    background: #d4a574;
                    height: 10px;
                    width: 10px;
                    margin: -2px -2px;
                    border-radius: 3px;
                }
            """)
            slider.valueChanged.connect(
                lambda v, n=name: self.stop_volume_changed.emit(n, v / 10.0)
            )
            self._vol_sliders[name] = slider
            grid.addWidget(slider, row, col + 1)

        group.setLayout(grid)
        return group

    def _stop_tooltip(self, name: str, stop_def) -> str:
        tips = {
            "Double Open Diapason 16'": "Deep foundation — Great manual 16' principal.",
            "Open Diapason 8'": "The backbone of the organ — rich, full principal tone.",
            "Geigen Diapason 8'": "Bright string-toned diapason — violin-like edge.",
            "Flûte Harmonique 8'": "Warm harmonic flute — round, singing tone.",
            "Principal 4'": "Bright octave principal — adds clarity and definition.",
            "Viola 4'": "Alto string stop — lean, penetrating colour.",
            "Open Flute 4'": "Clear open flute at 4' — gentle presence.",
            "Fifteenth 2'": "High principal — shimmer and brilliance in the upper ranks.",
            "Mixture IV": "Four-rank compound stop — crowns the plenum with brilliance.",
            "Double Trumpet 16'": "Powerful reed in the 16' octave — dramatic and commanding.",
            "Bassoon 16'": "Smooth soft reed — orchestral bassoon colour.",
            "Trumpet 8'": "Blazing solo reed — cuts through the full organ.",
            "Oboe 8'": "Thin characterful reed — plaintive and singing.",
            "Clarinet 8'": "Solo reed with strong fundamental — warm and woody.",
            "Trompette Harmonique 8'": "Brilliant harmonic trumpet — scintillating treble.",
            "Clarion 4'": "Bright trumpet at 4' pitch — piercing solo or chorus reed.",
            "Double Open Bass 32'": "Massive sub-bass — the deepest foundation rumble.",
            "Open Diapason 16'": "Pedal principal — solid 16' pedal foundation.",
            "Violone 16'": "Pedal string bass — lean, articulate 16' tone.",
            "Principal 8'": "Pedal principal at 8' — supports the ensemble.",
            "Bourdon 8'": "Stopped flute pedal — round, soft bass.",
            "Octave 4'": "Clear 4' pedal principal — definition in the bass.",
            "Ophicleide 16'": "Powerful pedal reed — the voice of the pedal division.",
            "Trombone 16'": "Commanding pedal reed — weight and majesty in the bass.",
        }
        return tips.get(name, name)

    def _button_style(self, active: bool) -> str:
        if active:
            return """
                QPushButton {
                    background-color: #8b4513;
                    color: #fff8e7;
                    border: 2px solid #d4a574;
                    border-radius: 6px;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 8px;
                }
                QPushButton:hover { background-color: #a0522d; }
            """
        return """
            QPushButton {
                background-color: #3a2a1a;
                color: #a09080;
                border: 2px solid #5a4a3a;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover { background-color: #4a3a2a; }
        """

    def update_stops(self, active_stops: set[str]) -> None:
        """Sync all button visual states with the given set of active stops."""
        for name, btn in self._buttons.items():
            is_active = name in active_stops
            btn.setChecked(is_active)
            btn.setStyleSheet(self._button_style(is_active))

    def _on_toggle(self, name: str, checked: bool) -> None:
        btn = self._buttons[name]
        btn.setStyleSheet(self._button_style(checked))
        self.stop_toggled.emit(name, checked)
