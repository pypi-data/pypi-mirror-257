import os
import random
from typing import Callable

import numpy as np
from numpy.typing import NDArray
from easy_vc_dev.const import DATA_TYPE, TRAINER_DIR
import multiprocessing
from scipy import signal
from scipy.io.wavfile import write
from easy_vc_dev.utils.load_audio import load_audio
import traceback
import fire
from easy_vc_dev.utils.Slicer import Slicer
import resampy


def is_running_on_colab():
    try:
        import google.colab  # NOQA

        return True
    except ImportError:
        return False


if is_running_on_colab():
    print("load tqdm for notebook")
    from tqdm.notebook import tqdm
else:
    #    print("load normal notebook")
    from tqdm import tqdm


def make_project_dir(project_name: str):
    dir_name = os.path.join(TRAINER_DIR, project_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)
        print(f"Directory {dir_name} has been created.")
    else:
        print(f"Directory {dir_name} already exists.")
    return dir_name


def _norm_write(project_dir: str, filename: str, tmp_audio: NDArray[np.float32], slice_id: int, sample_rate: int, data_type: DATA_TYPE):
    max = 0.9
    alpha = 0.75
    suffix = "_val" if data_type == "VAL" else "_test" if data_type == "TEST" else ""
    gt_wavs_dir = f"{project_dir}/0_gt_wavs{suffix}"
    wavs16k_dir = f"{project_dir}/1_16k_wavs{suffix}"
    os.makedirs(gt_wavs_dir, exist_ok=True)
    os.makedirs(wavs16k_dir, exist_ok=True)
    tmp_max = np.abs(tmp_audio).max()
    if tmp_max > 2.5:
        print(f"{filename}-{slice_id}-{tmp_max}-filtered")
        return

    if len(tmp_audio) > sample_rate * 20:  # whisperのモデルが30秒なので、(バッファをもって)20秒以上の音声は2秒に切り詰める(_load_audioでリサンプリング済み)
        tmp_audio = tmp_audio[: sample_rate * 20]

    filename = os.path.splitext(filename)[0]
    # モデルのサンプリングレートで保存(_load_audioでリサンプリング済み)
    tmp_audio = (tmp_audio / tmp_max * (max * alpha)) + (1 - alpha) * tmp_audio
    write(f"{gt_wavs_dir}/{filename}-{slice_id}.wav", sample_rate, tmp_audio.astype(np.float32))

    # 16Kのサンプリングレートで保存(要リサンプリング)
    # tmp_audio = librosa.resample(tmp_audio, orig_sr=sample_rate, target_sr=16000)
    tmp_audio = resampy.resample(tmp_audio, sample_rate, 16000, filter="kaiser_best")
    write(f"{wavs16k_dir}/{filename}-{slice_id}.wav", 16000, tmp_audio.astype(np.float32))


def pipeline(params: tuple[str, str, int, DATA_TYPE]):
    project_dir, wav_file, sample_rate, data_type = params
    slicer = Slicer(
        sr=sample_rate,
        threshold=-42,
        min_length=1500,
        min_interval=400,
        hop_size=15,
        max_sil_kept=500,
    )
    bh, ah = signal.butter(N=5, Wn=48, btype="high", fs=sample_rate)
    per = 3.0
    overlap = 0.3
    tail = per + overlap
    try:
        audio = load_audio(wav_file, sample_rate)
        audio = signal.lfilter(bh, ah, audio)
        filename = os.path.basename(wav_file)

        if data_type == "test":
            # テストデータの場合は、ファイルを分割しない。 # TODO: ファイルサイズによっては、メモリ溢れでエラーになる可能性がある対応が必要。
            _norm_write(project_dir, filename, audio, 0, sample_rate, data_type)
            return
        slice_id = 0
        for audio in slicer.slice(filename, audio):
            i = 0
            while 1:
                start = int(sample_rate * (per - overlap) * i)  # wav上の開始地点
                i += 1
                if len(audio[start:]) > tail * sample_rate:
                    tmp_audio = audio[start : start + int(per * sample_rate)]
                    _norm_write(project_dir, filename, tmp_audio, slice_id, sample_rate, data_type)
                    slice_id += 1
                else:
                    tmp_audio = audio[start:]
                    _norm_write(project_dir, filename, tmp_audio, slice_id, sample_rate, data_type)
                    slice_id += 1
                    break
    except:
        print(f"{filename}: {slice_id}->{traceback.format_exc()}")


def pipeline_mp(project_dir: str, wav_files: list[str], sample_rate: int, jobs: int, data_type: DATA_TYPE, callback: Callable[[DATA_TYPE, int, int, str], None] | None = None):
    params = [(project_dir, x, sample_rate, data_type) for x in wav_files]

    pool = multiprocessing.Pool(processes=jobs)
    with tqdm(total=len(params)) as pbar:
        for _, _ in enumerate(pool.imap_unordered(pipeline, params)):
            pbar.update()
            if callback is not None:
                callback(data_type, pbar.n, pbar.total, "RUNNING")
    if callback is not None:
        callback(data_type, pbar.n, pbar.total, "DONE")


def generate_silent_wav(project_dir: str, sample_rate: int, num: int):
    for i in range(1, num + 1):
        gt_wavs_dir = f"{project_dir}/0_gt_wavs"
        wavs16k_dir = f"{project_dir}/1_16k_wavs"
        gt_path = os.path.join(gt_wavs_dir, f"mute{i}.wav")
        wavs16k_path = os.path.join(wavs16k_dir, f"mute{i}.wav")

        silence = np.zeros((sample_rate * 3,), np.float32)
        write(gt_path, sample_rate, silence)
        write(wavs16k_path, 16000, silence)


def preprocess(project_name: str, wav_dir: str, sample_rate: int, jobs: int, valid_num: int = 0, test_dir: str | None = None, callback: Callable[[DATA_TYPE, int, int, str], None] | None = None):
    # プロジェクトディレクトリの作成
    project_dir = make_project_dir(project_name)

    # 学習データと検証データの分割、テストデータの列挙
    all_train_files = [os.path.join(wav_dir, x) for x in os.listdir(wav_dir) if os.path.splitext(x)[1].lower() in (".wav", ".mp3")]

    random.shuffle(all_train_files)
    if valid_num > 0:
        train_files = all_train_files[valid_num:]
        val_files = all_train_files[:valid_num]
    else:
        train_files = all_train_files
        val_files = None

    if test_dir is not None:
        test_files = [os.path.join(test_dir, x) for x in list(os.listdir(test_dir)) if os.path.splitext(x)[1].lower() in (".wav", ".mp3")]
    else:
        test_files = None

    pipeline_mp(project_dir, train_files, sample_rate, jobs, "TRAIN", callback)
    if val_files is not None:
        pipeline_mp(project_dir, val_files, sample_rate, jobs, "VAL", callback)
    if test_files is not None:
        pipeline_mp(project_dir, test_files, sample_rate, jobs, "TEST", callback)

    generate_silent_wav(project_dir, sample_rate, num=4)


def main():
    fire.Fire(preprocess)
