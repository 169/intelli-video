def format_timestamp(seconds: float,):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:"
    return f"{hours_marker}{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def write_srt(transcript: [dict], audio: str, language: str):
    srt_filename = f"{audio.removesuffix('.mp3')}.{language}.srt"

    with open(srt_filename, "w") as f:
        for i, segment in enumerate(transcript, start=1):
            start = format_timestamp(segment['start'])
            end = format_timestamp(segment['end'])
            f.write(f"{i}\n{start} --> {end}\n{segment['text'].strip().replace('-->', '->')}\n")

    return srt_filename


