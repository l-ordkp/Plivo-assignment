"""
Audio recording with Voice Activity Detection (VAD)
using mean absolute amplitude instead of RMS.
"""

import pyaudio
import wave
import numpy as np
import tempfile
from typing import Optional, Callable
from ..utils.logger import Logger
import config


class AudioRecorder:
    """Records audio with simple VAD based on mean absolute amplitude."""

    def __init__(
        self,
        logger: Logger,
        vad_threshold: int = config.DEFAULT_VAD_THRESHOLD,
        silence_duration: float = config.DEFAULT_SILENCE_DURATION,
    ):
        """
        :param logger: Logger instance
        :param vad_threshold: Threshold for detecting speech based on amplitude
        :param silence_duration: Duration (seconds) of silence after speech to stop recording
        """
        self.logger = logger
        self.vad_threshold = vad_threshold
        self.silence_duration = silence_duration

        self.audio = pyaudio.PyAudio()
        self.audio_buffer = []
        self.is_recording = False

    # ---------- Volume / VAD helpers ----------

    def calculate_level(self, audio_data: bytes) -> float:
        """
        Simpler volume measure: mean absolute amplitude of int16 samples.

        Returns a float that you compare with self.vad_threshold.
        """
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        if audio_array.size == 0:
            return 0.0

        # convert to float to avoid overflow issues
        audio_f = audio_array.astype(np.float32)
        level = float(np.mean(np.abs(audio_f)))
        return level

    # ---------- Main VAD recording loop ----------

    def record_with_vad(
        self,
        status_callback: Optional[Callable[[str], None]] = None,
    ) -> Optional[str]:
        """
        Record audio with Voice Activity Detection.
        - Starts in 'listening' mode.
        - When level > vad_threshold, it considers that as speech.
        - Continues recording until there's `silence_duration` seconds of silence after speech.
        - Returns path to a temporary WAV file if speech was detected, else None.
        """

        print("record-vad-start")

        audio_format = getattr(pyaudio, config.AUDIO_FORMAT)

        stream = self.audio.open(
            format=audio_format,
            channels=config.CHANNELS,
            rate=config.SAMPLE_RATE,
            input=True,
            frames_per_buffer=config.CHUNK_SIZE,
        )

        self.logger.info("Started listening...")
        if status_callback:
            status_callback("listening")

        self.audio_buffer = []
        silence_chunks = 0
        speech_detected = False

        # How many chunks correspond to the allowed trailing silence?
        max_silence_chunks = int(
            self.silence_duration * config.SAMPLE_RATE / config.CHUNK_SIZE
        )

        # Safety: maximum total time to wait if no speech is ever detected (e.g. 10 seconds)
        max_total_chunks = int(10 * config.SAMPLE_RATE / config.CHUNK_SIZE)
        total_chunks = 0

        try:
            self.is_recording = True

            while self.is_recording:
                data = stream.read(config.CHUNK_SIZE, exception_on_overflow=False)
                level = self.calculate_level(data)
                total_chunks += 1

                # Debug print – helpful while tuning threshold
                print(f"Level: {level:.2f}, threshold: {self.vad_threshold}")

                # If no speech was detected for too long, bail out
                if total_chunks > max_total_chunks and not speech_detected:
                    self.logger.info("No speech detected within timeout, stopping.")
                    break

                # ---- VAD logic ----
                if level > self.vad_threshold:
                    # We consider this as speech
                    if not speech_detected:
                        speech_detected = True
                        self.logger.info("Speech detected")
                        if status_callback:
                            status_callback("speaking")

                    silence_chunks = 0
                    self.audio_buffer.append(data)

                elif speech_detected:
                    # After we've detected speech once, track silence
                    silence_chunks += 1
                    self.audio_buffer.append(data)

                    if silence_chunks > max_silence_chunks:
                        self.logger.info("Silence detected, processing speech...")
                        break

        finally:
            stream.stop_stream()
            stream.close()

        if speech_detected and self.audio_buffer:
            return self._save_audio_buffer(audio_format)

        return None

    # ---------- File saving ----------

    def _save_audio_buffer(self, audio_format) -> str:
        """Save audio buffer to a temporary WAV file and return its path."""
        print("audio-buffer-save")

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

        with wave.open(temp_file.name, "wb") as wf:
            wf.setnchannels(config.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(audio_format))
            wf.setframerate(config.SAMPLE_RATE)
            wf.writeframes(b"".join(self.audio_buffer))

        return temp_file.name

    # ---------- Control / cleanup ----------

    def stop(self):
        """Stop recording loop."""
        self.is_recording = False

    def cleanup(self):
        """Clean up audio resources."""
        self.audio.terminate()

    # ---------- Optional: helper to tune threshold ----------

    def debug_print_levels(self, seconds: int = 3):
        """
        Helper to see typical levels for noise vs speech.
        Call this once and talk normally to choose a good vad_threshold.
        """
        audio_format = getattr(pyaudio, config.AUDIO_FORMAT)
        stream = self.audio.open(
            format=audio_format,
            channels=config.CHANNELS,
            rate=config.SAMPLE_RATE,
            input=True,
            frames_per_buffer=config.CHUNK_SIZE,
        )

        num_chunks = int(seconds * config.SAMPLE_RATE / config.CHUNK_SIZE)
        print(f"Collecting levels for {seconds} seconds...")

        try:
            for i in range(num_chunks):
                data = stream.read(config.CHUNK_SIZE, exception_on_overflow=False)
                level = self.calculate_level(data)
                print(f"Chunk {i}: level = {level:.2f}")
        finally:
            stream.stop_stream()
            stream.close()
