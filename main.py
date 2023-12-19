import click
from loguru import logger

from config import OUTPUT_DIR
from core.audio import generate_audio, generate_vtt
from core.downloader import download
from core.video import generate_video


class Mutex(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if: list = kwargs.pop("not_required_if")

        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs["help"] = (
            kwargs.get("help", "")
            + "Option is mutually exclusive with "
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
    default="zh,en",
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
