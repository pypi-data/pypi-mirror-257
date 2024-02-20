import ffmpeg
import numpy as np


def load_audio(file: str, sample_rate: int):
    try:
        file = file.strip(" ").strip('"').strip("\n").strip('"').strip(" ")  # 空白や"、改行がパスの先頭と末尾に挿入されることを防ぎ、小白のコピーを避けます。
        out, _ = ffmpeg.input(file, threads=0).output("-", format="f32le", acodec="pcm_f32le", ac=1, ar=sample_rate).run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
    except Exception as e:
        raise RuntimeError(f"Failed to load audio: {e}", file)

    return np.frombuffer(out, np.float32).flatten()
