# YouTube Summary Telegram Bot

Telegram bot for AGuild quest #2. It accepts a YouTube URL, downloads the audio,
transcribes speech with Whisper, and returns a structured summary with timestamps
and key takeaways.

## Features

- Telegram bot command and message handlers
- YouTube URL detection for `youtube.com`, `youtu.be`, Shorts, and live URLs
- Audio extraction through `yt-dlp` and `ffmpeg`
- Local Whisper transcription through `faster-whisper`
- English and Chinese transcript support
- Timestamped summary sections and key takeaways
- Telegram-safe message chunking
- Railway-ready Dockerfile, Procfile, and `railway.json`

## Environment Variables

| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Yes | | Token from BotFather |
| `WHISPER_MODEL` | No | `small` | `tiny`, `base`, `small`, `medium`, or another faster-whisper model |
| `WHISPER_DEVICE` | No | `cpu` | Use `cuda` on GPU hosts |
| `WHISPER_COMPUTE_TYPE` | No | `int8` | Good CPU default; use `float16` on many GPU hosts |
| `MAX_VIDEO_SECONDS` | No | `3600` | Reject videos longer than this limit |
| `MAX_SUMMARY_SECTIONS` | No | `8` | Maximum timestamped sections returned |
| `DOWNLOAD_DIR` | No | `downloads` | Temporary audio directory |

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
export TELEGRAM_BOT_TOKEN="your-telegram-token"
python -m app.telegram_bot
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
$env:TELEGRAM_BOT_TOKEN="your-telegram-token"
python -m app.telegram_bot
```

`ffmpeg` must be available locally. The Docker image installs it automatically.

## Railway Deployment

1. Create a new Railway project from this GitHub repository.
2. Set `TELEGRAM_BOT_TOKEN` in Railway variables.
3. Optionally set `WHISPER_MODEL=tiny` or `WHISPER_MODEL=base` for lower memory use.
4. Deploy. Railway will use the included Dockerfile.

The bot uses long polling, so it does not need a public webhook URL.

## How It Works

1. The Telegram handler extracts and validates the first YouTube URL in a message.
2. `yt-dlp` downloads the best available audio track and converts it to MP3.
3. `faster-whisper` transcribes the audio with language auto-detection.
4. The summarizer groups transcript segments by time, keeps timestamps, and returns
   an overview plus key takeaways.
5. Long responses are split into Telegram-safe chunks.

## Validation

```bash
python -m compileall app tests scripts
pytest
ruff check app tests scripts
python scripts/config_check.py --allow-missing-token
python scripts/smoke_demo.py
```

## Configuration Check

Before a live Railway deployment, verify the environment without printing any
secret values:

```bash
python scripts/config_check.py
```

For offline review without a Telegram token:

```bash
python scripts/config_check.py --allow-missing-token
```

The check reports whether required variables are present, shows optional values
or defaults, validates numeric limits, and hides the actual bot token.

## Reviewer Smoke Demo

Reviewers can check the summary formatting without a Telegram token, YouTube
download, Whisper model, or OpenAI key:

```bash
python scripts/smoke_demo.py
```

The demo prints one English and one Chinese sample reply using the same summary
renderer used by the bot.

For reviewers who do not want to run any commands, the committed
`reviewer-demo.md` file shows the same English and Chinese output shape.

## Quest Deliverable Checklist

- Telegram bot entrypoint: `app/telegram_bot.py`
- YouTube URL parsing and audio download: `app/youtube.py`
- Whisper transcription wrapper: `app/transcriber.py`
- English and Chinese timestamped summary rendering: `app/summarizer.py`
- Railway deployment files: `Dockerfile`, `Procfile`, `railway.json`
- Automated validation: `.github/workflows/ci.yml`
- Secret-safe configuration check: `scripts/config_check.py`
- Offline review demo: `scripts/smoke_demo.py`
- Static review artifact: `reviewer-demo.md`

## Notes for Review

Live deployment requires the quest owner to provide their own Telegram bot token
and Railway project access. This repository intentionally does not include any
secrets.
