import os
from typing import Callable
import fire
import traceback

import numpy as np
import soundfile as sf
import torch
import torch.nn.functional as F
from easy_vc_dev.const import DATA_TYPE, TRAINER_DIR
from easy_vc_dev.utils.whisper.audio import log_mel_spectrogram
from easy_vc_dev.utils.whisper.model import Whisper
from easy_vc_dev.utils.whisper.whisper import load_model


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


# wave must be 16k
def _readwave(wav_path, normalize=False):
    wav, sr = sf.read(wav_path)
    assert sr == 16000
    feats = torch.from_numpy(wav).float()
    if feats.dim() == 2:  # double channels
        feats = feats.mean(-1)
    assert feats.dim() == 1, feats.dim()
    if normalize:
        with torch.no_grad():
            feats = F.layer_norm(feats, feats.shape)
    feats = feats.view(1, -1)
    return feats


def extract_feature_with_whisper(whisper: Whisper, audio: torch.Tensor):
    try:
        if isinstance(audio, np.ndarray):
            audio = torch.from_numpy(audio.astype(np.float32))
        audio = audio.to(whisper.device)

        if audio.dim() != 1:
            raise RuntimeError(f"Exeption in extract_feature_with_whisper. audio.dim is not 1 (size :{audio.dim()}, {audio.shape})")

        # audln = audio.shape[0]
        # ppgln = audln // 320

        mel = log_mel_spectrogram(audio).to(whisper.device)

        # print(f"[whisper_ppg] audio:{audio.shape}({audio.shape[0]/16000}ms) -> ppg:{ppgln}")
        # print(f"[whisper_ppg] mel:{mel.shape}({mel.dtype})")
        with torch.no_grad():
            ppg = whisper.encoder(mel.unsqueeze(0))
            padding = (0, 384)
            ppg_padded = F.pad(ppg, padding, "constant", 0)
            ppg_padded = ppg_padded.data
            # print(f"[whisper_ppg] ppg:{ppg.shape}")
    except Exception as e:
        raise RuntimeError("Exeption in xtract_feature_with_whisper.", e)
    return ppg_padded


def extract(input_dir: str, output_dir: str, _version: int, device_id: int = 0, data_type: DATA_TYPE = "TRAIN", callback: Callable[[DATA_TYPE, int, int, str], None] | None = None):
    files = sorted(list(os.listdir(input_dir)))
    if len(files) == 0:
        print("[extract feats] no target files")
        return

    whisper_model = "models/embedder/whisper_tiny.pt"
    whisper = load_model(whisper_model).cuda(device_id)

    print(f"[extract feats] target files {len(files)}")
    with tqdm(total=len(files)) as pbar:
        for i, file in enumerate(files):
            try:
                if file.endswith(".wav"):
                    wav_path = f"{input_dir}/{file}"
                    out_path = f"{output_dir}/{file.replace('wav', 'npy')}"

                    # if os.path.exists(out_path):
                    #     continue

                    audio = _readwave(wav_path, normalize=False)
                    feats = extract_feature_with_whisper(whisper, audio.squeeze())
                    feats = feats.squeeze(0).float().cpu().numpy()

                    if i == 0:
                        pass
                        # print(feats)

                    if np.isnan(feats).sum() == 0:
                        np.save(out_path, feats, allow_pickle=False)
                    else:
                        print(f"{file}-contains nan")
            except:
                print(traceback.format_exc())
                print(f"file:{file}")
            pbar.update()
            if callback is not None:
                callback(data_type, pbar.n, pbar.total, "RUNNING")
    print("all-feature-done")
    if callback is not None:
        callback(data_type, pbar.n, pbar.total, "DONE")


def extract_feats(project_name: str, version: int, device_id: int = 0, callback: Callable[[DATA_TYPE, int, int, str], None] | None = None):
    # フォルダ構成の推定
    project_dir = os.path.join(TRAINER_DIR, project_name)
    train_input_dir = os.path.join(project_dir, "1_16k_wavs")
    train_output_dir = os.path.join(project_dir, "3_feature768")

    val_input_dir = os.path.join(project_dir, "1_16k_wavs_val")
    val_output_dir = os.path.join(project_dir, "3_feature768_val")

    test_input_dir = os.path.join(project_dir, "1_16k_wavs_test")
    test_output_dir = os.path.join(project_dir, "3_feature768_test")

    # Feats抽出
    os.makedirs(train_output_dir, exist_ok=True)
    extract(train_input_dir, train_output_dir, version, device_id, "TRAIN", callback)
    if os.path.exists(val_input_dir) and os.path.isdir(val_input_dir):
        os.makedirs(val_output_dir, exist_ok=True)
        extract(val_input_dir, val_output_dir, version, device_id, "VAL", callback)
    if os.path.exists(test_input_dir) and os.path.isdir(test_input_dir):
        os.makedirs(test_output_dir, exist_ok=True)
        extract(test_input_dir, test_output_dir, version, device_id, "TEST", callback)


def main():
    fire.Fire(extract_feats)
