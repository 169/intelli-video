import click
from loguru import logger
from whisper import _MODELS
from whisper.tokenizer import LANGUAGES

from config import OUTPUT_DIR, WHISPER_MODEL
from core.audio import generate_audio, generate_subtitle, generate_vtt
from core.downloader import download
from core.video import generate_video

WHISPER_SUPPORT_TYPES = ["vtt", "srt", "json", "txt", "tsv", "all"]
OPENAI_API_SUPPORT_TYPES = ["json", "text", "vtt", "srt"]


class Mutex(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if: list = kwargs.pop("not_required_if", [])

        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs["help"] = (
            kwargs.get("help", "")
            + ". Notice: this option is mutually exclusive with "
            + ", ".join(self.not_required_if)
            + "."
        ).strip()
        super(Mutex, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current_opt: bool = self.name in opts
        for mutex_opt in self.not_required_if:
            if mutex_opt in opts:
                if current_opt:
                    raise click.UsageError(
                        "Illegal usage: '"
                        + str(self.name)
                        + "' is mutually exclusive with "
                        + str(mutex_opt)
                        + "."
                    )
                else:
                    self.prompt = None
        if current_opt and not opts[self.name]:
            raise click.UsageError(
                f"Illegal usage: The value of '{self.name}' cannot be empty."
            )
        return super(Mutex, self).handle_parse_result(ctx, opts, args)


@click.group()
def cli():
    """`vt` is a tool for adding subtitle to videos and generating videos in other languages."""


@cli.command()
@click.option("-p", "--path", required=True, help="Local file path or video url.")
@click.option("-o", "--output", default=OUTPUT_DIR, help="Generated video dir.")
@click.option(
    "-l",
    "--language",
    default="en",
    type=click.Choice(LANGUAGES.keys(), case_sensitive=False),
    help="Subtitle language.",
)
@click.option(
    "-m",
    "--model",
    default=WHISPER_MODEL,
    type=click.Choice(_MODELS.keys(), case_sensitive=False),
    help="Whisper model name.",
)
@click.option(
    "-m",
    "--method",
    default="whisper",
    type=click.Choice(["whisper", "openai_api"], case_sensitive=False),
    help="Method for generating subtitle files.",
)
@click.option(
    "-f",
    "--format",
    default="vtt",
    help="Subtitle format.",
)
def subtitle(path, output, language, model, method, format):
    if method == "whisper" and format not in WHISPER_SUPPORT_TYPES:
        raise click.UsageError(
            f"Illegal usage: `whisper` method only support: {WHISPER_SUPPORT_TYPES}."
        )
    elif method == "openai_api" and format not in OPENAI_API_SUPPORT_TYPES:
        raise click.UsageError(
            f"Illegal usage: `openai_api` method only support: {OPENAI_API_SUPPORT_TYPES}."
        )

    if path.startswith("http"):
        media = download(path)
        audio = media.audio
    else:
        audio = generate_audio(path)
    generate_subtitle(audio, method, language, format, output, model_name=model)


@cli.command()
@click.option("-p", "--path", required=True, help="Local file path.")
@click.option("-o", "--output", default=OUTPUT_DIR, help="Generated video dir.")
@click.option(
    "-b",
    "--bilingual",
    default="",
    cls=Mutex,
    not_required_if=["subtitles"],
    help="Use bilingual subtitle. you can specify the subtitle language by `--subtitles`",
)
@click.option(
    "-s",
    "--subtitles",
    default="",
    cls=Mutex,
    not_required_if=["bilingual"],
    help='Subtitle languages. split by ","',
)
def local(path, output, bilingual, subtitles):
    if bilingual and "," not in bilingual:
        raise click.UsageError(
            "Illegal usage: `--bilingual` requires 2 language subtitles, you can use `cn,en` or `en,cn`"
        )
    audio = generate_audio(path)
    vtts = generate_vtt(audio, bilingual, subtitles)
    if not vtts:
        logger.warning("No subtitles generated.")
    for video in generate_video(path, vtts, output):
        logger.info(f"Generated: {video}")


@cli.command()
@click.option("-u", "--url", required=True, help="Video url.")
@click.option("-o", "--output", default=OUTPUT_DIR, help="Generated video dir.")
@click.option(
    "-b",
    "--bilingual",
    default="",
    cls=Mutex,
    not_required_if=["subtitles"],
    help="Use bilingual subtitle",
)
@click.option(
    "-s",
    "--subtitles",
    default="zh,en",
    cls=Mutex,
    not_required_if=["bilingual"],
    help='Subtitle languages. split by ","',
)
def web(url, output, bilingual, subtitles):
    if bilingual and "," not in bilingual:
        raise click.UsageError(
            "Illegal usage: `--bilingual` requires 2 language subtitles, you can use `cn,en` or `en,cn`"
        )
    media = download(url)
    vtts = generate_vtt(media.audio, bilingual, subtitles)
    if not vtts:
        logger.warning("No subtitles generated.")
    for video in generate_video(media.video, vtts, output):
        logger.info(f"Generated: {video}")


if __name__ == "__main__":
    cli()
