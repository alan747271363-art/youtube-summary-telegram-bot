from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from faster_whisper import WhisperModel


@dataclass(frozen=True)
class TranscriptSegment:
    start: float
    end: float
    text: str


@dataclass(frozen=True)
class Transcript:
    language: str
    segments: list[TranscriptSegment]


class WhisperTranscriber:
    def __init__(self, model_name: str, device: str, compute_type: str) -> None:
        self._model = WhisperModel(model_name, device=device, compute_type=compute_type)

    def transcribe(self, audio_path: Path) -> Transcript:
        segments, info = self._model.transcribe(
            str(audio_path),
            beam_size=5,
            vad_filter=True,
            word_timestamps=False,
        )
        transcript_segments = [
            TranscriptSegment(start=item.start, end=item.end, text=item.text.strip())
            for item in segments
            if item.text.strip()
        ]
        return Transcript(language=info.language or "unknown", segments=transcript_segments)
