from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from urllib.parse import parse_qs, urlparse

from yt_dlp import YoutubeDL


YOUTUBE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtu.be",
}


@dataclass(frozen=True)
class VideoDownload:
    title: str
    webpage_url: str
    duration: int | None
    audio_path: Path


def extract_youtube_url(text: str) -> str | None:
    match = re.search(r"https?://[^\s<>]+", text)
    if not match:
        return None
    url = match.group(0).rstrip(").,]")
    return url if is_youtube_url(url) else None


def is_youtube_url(url: str) -> bool:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if host not in YOUTUBE_HOSTS:
        return False
    if host == "youtu.be":
        return bool(parsed.path.strip("/"))
    if parsed.path == "/watch":
        return bool(parse_qs(parsed.query).get("v"))
    return parsed.path.startswith(("/shorts/", "/live/"))


def download_audio(url: str, download_dir: Path, max_video_seconds: int) -> VideoDownload:
    download_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(download_dir / "%(id)s.%(ext)s")
    options = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "64",
            }
        ],
    }

    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)

    duration = info.get("duration")
    if isinstance(duration, int) and duration > max_video_seconds:
        raise ValueError(
            f"Video is {duration} seconds, above the {max_video_seconds} second limit."
        )

    video_id = info["id"]
    audio_path = download_dir / f"{video_id}.mp3"
    if not audio_path.exists():
        raise FileNotFoundError(f"Expected downloaded audio at {audio_path}")

    return VideoDownload(
        title=info.get("title") or "Untitled YouTube video",
        webpage_url=info.get("webpage_url") or url,
        duration=duration if isinstance(duration, int) else None,
        audio_path=audio_path,
    )
