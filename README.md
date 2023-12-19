## video-translation

video-translation is an ongoing project. it uses [OpenAI Whisper](https://github.com/openai/whisper) and OpenAI API([TTS](https://platform.openai.com/docs/guides/text-to-speech)) to achieve the following purposes:

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

Currently 3 methods of adding subtitles are supported.

### Download video online and add subtitle

```bash
poetry run python main.py web --url=https://www.youtube.com/watch?v=CqRrByI-ONE
```

The `web` subcommand also supports more options, as follows:

```bash
poetry run vt web --help
Usage: vt web [OPTIONS]

Options:
  -u, --url TEXT        Video url.  [required]
  -o, --output TEXT     Generated video dir.
  -b, --bilingual TEXT  Use bilingual subtitle. Notice: this option is mutually exclusive
                        with subtitles.
  -s, --subtitles TEXT  Subtitle languages. split by ",". Notice: this option is mutually
                        exclusive with bilingual.
  --help                Show this message and exit.
```

### Use local video and add subtitle

```bash
poetry run vt local --path='/Users/169/Movies/test.mov
```

The `web` subcommand also supports more options, as follows:

```bash
poetry run vt local --help
Usage: vt local [OPTIONS]

Options:
  -p, --path TEXT       Local file path.  [required]
  -o, --output TEXT     Generated video dir.
  -b, --bilingual TEXT  Use bilingual subtitle. you can specify the subtitle
                        language by `--subtitles`. Notice: this option is
                        mutually exclusive with subtitles.
  -s, --subtitles TEXT  Subtitle languages. split by ",". Notice: this option
                        is mutually exclusive with bilingual.
  --help                Show this message and exit.
```

### Add bilingual subtitles to local video

Use `--bilingual` option to generate bilingual subtitles. The two languages are separated by commas. The first language is on top and the later language is on the bottom.

```bash
poetry run vt local --path="/Users/169/videos/Langchain C3_L6.mp4" --bilingual="cn,en" --output="/Users/169/Downloads"
```


## Custom config

All configuration items are in [config.py](https://github.com/169/video-translation/blob/main/config.py)

Projects also support limited custom configuration. You can add a file called `local_settings.py` under the project and add the settings you want to override.

for example. The default `debug` is False in `config.py`. You can add `debug = True` in `local_settings.py`, which will enable debug mode:

```bash
cat local_settings.py
debug = True
```

