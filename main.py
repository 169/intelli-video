import click

from core.downloader import download
from core.audio import generate_audio, generate_srt
from core.video import generate_video

@click.command()
@click.option('--path', required=True, help='Local file path.')
def local(path):
    audio = generate_audio(path)
    srt = generate_srt(audio)
    video = generate_video(path, srt)


if __name__ == '__main__':
    local()