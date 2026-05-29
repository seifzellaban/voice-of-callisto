"""Swell panel — 4 vertical sliders for frequency band volume control."""

from PyQt6.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QSlider, QLabel
from PyQt6.QtCore import Qt, pyqtSignal


SWELL_BAND_LABELS = ["Bass", "Mid\nLow", "Mid\nHigh", "Treble"]
SWELL_BAND_FREQS = ["< 200Hz", "200–600", "600–2k", "> 2kHz"]
_N_BANDS = 4


class SwellPanel(QGroupBox):
    """Four vertical sliders controlling volume of each frequency band."""

    swell_changed = pyqtSignal(int, float)  # (band_index, value 0.0–1.0)

    def __init__(self, initial_values: list[float] | None = None) -> None:
        super().__init__("Swell EQ")
        if initial_values is None:
            initial_values = [1.0] * _N_BANDS
        self._sliders: list[QSlider] = []

        layout = QHBoxLayout()
        layout.setSpacing(6)

        for i in range(_N_BANDS):
            col = QVBoxLayout()
            col.setSpacing(4)

            # Value label
            val_label = QLabel(str(int(initial_values[i] * 8)))
            val_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            val_label.setStyleSheet("color: #77ddff; font-size: 14px; font-weight: bold;")
            val_label.setFixedWidth(44)
            col.addWidget(val_label)

            # Vertical slider
            slider = QSlider(Qt.Orientation.Vertical)
            slider.setMinimum(0)
            slider.setMaximum(8)
            slider.setValue(int(initial_values[i] * 8))
            slider.setMinimumHeight(150)
            slider.setFixedWidth(44)
            slider.setStyleSheet(self._slider_style(i))
            slider.valueChanged.connect(
                lambda v, idx=i, lbl=val_label: self._on_change(idx, v, lbl)
            )
            self._sliders.append(slider)
            col.addWidget(slider, alignment=Qt.AlignmentFlag.AlignCenter)

            # Band label
            band_label = QLabel(SWELL_BAND_LABELS[i])
            band_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            band_label.setStyleSheet("color: #88ccdd; font-size: 10px; font-weight: bold;")
            col.addWidget(band_label)

            # Frequency label
            freq_label = QLabel(SWELL_BAND_FREQS[i])
            freq_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            freq_label.setStyleSheet("color: #668899; font-size: 9px;")
            col.addWidget(freq_label)

            layout.addLayout(col)

        self.setLayout(layout)
        self.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #77ccdd;
                border: 1px solid #3a5a6a;
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

    def _slider_style(self, index: int) -> str:
        colors = ["#4488cc", "#66aadd", "#88ccff", "#aaddff"]
        color = colors[index] if index < len(colors) else "#4488cc"
        return f"""
            QSlider::groove:vertical {{
                background: #0a1a2a;
                width: 16px;
                border-radius: 4px;
                border: 1px solid #3a6a8a;
            }}
            QSlider::handle:vertical {{
                background: {color};
                height: 20px;
                width: 26px;
                margin: -2px -5px;
                border-radius: 4px;
                border: 1px solid #888;
            }}
            QSlider::handle:vertical:hover {{
                border: 2px solid #77ddff;
            }}
        """

    def _on_change(self, index: int, value: int, label: QLabel) -> None:
        label.setText(str(value))
        self.swell_changed.emit(index, value / 8.0)

    def set_values(self, values: list[int]) -> None:
        for i, val in enumerate(values):
            if i < len(self._sliders):
                self._sliders[i].setValue(max(0, min(8, val)))
