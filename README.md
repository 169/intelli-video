## video-translation

It uses [OpenAI Whisper](https://github.com/openai/whisper) and OpenAI API([TTS](https://platform.openai.com/docs/guides/text-to-speech)) to achieve the following purposes:

video-translation is an ongoing project. Its purpose is as follows:

1. Video download. ✅
2. Get audio from video, the default is mp3 format. ✅
3. Generate subtitles based on audio and translate them into other languages. ✅
4. Add hard subtitles to videos. ✅
5. Support the production of videos in other languages based on subtitles. Not yet

Therefore, `vt` can automatically add subtitles in various languages to online videos and local videos. In the future, the voices in the videos can also be automatically converted into other languages. Welcome to follow this project and contribute code

## Setup

First, Install and update using `poetry`:

```bash
poetry install
```

It also requires the command-line tool ffmpeg to be installed on your system, which is available from most package managers:

```bash
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

## Command-line usage

By default, Chinese and English subtitles will be added to the video.

You can use the following 2 commands:

### Download video online

```bash
poetry run python main.py web --url=https://www.youtube.com/watch?v=CqRrByI-ONE
```

### Local video

```bash
poetry run vt local --path='/Users/169/Movies/test.mov
```

