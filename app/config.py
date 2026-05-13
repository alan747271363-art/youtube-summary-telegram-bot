from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    download_dir: Path
    whisper_model: str
    whisper_device: str
    whisper_compute_type: str
    max_video_seconds: int
    max_summary_sections: int


def load_settings() -> Settings:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    return Settings(
        telegram_bot_token=token,
        download_dir=Path(os.environ.get("DOWNLOAD_DIR", "downloads")),
        whisper_model=os.environ.get("WHISPER_MODEL", "small"),
        whisper_device=os.environ.get("WHISPER_DEVICE", "cpu"),
        whisper_compute_type=os.environ.get("WHISPER_COMPUTE_TYPE", "int8"),
        max_video_seconds=int(os.environ.get("MAX_VIDEO_SECONDS", "3600")),
        max_summary_sections=int(os.environ.get("MAX_SUMMARY_SECTIONS", "8")),
    )
