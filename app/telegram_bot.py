from __future__ import annotations

import asyncio
from contextlib import suppress
import logging

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from app.config import load_settings
from app.summarizer import build_structured_summary, chunk_message, render_summary
from app.transcriber import WhisperTranscriber
from app.youtube import download_audio, extract_youtube_url


logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if update.message is None:
        return
    await update.message.reply_text(
        "Send me a YouTube URL. I will download the audio, transcribe it with Whisper, "
        "and return a timestamped summary with key takeaways."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.message.text is None:
        return

    settings = context.application.bot_data["settings"]
    transcriber = context.application.bot_data["transcriber"]
    url = extract_youtube_url(update.message.text)
    if not url:
        await update.message.reply_text("Please send a valid YouTube URL.")
        return

    await update.message.reply_text("Got it. Downloading audio and transcribing now...")
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)

    try:
        result = await asyncio.to_thread(
            download_audio,
            url,
            settings.download_dir,
            settings.max_video_seconds,
        )
        await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
        transcript = await asyncio.to_thread(transcriber.transcribe, result.audio_path)
        summary = build_structured_summary(
            transcript,
            max_sections=settings.max_summary_sections,
        )
        rendered = render_summary(summary, result.title, result.webpage_url)
        for chunk in chunk_message(rendered):
            await update.message.reply_text(chunk, disable_web_page_preview=True)
    except Exception:
        logger.exception("Failed to summarize video")
        await update.message.reply_text(
            "I could not summarize that video. Please check the link, video length, "
            "and whether the video is publicly accessible."
        )
    finally:
        if "result" in locals():
            with suppress(OSError):
                result.audio_path.unlink()


def main() -> None:
    settings = load_settings()
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required.")

    application = Application.builder().token(settings.telegram_bot_token).build()
    application.bot_data["settings"] = settings
    application.bot_data["transcriber"] = WhisperTranscriber(
        settings.whisper_model,
        settings.whisper_device,
        settings.whisper_compute_type,
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
