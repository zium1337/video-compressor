import os
import sys
import ffmpeg

sys.path.append(r".\ffmpeg\ffmpeg.exe")


def compress_video(video_input, s, ext):
    size = s * 1024
    print(f"Info \n File size: {size} \n Output: {ext}")
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000
    probe = ffmpeg.probe(video_input)
    duration = float(probe['format']['duration'])
    audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
    target_total_bitrate = (size * 1024 * 8) / (1.073741824 * duration)
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate
    video_bitrate = target_total_bitrate - audio_bitrate
    i = ffmpeg.input(video_input)
    ffmpeg.output(i, os.devnull,
                  **{'c:v': 'h264_amf', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                  ).overwrite_output().run()
    ffmpeg.output(i, ext,
                  **{'c:v': 'h264_amf', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                  ).overwrite_output().run()
