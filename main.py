import click

from core.audio import generate_audio, generate_srt
from core.downloader import download
from core.video import generate_video


@click.group()
def cli():
    """`vt` is a tool for adding subtitle to videos and generating videos in other languages."""


@cli.command()
@click.option("--path", required=True, help="Local file path.")
def local(path):
    audio = generate_audio(path)
    srts = generate_srt(audio)
    for video in generate_video(path, srts):
        click.echo(f"Generated: {video}")


@cli.command()
@click.option("--url", required=True, help="video url.")
def web(url):
    media = download(url)
    srts = generate_srt(media.audio)
    for video in generate_video(media.video, srts):
        click.echo(f"Generated: {video}")


if __name__ == "__main__":
    cli()
