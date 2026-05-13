# Offline Reviewer Demo Output

This file shows the same type of output produced by `python scripts/smoke_demo.py`.
It is included so reviewers can inspect the English and Chinese formatting without
running Telegram, YouTube download, Whisper, Railway, or any secrets.

## English Demo

```text
Video: English demo
Source: https://youtu.be/demo
Detected language: en

Overview
This video explains how a Telegram bot receives a YouTube link.

Timestamped summary
- 0:00-0:18: Video / Explains / Telegram
  - This video explains how a Telegram bot receives a YouTube link.
- 0:18-0:44: Downloads / Audio / Transcribes
  - The bot downloads audio, transcribes it with Whisper, and builds a timestamped summary for the user.
- 0:44-1:10: Railway / Deployment / Keeps
  - The Railway deployment keeps secrets outside the repository and uses environment variables for the Telegram token.

Key takeaways
- 0:44 - The Railway deployment keeps secrets outside the repository and uses environment variables for the Telegram token.
- 0:18 - The bot downloads audio, transcribes it with Whisper, and builds a timestamped summary for the user.
- 0:00 - This video explains how a Telegram bot receives a YouTube link.
```

## Chinese Demo

```text
Video: Chinese demo
Source: https://youtu.be/demo
Detected language: zh

Overview
这个视频介绍如何把 YouTube 链接发送给 Telegram 机器人。

Timestamped summary
- 0:00-0:14: 这个视频介绍如何把 / Youtube / 链接发送给
  - 这个视频介绍如何把 YouTube 链接发送给 Telegram 机器人。
- 0:14-0:36: 机器人会下载音频 / 使用 / Whisper
  - 机器人会下载音频，使用 Whisper 转写，然后生成带时间戳的摘要。
- 0:36-0:58: 部署到 / Railway / Telegram
  - 部署到 Railway 时，Telegram token 只放在环境变量里，不写进代码仓库。

Key takeaways
- 0:36 - 部署到 Railway 时，Telegram token 只放在环境变量里，不写进代码仓库。
- 0:00 - 这个视频介绍如何把 YouTube 链接发送给 Telegram 机器人。
- 0:14 - 机器人会下载音频，使用 Whisper 转写，然后生成带时间戳的摘要。
```
