## video-translation

video-translation is an ongoing project leveraging [OpenAI Whisper](https://github.com/openai/whisper) and the OpenAI API ([TTS](https://platform.openai.com/docs/guides/text-to-speech)) to accomplish the following objectives:

1. Video Download: ✅
2. Extract Audio from Video: Default format is mp3. ✅
3. Generate Subtitles from Audio and Translate: ✅
4. Embed Hard Subtitles into Videos: ✅
5. Support for Video Production in Different Languages based on Subtitles: In progress

Hence, vt autonomously adds subtitles in multiple languages to both online and local videos. Future capabilities aim to automatically convert video voices into various languages. Feel free to follow and contribute to this project.

## Setup

Begin by installing and updating using poetry:

```bash
poetry install
```

Additionally, ensure you have the command-line tool `ffmpeg` installed on your system. It's available via most package managers:
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

## Streamlit-based Web UI

Our project's Web UI, powered by Streamlit, allows users to add subtitles to videos through an intuitive web interface. This section outlines the primary features of this functionality:

1. **Configurable Options**: Users can specify multiple settings such as the Whisper model for audio processing, language preferences, video file types, and subtitle styles to suit various requirements.
2. **Automatic Subtitle Generation**: The tool supports generating subtitles directly from the video content, leveraging advanced speech-to-text technology for accuracy.
3. **Subtitle Preview Mode**: After adding subtitles, users can engage a preview mode to see how subtitles appear on the actual video, ensuring proper synchronization and styling.
4. **Editable Subtitles with Auto Save**: This feature allows users to edit subtitles and see changes in real-time. The 'Auto Save' option can be toggled to apply modifications instantly.
5. **Subtitle File Download**: Once subtitles are created or edited, users have the option to download these files in different formats (e.g., SRT, VTT), making them compatible with various media players and platforms.
6. **Export Video with Subtitles**: Users can export the final video with subtitles embedded, ready for sharing on different platforms or for personal use.

Launching the Web UI:

```bash
poetry run streamlit run webui.py
```

And, open your web browser and enter the following address to access the Web UI: `http://localhost:8501/`

## Command-line usage

There are two primary command-line usage types:

1. **Generate Subtitle Files**: Supports srt, vtt format based on video content. You can use video tools or website functions to add these subtitles to videos.
2. **Directly Add Subtitles to Videos**: Currently supports three methods of subtitle addition.

### Generate subtitle files(Supports srt, vtt, json, txt, tsv and all format)

```bash
poetry run vt subtitle --path='https://www.bilibili.com/video/BV1tb4y1L7yA' --language=en --method=whisper --format=vtt --output=/Users/169/Downloads
```

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

The `local` subcommand also supports more options, as follows:

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

Use the `--bilingual` option to create bilingual subtitles. Separate the two languages with commas, with the first language on top and the latter at the bottom.

```bash
poetry run vt local --path="/Users/169/videos/Langchain C3_L6.mp4" --bilingual="cn,en" --output="/Users/169/Downloads"
```

## Custom config

All configuration items reside in [config.py](https://github.com/169/video-translation/blob/main/config.py).

The project also supports limited custom configuration. Add a file named `local_settings.py` within the project and include the settings you wish to override.

For instance, if the default debug is set to `False` in `config.py`, you can enable debug mode by adding `debug = True` in local_settings.py:

```bash
cat local_settings.py
debug = True
```

