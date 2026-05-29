"""Main window — assembles all panels: stops, drawbars, MIDI player, and keyboard.

ALL keyboard input is intercepted at the window level via an event filter
and routed exclusively to the PianoKeyboard. No other widget ever receives
keyboard focus or key events. This prevents Qt's accessibility system
(Tab navigation, Space to toggle buttons, arrow keys on sliders) from
interfering with organ controls.

Controls:
  Numpad 0     All stops on
  Numpad 1–9   Stop group presets
  Shift+Num1–9 Select drawbar, then ↑/↓ to adjust
  ←/→          Move both hands
  LCtrl + ←/→  Move left hand only
  RCtrl + ←/→  Move right hand only
"""

from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QFont, QKeyEvent
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from engine.midi_player import MidiPlayer
from engine.mixer import DEFAULT_ROOM_PRESET, ROOM_PRESETS, Mixer
from engine.tunings import TUNINGS
from gui.drawbar_presets import DrawbarPresetPanel
from gui.drawbars import DrawbarPanel
from gui.keyboard import PianoKeyboard
from gui.midi_panel import MidiPlayerPanel
from gui.recorder import RecorderPanel
from gui.room_panel import RoomPresetPanel
from gui.stop_panel import StopPanel
from gui.swell import SwellPanel
from stops.profiles import DRAWBAR_LABELS, STOP_DEFS

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def _note_name(midi: int) -> str:
    return NOTE_NAMES[midi % 12] + str(midi // 12 - 1)


# ── Stop group presets ──────────────────────────────────────────────
# Each group is a set of stop names to activate (all others deactivated).
# These follow traditional organ registration patterns.
STOP_GROUPS: dict[int, tuple[str, list[str]]] = {
    0: ("All Stops", list(STOP_DEFS.keys())),
    1: ("Foundation 8'", ["Open Diapason 8'"]),
    2: (
        "Great Plenum",
        ["Open Diapason 8'", "Principal 4'", "Fifteenth 2'", "Mixture IV"],
    ),
    3: (
        "Full Plenum",
        [
            "Double Open Diapason 16'",
            "Open Diapason 8'",
            "Principal 4'",
            "Fifteenth 2'",
            "Mixture IV",
        ],
    ),
    4: ("Reeds", ["Double Trumpet 16'", "Trumpet 8'", "Clarion 4'"]),
    5: ("Solo Trumpet", ["Trumpet 8'"]),
    6: ("Pedal Foundation", ["Open Diapason 16'", "Principal 8'"]),
    7: (
        "Pedal Full",
        ["Double Open Bass 32'", "Open Diapason 16'", "Principal 8'", "Ophicleide 16'"],
    ),
    8: (
        "Full Organ",
        [
            "Double Open Diapason 16'",
            "Open Diapason 8'",
            "Principal 4'",
            "Fifteenth 2'",
            "Mixture IV",
            "Double Trumpet 16'",
            "Trumpet 8'",
            "Clarion 4'",
            "Double Open Bass 32'",
            "Open Diapason 16'",
            "Principal 8'",
            "Ophicleide 16'",
        ],
    ),
    9: (
        "Festal",
        [
            "Open Diapason 8'",
            "Principal 4'",
            "Trumpet 8'",
            "Open Diapason 16'",
            "Principal 8'",
            "Tremulant",
        ],
    ),
}


def _disable_focus_recursive(widget: QWidget) -> None:
    """Set NoFocus on every child widget to prevent keyboard stealing."""
    widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    for child in widget.findChildren(QWidget):
        child.setFocusPolicy(Qt.FocusPolicy.NoFocus)


class MainWindow(QMainWindow):
    """Top-level window for the Organum pipe organ synthesizer."""

    def __init__(self, mixer: Mixer, midi_player: MidiPlayer) -> None:
        super().__init__()
        self._mixer = mixer
        self._midi_player = midi_player

        self.setWindowTitle("Organum — Pipe Organ Synthesizer")
        self.setMinimumWidth(960)
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1208; }
            QWidget { background-color: #1e1208; }
        """)

        central = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(central)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background-color: #1e1208; }
            QScrollArea > QWidget > QWidget { background-color: #1e1208; }
            QScrollBar:vertical {
                background: #2a1a0a; width: 10px; border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #5a4a3a; border-radius: 4px; min-height: 30px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0; background: none;
            }
        """)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setCentralWidget(scroll)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(16, 10, 16, 14)

        # ── Title ───────────────────────────────────────────────────
        title = QLabel("𝖁𝖔𝖎𝖈𝖊 𝖔𝖋 𝕮𝖆𝖑𝖑𝖎𝖘𝖙𝖔")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Serif", 26, QFont.Weight.Bold))
        title.setStyleSheet("color: #d4a574; margin-bottom: 2px;")
        layout.addWidget(title)

        subtitle = QLabel(
            "Keys: Z–M (left hand) / Y–] (right hand)  ·  "
            "← → Octave  ·  LCtrl/RCtrl + ← → per hand  ·  "
            "Numpad: stop groups  ·  Shift+Num: drawbars"
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #8a7a6a; font-size: 11px; margin-bottom: 4px;")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        # ── Stop panel ──────────────────────────────────────────────
        self._stop_panel = StopPanel(list(STOP_DEFS.keys()), mixer.active_stop_names)
        self._stop_panel.stop_toggled.connect(self._on_stop_toggle)
        self._stop_panel.stop_volume_changed.connect(self._on_stop_volume)
        layout.addWidget(self._stop_panel)

        # ── Drawbar presets + Drawbars + Room presets ────────────────
        drawbar_row = QHBoxLayout()
        drawbar_row.addStretch()

        # Drawbar presets — left of drawbars
        self._drawbar_preset_panel = DrawbarPresetPanel()
        self._drawbar_preset_panel.preset_selected.connect(self._on_drawbar_preset)
        drawbar_row.addWidget(self._drawbar_preset_panel)

        # Drawbars (center)
        self._drawbar_panel = DrawbarPanel(DRAWBAR_LABELS, mixer.drawbar_values)
        self._drawbar_panel.drawbar_changed.connect(self._on_drawbar_change)
        drawbar_row.addWidget(self._drawbar_panel)

        # Swell EQ — right of drawbars
        self._swell_panel = SwellPanel(mixer.swell_values)
        self._swell_panel.swell_changed.connect(self._on_swell_change)
        drawbar_row.addWidget(self._swell_panel)

        # Room presets — right of drawbars
        self._room_panel = RoomPresetPanel(
            list(ROOM_PRESETS.keys()),
            mixer.current_room_preset,
        )
        self._room_panel.room_selected.connect(self._on_room_selected)
        drawbar_row.addWidget(self._room_panel)

        drawbar_row.addStretch()
        layout.addLayout(drawbar_row)

        # ── MIDI Player ─────────────────────────────────────────────
        self._midi_panel = MidiPlayerPanel(midi_player)
        layout.addWidget(self._midi_panel)

        # ── Recorder ─────────────────────────────────────────────────
        self._recorder_panel = RecorderPanel(mixer.recorder)
        layout.addWidget(self._recorder_panel)

        # ── Utility row: sustain + transpose + tuning ───────────────
        util_row = QHBoxLayout()
        util_row.setSpacing(16)

        # Sustain toggle
        self._sustain_btn = QPushButton("Sustain")
        self._sustain_btn.setCheckable(True)
        self._sustain_btn.setChecked(mixer.is_sustain_active)
        self._sustain_btn.setMinimumWidth(80)
        self._sustain_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a1a1a;
                color: #884040;
                border: 2px solid #5a2a2a;
                border-radius: 6px;
                font-size: 12px; font-weight: bold; padding: 6px 12px;
            }
            QPushButton:checked {
                background-color: #8b2222;
                color: #ffffff;
                border: 2px solid #ff6347;
            }
            QPushButton:hover { background-color: #3a2020; }
        """)
        self._sustain_btn.toggled.connect(self._on_sustain_toggle)
        util_row.addWidget(self._sustain_btn)

        # Tremulant toggle
        self._trem_btn = QPushButton("⚡ TREMULANT ⚡")
        self._trem_btn.setCheckable(True)
        self._trem_btn.setChecked("Tremulant" in mixer.active_stop_names)
        self._trem_btn.setMinimumWidth(120)
        self._trem_btn.setMinimumHeight(32)
        self._trem_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a1a1a;
                color: #884040;
                border: 2px solid #5a2a2a;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                padding: 4px 10px;
                letter-spacing: 1px;
            }
            QPushButton:checked {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #b22222, stop:0.5 #ff4500, stop:1 #b22222
                );
                color: #ffffff;
                border: 2px solid #ff6347;
            }
            QPushButton:hover {
                background-color: #3a2020;
            }
            QPushButton:checked:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #cc3333, stop:0.5 #ff5722, stop:1 #cc3333
                );
            }
        """)
        self._trem_btn.toggled.connect(lambda checked: self._mixer.toggle_stop("Tremulant"))
        util_row.addWidget(self._trem_btn)

        # Transpose controls
        transp_label = QLabel("Transpose:")
        transp_label.setStyleSheet("color: #c0b0a0; font-size: 12px; font-weight: bold;")
        util_row.addWidget(transp_label)

        self._transp_down = QPushButton("−")
        self._transp_down.setFixedSize(28, 28)
        self._transp_down.setStyleSheet("""
            QPushButton { background: #3a2a1a; color: #c0b0a0; border: 1px solid #5a4a3a;
                          border-radius: 4px; font-size: 16px; font-weight: bold; }
            QPushButton:hover { background: #4a3a2a; }
        """)
        self._transp_down.clicked.connect(self._on_transpose_down)
        util_row.addWidget(self._transp_down)

        self._transp_label = QLabel("0")
        self._transp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._transp_label.setFixedWidth(30)
        self._transp_label.setStyleSheet("color: #ffd700; font-size: 14px; font-weight: bold;")
        util_row.addWidget(self._transp_label)

        self._transp_up = QPushButton("+")
        self._transp_up.setFixedSize(28, 28)
        self._transp_up.setStyleSheet("""
            QPushButton { background: #3a2a1a; color: #c0b0a0; border: 1px solid #5a4a3a;
                          border-radius: 4px; font-size: 16px; font-weight: bold; }
            QPushButton:hover { background: #4a3a2a; }
        """)
        self._transp_up.clicked.connect(self._on_transpose_up)
        util_row.addWidget(self._transp_up)

        # Tuning selector
        tuning_label = QLabel("Tuning:")
        tuning_label.setStyleSheet("color: #c0b0a0; font-size: 12px; font-weight: bold;")
        util_row.addWidget(tuning_label)

        self._tuning_combo = QComboBox()
        self._tuning_combo.addItems(list(TUNINGS.keys()))
        self._tuning_combo.setCurrentText(mixer.current_tuning)
        self._tuning_combo.setStyleSheet("""
            QComboBox {
                background: #3a2a1a; color: #e0d4c0; border: 1px solid #5a4a3a;
                border-radius: 4px; padding: 4px 8px; font-size: 12px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background: #2a1a0a; color: #e0d4c0; selection-background-color: #5a3a2a;
            }
        """)
        self._tuning_combo.currentTextChanged.connect(self._on_tuning_changed)
        util_row.addWidget(self._tuning_combo)

        util_row.addStretch()
        layout.addLayout(util_row)

        # ── Status row: octave + stop group + drawbar info ──────────
        status_row = QHBoxLayout()
        status_row.setSpacing(20)

        self._octave_label = QLabel("")
        self._octave_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._octave_label.setStyleSheet(
            "color: #ffd700; font-size: 13px; font-weight: bold;"
        )
        status_row.addWidget(self._octave_label, 1)

        self._group_label = QLabel("Group: —")
        self._group_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._group_label.setStyleSheet(
            "color: #77bbff; font-size: 12px; font-weight: bold;"
        )
        status_row.addWidget(self._group_label, 1)

        self._drawbar_select_label = QLabel("Drawbar: —")
        self._drawbar_select_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._drawbar_select_label.setStyleSheet(
            "color: #ffaa55; font-size: 12px; font-weight: bold;"
        )
        status_row.addWidget(self._drawbar_select_label, 1)

        layout.addLayout(status_row)

        # ── Keyboard ───────────────────────────────────────────────
        kb_row = QHBoxLayout()
        kb_row.addStretch()
        self._keyboard = PianoKeyboard(base_note=48)
        self._keyboard.note_on.connect(self._on_note_on)
        self._keyboard.note_off.connect(self._on_note_off)
        self._keyboard.octave_changed.connect(self._update_octave_label)
        self._keyboard.hands_changed.connect(self._update_hands_label)
        self._keyboard.stop_group_selected.connect(self._on_stop_group)
        self._keyboard.drawbar_selected.connect(self._on_drawbar_selected)
        self._keyboard.drawbar_adjust.connect(self._on_drawbar_adjust)
        kb_row.addWidget(self._keyboard)
        kb_row.addStretch()
        layout.addLayout(kb_row)

        layout.addStretch()

        central.setLayout(layout)

        # ── Disable focus on ALL widgets except the keyboard ────────
        # This prevents buttons, sliders, etc. from stealing keyboard
        # input (Tab, Space, arrow keys, etc.)
        _disable_focus_recursive(central)
        self._keyboard.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._keyboard.setFocus()

        # ── Install application-wide event filter ───────────────────
        # Intercepts ALL key events before any widget sees them and
        # routes them directly to the piano keyboard.
        app = QApplication.instance()
        if app:
            app.installEventFilter(self)

        # Initialize labels
        self._update_hands_label(self._keyboard.left_base, self._keyboard.right_base)

        # ── MIDI note visualization timer ───────────────────────────
        # Poll MIDI player's active notes and highlight them on keyboard
        from PyQt6.QtCore import QTimer

        self._midi_viz_timer = QTimer()
        self._midi_viz_timer.timeout.connect(self._update_midi_visualization)
        self._midi_viz_timer.start(50)  # 20fps — smooth enough for visual feedback

    def eventFilter(self, obj, event: QEvent) -> bool:
        """Intercept ALL key events at the application level.

        Every KeyPress and KeyRelease is routed to the piano keyboard,
        bypassing Qt's normal focus/accessibility system entirely.
        """
        if event.type() in (QEvent.Type.KeyPress, QEvent.Type.KeyRelease):
            key_event = event
            if key_event.key() == Qt.Key.Key_F11:
                if self.isFullScreen():
                    self.showMaximized()
                else:
                    self.showFullScreen()
                return True
            if event.type() == QEvent.Type.KeyPress:
                self._keyboard.keyPressEvent(key_event)
            else:
                self._keyboard.keyReleaseEvent(key_event)
            return True

        # For ShortcutOverride events (Qt trying to match shortcuts):
        # accept them to prevent Qt from consuming the key
        if event.type() == QEvent.Type.ShortcutOverride:
            event.accept()
            return True

        return super().eventFilter(obj, event)

    def _update_midi_visualization(self) -> None:
        """Poll MIDI player for active notes and highlight on keyboard."""
        notes = self._midi_player.active_notes
        self._keyboard.set_highlighted_notes(notes)

    def _update_octave_label(self, base_note: int) -> None:
        self._update_hands_label(self._keyboard.left_base, self._keyboard.right_base)

    def _update_hands_label(self, left_base: int, right_base: int) -> None:
        lh_low = _note_name(left_base)
        lh_high = _note_name(left_base + 11)
        rh_low = _note_name(right_base)
        rh_high = _note_name(right_base + 11)
        self._octave_label.setText(
            f"🎹  LH: {lh_low}–{lh_high}  |  RH: {rh_low}–{rh_high}"
        )

    def _on_note_on(self, note: int) -> None:
        self._mixer.note_on(note)

    def _on_note_off(self, note: int) -> None:
        self._mixer.note_off(note)

    def _on_sustain_toggle(self, on: bool) -> None:
        self._mixer.set_sustain(on)

    def _on_transpose_up(self) -> None:
        new_val = max(-12, min(12, self._mixer.current_transpose + 1))
        self._mixer.set_transpose(new_val)
        self._transp_label.setText(str(new_val))

    def _on_transpose_down(self) -> None:
        new_val = max(-12, min(12, self._mixer.current_transpose - 1))
        self._mixer.set_transpose(new_val)
        self._transp_label.setText(str(new_val))

    def _on_tuning_changed(self, name: str) -> None:
        self._mixer.set_tuning(name)

    def _on_drawbar_change(self, index: int, value: float) -> None:
        self._mixer.set_drawbar(index, value)

    def _on_stop_toggle(self, name: str, active: bool) -> None:
        self._mixer.toggle_stop(name)

    def _on_stop_group(self, group_id: int) -> None:
        """Apply a stop group preset from numpad."""
        if group_id not in STOP_GROUPS:
            return

        group_name, desired_stops = STOP_GROUPS[group_id]

        # Get current active stops
        current = self._mixer.active_stop_names

        # Turn off stops not in the desired group
        for name in list(current):
            if name not in desired_stops:
                self._mixer.toggle_stop(name)

        # Turn on stops that should be active
        # Re-read after toggling off
        current = self._mixer.active_stop_names
        for name in desired_stops:
            if name not in current and name in STOP_DEFS:
                self._mixer.toggle_stop(name)

        # Update stop panel buttons to reflect new state
        new_active = self._mixer.active_stop_names
        self._stop_panel.update_stops(new_active)

        self._group_label.setText(f"Group {group_id}: {group_name}")

    def _on_drawbar_selected(self, index: int) -> None:
        """Highlight the selected drawbar."""
        if 0 <= index < len(DRAWBAR_LABELS):
            self._drawbar_select_label.setText(
                f"Drawbar: {DRAWBAR_LABELS[index]} (↑/↓ to adjust)"
            )
            self._drawbar_panel.highlight_drawbar(index)

    def _on_drawbar_adjust(self, index: int, delta: int) -> None:
        """Adjust a drawbar value via keyboard."""
        self._drawbar_panel.adjust_drawbar(index, delta)

    def _on_drawbar_preset(self, name: str, values: list) -> None:
        """Apply a drawbar preset."""
        self._drawbar_panel.set_values(values)

    def _on_swell_change(self, index: int, value: float) -> None:
        self._mixer.set_swell(index, value)

    def _on_stop_volume(self, stop_name: str, volume: float) -> None:
        self._mixer.set_stop_volume(stop_name, volume)

    def _on_room_selected(self, preset_name: str) -> None:
        """Apply a room preset."""
        self._mixer.set_room_preset(preset_name)
