"""Recording engine — captures audio frames, saves WAV/MP3.

Thread-safe: audio callback calls add_frames(), GUI thread calls
start()/stop(). Lock protects the buffer list.
"""

import threading
import subprocess
import numpy as np
import wave


class Recorder:
    """Captures stereo audio frames while recording is active."""

    def __init__(self, sample_rate: int = 44100) -> None:
        self._sample_rate = sample_rate
        self._lock = threading.Lock()
        self._recording = False
        self._buffers: list[np.ndarray] = []

    @property
    def is_recording(self) -> bool:
        return self._recording

    @property
    def sample_rate(self) -> int:
        return self._sample_rate

    def start(self) -> None:
        with self._lock:
            self._buffers.clear()
            self._recording = True

    def stop(self) -> np.ndarray:
        """Stop recording and return all captured frames as (N, 2) float32."""
        with self._lock:
            self._recording = False
            if not self._buffers:
                result = np.zeros((0, 2), dtype=np.float32)
            else:
                result = np.concatenate(self._buffers, axis=0)
            self._buffers.clear()
            return result

    def add_frames(self, frames: np.ndarray) -> None:
        """Append stereo frame block (called from audio callback)."""
        if self._recording:
            with self._lock:
                if self._recording:
                    self._buffers.append(frames.copy())

    def save_wav(self, path: str, data: np.ndarray) -> None:
        """Write float32 data to 16-bit WAV file."""
        with wave.open(path, "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(self._sample_rate)
            int_data = (data * 32767.0).clip(-32768.0, 32767.0).astype(np.int16)
            wf.writeframes(int_data.tobytes())

    def save_mp3(self, wav_path: str, mp3_path: str) -> None:
        """Convert WAV to MP3 via external ffmpeg."""
        subprocess.run(
            ["ffmpeg", "-y", "-i", wav_path, "-codec:a", "libmp3lame", mp3_path],
            capture_output=True, check=True,
        )
