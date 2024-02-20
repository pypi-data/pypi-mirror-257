from dataclasses import dataclass
from typing import Tuple


@dataclass
class HParamsTrain:
    seed: int
    learning_rate: float
    betas: Tuple[float, float]
    eps: float
    batch_size: int
    fp16_run: bool
    lr_decay: float
    segment_size: int
    c_mel: int
    c_kl: float


@dataclass
class HParamsData:
    max_wav_value: float
    sampling_rate: int
    filter_length: int
    hop_length: int
    win_length: int
    n_mel_channels: int
    mel_fmin: float
    mel_fmax: float | None


@dataclass
class HParams2:
    train: HParamsTrain
    data: HParamsData


def get_LightweightRVC_Synthesizer_nof0_hparams():
    hparams = HParams2(
        train=HParamsTrain(
            seed=1234,
            learning_rate=1e-4,
            betas=[0.8, 0.99],
            eps=1e-9,
            batch_size=4,
            fp16_run=True,
            lr_decay=0.999875,
            segment_size=6400,
            c_mel=45,
            c_kl=1.0,
        ),
        data=HParamsData(
            max_wav_value=32768.0,
            sampling_rate=16000,
            filter_length=1024,
            hop_length=160,
            win_length=1024,
            n_mel_channels=80,
            mel_fmin=0.0,
            mel_fmax=None,
        ),
    )
    return hparams
