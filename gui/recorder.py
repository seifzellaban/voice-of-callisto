"""Recorder panel — record/stop button, format selector, status."""

from pathlib import Path

from PyQt6.QtWidgets import (
    QFileDialog, QHBoxLayout, QLabel, QPushButton, QComboBox, QWidget,
)
from PyQt6.QtCore import Qt, QTimer

from engine.recorder import Recorder


_FORMATS = ["WAV", "MP3"]


class RecorderPanel(QWidget):
    """Record/stop button with format selection and status display."""

    def __init__(self, recorder: Recorder, sample_rate: int = 44100) -> None:
        super().__init__()
        self._recorder = recorder
        self._sample_rate = sample_rate
        self._data: list | None = None

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self._record_btn = QPushButton("⏺ Record")
        self._record_btn.setCheckable(True)
        self._record_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a1a1a; color: #cc6666;
                border: 2px solid #5a2a2a; border-radius: 6px;
                font-size: 12px; font-weight: bold; padding: 6px 14px;
            }
            QPushButton:checked {
                background-color: #cc2222; color: #ffffff;
                border: 2px solid #ff4444;
            }
            QPushButton:hover { background-color: #4a2020; }
        """)
        self._record_btn.toggled.connect(self._on_record_toggle)
        layout.addWidget(self._record_btn)

        self._format_combo = QComboBox()
        self._format_combo.addItems(_FORMATS)
        self._format_combo.setStyleSheet("""
            QComboBox {
                background: #3a2a1a; color: #e0d4c0; border: 1px solid #5a4a3a;
                border-radius: 4px; padding: 4px 8px; font-size: 11px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background: #2a1a0a; color: #e0d4c0;
                selection-background-color: #5a3a2a;
            }
        """)
        layout.addWidget(self._format_combo)

        self._status_label = QLabel("")
        self._status_label.setStyleSheet("color: #88aa88; font-size: 11px;")
        layout.addWidget(self._status_label)

        layout.addStretch()
        self.setLayout(layout)

    def _on_record_toggle(self, checked: bool) -> None:
        if checked:
            self._recorder.start()
            self._record_btn.setText("⏹ Stop")
            self._status_label.setText("Recording...")
        else:
            self._record_btn.setText("⏺ Record")
            data = self._recorder.stop()
            if data.shape[0] == 0:
                self._status_label.setText("Empty recording")
                return
            self._save_recording(data)

    def _save_recording(self, data) -> None:
        fmt = self._format_combo.currentText()
        self._status_label.setText("Saving...")

        path, _ = QFileDialog.getSaveFileName(
            self, "Save Recording", str(Path.home()),
            f"{'WAV' if fmt == 'WAV' else 'MP3'} Files (*.{fmt.lower()})",
        )
        if not path:
            self._status_label.setText("Cancelled")
            return

        try:
            wav_path = str(Path(path).with_suffix(".wav"))
            self._recorder.save_wav(wav_path, data)

            if fmt == "MP3":
                mp3_path = str(Path(path).with_suffix(".mp3"))
                self._recorder.save_mp3(wav_path, mp3_path)
                Path(wav_path).unlink(missing_ok=True)

            self._status_label.setText(f"Saved: {Path(path).name}")
        except Exception as e:
            self._status_label.setText(f"Error: {e}")
