import click

from core.downloader import download
from core.audio import generate_audio, generate_srt
from core.video import generate_video

@click.group()
def cli():
    ...

@cli.command()
@click.option('--path', required=True, help='Local file path.')
def local(path):
    audio = generate_audio(path)
    srts = generate_srt(audio)
    video = generate_video(path, srts)
    click.echo(f'Generated: {video}')


@cli.command()
@click.option('--url', required=True, help='video url.')
def web(url):
    media = download(url)
    srts = generate_srt(media.audio)
    video = generate_video(media.video, srts)
    click.echo(f'Generated: {video}')


if __name__ == '__main__':
    cli()